from . import asda_func
from . import tesco_func
from . import sains_func


def get_items(item: str = 'Milk', n: int = 5, business: str = 'sainsbury'):

    if business == 'sainsbury':
        item_list = sains_func.sainsbury(item=item, n=n)
    elif business == 'asda':
        item_list = asda_func.asda(item=item, n=n)
    elif business == 'tesco':
        item_list = tesco_func.tesco(item=item, n=n)
    else:
        raise Exception('Grocery store not supported.')

    return item_list
