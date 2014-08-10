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


def handle_nested_type(json_data, key):
    """
    Extract data from big JSON data, append all items to a list,
    turn that list into a set to avoid duplicates and sort the set alphabetically.
    Special case for food types since they are nested together
    """
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


def save_to_file(obj, obj_name):

    filename = "json/formatted/%s.json" % obj_name
    with open(filename, "w") as f:
        json.dump(obj, f, ensure_ascii=False)
    return None

if __name__ == "__main__":

    # TODO: Open the latest file in the dir
    latest_file = "json/20140810_1103.json"

    with open(latest_file, "r") as f:
        json_data = json.load(f)

        # start with populating the relations
        PRICE_RANGE = handle_nested_type(json_data, "price_range")
        FOOD_RANGE = handle_nested_type(json_data, "food_range")
        CATEGORY = handle_nested_type(json_data, "category")
        SERVICE = handle_nested_type(json_data, "service")
        # food type is currently a bit off
        FOOD_TYPE = handle_nested_type(json_data, "food_type")

        save_to_file(PRICE_RANGE, "price_range")
        save_to_file(FOOD_RANGE, "food_range")
        save_to_file(FOOD_TYPE, "food_type")
        save_to_file(CATEGORY, "category")
        save_to_file(SERVICE, "service")

        for item in json_data:
            import ipdb; ipdb.set_trace()