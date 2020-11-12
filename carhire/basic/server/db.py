"""
This module provides database utility functions for the car hire database
"""
import sqlite3

def dict_row_factory(cursor, row):
    """
    This method is used to put the SQL results into an easily readable
    format rather than a raw tuple
    """
    d = {}
    for idx, entry in enumerate(cursor.description):
        col = entry[0]
        d[col] = row[idx]
    return d

def create_where_expression(mapping, criteria):
    where_parts = []
    where_args  = []
    unknown_criteria = []
    for key in criteria.keys():
        if key in mapping:
            where_parts.append(
                mapping[key]
            )
            where_args.append(
                criteria[key]
            )
        else:
            unknown_criteria.append(key)

    if unknown_criteria:
        raise KeyError(
            f"Unknown search criteria: {', '.join(unknown_criteria)}",
            f"Expected one of: {', '.join(mapping.keys())}"
        )

    if where_parts:
        return "WHERE " + " AND ".join(where_parts), where_args
    else:
        return "", tuple()

def initialise(conn):
    print("Initialising database")
    # create the tables in the database
    with conn:
        c = conn.cursor()
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

def find_models(conn, **criteria):
    where_expression, where_args = create_where_expression(
        {
            "id":           "id           =    ?",
            "name":         "name         LIKE ?",
            "manufacturer": "manufacturer LIKE ?",
            "people":       "people       =    ?",
            "luggage":      "luggage      =    ?",
        },
        criteria
    )
    with conn:
        c = conn.cursor()
        c.row_factory = dict_row_factory
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
            where_args
        )
        return c.fetchall()

def create_model(conn, name, manufacturer, people, luggage):
    with conn:
        c = conn.cursor()
        c.row_factory = dict_row_factory
        try:
            c.execute(
                """
                INSERT INTO models (name, manufacturer, people, luggage) VALUES(?,?,?,?)
                """,
                (name, manufacturer, people, luggage)
            )
        except sqlite3.IntegrityError as err:
            raise ValueError(*err.args)
    
    return find_models(conn, name=name)[0]

def delete_model(conn, id):
    with conn:
        c = conn.cursor()
        c.row_factory = dict_row_factory
        c.execute(
            """
            DELETE FROM models WHERE id = ?
            """,
            (id,)
        )

def find_cars(conn, **criteria):
    where_expression, where_args = create_where_expression(
            {
                "id":           "cars.id      =    ?",
                "registration": "registration LIKE ?",
                "model":        "models.name  LIKE ?",
                "color":        "color        =    ?",
            },
            criteria
        )
    with conn:
        c = conn.cursor()
        c.row_factory = dict_row_factory
        c.execute(
            f"""
            SELECT
                cars.id,
                cars.registration,
                cars.color,
                models.manufacturer,
                models.name          AS model,
                models.people,
                models.luggage
            FROM cars
            INNER JOIN models
                ON models.id = cars.model_id
            {where_expression}
            """,
            where_args
        )
        return c.fetchall()

def create_car(conn, model, registration, color):

    model = find_models(conn, name=model)[0]

    with conn:
        c = conn.cursor()
        c.row_factory = dict_row_factory
        c.execute(
            """
            INSERT INTO cars (model_id, registration,color) VALUES(?,?,?)
            """,
            (model['id'], registration, color)
        )
    return find_cars(conn, registration=registration)[0]


def delete_car(conn, id):
    with conn:
        c = conn.cursor()
        c.row_factory = dict_row_factory
        c.execute(
            """
            DELETE FROM cars WHERE id = ?
            """,
            (id,)
        )


def find_bookings(conn, **criteria):
    where_expression, where_args = create_where_expression(
        {
            "id":           "bookings.id         =    ?",
            "customer":     "customer            LIKE ?",
            "manufacturer": "models.manufacturer LIKE ?",
            "model":        "models.name         LIKE ?",
            "people":       "models.people       >=   ?",
            "luggage":      "models.luggage      >=   ?",
        },
        criteria
    )
    with conn:
        c = conn.cursor()
        c.row_factory = dict_row_factory
        c.execute(
            f"""
            SELECT
                bookings.id,
                bookings.customer,
                bookings.start_date,
                bookings.end_date,
                models.manufacturer,
                models.name          AS model,
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
            where_args
        )
        return c.fetchall()


def create_booking(conn, start_date, end_date, customer, **criteria):

    car = find_cars(conn, **criteria)[0] # take the first one for now

    with conn:
        c = conn.cursor()
        c.row_factory = dict_row_factory
        c.execute(
            """
            INSERT INTO bookings (start_date, end_date, customer, car_id) VALUES(?,?,?,?)
            """,
            (start_date, end_date, customer, car['id'])
        )
        booking_id = c.lastrowid

    return find_bookings(conn, id=booking_id)[0]


def delete_booking(conn, id):
    with conn:
        c = conn.cursor()
        c.row_factory = dict_row_factory
        c.execute(
            """
            DELETE FROM bookings WHERE id = ?
            """,
            (id,)
        )


if __name__ == "__main__":
    import os

    conn = sqlite3.connect("carhire.db")

    initialise(conn)

    create_model(conn, name = "s-max", manufacturer="Ford", people=5, luggage=5)
    create_model(conn, name = "mini", manufacturer="BMW", people=4, luggage=2)

    create_car(conn, model="s-max", registration="ABC 123", color="red")
    create_car(conn, model="s-max", registration="ABC 456", color="blue")
    create_car(conn, model="mini",  registration="M1N1 2",  color="black")
    create_car(conn, model="mini",  registration="M1N1 1",  color="silver")

    create_booking(conn, start_date="11-09-2020", end_date="12-09-2020", customer="Fred Flintstone", model="mini")
    create_booking(conn, start_date="13-09-2020", end_date="15-09-2020", customer="Wilma Flintstone", model="mini")
    create_booking(conn, start_date="11-09-2020", end_date="12-09-2020", customer="Barney Rubble", model="s-max")
    create_booking(conn, start_date="13-09-2020", end_date="15-09-2020", customer="Betty Rubble", model="s-max")

    print("ALL MODELS")
    for model in find_models(conn):
        print(model)

    print("ALL CARS")
    for car in find_cars(conn):
        print(car)

    print("findByModelName")
    for car in find_cars(conn, model = "mini"):
        print(car)

    print("ALL BOOKINGS")
    for booking in find_bookings(conn):
        print(booking)

    print("findByCustomer")
    for booking in find_bookings(conn, customer = "Fred Flintstone"):
        print(booking)

    conn.close()

