import datetime
from enum import Enum
from typing import Optional

from TimeDelta import TimeDelta


class TicketType(Enum):
    aircraft = 0
    train = 1
    bus = 2


class TicketData:
    ticketType: TicketType
    cityFrom: str
    cityTo: str
    arrivalDate: datetime.date
    arrivalTime: datetime.time
    startDate: datetime.date
    startTime: datetime.time
    travelTime: TimeDelta
    numberOfSeats: Optional[int]
    price: int
    URL: str

    change: bool
    changeTime: Optional[TimeDelta]
    fullWayTime: Optional[TimeDelta]
    fullWayPrice: Optional[int]

    # def __init__(self, text_price: str, text_desc: str, url):

    # data_price = text_price.split('\n')
    # data_desc = text_desc.split('\n')
    # val = len(data_desc)

    # self.arrivalDate = data_desc[val-1]
    # self.arrivalTime = data_desc[val-3]
    # self.startDate = data_desc[val-7]
    # self.startTime = data_desc[val-9]
    # self.travelTime = data_desc[val-6]
    # self.carriageType = NULL
    # self.numberOfSeats = 0
    # self.URL = url
    # self.price = data_price[0]

    def __init__(self, cityFrom: str, cityTo: str, arrivalDate: datetime.date, arrivalTime: datetime.time,
                 startDate: datetime.date, startTime: datetime.time, travelTime: TimeDelta, numberOfSeats: int,
                 price: int, URL: str, ticketType: TicketType, change: bool = False, changeTime: TimeDelta = None,
                 fullWayTime: TimeDelta = None, fullWayPrice: int = None):
        self.cityFrom = cityFrom
        self.cityTo = cityTo
        self.arrivalDate = arrivalDate
        self.arrivalTime = arrivalTime
        self.startDate = startDate
        self.startTime = startTime
        self.travelTime = travelTime
        self.numberOfSeats = numberOfSeats
        self.URL = URL
        self.ticketType = ticketType
        self.price = price
        self.change = change
        self.changeTime = changeTime
        self.fullWayTime = fullWayTime
        self.fullWayPrice = fullWayPrice

    def __str__(self) -> str:
        return f"{self.arrivalDate}\n" \
               f"{self.arrivalTime}\n" \
               f"{self.startDate}\n" \
               f"{self.startTime}\n" \
               f"{self.travelTime}\n" \
               f"{self.numberOfSeats}\n" \
               f"{self.URL}\n" \
               f"{self.price}\n"
