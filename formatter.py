# coding: utf-8
# formats a created JSON file into separate files and better structure

import json

OUTPUT_DIR = "json/formatted"


def price_ranges(data):
    data = data


# ONE TO ONE
PRICE_RANGE = {}
FOOD_RANGE = {}
CATEGORY = {}
VEGAN_ON_MENU = {
    0: False,
    1: True,
    2: "N/A"
}
UNION_AGREMENT = {
    0: False,
    1: True,
    2: "N/A"
}

# MANY TO MANY
SERVICE = {}


def handle_food_type(json_data, key):
    _list = []
    _dict = {}
    for item in json_data:
        field = item.get(key)
        if field:
            _list.append(field)

    food_types = [i.split(',') for i in _list]
    food_list = [item.replace(" ", "") for sublist in food_types for item in sublist]
    food_type_set = sorted(set(food_list))

    for idx, item in enumerate(food_type_set):
        _dict.update({idx: item})
    return _dict


def set_dict_by_key(json_data, key):
    """ Mutates a given dict with values from a given key
    """
    _list = []
    _dict = {}
    for item in json_data:
        field = item.get(key)
        if field:
            _list.append(field)

    for idx, item in enumerate(set(_list)):
        _dict.update({idx: item})

    return _dict


if __name__ == "__main__":

    # TODO: Open the latest file in the dir
    latest_file = "json/20140810_1103.json"

    with open(latest_file, "r") as f:
        json_data = json.load(f)

        # start with populating the relations
        PRICE_RANGE = set_dict_by_key(json_data, "price_range")
        FOOD_RANGE = set_dict_by_key(json_data, "food_range")
        CATEGORY = set_dict_by_key(json_data, "category")
        SERVICE = set_dict_by_key(json_data, "service")

        # food type is currently a bit off
        FOOD_TYPE = handle_food_type(json_data, "food_type")

        for item in json_data:
            import ipdb; ipdb.set_trace()