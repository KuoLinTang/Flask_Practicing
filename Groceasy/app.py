from flask import Flask, render_template, request
from grocery_scraping import asda_func, sains_func, tesco_func
from itemdata import ItemData

app = Flask('Stock Exchanger', static_folder='static',
            template_folder='template')


@app.route('/')
def home():
    return render_template('homepage.html')


if __name__ == "__main__":
    app.run(debug=True)
