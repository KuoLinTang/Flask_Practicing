from stockdata import StockData
from plot_config import plot_stock_data
from flask import Flask, render_template, request

app = Flask('Stock Exchanger', static_folder='static',
            template_folder='template')

company_list = ['Microsoft', 'Tesla', 'Nvidia', 'Apple',
                'Google', 'Amazon', 'Meta', 'AMD', 'Netflix']
stock_list = ['MSFT', 'TSLA', 'NVDA', 'AAPL',
              'GOOGL', 'AMZN', 'META', 'AMD', 'NFLX']
stock_dict = dict(zip(company_list, stock_list))
stock_data = StockData()


@app.route('/')
def home():
    return render_template('homepage.html', company_options=company_list)


@app.route('/stock/', methods=["POST", "GET"])
def stock():
    global stock_data
    company = request.form['selection']
    stock = stock_dict[company]  # get value of a business key
    stock_data = StockData(stock)
    plot_data = plot_stock_data(stock_data.get_close_price(), 'Max')
    return render_template('stock.html', company=company, stock=stock,
                           dataframe_left=stock_data.data.iloc[-14:-7].to_html(),
                           dataframe_right=stock_data.data.iloc[-7:].to_html(),
                           plot_data=plot_data)


# flask will create the plot when the stock.html is rendered
@app.route('/stock/update_plot', methods=['POST'])
def update_plot():
    global stock_data
    time_period = request.form['period']
    plot_data = plot_stock_data(stock_data.get_close_price(), time_period)
    return {'plot_data': plot_data}


if __name__ == "__main__":
    app.run(debug=True)
