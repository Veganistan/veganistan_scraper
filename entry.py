# coding: utf-8


class EntryManager(object):
    entries = []
    def __init__(self, data_dict=None):
        """
        Initialize the entry manager.
        If supplied with a data dict, attempt to create Entry instances
        """
        if data_dict:

            fields = list(Entry().__dict__.keys())
            for item in data_dict:
                entry = Entry()
                for field in fields:
                    setattr(entry, field, item.get(field))
                self.add_entry(entry)

    def add_entry(self, entry):
        # start with adding the id for this entry
        id = len(self.entries)
        entry.set_id(id)
        self.entries.append(entry)
        print("added entry %s : %s " % (id, entry.name))

    def get_entries(self):
        return self.entries

    def get_by_name(self, name):
        for entry in self.entries:
            if entry.name.lower() == name.lower():
                return entry

    def get_by_town(self, town):
        def filter_by_town(entry):
            return entry.town.lower() == town.lower()

        return filter(filter_by_town, self.entries)


class Entry(object):

    BASE_URL = "http://veganistan.se"

    def __init__(self, name=None, absolute_url=None, category=None,
                 town=None, rating=None, nof_votes=None):
        self.name = name
        self.absolute_url = absolute_url
        self.category = category
        self.town = town
        self.rating = rating
        self.nof_votes = nof_votes

        # added through the detail scraper
        self.url = None
        self.phone = None
        self.price_range = None
        self.food_type = None
        self.food_range = None
        self.service = None
        self.vegan_on_menu = None
        self.union_agreement = None
        self.warnings = None
        self.accessibility = None

    def get_absolute_url(self):
        return u'%s%s' % (self.BASE_URL, self.absolute_url)

    def set_id(self, id):
        self.id = id

    def __unicode__(self):
        return u'%s %s' % (self.name, self.town)

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__str__()


class Address(object):

    def __init__(self, entry=None, street_address=None,
                 postal_code=None, town=None):
        self.entry = entry
        self.street_address = street_address
        self.postal_code = postal_code
        self.town = town

