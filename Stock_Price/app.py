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
time_period, measure = '', ''


@app.route('/')
def home():
    return render_template('homepage.html', company_options=company_list)


@app.route('/stock/', methods=["POST", "GET"])
def stock():
    global stock_data
    company = request.form['selection']
    stock = stock_dict[company]  # get value of a business key
    stock_data = StockData(stock)
    current_price = stock_data.get_current_price()
    plot_data = plot_stock_data(stock_data, period='Max', measure='Price')
    return render_template('stockpage.html',
                           company=company, stock=stock, current_price=f'{current_price:.6f}',
                           table_left=stock_data.get_data_by_range(start_index=-28, end_index=-14).to_html(
                               classes='data', header=True),
                           table_right=stock_data.get_data_by_range(start_index=-14).to_html(
                               classes='data', header=True),
                           plot_data=plot_data)


# update period of plot
@app.route('/stock/update_plot_period/', methods=['POST'])
def update_plot_period():
    global stock_data, time_period, measure
    time_period = request.form['period']
    plot_data = plot_stock_data(
        stock_data, measure=measure, period=time_period
    )
    return {'plot_data': plot_data}


# update period of plot
@app.route('/stock/update_plot_measure/', methods=['POST'])
def update_plot_measure():
    global stock_data, time_period, measure
    measure = request.form['measure']
    plot_data = plot_stock_data(
        stock_data, measure=measure, period=time_period
    )
    return {'plot_data': plot_data, }


@app.route('/initialise-variables/', methods=['POST'])
def initialise_variables():
    global stock_data, time_period, measure
    stock_data = StockData()
    time_period = 'Max'
    measure = 'Price'


if __name__ == "__main__":
    app.run(debug=True)
