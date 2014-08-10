# Veganistan Scraper


Scraping the public pages of veganistan.se to find resturants and stores

This project scrapes veganistan.se for resturants/stores/etc and saves them
in a JSON file for easy parsing. The aim for this project is to provide the
base data from the site to be imported into an API service.


## Development

Requirements::

    Python 3.4
    Virtualenv
    Pip for python3
    Beautifulsoup4


Create a virtualenvironment and install the dependencies using ``pip3``::

    mkvirtualenv --python=/usr/local/bin/python3 veganistan_scraper
    pip3 install requirements/default.pip



## Running

The scraper connects to veganistan.se and pulls all important data down into a
datetime-named JSON-file.

Run the scraper::

    python scraper.py


The formatter is responsible for creating the actual API resources.
The created JSON-file is then fed into the formatter which extracts relational
data like categories, food types, etc and merges these into each resturant, store, etc.

Run the formatter::

    python formatter.py


Output from the formatter is found in ``json/formatted``


## Files and resources

### category.json
Boutique, pub, etc


### food_range.json
Omni, vegan, veggie


### food_type.json
American, French, Greek, etc


### price_range.json
Cheap, expensive, etc


### service.json
Home delivery, catering, etc


### entries.json
Each individual resturant, store, café
