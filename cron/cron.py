# Python program to pull, normalize and store parking data.

from datetime import datetime
import pytz
from multiprocessing import Process


def log_cron():
    singapore_timezone = pytz.timezone('Asia/Singapore')
    current_datetime = datetime.now(singapore_timezone).strftime("%H:%M:%S")
    print("Pulling latest data: " + current_datetime)


def cron_lta():
    print("Pulling LTA carpark data...")


def cron_ura():
    print("Pulling URA carpark data...")


def cron_hdb():
    print("Pulling HDB carpark data...")


def run_cron_async():
    lta = Process(target=cron_lta)
    ura = Process(target=cron_ura)
    hdb = Process(target=cron_hdb)

    lta.start()
    ura.start()
    hdb.start()

    lta.join()
    ura.join()
    hdb.join()


log_cron()
run_cron_async()

