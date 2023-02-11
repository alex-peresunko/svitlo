import json
import os
import database


def main():

    # Load configuration
    script_folder = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_folder, 'config.json')) as config_file:
        config = json.load(config_file)
    db = config['db_file']

    if os.path.isfile(db):
        db_conn = database.get_db_connection(str(db))
    else:
        raise Exception

    result = database.is_there_input_watts(db_conn)
    print(result)


if __name__ == "__main__":
    main()
