# coding: utf-8

"""
Usage:: python geocode.py path/to/file.json
The file to geocode should in this version be the one created by
``scraper.py``
"""

import sys
import json
import requests
from scraper import serialize_and_save

from settings import GOOGLE_MAPS_BASE_URI, GOOGLE_MAPS_API_KEY, USER_IP


def build_gmaps_uri(gmaps_base_uri, api_key, user_ip, address):
    """
    Construct a URI to the Google Maps API with a particular address and APIkey
    :params: gmaps_base_uri - base uri for the google maps api
    :params: api_key - the google maps api key
    :params: address - comma separated address
    """
    uri = gmaps_base_uri + "?address=" + address + "&key=" + api_key + "&userIp=" + user_ip
    return uri


def geocode(address):
    """
    Geocode a particular address
    :Return:
    """
    gmaps_uri = build_gmaps_uri(
        GOOGLE_MAPS_BASE_URI,
        GOOGLE_MAPS_API_KEY,
        USER_IP,
        address)

    # do GET request to Googles Geocode API
    google_geodata = requests.get(gmaps_uri)

    if google_geodata.status_code == 200:
        data = json.loads(google_geodata.text)
        geodata = data['results'][0]['geometry']['location']
        return geodata['lat'], geodata['lng']
    return None, None


def run(filename):
    # store the geocoded results here so that we can save them
    # to a new file when we're done
    geocoded_entries = []
    with open(filename, 'r') as f:

        for line in f.readlines():

            entries = json.loads(line)
            for entry in entries:
                address = "%s, %s, %s" % (
                    entry.get("street_address"),
                    entry.get("postal_code"),
                    entry.get("town")
                )
                print("address", address)

                lat, long = geocode(address)
                entry['geodata'] = {
                    'long': long,
                    'lat': lat
                }
                geocoded_entries.append(entry)

    filename_parts = filename.split('.')

    new_filename = u'%s_%s.%s' % (
        filename_parts[-2],
        'geocoded',
        filename_parts[-1])

    serialize_and_save(geocoded_entries, new_filename, use_serializer=False)


if __name__ == "__main__":
    filename = sys.argv[1]
    run(filename)