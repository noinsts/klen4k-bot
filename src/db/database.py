from .base import DatabaseConnection

from .models import *


class Database:
    def __init__(self):
        self.connection = DatabaseConnection()

        self.auction = AuctionModel(self.connection)
        self.balance = BalanceModel(self.connection)
        self.birthday = BirthdayModel(self.connection)
        self.color = ColorModel(self.connection)
        self.location = LocationModel(self.connection)
        self.logs = LogsModel(self.connection)
        self.phone = PhoneModel(self.connection)
        self.taxes = TaxModel(self.connection)
        self.weather_advice = WeatherAdviceModel(self.connection)


    def close(self):
        self.connection.close()
