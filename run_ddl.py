import json
import os
import sys

from database import *


def main():
    query = sys.argv[1]
    # Load configuration
    script_folder = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_folder, 'config.json')) as config_file:
        config = json.load(config_file)
    db_file = config['db_file']
    if not os.path.isfile(db_file):
        raise Exception

    db_conn = get_db_connection(str(db_file))
    result = None
    try:
        cur = db_conn.cursor()
        result = cur.execute(query)
    except Error as e:
        print(e)
    finally:
        print(result)
        if db_conn:
            db_conn.commit()


if __name__ == "__main__":
    main()
