# Python program to pull, normalize and store parking data.

from datetime import datetime
import pytz
from multiprocessing import Process
from database import CarPark
from database import Database


def log_cron():
    singapore_timezone = pytz.timezone('Asia/Singapore')
    current_datetime = datetime.now(singapore_timezone).strftime("%H:%M:%S")
    print("Pulling latest data: " + current_datetime)


def cron_lta():
    print("Pulling LTA carpark data...")
    session = Database().get_session()
    session.add(CarPark(address='Tembu', x_coordinate='53.1', y_coordinate='40.2', lots_available='1'))
    session.commit()


def cron_ura():
    print("Pulling URA carpark data...")
    session = Database().get_session()
    session.add(CarPark(address='Capt', x_coordinate=12.1, y_coordinate=29.3, lots_available=10))
    session.commit()


def cron_hdb():
    print("Pulling HDB carpark data...")
    session = Database().get_session()
    session.add(CarPark(address='USP', x_coordinate=20.1, y_coordinate=51.2, lots_available=2))
    session.commit()


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
