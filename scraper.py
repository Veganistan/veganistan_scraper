# coding: utf-8
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from entry import EntryManager, Entry
from scrape_details import get_description, get_url, get_phone, get_price_range, get_food_type, get_food_range, get_service, get_vegan_on_menu, get_union_agreement, get_warnings, get_accessibility
from utils import serialize_items, save_json_file, load_json_file

PAGINATE_SUFFIX = "?page="

LIST_PAGES = (
    "http://veganistan.se/stockholm/",
    "http://veganistan.se/goteborg/",
    "http://veganistan.se/malmo/",
    "http://veganistan.se/spenaten/",
)


def add_to_list(original_list, entry):
    if entry not in original_list:
        original_list.append(entry)
    return original_list


def clean_string(string):
    return string.replace("\n", "").rstrip().lstrip()


def get_nof_pages(soup):
    """
    we want the number (8) in this example
    split: <a href="/spenaten?page=8" title="Gå till sista sidan">sista »</a>
    """
    pager_last = soup.find_all("li", class_="pager-last")
    if pager_last:
        pl = pager_last[0]
        stringified = u'%s' % pl

        href = pl.find_all("a")[0].attrs.get('href')
        return int(href.split("=")[1])
    return 1


def get_name(row):
    # return the title portion of the href
    # example: <a href="/gavle/alternativboden-lyktan">Alternativboden Lyktan</a>]
    # returns Alternativboden Lyktan
    return row.find_all(class_="views-field-title")[0].find_all("a")[0].text


def get_absolute_url(row):
    return row.find_all(
        class_="views-field-title")[0].find_all("a")[0].attrs.get('href')


def get_category(row):
    """ Typ av ställe """
    category = row.find_all(class_="views-field-field-typ-av-stalle")[0].text
    return clean_string(category)


def get_town(row):
    """ Ort """
    town = row.find_all(class_="views-field-field-adress")[0].text
    return clean_string(town)


def get_rating(row):
    avg_rating = row.find_all(class_="average-rating")

    if avg_rating:
        try:
            return float(avg_rating[0].text.split(":")[1])
        except IndexError:
            pass

    return None


def get_nof_votes(row):
    total_votes = row.find_all(class_="total-votes")
    if total_votes:
        try:
            return int(total_votes[0].text.split(" ")[0][1::])
        except IndexError:
            pass
    return None


def create_entry(row):
    entry = Entry(
        name=get_name(row),
        absolute_url=get_absolute_url(row),
        category=get_category(row),
        town=get_town(row),
        rating=get_rating(row),
        nof_votes = get_nof_votes(row)
    )
    return entry


def scrape_base_info():
    """
    Scrape the base info of all resturants based on veganistan.se's list pages
    This is returned when all is finished.
    """
    categories = []
    towns = []

    entry_manager = EntryManager()

    for url in LIST_PAGES:
        print("URL: ", url)
        list_page = requests.get(url)
        soup = BeautifulSoup(list_page.content)
        on_first_page = True
        # get the number of pages from the pagination section
        nof_pages = get_nof_pages(soup)

        for page_id in range(0, nof_pages):
            if not on_first_page:
                # fetch the new page
                url = u'%s%s%s' % (LIST_PAGES[0], PAGINATE_SUFFIX, (page_id+1))
                list_page = requests.get(url)
                print("fetching a new page %s " % page_id)
                soup = BeautifulSoup(list_page.content)

            # <tr> rows inside the only <tbody> contains all entries
            table_rows = soup.find_all("tbody")[0].find_all("tr")
            # one row is one entry
            for row in table_rows:
                # here starts a new entry
                e = create_entry(row)

                entry_manager.add_entry(e)
                categories = add_to_list(categories, e.category)
                towns = add_to_list(towns, e.town)

                print(e.name, e.absolute_url)

        if on_first_page:
            on_first_page = False
    return entry_manager


def scrape_detail(entry):
    """
    Scrape the detail page for an entry
    """

    url = "http://veganistan.se"+entry.absolute_url
    print("fetching url", url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content)

    entry.description = get_description(soup)
    entry.url = get_url(soup)
    entry.phone = get_phone(soup)
    entry.price_range = get_price_range(soup)
    entry.food_type = get_food_type(soup)
    entry.food_range = get_food_range(soup)
    entry.service = get_service(soup)
    entry.vegan_on_menu = get_vegan_on_menu(soup)
    entry.union_agreement = get_union_agreement(soup)
    entry.warnings = get_warnings(soup)
    entry.accessibility = get_accessibility(soup)

    print("entry %s updated" % entry)
    return entry


def serialize_and_save(entries, filename):
    json_data = serialize_items(entries)

    return save_json_file(
        data=json_data,
        filename=filename)


if __name__ == "__main__":

    # TODO: Accept sys args
    load = False

    created_file = None
    if load:
        data = load_json_file("json", "20140725_0940.json")
        entry_manager = EntryManager(data_dict=data)
    else:
        # start scraping the base data for all entries.
        entry_manager = scrape_base_info()

        created_file = serialize_and_save(
            entries=entry_manager.get_entries(),
            filename='json/%s.json' % datetime.now().strftime("%Y%m%d_%H%M")
        )

    # json_data = serialize_items(entry_manager.get_entries())
    # save_json_file(
    #     json_data,
    #     "json",
    #     '%s.json' % datetime.now().strftime("%Y%m%d_%H%M"))

    for entry in entry_manager.get_entries():
        scrape_detail(entry)

    if created_file:
        serialize_and_save(entry_manager.get_entries(), created_file)