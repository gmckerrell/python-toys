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
    def __init__(self, con):
        self.con = con

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
            
        c             = self.con.cursor()
        c.row_factory = factory
        return c
        
    def initialise(self):
        print("Initialising database")
        # create the tables in the database
        with self.con:
            c = self.cursor()
            c.executescript(
                """
                CREATE TABLE models (
                    id            INTEGER PRIMARY KEY,
                    name          TEXT    NOT NULL,
                    manufacturer  TEXT    NOT NULL,
                    luggage       INTEGER NOT NULL,
                    people        INTEGER NOT NULL
                );
                CREATE TABLE cars (
                    id           INTEGER PRIMARY KEY,
                    registration TEXT    NOT NULL,
                    model_id     INTEGER NOT NULL,
                    FOREIGN KEY (model_id)
                        REFERENCES models (id)
                            ON DELETE RESTRICT
                );
                CREATE TABLE bookings (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer   TEXT    NOT NULL,
                    start_date DATE    NOT NULL,
                    end_date   DATE    NOT NULL,
                    car_id     INTEGER NOT NULL,
                    FOREIGN KEY (car_id)
                        REFERENCES cars (id)
                            ON DELETE RESTRICT
                );
                """
            )
            c.executemany(
                "INSERT INTO models VALUES(?,?,?,?,?)",
                (
                    (1, "s-max", "Ford", 4, 5),
                    (2, "mini", "BMW",   2, 4),
                )
            )
            c.executemany(
                "INSERT INTO cars VALUES(?,?,?)",
                (
                    (1, "ABC 123", 1),
                    (2, "ABC 456", 1),
                    (3, "M1N1 1",  2),
                    (4, "M1N1 2",  2),
                )
            )
            c.executemany(
                "INSERT INTO bookings (customer, start_date, end_date, car_id) VALUES(?,?,?,?)",
                (
                    ("Fred Flintstone", "11-09-2020", "12-09-2020", 3),
                    ("Barney Rubble", "11-09-2020", "20-10-2020", 2),
                    ("Betty Rubble", "11-09-2020", "20-10-2020", 1),
                )
            )
        
    def find_models(self, **criteria):
        where_expression = WhereExpression(
            {
                "name":         "models.name LIKE ?",
                "manufacturer": "models.manufacturer LIKE ?"
            },
            criteria
        )
        with self.con:
            c = self.cursor()
            c.execute(
                f"""
                SELECT
                    models.id,
                    models.manufacturer,
                    models.name,
                    models.people,
                    models.luggage
                FROM models
                {where_expression}
                """,
                where_expression.values
            )
            return c.fetchall()

    def find_cars(self, **criteria):
        where_expression = WhereExpression(
            {
                "model_name": "models.name = ?"
            },
            criteria
        )
        with self.con:
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
        with self.con:
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
    con = sqlite3.connect(dbpath)
    
    car_hire = CarHire(con)
    
    if first_time:
        car_hire.initialise()

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

    con.close()

