# coding: utf-8

import requests
from bs4 import BeautifulSoup
from entry import EntryManager, Entry

PAGINATE_SUFFIX = "?page="

list_pages = (
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
    category = row.find_all(class_="views-field-field-typ-av-stalle")[0].text
    return clean_string(category)


def get_town(row):
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


def start_scraping():
    """
    Run the scraping and add results to an EntryManager.
    This is returned when all is finished.
    """
    categories = []
    towns = []

    entry_manager = EntryManager()

    for url in list_pages:
        print("URL: ", url)
        list_page = requests.get(url)
        soup = BeautifulSoup(list_page.content)
        on_first_page = True
        # get the number of pages from the pagination section
        nof_pages = get_nof_pages(soup)

        for page_id in range(0, nof_pages):
            if not on_first_page:
                # fetch the new page
                url = u'%s%s%s' % (list_pages[0], PAGINATE_SUFFIX, (page_id+1))
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

if __name__ == "__main__":

    entry_manager = start_scraping()
