from forex_python.bitcoin import BtcConverter
import datetime

class PriceGetter:
    def __init__(self, currencies_list):
        self.currencies = currencies_list
        self.bitcoin = BtcConverter()

    def get_price(self):
        result = dict()
        result['datetime'] = str(datetime.datetime.now())
        for curr in self.currencies:
            result[curr] = self.bitcoin.get_latest_price(curr)
        
        return result
