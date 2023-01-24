import sqlite3
from sqlite3 import Error


def get_db_connection(db):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as e:
        print(e)


def create_db_schema(db):
    db_conn = get_db_connection(str(db))
    cur = db_conn.cursor()
    try:
        cur.execute("CREATE TABLE ecoflow_telemetry "
                    "(ts integer, code text, message text, soc integer, remainTime integer, "
                    "wattsOutSum integer, wattsInSum integer)")
    except Error as e:
        print(e)
    finally:
        if db_conn:
            db_conn.commit()


def validate_and_transform_data(data):
    if not ("data" in data):
        data["data"] = {
            "soc": None,
            "remainTime": None,
            "wattsOutSum": None,
            "wattsInSum": None
        }
    return data


def save_telemetry(conn, ts, data):
    cur = conn.cursor()
    data = validate_and_transform_data(data)
    try:
        cur.execute("INSERT INTO ecoflow_telemetry "
                    "(ts, code, message, soc, remainTime, wattsOutSum, wattsInSum) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (int(ts), data['code'], data['message'], data['data']['soc'],
                     data['data']['remainTime'], data['data']['wattsOutSum'],
                     data['data']['wattsInSum']))
        conn.commit()
    except Error as e:
        print(e)
