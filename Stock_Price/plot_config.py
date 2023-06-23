import io
import base64
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
# Avoid UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
matplotlib.use('agg')


def slice_data(stock_data, period):
    today = datetime.now()

    if period == "1_year":
        start_date = today - pd.DateOffset(years=1)
    elif period == "2_years":
        start_date = today - pd.DateOffset(years=2)
    elif period == "6_months":
        start_date = today - pd.DateOffset(months=6)
    elif period == "1_month":
        start_date = today - pd.DateOffset(months=1)
    else:
        # max
        return stock_data

    start_date = start_date.strftime('%Y-%m-%d')
    dataframe_for_plot = stock_data[start_date:]
    return dataframe_for_plot


def plot_stock_data(stock_data, period):

    dataframe_for_plot = slice_data(stock_data, period)

    plt.figure(figsize=(10, 4))
    plt.plot(dataframe_for_plot['Close'], linewidth=1)
    plt.ylabel('Close Price')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return plot_data
