import sqlite3
from sqlite3 import Error


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


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
        cur.execute("CREATE INDEX eco_index_ts on ecoflow_telemetry (ts, code)")
        cur.execute("CREATE TABLE svitlo_status (ts integer, status integer)")
        cur.execute("CREATE INDEX svitlo_status_index_ts on svitlo_status (ts)")
        cur.execute("INSERT INTO svitlo_status (ts, status) VALUES (0, -1)")
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


def get_latest_saved_telemetry(conn):
    conn.row_factory = dict_factory
    cur = conn.cursor()
    try:
        cur.execute("SELECT ts, code, message, soc, remainTime, wattsOutSum, wattsInSum "
                    "FROM ecoflow_telemetry "
                    "WHERE code = 0 "
                    "ORDER BY ts DESC "
                    "LIMIT 1")
        row = cur.fetchone()
        return row
    except Error as e:
        print(e)


def get_latest_db_status_row(conn) -> dict:
    conn.row_factory = dict_factory
    cur = conn.cursor()
    try:
        cur.execute("SELECT ts, status "
                    "FROM svitlo_status "
                    "ORDER BY ts DESC "
                    "LIMIT 1")
        row = cur.fetchone()
        print(row)
        return row
    except Error as e:
        print(e)


def get_latest_saved_status(conn):
    row = get_latest_db_status_row(conn)
    if 'status' in row.keys():
        if row['status'] == -1:
            return None
        if row['status'] == 0:
            return False
        else:
            return True


def is_there_input_watts(conn) -> bool:
    latest_row = get_latest_saved_telemetry(conn)
    if latest_row and 'wattsInSum' in latest_row.keys():
        if latest_row['wattsInSum'] > 0:
            return True
        else:
            return False


def save_status(conn, ts: int, status: int):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO svitlo_status "
                    "(ts, status) "
                    "VALUES (?, ?)",
                    (int(ts), status))
        conn.commit()
    except Error as e:
        print(e)


def get_status_history(conn, ts_from=0):
    conn.row_factory = dict_factory
    cur = conn.cursor()
    try:
        cur.execute("SELECT * "
                    "FROM svitlo_status "
                    "WHERE ts > ? "
                    "ORDER BY ts DESC ", (ts_from,))
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(e)
