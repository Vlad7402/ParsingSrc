class XPaths:
    TrainBanner = '//*[@id="app"]/div[6]/div[2]'
    TrainMoveTo = '//*[@id="app"]/div[1]/div[2]/div/form/div/div[3]/div/div[1]/span/label/input'
    TrainMoveFrom = '//*[@id="app"]/div[1]/div[2]/div/form/div/div[1]/div/div[1]/span/label/input'
    TrainCheckButton = '//*[@id="app"]/div[1]/div[2]/div/form/div/div[5]/button'
    TrainOffers = './div/div/div[2]/div/div/div/div[1]/div/button'
    TrainPrice = './div[2]/div/span[1]/span[2]'
    TrainType = './div[1]/div[1]'
    TrainArrivalDate = './div/div[1]/span[2]'
    TrainNumberOfSeats = './div[1]/div[2]/div/span'
    BusMoveToField = '/html/body/header/div[2]/div/div/form/div[2]/div/div[3]/input[1]'
    BusDateField = '/html/body/header/div[2]/div/div/form/div[2]/div/div[4]/input'
    BusMoveFromField = '/html/body/header/div[2]/div/div/form/div[2]/div/div[1]/input[1]'
    BusCheckButton = '/html/body/header/div[2]/div/div/form/div[2]/button'
    BusSearchError = '/html/body/main/div/section/section[1]/div/div/input'
    BusWithoutChangeCheck = './div[3]/a'
    BusStartTime = './div[1]/span[1]'
    BusArrivalTime = './div[1]/span[1]'
    BusStartDate = './div[1]/span[2]/span'
    BusArrivalDate = './div[1]/span[2]'
    BusSeatsNumber = './div[3]/div[1]/span/span'
    BusShowDetails = './div[6]/ul/li[4]/div/div[2]/span'
    BusDetailsLoadCheck = './div[7]/div[5]/div[2]/span'
    BusChStartTime = './div[1]/span[1]'
    BusChArrivalTime = './div[1]/span[1]'
    BusChStartDate = './div[1]/span[2]/span'
    BusChArrivalDate = './div[1]/span[2]'
    BusChFullTime = './b'


class ClassNames:
    TrainSearchError = '1iUgJ5URl6z56ghLwPPIn'
    TrainCityError = 'titleWrapper__title__3VRv_'
    TrainInfoFields = 'o33164'
    TrainDateFields = 'o33216'
    TrainTimeField = '_3a1WYL55zgpazWtDqg5UKO'
    TrainTravelTime = 'o3369'
    BusInfoFields = 'j-ride-card'
    BusStartField = 'waypoint-thread__point--start'
    BusArrivalField = 'waypoint-thread__point--end'
    BusDetails = 'ride-date__details-link'
    BusTravelTime = 'ride-date__duration'
    BusTicketPrice = 'ride-date__price'
    BusTicketURL = 'j-ride-button'
    BusChMainIfo = 'ride-transfer-segment__route'
    BusChDetailedInfo = 'ride-transfer-info__segment'
    BusChAddInfo = 'ride-transfer-info__header'
    BusChDetails = 'ride-transfer-info__dropdown-control-entity'
    BusChTravelTime = 'ride-transfer-segment__duration'
    BusChStartPointInfo = 'j-ride-point-start'
    BusChArrivalPointInfo = 'j-ride-point-end'
    BusChCityInfo = 'ride-transfer-info__route-title'
    BusChTicketPrice = 'ride-transfer-info__route-price'
    BusChFullPrice = 'price-value'
    BusChChangeTime = 'ride-transfer-info__trip'
    BusChSeatsNumber = 'ride-transfer-segment__places'
    BusChTicketURL = 'ride-transfer-info__button'
