import datetime

from TimeDelta import TimeDelta
from typing import Optional


class BusData:
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

    def __init__(self, arrivalDate: datetime.date, arrivalTime: datetime.time, startDate: datetime.date,
                 startTime: datetime.time, travelTime: TimeDelta, numberOfSeats: Optional[int], price: int, URL: str,
                 change: bool, changeTime: Optional[TimeDelta], fullWayTime: Optional[TimeDelta], fullWayPrice: Optional[int]):
        self.arrivalDate = arrivalDate
        self.arrivalTime = arrivalTime
        self.startDate = startDate
        self.startTime = startTime
        self.travelTime = travelTime
        self.numberOfSeats = numberOfSeats
        self.URL = URL
        self.price = price
        self.change = change
        self.changeTime = changeTime
        self.fullWayTime = fullWayTime
        self.fullWayPrice = fullWayPrice
