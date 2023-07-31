from flask import Flask, render_template, request
from grocery_scraping import all_in_one
from itemdata import ItemData


app = Flask('Stock Exchanger', static_folder='static',
            template_folder='template')


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/get-item/', methods=['POST'])
def get_item():

    data = request.json
    business = data['business']
    item = data['item']

    try:
        results = all_in_one.get_items(item=item, n=30, business=business)
        list_objs = ItemData.list_to_object(results, business=business)

    except Exception as e:
        print(e)
        list_objs = []

    finally:
        return list_objs


@app.route('/get-item/fetch-compare/', methods=['POST'])
def fetch_compare():

    data = request.json
    item = data['item']

    item_list_dict = all_in_one.get_all_businesses(item=item, n=10)

    item_obj_dict = {}
    for k, v in item_list_dict.items():
        print(k)
        item_obj_dict[k] = ItemData.list_to_object(v, k)

    print(item)
    return {'item': item}
    # return item_obj_dict  # should return a new page


@app.route('/get-item/display-compare/', methods=['GET'])
def display_compare():
    data = request.args.get('data')
    return render_template('comparison.html', item=data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
