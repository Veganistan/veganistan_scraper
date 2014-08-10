# coding: utf-8


def field_items_text(content):
    """
    Creates a comma separated string of values for a particular field
    """
    if len(content):
        tag = content[0].find_all(class_="field-items")[0]
        if len(tag.contents):
            return ', '.join([c.text for c in tag.contents])
        else:
            return tag.text
    return None


def get_rel_class(soup, class_name):
    """
    Extracts text from a given html class and comma separates the values.
    """
    return field_items_text(soup.find_all(class_=class_name))


def get_class_text(soup, class_name):
    """
    Extracts text from a given html class
    """
    data = soup.find_all(class_=class_name)
    if len(data):
        return data[0].text
