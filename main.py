import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from multiprocessing.pool import ThreadPool

from HTMLData import ClassNames as CN
from HTMLData import XPaths as Paths
from TimeDelta import TimeDelta
from TrainData import TrainData
from TrainData import TrainTypeDict
from TrainParsing import TrainParser


def CheckBuses(cityFrom, cityTo, date, driver):
    driver.get('https://bus.tutu.ru/расписание_автобусов/')
    moveTo = driver.find_element(By.XPATH, Paths.BusMoveToField)
    moveTo.send_keys(cityTo)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, Paths.BusMoveToSelector)))
    moveTo = driver.find_element(By.XPATH, Paths.BusMoveToSelector)
    moveTo.click()
    moveFrom = driver.find_element(By.XPATH, Paths.BusMoveFromField)
    moveFrom.send_keys(cityFrom)
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, Paths.BusMoveFromSelector)))
    moveFrom = driver.find_element(By.XPATH, Paths.BusMoveFromSelector)
    moveFrom.click()
    checkButton = driver.find_element(By.XPATH, Paths.BusCheckButton)
    checkButton.click()


def GetTime(timeStr):
    timeT = datetime.time(int(timeStr[:2]), int(timeStr[3:]))
    return timeT


def GetTravelTime(dateStr: str):
    dayIndex = str.find(dateStr, 'д')
    hourIndex = str.find(dateStr, 'ч')
    minuteIndex = str.find(dateStr, 'м')
    travelTime: TimeDelta = TimeDelta()
    if hourIndex != -1:
        if minuteIndex != -1:
            travelTime.Minutes = int(dateStr[hourIndex + 1: minuteIndex - 1])
        if dayIndex != -1:
            travelTime.Hours = int(dateStr[dayIndex + 1: hourIndex - 1])
            travelTime.Days = int(dateStr[: dayIndex - 1])
        else:
            travelTime.Hours = int(dateStr[: hourIndex - 1])
    else:
        if dayIndex != -1:
            travelTime.Days = int(dateStr[: dayIndex - 1])
            if minuteIndex != -1:
                travelTime.Minutes = int(dateStr[dayIndex + 1: minuteIndex - 1])
        elif minuteIndex != -1:
            travelTime.Minutes = int(dateStr[: minuteIndex - 1])
    return travelTime


def GetNumberOfSeats(inputStr):
    inputStr = inputStr.replace(' ниж', 'н')
    inputStr = inputStr.replace(' верх', 'в')
    inputStr = inputStr.replace(',', '')
    inputStr = inputStr.replace(' ', '')
    lowNumIndex = str.find(inputStr, 'н')
    highNumIndex = str.find(inputStr, 'в')
    if lowNumIndex != -1 and highNumIndex != -1:
        lowNum = int(inputStr[:lowNumIndex])
        highNum = int(inputStr[lowNumIndex + 1:highNumIndex])
        return lowNum + highNum
    elif lowNumIndex != -1:
        return int(inputStr[:lowNumIndex])
    else:
        return int(inputStr[:highNumIndex])


def GetPrice(inputStr):
    inputStr = inputStr.replace(' ', '')
    inputStr = inputStr.replace('₽', '')
    return int(inputStr)


def GetArrivalDate(inputStr):
    spaceIndex = str.find(inputStr, ' ')
    return int(inputStr[:spaceIndex])


if __name__ == '__main__':
    date = datetime.date(2022, 7, 10)
    pool = ThreadPool(processes=1)
    EXE_PATH = r'C:\chromedriver.exe'
    driver1 = webdriver.Chrome(EXE_PATH)
    driver2 = webdriver.Chrome(EXE_PATH)
    parser = TrainParser('Челябинск', 'Златоуст', date, driver1)
    resTrains = pool.apply_async(parser.CheckTrains, ())
    CheckBuses('Челябинск', 'Златоуст', date, driver2)
    resTrains = resTrains.get(60)
    print('')
