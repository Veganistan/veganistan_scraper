# coding: utf-8
# formats a created JSON file into separate files and better structure

import json
import time

OUTPUT_DIR = "json/formatted"
DEBUG = True


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
    # TODO: replace only spaces in first or last position
    food_list = [item.lstrip().rstrip() for sublist in food_types for item in
                 sublist]
    food_type_set = sorted(set(food_list))

    for idx, item in enumerate(food_type_set):
        _dict.update({idx: item})
    return _dict


def save_to_file(obj, obj_name):
    filename = "json/formatted/%s.json" % obj_name

    # in the case for all individual items such as food_range, service and so on
    # we want to convert these into a dict
    try:
        obj = [{"id": id, "value": value} for id, value in obj.items()]
    except:
        # this is where we'll saving the json_data object
        pass

    with open(filename, "w") as f:
        json.dump(obj, f, ensure_ascii=False)
        if DEBUG:
            print("Saved %s" % filename)
    return filename


def match_values(obj, values):
    if values:
        return [(k, v) for k, v in obj.items() if v in values]
    return []


def set_value(obj):
    return [{"id": id, "value": value} for id, value in obj]


if __name__ == "__main__":

    time_started = time.time()
    # TODO: Open the latest file in the dir
    latest_file = "json/20140810_2257.json"

    # we're interested in these fields for populating the json file
    # all these fields with corresponding data will also get saved to separate
    # json files such as ``field.json``.
    fields = ["food_type", "price_range", "food_range", "category", "service",
              "accessibility", "union_agreement", "vegan_on_menu"]

    with open(latest_file, "r") as f:

        json_data = json.load(f)

        entries = {}

        for field in fields:
            result = handle_nested_type(json_data, field)
            save_to_file(result, field)
            # save all results in a dict for future use
            entries.update({field: result})

        # loop over each entry - each resturant, store, etc
        for item in json_data:

            results = {}
            for field in fields:
                result_for_field = match_values(entries.get(field), item[field])
                # reset the value
                item[field] = set_value(result_for_field)

        # finally save the resturants/stores and other entries into a json file
        save_to_file(json_data, "entries")
        ended_in = time.time() - time_started
        print("Finished. Formatted and saved all entries in: %s seconds" % ended_in)