import requests
import googlemaps
import os

try:
    API_KEY = os.environ["APIKEY"]
except KeyError:
    print "You need a Google API Key for the Distance Matrix API"

gmaps_client = googlemaps.Client(key=API_KEY)

def get_resource_addresses(names):
    # make a call to the Google Places API for each therapist address
    info = []
    for name in names:
        try: 
            resp = gmaps_client.places(name)
            if resp['status'] == "OK":
                print "OK"
                info.append((name, resp['results'][0]['formatted_address']))
        except ApiError, e:
            print e
    return info

def find_nearest_resource(current_location):
    # given a current location, find the nearest resources
    resource_locations = get_resources_from_file("therapists.txt")
    addresses = [pair[2] for pair in resource_locations]
    resp = gmaps_client.distance_matrix(current_location, addresses, units="imperial")
    distances = []
    for el in resp['rows'][0]['elements']:
        distances.append(el['distance'])
    tups = [(distances[i]['value'], shelter_locations[i][0], addresses[i], distances[i]['next']) for i in range(len(addresses))]
    return min(tups)

def get_resources_from_file(filename):
    # make a list of shelters names and addresses given a file
    f = open(filename)
    resource = []
    for line in f:
        line_split = line.split(" | ")
        resource.append((line_split[0], line_split[1], line_split[2]))
	f.close()
    return resource
