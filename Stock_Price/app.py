from stockdata import StockData
import io
from flask import Flask, render_template, request, Response
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
# Avoid UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
matplotlib.use('agg')

app = Flask('Stock Exchanger', static_folder='static',
            template_folder='template')

company_list = ['Microsoft', 'Tesla', 'Nvidia', 'Apple',
                'Google', 'Amazon', 'Meta', 'AMD', 'Netflix']
stock_list = ['MSFT', 'TSLA', 'NVDA', 'AAPL',
              'GOOGL', 'AMZN', 'META', 'AMD', 'NFLX']
stock_dict = dict(zip(company_list, stock_list))
stock_data = StockData()


def plot_stock_data(stock_data):

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(stock_data['Close'], linewidth=1)
    ax.set_ylabel('Close Price')

    return fig


@app.route('/')
def home():
    return render_template('homepage.html', company_options=company_list)


@app.route('/stock/', methods=["POST", "GET"])
def stock():
    global stock_data
    company = request.form['selection']
    stock = stock_dict[company]  # get value of a business key
    stock_data = StockData(stock)
    return render_template('stock.html', company=company, stock=stock,
                           dataframe_left=stock_data.data.iloc[-14:-7].to_html(),
                           dataframe_right=stock_data.data.iloc[-7:].to_html())


# flask will create the plot when the stock.html is rendered
@app.route('/stock/plot.png')
def plot():
    global stock_data
    fig = plot_stock_data(stock_data.get_close_price())
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)
