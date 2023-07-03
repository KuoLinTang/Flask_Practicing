from flask import Flask, render_template, request
from grocery_scraping import asda_func, sains_func, tesco_func, all_in_one
from itemdata import ItemData
from multiprocessing import Pool

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
        grocery_store = ['asda', 'sainsbury', 'tesco']

        # multiprocessing the web scraping process
        with Pool() as p:
            result_list = p.starmap(all_in_one.get_items, zip(
                [item_name]*3, [n]*3, grocery_store))

        ItemData_list = []
        for i in range(len(grocery_store)):
            for j in result_list[i]:
                ItemData_list.append(
                    ItemData(
                        business=grocery_store[i],
                        name=j[0],
                        volume=j[1],
                        price=j[2],
                        unit_price=j[3],
                        img=j[4]
                    )
                )

        print(ItemData_list[0].business,
              ItemData_list[0].name, ItemData_list[0].price)

        return 0


if __name__ == "__main__":
    app.run(debug=True)
