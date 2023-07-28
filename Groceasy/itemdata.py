class ItemData:

    def __init__(self, business, name, volume, price, unit_price, img=None):
        self.business = business
        self.name = name
        self.volume = volume
        self.price = price
        self.unit_price = unit_price
        self.img = img

    @staticmethod
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


if __name__ == "__main__":
    obj = ItemData('tesco', 'milk', '1L', '20p', '20p', 'image')
    print(obj.__dict__)
