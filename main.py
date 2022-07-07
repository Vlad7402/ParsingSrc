import datetime
import time
from multiprocessing.pool import ThreadPool

from selenium import webdriver

from TrainParsing import TrainParser
from bus_parser import BusParser

if __name__ == '__main__':
    date = datetime.date(2022, 7, 16)
    EXE_PATH = r'C:\chromedriver.exe'
    driver1 = webdriver.Chrome(EXE_PATH)
    driver2 = webdriver.Chrome(EXE_PATH)
    pool1 = ThreadPool(processes=1)
    pool2 = ThreadPool(processes=1)
    parser1 = TrainParser('Челябинск', 'Москва', date, driver1)
    parser2 = BusParser('Челябинск', 'Москва', date, driver2)
    resTrains = pool1.apply_async(parser1.CheckTrains, ())
    resBuses = pool2.apply_async(parser2.CheckBuses, ())
    i = 0
    while True:
        print(i)

        if resBuses.ready() and resTrains.ready():
            if resBuses.successful():
                resBuses = resBuses.get(10)
                for res in resBuses:
                    print(res)

            if resTrains.successful():
                resTrains = resTrains.get(10)
                for res in resTrains:
                    print(res)
            break

        i += 1
        time.sleep(1)
