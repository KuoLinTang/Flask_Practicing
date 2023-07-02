from flask import Flask, render_template, request
from grocery_scraping import asda_func, sains_func, tesco_func
from itemdata import ItemData

app = Flask('Stock Exchanger', static_folder='static',
            template_folder='template')


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/scrap_items/', methods=["POST", "GET"])
def scrap_items():

    item_name = request.form['item_name']

    if item_name != None and len(item_name) > 0:

        print(item_name)
        n = 10
        asda_list = [ItemData(*i) for i in asda_func.asda(item=item_name, n=n)]
        sains_list = [ItemData(*i)
                      for i in sains_func.sainsbury(item=item_name, n=n)]
        tesco_list = [ItemData(*i)
                      for i in tesco_func.tesco(item=item_name, n=n)]

        print(asda_list[0].name)


if __name__ == "__main__":
    app.run(debug=True)
