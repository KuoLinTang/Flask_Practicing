import json


class ItemData:

    def __init__(self, business, name, volume, price, unit_price, img=None):
        self.business = business
        self.name = name
        self.volume = volume
        self.price = price
        self.unit_price = unit_price
        self.img = img


if __name__ == "__main__":
    obj = ItemData('tesco', 'milk', '1L', '20p', '20p', 'image')
    print(obj.__dict__)
