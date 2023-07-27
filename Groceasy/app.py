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
                ).__dict__  # convert into JSON
            )
        return result_list

    data = request.json
    business = data['business']
    item = data['item']

    try:
        results = all_in_one.get_items(item=item, n=20, business=business)
        list_objs = list_to_object(results, business=business)

    except Exception as e:
        print(e)
        list_objs = []

    finally:
        return list_objs


if __name__ == '__main__':
    app.run(debug=True)
