from flask import Flask, render_template, request, jsonify, Response
from grocery_scraping import asda_func, sains_func, tesco_func, all_in_one
from itemdata import ItemData
from multiprocessing.dummy import Pool as ThreadPool
import json

app = Flask('Stock Exchanger', static_folder='static',
            template_folder='template')


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/scrap_items/', methods=["POST"])
def scrap_items():

    def list_to_object(item_list, business):

        result_list = []
        for i in item_list:
            result_list.append(
                ItemData(
                    business=business,
                    name=i[0],
                    volume=i[1],
                    price=i[2],
                    unit_price=i[3],
                    img=i[4]
                )
            )
        return result_list

    item_name = request.form['item_name']
    print(item_name)

    if item_name != None and len(item_name) > 0:

        n = 10
        grocery_store = ['asda', 'sainsbury', 'tesco']

        # multiprocessing the web scraping process
        with ThreadPool(3) as p:
            result_list = p.starmap(all_in_one.get_items, zip(
                [item_name]*3, [n]*3, grocery_store))

        asda_list = list_to_object(result_list[0], 'asda')
        sains_list = list_to_object(result_list[0], 'sainsbury')
        tesco_list = list_to_object(result_list[0], 'tesco')

        enc_asda = [i.__dict__ for i in asda_list]
        enc_sains = [i.__dict__ for i in sains_list]
        enc_tesco = [i.__dict__ for i in tesco_list]

        response = jsonify(asda_result=enc_asda,
                           sains_result=enc_sains, tesco_result=enc_tesco)
        return response, 200

    else:
        response = jsonify({'message': 'invalid item name'})
        return response, 400


if __name__ == "__main__":
    app.run(debug=True)
