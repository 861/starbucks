import urllib2
import untangle
import pandas as pd
import numpy as np

#https://openapi.starbucks.com/location/v1/stores?&radius=100&limit=50&brandCode=SBUX&latLng=51.5072%2C-0.1275&apikey=7b35m595vccu6spuuzu2rjh4&_=1370295322059
#https://openapi.starbucks.com/location/v1/stores?&radius=10&limit=50&latLng=50.5072%2C-0.1275&apikey=7b35m595vccu6spuuzu2rjh4&_=1370295322059

# 51.506244, -0.220263
# 51.507420, -0.064738
# 51.476211, -0.130312
# 51.526648, -0.142329

def get_all_in_london():
    results = []

    for lat in np.arange(51.4, 51.6, 0.05):
        for lon in np.arange(-0.3, 0, 0.05):
            print lat, lon
            results.append(get_starbucks_locations(lat, lon))

    return results

def get_and_append_data(data, results):
    obj = untangle.parse(data)

    if obj.result.paging.returned.cdata == '0':
        return

    for item in obj.result.items.item:
        lat = item.store.coordinates.latitude.cdata
        lon = item.store.coordinates.longitude.cdata
        name = item.store.name.cdata
        results.append({'name':name, 'lat':lat, 'lon':lon})

    #return results

def get_starbucks_locations(lat, lon):
    results = []

    url = "https://openapi.starbucks.com/location/v1/stores?&radius=10&limit=50&latLng=" + str(lat) + "%2C" + str(lon) + "&apikey=7b35m595vccu6spuuzu2rjh4&_=1370295322059"
    print url
    data = urllib2.urlopen(url).read()

    get_and_append_data(data, results)

    data = urllib2.urlopen(url+"&offset=50").read()
    get_and_append_data(data, results)

    return pd.DataFrame(results)

