import yfinance as yf


class StockData:

    def __init__(self, stock_code: str = 'TSLA', period: str = 'max', interval: str = '1d'):
        self.stock_code = stock_code
        self.period = period
        self.interval = interval
        self.data = yf.Ticker(stock_code).history(
            period=period, interval=interval)

    def get_close_price(self):
        return self.data[['Close']]

    def get_volume(self):
        return self.data[['Volume']]
