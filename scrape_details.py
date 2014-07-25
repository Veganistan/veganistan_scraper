# coding: utf-8


def field_items_text(content):

    if len(content):
        return content[0].find_all(class_="field-items")[0].text
    return None


def get_description(soup):
    content = soup.find_all(class_="field-type-text-with-summary")
    if len(content):
        return content[0].text
    return None


def get_url(soup):
    content = soup.find_all(class_="field-name-field-hemsida")
    if len(content):
        return content[0].find_all("a")[0].attrs.get("href")
    return None


def get_phone(soup):
    content = soup.find_all(class_="field-name-field-telefonnummer")
    return field_items_text(content)


def get_price_range(soup):
    content = soup.find_all(class_="field-name-field-prisintervall")
    return field_items_text(content)


def get_food_type(soup):
    """
    Typ av mat
    """
    content = soup.find_all(class_="field-name-field-typ-av-mat")
    return field_items_text(content)


def get_food_range(soup):
    """
    Utbud field-name-field-utbud
    """
    content = soup.find_all(class_="field-name-field-utbud")
    return field_items_text(content)


def get_service(soup):
    """
    Service
    """
    content = soup.find_all(class_="field-name-field-utbud-och-service")
    return field_items_text(content)


def get_vegan_on_menu(soup):
    """
    Service
    """
    content = soup.find_all(class_="field-name-field-veganskt-pa-menyn")
    return field_items_text(content)


def get_union_agreement(soup):
    """
    Kollektivavtal
    """
    content = soup.find_all(class_="field-name-field-kollektivavtal")
    return field_items_text(content)


def get_warnings(soup):
    """
    Varningar
    """
    content = soup.find_all(class_="field-name-field-varningar")
    return field_items_text(content)


def get_accessibility(soup):
    """
    Tillgänglighetsanpassad
    """
    content = soup.find_all(class_="field-name-field-tillganglighetsanpassad")
    return field_items_text(content)

