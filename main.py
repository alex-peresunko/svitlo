import datetime
import json
import os
import threading
import time

import croniter
from flask import Flask

import database
import ecoflow_api
import pytz


def process_iter(db_conn, config, secrets):
    # Get and save telemetry once
    ts = int(time.time())
    telemetry = ecoflow_api.fetch_data(secrets['device_sn'], app_key=secrets['app_key'],
                                       secret_key=secrets['secret_key'])
    if telemetry is not None:
        database.save_telemetry(db_conn, ts, telemetry)

    # update status if it gets changed
    last_status_from_telemetry = database.is_there_input_watts(db_conn)
    last_saved_status = database.get_latest_saved_status(db_conn)

    # Update status if it got changed since last record
    if last_saved_status != last_status_from_telemetry or last_saved_status is None:
        database.save_status(db_conn, ts, last_status_from_telemetry)


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

    last_run_ts = int(time.time())
    cron = croniter.croniter(config['schedule'], last_run_ts)

    app = Flask(__name__)

    @app.route("/")
    def endpoint_root():
        return "Hello!"

    @app.route("/status")
    def endpoint_status():
        conn = database.get_db_connection(str(db))
        rows = database.get_status_history(conn)
        response = '<table border=1><tr><th>Time (Europe/Kyiv)</th><th>Status</th></tr>'
        for row in rows:
            dt = datetime.datetime.fromtimestamp(row['ts'], pytz.timezone('Europe/Kyiv'))
            if row['status'] == 1:
                status = 'Увімкнули'
            else:
                status = 'Вимкнули'
            response += '<tr><td>{}</td><td>{}</td></tr>'.format(dt, status)
        response += '</table>'
        return response

    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)).start()

    sleep_time = 0
    while True:
        if sleep_time > 0:
            print("Sleeping {} seconds".format(sleep_time))
            time.sleep(sleep_time)

        next_run_ts = cron.get_next(float)
        print("{}: Processing iteration...".format(time.ctime()))
        process_iter(db_conn, config, secrets)
        last_run_ts = time.time()
        sleep_time = next_run_ts - last_run_ts


if __name__ == "__main__":
    main()
