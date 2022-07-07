import datetime
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from HTMLData import ClassNames as CN
from HTMLData import XPaths as Paths
from TimeDelta import TimeDelta
from ticket_data import TicketData, TicketType


def CheckBuses(cityFrom, cityTo, date, driver):
    driver.get('https://unitiki.com')
    moveTo = driver.find_element(By.XPATH, Paths.BusMoveToField)
    moveTo.send_keys(cityTo)
    time.sleep(1.5)
    moveFrom = driver.find_element(By.XPATH, Paths.BusMoveFromField)
    moveFrom.send_keys(cityFrom)
    time.sleep(1.5)
    dateField = driver.find_element(By.XPATH, Paths.BusDateField)
    driver.execute_script("arguments[0].removeAttribute('readonly')", dateField)
    for i in range(11):
        dateField.send_keys(Keys.BACKSPACE)
    dateField.send_keys(str(date.day) + '.' + str(date.month) + '.' + str(date.year))
    checkButton = driver.find_element(By.XPATH, Paths.BusCheckButton)
    checkButton.click()
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, CN.BusInfoFields)))
    except:
        return None
    time.sleep(4)
    busInfoFields = driver.find_elements(By.CLASS_NAME, CN.BusInfoFields)
    try:
        busInfoFields[0].find_element(By.CLASS_NAME, CN.BusDetails)
        GetBussDataWithoutChange(busInfoFields, driver)
    except:
        GetBussDataWithChange(busInfoFields, driver)


def GetBussDataWithChange(busInfoFields: list[WebElement], driver):
    for busInfoField in busInfoFields:
        tickets = list[TicketData]
        driver.execute_script("arguments[0].scrollIntoView(true);", busInfoField)
        showDetails = busInfoField.find_element(By.CLASS_NAME, CN.BusChDetails)
        showDetails.click()
        success = True
        while success:
            time.sleep(0.2)
            try:
                detailedInfoFields = busInfoField.find_elements(By.CLASS_NAME, CN.BusChDetailedInfo)
                detailedInfoFields[0].find_element(By.CLASS_NAME, CN.BusChStartPointInfo)
                success = False
            except:
                success = True
        mainInfoFields = busInfoField.find_elements(By.CLASS_NAME, CN.BusChMainIfo)
        detailedInfoFields = busInfoField.find_elements(By.CLASS_NAME, CN.BusChDetailedInfo)
        addInfoField = busInfoField.find_element(By.CLASS_NAME, CN.BusChAddInfo)
        travelTime1 = mainInfoFields[0].find_element(By.CLASS_NAME, CN.BusChTravelTime)
        travelTime1 = GetTravelTime(travelTime1)
        travelTime2 = mainInfoFields[1].find_element(By.CLASS_NAME, CN.BusChTravelTime)
        travelTime2 = GetTravelTime(travelTime2)
        startPointInfo = detailedInfoFields[0].find_element(By.CLASS_NAME, CN.BusChStartPointInfo)
        arrivalPointInfo = detailedInfoFields[0].find_element(By.CLASS_NAME, CN.BusChArrivalPointInfo)
        startTime = startPointInfo.find_element(By.XPATH, Paths.BusChStartTime)
        startTime = GetTime(startTime.text)
        arrivalTime = arrivalPointInfo.find_element(By.XPATH, Paths.BusChArrivalTime)
        arrivalTime = GetTime(arrivalTime.text)
        startDate = startPointInfo.find_element(By.XPATH, Paths.BusChStartDate)
        startDate = GetDate(startDate.text, date)
        arrivalDate = arrivalPointInfo.find_element(By.XPATH, Paths.BusChArrivalDate)
        arrivalDate = GetDate(arrivalDate.text, date)
        # Вставляем в таблицу, потом перееиспользуем
        startPointInfo = detailedInfoFields[1].find_element(By.CLASS_NAME, CN.BusChStartPointInfo)
        arrivalPointInfo = detailedInfoFields[1].find_element(By.CLASS_NAME, CN.BusChArrivalPointInfo)
        startTime = startPointInfo.find_element(By.XPATH, Paths.BusChStartTime)
        startTime = GetTime(startTime.text)
        arrivalTime = arrivalPointInfo.find_element(By.XPATH, Paths.BusChArrivalTime)
        arrivalTime = GetTime(arrivalTime.text)
        startDate = startPointInfo.find_element(By.XPATH, Paths.BusChStartDate)
        startDate = GetDate(startDate.text, date)
        arrivalDate = arrivalPointInfo.find_element(By.XPATH, Paths.BusChArrivalDate)
        arrivalDate = GetDate(arrivalDate.text, date)
        citys1 = detailedInfoFields[0].find_element(By.CLASS_NAME, CN.BusChCityInfo)
        citys2 = detailedInfoFields[1].find_element(By.CLASS_NAME, CN.BusChCityInfo)
        price1 = detailedInfoFields[0].find_element(By.CLASS_NAME, CN.BusChTicketPrice)
        price1 = GetPrice(price1.text)
        price2 = detailedInfoFields[1].find_element(By.CLASS_NAME, CN.BusChTicketPrice)
        price2 = GetPrice(price2.text)
        changeTime = addInfoField.find_element(By.CLASS_NAME, CN.BusChChangeTime)
        fullTime = changeTime.find_element(By.XPATH, Paths.BusChFullTime)
        changeTime = GetTravelTime(changeTime)
        fullTime = GetTravelTime(fullTime)
        fullPrice = addInfoField.find_element(By.CLASS_NAME, CN.BusChFullPrice)
        fullPrice = GetPrice(fullPrice.text)
        ticketURL = addInfoField.find_element(By.CLASS_NAME, CN.BusTicketURL)
        ticketURL = ticketURL.get_attribute('href')
        try:
            seatsNumber = mainInfoFields[0].find_element(By.CLASS_NAME, CN.BusChSeatsNumber)
            seatsNumber = GetNumberOfSeats(seatsNumber.text)
        except:
            pass
        try:
            seatsNumber = mainInfoFields[1].find_element(By.CLASS_NAME, CN.BusChSeatsNumber)
            seatsNumber = GetNumberOfSeats(seatsNumber.text)
        except:
            pass


