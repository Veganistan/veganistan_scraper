# coding: utf-8


class EntryManager(object):
    entries = []

    def add_entry(self, entry):
        self.entries.append(entry)
        print("added entry", entry.name)

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

    def __init__(self, name, absolute_url, category, town,
                 rating, nof_votes):
        self.name = name
        self.absolute_url = absolute_url
        self.category = category
        self.town = town
        self.rating = rating
        self.nof_votes = nof_votes

    def get_absolute_url(self):
        return u'%s%s' % (self.BASE_URL, self.absolute_url)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.town)

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__str__()

