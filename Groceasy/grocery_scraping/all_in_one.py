from . import asda_func
from . import tesco_func
from . import sains_func
from multiprocessing.dummy import Pool as ThreadPool


def get_items(item: str = 'Milk', n: int = 5, business: str = "Sainsbury's"):

    if business == "Sainsbury's":
        item_list = sains_func.sainsbury(item=item, n=n)
    elif business == "ASDA":
        item_list = asda_func.asda(item=item, n=n)
    elif business == "Tesco":
        item_list = tesco_func.tesco(item=item, n=n)
    else:
        raise Exception('Grocery store not supported.')

    return item_list


def get_all_businesses(item: str = 'Milk', n: int = 5):

    grocery_stores = ['ASDA', "Sainsbury's", 'Tesco']

    with ThreadPool(3) as p:
        result_list = p.starmap(get_items, zip(
            [item]*3, [n]*3, grocery_stores))

    item_list_dict = dict(zip(grocery_stores, result_list))

    return item_list_dict
