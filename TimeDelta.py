class TimeDelta:
    Days: int = 0
    Hours: int = 0
    Minutes: int = 0

    def __str__(self) -> str:
        return \
            f"{self.Days }" + ' дней, ' + f"{self.Hours}" + ' часов, ' + f"{self.Minutes}" + ' минут'

