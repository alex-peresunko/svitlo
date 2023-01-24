import json
import os
import time
import croniter
import ecoflow_api
import database


def process_iter(db_conn, config, secrets):
    # Get and save telemetry once
    telemetry = ecoflow_api.fetch_data(secrets['device_sn'], app_key=secrets['app_key'],
                                       secret_key=secrets['secret_key'])
    if telemetry is not None:
        database.save_telemetry(db_conn, time.time(), telemetry)


def main():

    # Load configuration
    script_folder = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_folder, 'config.json')) as config_file:
        config = json.load(config_file)
    db = config['db_file']
    main_schedule = config['schedule']

    # Load secrets
    with open(os.path.join(script_folder, 'secrets.json')) as secret_file:
        secrets = json.load(secret_file)

    if not os.path.isfile(db):
        database.create_db_schema(db)
    db_conn = database.get_db_connection(str(db))

    last_run_ts = time.time()
    cron = croniter.croniter(config['schedule'], last_run_ts)

    sleep_time = 0
    while True:
        if sleep_time > 0:
            print("Sleeping {} seconds".format(sleep_time))
            time.sleep(sleep_time)

        next_run_ts = cron.get_next(float)
        print("Processing iteration...")
        process_iter(db_conn, config, secrets)
        last_run_ts = time.time()
        sleep_time = next_run_ts - last_run_ts


if __name__ == "__main__":
    main()
