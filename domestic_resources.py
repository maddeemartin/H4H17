from BeautifulSoup import BeutifulSoup
import requests
import googlemaps
import os

PHONE_NUMBERS_URL = "http://ncadv.org/learn-more/resources"
THERAPIST_URL = "https://therapists.psychologytoday.com/rms/state/California.html"
SUPPORT_GROUP_URL = "https://groups.psychologytoday.com/rms/prof_results.php?state=CA&spec=8"

try:
    API_KEY = os.environ["APIKEY"]
except KeyError:
    print "You need a Google API Key for the Distance Matrix API"

gmaps_client = googlemaps.Client(key=API_KEY)

def get_soup(url):
  # requests a webpage and returns a Beautiful Soup object
  resp = requests.get(url)
  soup = BeautifulSoup(resp.text)
  return soup

def get_therapist_phone_numbers(webpage_soup):
  # get nescessary info from the webpage
  #all_numbers = webpage_soup.find('div', {'class':'result-phone hidden-xs'})
  #numbers = []
  #return numbers
  holding_div = webpage_soup.find('div', {'class':'mw-content-ltr'})
  all_food_links = holding_div.findAll('a')
  names = [ a['title'] for a in all_food_links]
  return names

def get_resource_addresses(names):
  # make a call to the Google Places API for each shelter name
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
  shelter_locations = get_shelters_from_file("shelters.txt")
  addresses = [pair[1] for pair in shelter_locations]
  resp = gmaps_client.distance_matrix(current_location, addresses, units="imperial")
  distances = []
  for el in resp['rows'][0]['elements']:
    distances.append(el['distance'])
  tups = [(distances[i]['value'], shelter_locations[i][0], addresses[i], distances[i]['next']) for i in range(len(addresses))]
  return min(tups)

def get_shelters_from_file(filename):
  # make a list of shelters names and addresses given a file
  
  f = open(filename)
  shelters = []
  for line in f:
    line_split = line.split("|")
    shelters.appand((line_split[0], line_split[1]))
  return shelters
