import yfinance as yf


class StockData:

    len_table = 28  # length of dataframe shown in HTML

    def __init__(self, stock_code: str = 'TSLA', period: str = 'max', interval: str = '1d'):
        self.stock_code = stock_code
        self.period = period
        self.interval = interval
        self.raw_data = yf.Ticker(stock_code).history(
            period=period, interval=interval)
        self.data = self.data_cleaning()
        self.current_table_page = 1
        self.max_table_page = self.data.shape[0] // StockData.len_table

    def data_cleaning(self):
        data = self.raw_data.copy()
        # data.index = data.index.date  # set datetime index to date index
        data.index.name = None
        return data

    # data for plotting
    def get_close_price(self):
        return self.data[['Close']]

    def get_volume(self):
        return self.data[['Volume']]

    # data for displaying tables
    def get_table_data(self, columns: list = ['Open', 'Close', 'Volume']):
        if self.current_table_page == 1:
            return self.data[columns].iloc[-(StockData.len_table*self.current_table_page):]
        else:
            return self.data[columns].iloc[-(StockData.len_table*self.current_table_page):-(StockData.len_table*(self.current_table_page-1))]

    def update_table_data(self, columns: list = ['Open', 'Close', 'Volume'], action: str = 'prev'):
        if action == 'prev':
            if self.max_table_page > self.current_table_page:
                self.current_table_page += 1
        elif action == 'next':
            if self.current_table_page > 1:
                self.current_table_page -= 1
        else:
            raise Exception('Table Action Not Defined!')
        return self.get_table_data(columns)

    # get single point data
    def get_current_price(self):
        return float(self.data['Close'].iloc[-1])
