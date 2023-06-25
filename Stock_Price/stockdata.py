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

    def get_current_price(self):
        return float(self.data['Close'].iloc[-1])

    def get_data_by_range(self, columns: list = ['High', 'Low', 'Close', 'Volume'], start_index: int = 0, end_index=None):
        return self.data[columns].iloc[start_index:end_index]
