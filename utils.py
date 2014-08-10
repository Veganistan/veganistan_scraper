# coding: utf-8
import json


def serialize_items(items):
    """
    Returns a list of dicts with all the entries
    """
    final_list = []
    for item in items:
        final_list.append(item.__dict__)
    return final_list


def save_json_file(data, filename):
    # filename
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False)
    print("Saved %s successfully" % filename)
    return filename


def load_json_file(directory, filename):
    """
    Reads a JSON file and returns its content as a python list
    """
    fn = directory+"/"+filename
    with open(fn, "r") as f:
        return json.load(f)
