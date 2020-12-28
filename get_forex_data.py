from forex_python.bitcoin import BtcConverter

class PriceGetter:
    def __init__(self, currencies_list):
        self.currencies = currencies_list
        self.bitcoin = BtcConverter()

    def get_price(self):
        result = dict()
        for curr in self.currencies:
            result[curr] = self.bitcoin.get_latest_price(curr)
        return result
