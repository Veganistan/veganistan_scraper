# coding: utf-8

GOOGLE_MAPS_API_KEY = "something"
# full URI, append the API KEY to this string
GOOGLE_MAPS_BASE_URI = "https://maps.googleapis.com/maps/api/geocode/json"

# local settings are stored in local.py
try:
    from settings_local import *
except ImportError:
    pass

