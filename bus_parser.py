import datetime
import time

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


class BusParser:
    driver: webdriver
    date: datetime.date
    cityFrom: str
    cityTo: str

    def __init__(self, cityFrom, cityTo, date: datetime.date, driver: webdriver):
        self.cityTo = cityTo
        self.cityFrom = cityFrom
        self.date = date
        self.driver = driver

    def CheckBuses(self):
        self.driver.get('https://unitiki.com')
        moveTo = self.driver.find_element(By.XPATH, Paths.BusMoveToField)
        moveTo.send_keys(self.cityTo)
        time.sleep(1.5)
        moveFrom = self.driver.find_element(By.XPATH, Paths.BusMoveFromField)
        moveFrom.send_keys(self.cityFrom)
        time.sleep(1.5)
        dateField = self.driver.find_element(By.XPATH, Paths.BusDateField)
        self.driver.execute_script("arguments[0].removeAttribute('readonly')", dateField)
        for i in range(11):
            dateField.send_keys(Keys.BACKSPACE)
        dateField.send_keys(str(self.date.day) + '.' + str(self.date.month) + '.' + str(self.date.year))
        checkButton = self.driver.find_element(By.XPATH, Paths.BusCheckButton)
        checkButton.click()
        try:
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, CN.BusInfoFields)))
        except:
            return None
        time.sleep(4)
        busInfoFields = self.driver.find_elements(By.CLASS_NAME, CN.BusInfoFields)
        try:
            busInfoFields[0].find_element(By.CLASS_NAME, CN.BusDetails)
            return self.__GetBussDataWithoutChange(busInfoFields)
        except:
            return self.__GetBussDataWithChange(busInfoFields)

    def __GetBussDataWithChange(self, busInfoFields: list[WebElement]):
        tickets = []
        for busInfoField in busInfoFields:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", busInfoField)
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
            travelTime1 = self.__GetTravelTime(travelTime1)
            travelTime2 = mainInfoFields[1].find_element(By.CLASS_NAME, CN.BusChTravelTime)
            travelTime2 = self.__GetTravelTime(travelTime2)
            startPointInfo = detailedInfoFields[0].find_element(By.CLASS_NAME, CN.BusChStartPointInfo)
            arrivalPointInfo = detailedInfoFields[0].find_element(By.CLASS_NAME, CN.BusChArrivalPointInfo)
            startTime1 = startPointInfo.find_element(By.XPATH, Paths.BusChStartTime)
            startTime1 = self.__GetTime(startTime1.text)
            arrivalTime1 = arrivalPointInfo.find_element(By.XPATH, Paths.BusChArrivalTime)
            arrivalTime1 = self.__GetTime(arrivalTime1.text)
            startDate1 = startPointInfo.find_element(By.XPATH, Paths.BusChStartDate)
            startDate1 = self.__GetDate(startDate1.text, self.date)
            arrivalDate1 = arrivalPointInfo.find_element(By.XPATH, Paths.BusChArrivalDate)
            arrivalDate1 = self.__GetDate(arrivalDate1.text, self.date)
            startPointInfo = detailedInfoFields[1].find_element(By.CLASS_NAME, CN.BusChStartPointInfo)
            arrivalPointInfo = detailedInfoFields[1].find_element(By.CLASS_NAME, CN.BusChArrivalPointInfo)
            startTime2 = startPointInfo.find_element(By.XPATH, Paths.BusChStartTime)
            startTime2 = self.__GetTime(startTime2.text)
            arrivalTime2 = arrivalPointInfo.find_element(By.XPATH, Paths.BusChArrivalTime)
            arrivalTime2 = self.__GetTime(arrivalTime2.text)
            startDate2 = startPointInfo.find_element(By.XPATH, Paths.BusChStartDate)
            startDate2 = self.__GetDate(startDate2.text, self.date)
            arrivalDate2 = arrivalPointInfo.find_element(By.XPATH, Paths.BusChArrivalDate)
            arrivalDate2 = self.__GetDate(arrivalDate2.text, self.date)
            citys1 = detailedInfoFields[0].find_element(By.CLASS_NAME, CN.BusChCityInfo)
            citys1 = self.__GetCitys(citys1.text)
            citys2 = detailedInfoFields[1].find_element(By.CLASS_NAME, CN.BusChCityInfo)
            citys2 = self.__GetCitys(citys2.text)
            price1 = detailedInfoFields[0].find_element(By.CLASS_NAME, CN.BusChTicketPrice)
            price1 = self.__GetPrice(price1.text)
            price2 = detailedInfoFields[1].find_element(By.CLASS_NAME, CN.BusChTicketPrice)
            price2 = self.__GetPrice(price2.text)
            changeTime = addInfoField.find_element(By.CLASS_NAME, CN.BusChChangeTime)
            fullTime = changeTime.find_element(By.XPATH, Paths.BusChFullTime)
            changeTime = self.__GetTravelTime(changeTime)
            fullTime = self.__GetTravelTime(fullTime)
            fullPrice = addInfoField.find_element(By.CLASS_NAME, CN.BusChFullPrice)
            fullPrice = self.__GetPrice(fullPrice.text)
            ticketURL = addInfoField.find_element(By.CLASS_NAME, CN.BusTicketURL)
            ticketURL = ticketURL.get_attribute('href')
            seatsNumber = None
            try:
                seatsNumber = mainInfoFields[0].find_element(By.CLASS_NAME, CN.BusChSeatsNumber)
                seatsNumber = self.__GetNumberOfSeats(seatsNumber.text)
            except:
                pass
            tickets.append(TicketData(citys1[0], citys1[1], arrivalDate1, arrivalTime1, startDate1, startTime1,
                                      travelTime1, seatsNumber, price1, ticketURL, TicketType.bus, True, changeTime,
                                      fullTime, fullPrice))
            try:
                seatsNumber = mainInfoFields[1].find_element(By.CLASS_NAME, CN.BusChSeatsNumber)
                seatsNumber = self.__GetNumberOfSeats(seatsNumber.text)
            except:
                pass
            tickets.append(TicketData(citys2[0], citys2[1], arrivalDate2, arrivalTime2, startDate2, startTime2,
                                      travelTime2, seatsNumber, price2, ticketURL, TicketType.bus))
        return tickets

    def __GetBussDataWithoutChange(self, busInfoFields: list[WebElement]):
        tickets = []
        for busInfoField in busInfoFields:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", busInfoField)
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
            startTime = self.__GetTime(startTime.text)
            arrivalTime = arrivalField.find_element(By.XPATH, Paths.BusArrivalTime)
            arrivalTime = self.__GetTime(arrivalTime.text)
            startDate = startField.find_element(By.XPATH, Paths.BusStartDate)
            startDate = self.__GetDate(startDate.text, self.date)
            arrivalDate = arrivalField.find_element(By.XPATH, Paths.BusArrivalDate)
            arrivalDate = self.__GetDate(arrivalDate.text, self.date)
            travelTime = busInfoField.find_element(By.CLASS_NAME, CN.BusTravelTime)
            travelTime = self.__GetTravelTime(travelTime)
            ticketPrice = busInfoField.find_element(By.CLASS_NAME, CN.BusTicketPrice)
            ticketPrice = self.__GetPrice(ticketPrice.text)
            ticketURL = busInfoField.find_element(By.CLASS_NAME, CN.BusTicketURL)
            ticketURL = ticketURL.get_attribute('href')
            seatsNumber = None
            try:
                seatsNumber = busInfoField.find_element(By.XPATH, Paths.BusSeatsNumber)
                seatsNumber = self.__GetNumberOfSeats(seatsNumber.text)
            except:
                pass
            tickets.append(
                TicketData(self.cityFrom, self.cityTo, arrivalDate, arrivalTime, startDate, startTime, travelTime,
                           seatsNumber, ticketPrice, ticketURL, TicketType.bus))
        return tickets

    def __GetTime(self, timeStr):
        timeT = datetime.time(int(timeStr[:2]), int(timeStr[3:]))
        return timeT

    def __GetDate(self, inputDate, date: datetime.date):
        return datetime.date(date.year, int(inputDate[3:5]), int(inputDate[:2]))

    def __GetPrice(self, price: str):
        price = price.replace(' ', '')
        price = price.replace('руб', '')
        price = price.replace('.', '')
        return int(price)

    def __GetNumberOfSeats(self, numberOfSeats: str):
        numberOfSeats = numberOfSeats.replace('Осталось ', '')
        numberOfSeats = numberOfSeats.replace(' места', '')
        numberOfSeats = numberOfSeats.replace(' место', '')
        numberOfSeats = numberOfSeats.replace(' мест', '')
        return int(numberOfSeats)

    def __GetCitys(self, citys: str):
        citys = citys.replace(' – ', '+')
        citysList = [citys[:citys.find('+')], citys[citys.find('+') + 1:]]
        return citysList

    def __GetTravelTime(self, inputTime: WebElement):
        timeElements = inputTime.find_elements(By.TAG_NAME, 'span')
        travelTime: TimeDelta = TimeDelta()
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
