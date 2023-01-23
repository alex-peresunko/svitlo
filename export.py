import json
import os
import csv
import sys

from database import *


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def main():

    # Load configuration
    script_folder = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_folder, 'config.json')) as config_file:
        config = json.load(config_file)
    db_file = config['db_file']

    if not os.path.isfile(db_file):
        raise Exception
    db_conn = get_db_connection(str(db_file))
    db_conn.row_factory = dict_factory
    cur = db_conn.cursor()
    cur.execute("SELECT * FROM ecoflow_telemetry ORDER BY ts ASC")
    data = cur.fetchall()

    export_file = sys.argv[1]
    with open(export_file, 'w', newline='') as f:
        w = csv.DictWriter(f, data[0].keys())
        w.writeheader()
        w.writerows(data)


if __name__ == "__main__":
    main()
