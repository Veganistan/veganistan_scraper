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


If installation fails on ``lncurses`` try installing the development library 
for ``ncurses``.
``sudo apt-get install libncurses5-dev`

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

### accessibility.json
Adapted for accessibility


### category.json
Boutique, pub, etc


### entries.json
Contains the bulk of data. All resturants etc.


### food_range.json
Omni, vegan, veggie


### food_type.json
American, French, Greek, etc


### price_range.json
Cheap, expensive, etc


### service.json
Home delivery, catering, etc


### union_agreement.json
Has agreement with the union


### vegan_on_menu.json
Vegan options


