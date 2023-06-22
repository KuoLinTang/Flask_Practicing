import io
from flask import Flask, render_template, request, Response
import yfinance as yf
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


def get_stock_data(stock_code: str):
    stock_data = yf.Ticker(stock_code).history(period="max")
    return stock_data


def plot_stock_data(stock_data, stock):

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(stock_data['Close'], linewidth=1)
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price')
    ax.set_title(f'{stock} Historical Chart')

    return fig


@app.route('/')
def home():
    return render_template('homepage.html', company_options=company_list)


@app.route('/stock/', methods=["POST", "GET"])
def stock():
    company = request.form['selection']
    stock = stock_dict[company]  # get value of a business key
    dataframe = get_stock_data(stock)
    return render_template('stock.html', company=company, stock=stock,
                           dataframe=dataframe.tail(14).to_html())


# flask will create the plot when the stock.html is rendered
@app.route('/stock/plot.png')
def plot():
    stock = request.args.get('stock')
    dataframe = get_stock_data(stock)
    fig = plot_stock_data(dataframe, stock)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)
