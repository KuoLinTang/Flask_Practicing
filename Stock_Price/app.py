from flask import Flask, render_template, request
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os
import time

img_name = 'line_plot.png'
img_full_name = f'D:/Programming/Flask_Practicing/Stock_Price/template/{img_name}'

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


# def plot_stock_data(stock_data, stock):
#     if os.path.isfile(img_full_name):
#         os.remove(img_full_name)
#     time.sleep(1)
#     plt.plot(stock_data['Close'], linewidth=1)
#     plt.xlabel('Date')
#     plt.ylabel('Close Price')
#     plt.title(f'{stock} Historical Chart')
#     plt.savefig(img_full_name)
#     plt.close()


@app.route('/')
def home():
    return render_template('homepage.html', company_options=company_list)


@app.route('/stock/', methods=["POST"])
def stock():
    company = request.form['selection']
    stock = stock_dict[company]  # get value of a business key
    dataframe = get_stock_data(stock)
    # plot_stock_data(dataframe, stock)
    return render_template('stock.html', company=company, stock=stock,
                           dataframe=dataframe.tail(14).to_html())


if __name__ == "__main__":
    app.run(debug=True)
