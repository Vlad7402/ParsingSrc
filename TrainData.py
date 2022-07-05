import datetime
import enum
from TimeDelta import TimeDelta


class TrainType(enum.Enum):
    Seating = 1  # Сидячий вагон
    Lying = 2  # Плацкарт вагон
    Coupe = 3  # Купе вагон
    Slipping = 4  # Спальный вагон (СВ)


TrainTypeDict = dict(Плацкарт=TrainType.Lying, Сидячий=TrainType.Seating, Купе=TrainType.Coupe, СВ=TrainType.Slipping)

class TrainData:
    arrivalDate: datetime.date
    arrivalTime: datetime.time
    startDate: datetime.date
    startTime: datetime.time
    travelTime: TimeDelta
    carriageType: TrainType
    numberOfSeats: int
    price: int
    URL: str

    def __init__(self, arrivalDate: datetime.date, arrivalTime: datetime.time, startDate: datetime.date,
                 startTime: datetime.time, travelTime: TimeDelta,
                 carriageType: TrainType, numberOfSeats: int, price: int, URL: str):
        self.arrivalDate = arrivalDate
        self.arrivalTime = arrivalTime
        self.startDate = startDate
        self.startTime = startTime
        self.travelTime = travelTime
        self.carriageType = carriageType
        self.numberOfSeats = numberOfSeats
        self.URL = URL
        self.price = price
