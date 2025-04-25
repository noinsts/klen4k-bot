from src.db.base import DatabaseConnection

from src.db.models.auction import AuctionModel
from src.db.models.balance import BalanceModel
from src.db.models.birthdays import BirthdayModel
from src.db.models.colors import ColorModel
from src.db.models.location import LocationModel
from src.db.models.logs import LogsModel
from src.db.models.phones import PhoneModel
from src.db.models.taxes import TaxModel
from src.db.models.weather_advices import WeatherAdviceModel


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
