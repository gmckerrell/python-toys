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

def initialise(con):
    print("Initialising database")
    # create the tables in the database
    with con:
        c = con.cursor()
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
    
def find_models(con, **criteria):
    where_expression, where_args = create_where_expression(
        {
            "name":         "models.name LIKE ?",
            "manufacturer": "models.manufacturer LIKE ?"
        },
        criteria
    )
    with con:
        c = con.cursor()
        c.row_factory = dict_row_factory
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
            where_args
        )
        return c.fetchall()

def find_cars(con, **criteria):
    where_expression, where_args = create_where_expression(
            {
                "model": "models.name = ?"
            },
            criteria
        )
    with con:
        c = con.cursor()
        c.row_factory = dict_row_factory
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
            where_args
        )
        return c.fetchall()
    
def find_bookings(con, **criteria):
    where_expression, where_args = create_where_expression(
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
    with con:
        c = con.cursor()
        c.row_factory = dict_row_factory
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
            where_args
        )
        return c.fetchall()

if __name__ == "__main__":
    import os
    
    dbpath = "carhire.db"
    first_time = not os.path.exists(dbpath)
    con = sqlite3.connect(dbpath)
    
    if first_time:
        initialise(con)

    print("ALL MODELS")
    for model in find_models(con):
        print(model)

    print("ALL CARS")
    for car in find_cars(con):
        print(car)

    print("findByModelName")
    for car in find_cars(con, model_name = "mini"):
        print(car)

    print("ALL BOOKINGS")
    for booking in find_bookings(con):
        print(booking)

    print("findByCustomer")
    for booking in find_bookings(con, customer = "Fred Flintstone"):
        print(booking)

    con.close()

