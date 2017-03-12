"""
Alisha Pegan's code for Geocoding and Web APIs Project Toolbox exercise
March 12, 2017
Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

from urllib.request import urlopen
import json

# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"
# A little bit of scaffolding if you want to use it


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urlopen(url)
    response_text = f.read()
    response_data = json.loads(str(response_text, "utf-8"))
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.

    >>> get_lat_long('Starbucks Coffee in Ukiah')
    (39.15196210000001, -123.1955585)
    """
    name = place_name.replace(" ", "")
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s' % name
    response_data = get_json(url)
    lat = response_data['results'][0]['geometry']['location']['lat']
    lng = response_data['results'][0]['geometry']['location']['lng']
    return (lat, lng)


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    # MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
    url = (MBTA_BASE_URL +
           '?api_key=%s&lat=%s&lon=%s&format=json' % (API_KEY, latitude, longitude))
    stop_data = get_json(url)
    # get the shortest distance
    nearest = min(stop['distance'] for stop in stop_data['stop'])
    # print the name for the nearst stop
    name = [stop['stop_name'] for stop in stop_data['stop'] if stop['distance'] == nearest]
    return (name[0], nearest)
    # print(url)


def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the
    distance from the given place to that stop.

    >>> find_stop_near('Boston Commons')
    ('Beacon St opp Walnut St', '0.127313360571861')
    """
    geo = get_lat_long(place_name)
    station = get_nearest_station(geo[0], geo[1])
    return station


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # doctest.run_docstring_examples(get_lat_long, globals())

find_stop_near('Wellesley CVS')
