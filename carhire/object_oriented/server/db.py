import sqlite3
import collections

class WhereExpression:
    def __init__(self, mapping, criteria):
        parts   = []
        values  = []
        unknown_criteria = []
        for key in criteria.keys():
            if key in mapping:
                parts.append(
                    mapping[key]
                )
                values.append(
                    criteria[key]
                )
            else:
                unknown_criteria.append(key)

        if unknown_criteria:
            raise KeyError(
                f"Unknown search criteria: {', '.join(unknown_criteria)}",
                f"Expected one of: {', '.join(mapping.keys())}"
            )

        if parts:
            self._expression = "WHERE " + " AND ".join(parts)
            self.values      = values
        else:
            self._expression = ""
            self.values      = tuple()

    def __str__(self):
        return self._expression


class CarHire:
    def __init__(self, conn):
        self.conn = conn

    def cursor(self):
        def factory(cursor, row):
            """
            This method is used to put the SQL results into an easily readable
            format rather than a raw tuple
            """
            d = {}
            for idx, entry in enumerate(cursor.description):
                col = entry[0]
                d[col] = row[idx]
            return d

        c             = self.conn.cursor()
        c.row_factory = factory
        return c

    def initialise(self):
        print("Initialising database")
        # create the tables in the database
        with self.conn:
            c = self.cursor()
            c.executescript(
                """
                DROP TABLE IF EXISTS models;
                CREATE TABLE models (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    name          TEXT    UNIQUE      NOT NULL,
                    manufacturer  TEXT                NOT NULL,
                    luggage       INTEGER             NOT NULL,
                    people        INTEGER             NOT NULL
                );

                DROP TABLE IF EXISTS cars;
                CREATE TABLE cars (
                    id           INTEGER PRIMARY KEY  AUTOINCREMENT,
                    registration TEXT    UNIQUE       NOT NULL,
                    color        TEXT                 NOT NULL,
                    model_id     INTEGER              NOT NULL,
                    
                    FOREIGN KEY(model_id) REFERENCES models(id)
                );

                DROP TABLE IF EXISTS bookings;
                CREATE TABLE bookings (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer   TEXT                NOT NULL,
                    start_date DATE                NOT NULL,
                    end_date   DATE                NOT NULL,
                    car_id     INTEGER             NOT NULL,
                    
                    FOREIGN KEY(car_id) REFERENCES cars(id)
                );
                """
            )

    def find_models(self, **criteria):
        where_expression = WhereExpression(
            {
                "id":           "id           =    ?",
                "name":         "name         LIKE ?",
                "manufacturer": "manufacturer LIKE ?",
                "people":       "people       =    ?",
                "luggage":      "luggage      =    ?",
            },
            criteria
        )
        with self.conn:
            c = self.cursor()
            c.execute(
                f"""
                SELECT
                    models.id,
                    models.name,
                    models.manufacturer,
                    models.people,
                    models.luggage
                FROM models
                {where_expression}
                """,
                where_expression.values
            )
            return c.fetchall()
        
    def create_model(self, name, manufacturer, people, luggage):
        print(f"LOCALS: {locals()}")
        with conn:
            c = self.cursor()
            try:
                c.execute(
                    """
                    INSERT INTO models (name, manufacturer, people, luggage) VALUES(?,?,?,?)
                    """,
                    (name, manufacturer, people, luggage)
                )
            except sqlite3.IntegrityError as err:
                raise ValueError(*err.args)

    def delete_model(self, id):
        with conn:
            c = self.cursor()
            c.execute(
                """
                DELETE FROM models WHERE id = ?
                """,
                (id,)
            )
            

    def find_cars(self, **criteria):
        where_expression = WhereExpression(
            {
                "model_name": "models.name = ?"
            },
            criteria
        )
        with self.conn:
            c = self.cursor()
            c.execute(
                f"""
                SELECT
                    cars.id,
                    cars.registration,
                    models.manufacturer,
                    models.name,
                    models.people,
                    models.luggage
                FROM cars
                INNER JOIN models
                    ON models.id = cars.model_id
                {where_expression}
                """,
                where_expression.values
            )
            return c.fetchall()

    def find_bookings(self, **criteria):
        where_expression = WhereExpression(
            {
                "booking_id":   "booking_id        =    ?",
                "customer":     "bookings.customer LIKE ?",
                "manufacturer": "models.manufacturer       LIKE ?",
                "model":        "models.name       LIKE ?",
                "people":       "models.people     >=   ?",
                "luggage":      "models.luggage    >=   ?"
            },
            criteria
        )
        with self.conn:
            c = self.cursor()
            c.execute(
                f"""
                SELECT
                    bookings.id                AS booking_id,
                    bookings.customer,
                    bookings.start_date,
                    bookings.end_date,
                    models.manufacturer,
                    models.name                AS model,
                    models.people,
                    models.luggage,
                    cars.registration
                FROM bookings
                INNER JOIN cars
                    ON bookings.car_id = cars.id
                INNER JOIN models
                    ON cars.model_id = models.id
                {where_expression}
                """,
                where_expression.values
            )
            return c.fetchall()

if __name__ == "__main__":
    import os

    dbpath = "carhire.db"
    first_time = not os.path.exists(dbpath)
    conn = sqlite3.connect(dbpath)

    car_hire = CarHire(conn)

    car_hire.initialise()

    car_hire.create_model(name = "s-max", manufacturer="Ford", people=5, luggage=5)
    car_hire.create_model(name = "mini", manufacturer="BMW", people=4, luggage=2)

#    create_car(conn, model="s-max", registration="ABC 123", color="red")
#    create_car(conn, model="s-max", registration="ABC 456", color="blue")
#    create_car(conn, model="mini",  registration="M1N1 2",  color="black")
#    create_car(conn, model="mini",  registration="M1N1 1",  color="silver")

#    create_booking(conn, start_date="11-09-2020", end_date="12-09-2020", customer="Fred Flintstone", model="mini")
#    create_booking(conn, start_date="13-09-2020", end_date="15-09-2020", customer="Wilma Flintstone", model="mini")
#    create_booking(conn, start_date="11-09-2020", end_date="12-09-2020", customer="Barney Rubble", model="s-max")
#    create_booking(conn, start_date="13-09-2020", end_date="15-09-2020", customer="Betty Rubble", model="s-max")

    print("ALL MODELS")
    for model in car_hire.find_models():
        print(model)

    print("ALL CARS")
    for car in car_hire.find_cars():
        print(car)

    print("findByModelName")
    for car in car_hire.find_cars(model_name = "mini"):
        print(car)

    print("ALL BOOKINGS")
    for booking in car_hire.find_bookings():
        print(booking)

    print("findByCustomer")
    for booking in car_hire.find_bookings(customer = "Fred Flintstone"):
        print(booking)

    conn.close()

