from flask import Flask, render_template, request, jsonify
from grocery_scraping import asda_func, sains_func, tesco_func, all_in_one
from itemdata import ItemData
from multiprocessing.dummy import Pool as ThreadPool
import json

app = Flask('Stock Exchanger', static_folder='static',
            template_folder='template')


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ItemData):
            return obj.__dict__  # 將自定義物件轉換為字典
        return super().default(obj)


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/scrap_items/', methods=["POST", "GET"])
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

    if item_name != None and len(item_name) > 0:

        # n = 10
        # grocery_store = ['asda', 'sainsbury', 'tesco']

        # # multiprocessing the web scraping process
        # with ThreadPool(3) as p:
        #     result_list = p.starmap(all_in_one.get_items, zip(
        #         [item_name]*3, [n]*3, grocery_store))

        # asda_list = list_to_object(result_list[0], 'asda')
        # sains_list = list_to_object(result_list[0], 'sainsbury')
        # tesco_list = list_to_object(result_list[0], 'tesco')

        # business_list = [[o.to_json() for o in asda_list], [o.to_json() for o in sains_list], [o.to_json() for o in tesco_list]]
        business_list = [[ItemData('asda', 'milk', '1L', '2.5', '1').to_json(),
                          ItemData('asda', 'bacon', '1g', '2.5', '1').to_json()],
                         [ItemData('sainsbury', 'milk', '1L', '2.5', '1').to_json(),
                          ItemData('sainsbury', 'bacon', '1g', '2.5', '1').to_json()],
                         [ItemData('tesco', 'milk', '1L', '2.5', '1').to_json(),
                          ItemData('tesco', 'bacon', '1g', '2.5', '1').to_json()]]
        business_list = [[ItemData('asda', 'milk', '1L', '2.5', '1'),
                          ItemData('asda', 'bacon', '1g', '2.5', '1')],
                         [ItemData('sainsbury', 'milk', '1L', '2.5', '1'),
                          ItemData('sainsbury', 'bacon', '1g', '2.5', '1')],
                         [ItemData('tesco', 'milk', '1L', '2.5', '1'),
                          ItemData('tesco', 'bacon', '1g', '2.5', '1')]]
        encoded_result = json.dumps(business_list, cls=MyEncoder)

        return encoded_result, 200, {'Content-Type': 'application/json'}
        # return jsonify(businesses=business_list)


if __name__ == "__main__":
    app.run(debug=True)
