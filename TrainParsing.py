import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from HTMLData import ClassNames as CN
from HTMLData import XPaths as Paths
from TimeDelta import TimeDelta
from ticket_data import TicketData, TicketType


class TrainParser:
    driver: webdriver
    date: datetime.date
    cityFrom: str
    cityTo: str

    def __init__(self, cityFrom, cityTo, date: datetime.date, driver: webdriver):
        self.cityTo = cityTo
        self.cityFrom = cityFrom
        self.date = date
        self.driver = driver

    def CheckTrains(self):
        self.__TrainsLookForRoot(self.cityFrom, self.cityTo, self.driver)
        success = True
        while success:
            try:
                self.driver.get(
                    self.driver.current_url + '&date=' + str(self.date.day) + '.' + str(self.date.month) + '.' + str(
                        self.date.year))
                success = False
            except:
                success = True
        try:
            self.driver.find_element(By.CLASS_NAME, CN.TrainSearchError)
            return None
        except:
            pass
        page = self.driver.find_element(By.TAG_NAME, 'html')
        for i in range(50):
            page.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
        trains = self.driver.find_elements(By.CLASS_NAME, CN.TrainInfoFields)
        trainsData = []
        for trainIfoField in trains:
            dateFields = trainIfoField.find_elements(By.CLASS_NAME, CN.TrainDateFields)
            startTime = dateFields[0].find_element(By.CLASS_NAME, CN.TrainTimeField)
            arrivalTime = dateFields[1].find_element(By.CLASS_NAME, CN.TrainTimeField)
            travelTime = dateFields[2].find_element(By.CLASS_NAME, CN.TrainTravelTime)
            travelTime = travelTime.find_element(By.TAG_NAME, 'span')
            trainOffers = trainIfoField.find_elements(By.XPATH, Paths.TrainOffers)
            startTime = self.__GetTime(startTime.text)
            arrivalTime = self.__GetTime(arrivalTime.text)
            travelTime = self.__GetTravelTime(travelTime.text)
            for trainOffer in trainOffers:
                try:
                    priceOffer = trainOffer.find_element(By.XPATH, Paths.TrainPrice)
                    priceOffer = self.__GetPrice(priceOffer.text)
                    trainType = trainOffer.find_element(By.XPATH, Paths.TrainType)
                    numberOfSeats = trainOffer.find_element(By.XPATH, Paths.TrainNumberOfSeats)
                    numberOfSeats = self.__GetNumberOfSeats(numberOfSeats.text)
                    try:
                        arrivalDate = dateFields[1].find_element(By.XPATH, Paths.TrainArrivalDate)
                        arrivalDate = self.__GetArrivalDate(arrivalDate.text)
                        arrivalDate = datetime.date(self.date.year, self.date.month, arrivalDate)
                        if arrivalDate.day < self.date.day:
                            arrivalDate.month += 1
                    except:
                        arrivalDate = self.date
                    trainsData.append(
                        TicketData(self.cityFrom, self.cityTo, arrivalDate, arrivalTime, self.date, startTime,
                                   travelTime, numberOfSeats, priceOffer, self.driver.current_url, TicketType.train))
                except:
                    pass
        return trainsData

    def __GetTime(self, timeStr):
        timeT = datetime.time(int(timeStr[:2]), int(timeStr[3:]))
        return timeT

    def __GetTravelTime(self, dateStr: str):
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

    def __GetNumberOfSeats(self, inputStr):
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

    def __GetPrice(self, inputStr):
        inputStr = inputStr.replace(' ', '')
        inputStr = inputStr.replace('₽', '')
        return int(inputStr)

    def __GetArrivalDate(self, inputStr):
        spaceIndex = str.find(inputStr, ' ')
        return int(inputStr[:spaceIndex])

    def CheckCityName(self, name, driver):
        self.__TrainsLookForRoot(name, driver)
        try:
            driver.find_element(By.CLASS_NAME, CN.TrainCityError)
            return False
        except:
            return True

    def __TrainsLookForRoot(self, cityFrom, cityTo, driver):
        driver.get('https://m.tutu.ru/poezda/')
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Paths.TrainBanner)))
            banner = driver.find_element(By.XPATH, Paths.TrainBanner)
            banner.click()
        except:
            pass
        moveTo = driver.find_element(By.XPATH, Paths.TrainMoveTo)
        moveTo.send_keys(cityTo)
        time.sleep(1.5)
        moveFrom = driver.find_element(By.XPATH, Paths.TrainMoveFrom)
        moveFrom.send_keys(cityFrom)
        time.sleep(1.5)
        checkButton = driver.find_element(By.XPATH, Paths.TrainCheckButton)
        checkButton.click()