def GetBussDataWithoutChange(busInfoFields: list[WebElement], driver):
    for busInfoField in busInfoFields:
        driver.execute_script("arguments[0].scrollIntoView(true);", busInfoField)
        showDetails = busInfoField.find_element(By.CLASS_NAME, CN.BusDetails)
        showDetails.click()
        startField = WebElement
        success = True
        while success:
            time.sleep(0.2)
            try:
                startField = busInfoField.find_element(By.CLASS_NAME, CN.BusStartField)
                success = False
            except:
                success = True
        arrivalField = busInfoField.find_element(By.CLASS_NAME, CN.BusArrivalField)
        startTime = startField.find_element(By.XPATH, Paths.BusStartTime)
        startTime = GetTime(startTime.text)
        arrivalTime = arrivalField.find_element(By.XPATH, Paths.BusArrivalTime)
        arrivalTime = GetTime(arrivalTime.text)
        startDate = startField.find_element(By.XPATH, Paths.BusStartDate)
        startDate = GetDate(startDate.text, date)
        arrivalDate = arrivalField.find_element(By.XPATH, Paths.BusArrivalDate)
        arrivalDate = GetDate(arrivalDate.text, date)
        travelTime = busInfoField.find_element(By.CLASS_NAME, CN.BusTravelTime)
        travelTime = GetTravelTime(travelTime)
        ticketPrice = busInfoField.find_element(By.CLASS_NAME, CN.BusTicketPrice)
        ticketPrice = GetPrice(ticketPrice.text)
        ticketURL = busInfoField.find_element(By.CLASS_NAME, CN.BusTicketURL)
        ticketURL = ticketURL.get_attribute('href')
        try:
            seatsNumber = busInfoField.find_element(By.XPATH, Paths.BusSeatsNumber)
            seatsNumber = GetNumberOfSeats(seatsNumber.text)
        except:
            pass


def GetTime(timeStr):
    timeT = datetime.time(int(timeStr[:2]), int(timeStr[3:]))
    return timeT


def GetDate(inputDate, date: datetime.date):
    return datetime.date(date.year, int(inputDate[3:5]), int(inputDate[:2]))


def GetPrice(price: str):
    price = price.replace(' ', '')
    price = price.replace('руб', '')
    price = price.replace('.', '')
    return int(price)


def GetNumberOfSeats(numberOfSeats: str):
    numberOfSeats = numberOfSeats.replace('Осталось ', '')
    numberOfSeats = numberOfSeats.replace(' места', '')
    numberOfSeats = numberOfSeats.replace(' место', '')
    numberOfSeats = numberOfSeats.replace(' мест', '')
    return int(numberOfSeats)


def GetTravelTime(inputTime: WebElement):
    timeElements = inputTime.find_elements(By.TAG_NAME, 'span')
    travelTime = TimeDelta
    for timeElement in timeElements:
        timeElement = timeElement.text
        dayIndex = timeElement.find('д')
        hourIndex = timeElement.find('ч')
        minuteIndex = timeElement.find('м')
        if dayIndex != -1:
            travelTime.Days = int(timeElement[:dayIndex])
        elif hourIndex != -1:
            travelTime.Hours = int(timeElement[:hourIndex])
        elif minuteIndex != -1:
            travelTime.Minutes = int(timeElement[:minuteIndex])
    return travelTime


if __name__ == '__main__':
    date = datetime.date(2022, 7, 16)
    EXE_PATH = r'C:\chromedriver.exe'
    driver2 = webdriver.Chrome(EXE_PATH)
    CheckBuses('Челябинск', 'Пермь', date, driver2)
