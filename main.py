import json

import requests

BingMapsKey = "AhkZGTzNUxseN5Tb-IxxOzQZ2k2IkXksXBua-LbD0FO_L-vXwg4yshTifpr0BF9H"


# def find_grocery_stores(parameters):
#     type = "Grocers"
#     r = requests.get(
#         f"https://dev.virtualearth.net/REST/v1/LocalSearch/?type=Supermarkets&userCircularMapView={parameters}&key={BingMapsKey}")

#     stores = r.json()
#     lst = []
#     if len(stores['resourceSets']) != 0:
#         for store in stores['resourceSets'][0]['resources']:
#             coordinates = (str(store['point']['coordinates'])[1:-1])
#             address = str(store['Address']['formattedAddress'])
#             store_name = str(store['name'])
#             info = (store_name, address, coordinates)
#             lst.append(info)
#     else:
#         return
#     # returns information in a tuple
#     return lst


# def find_directions(user_location, destination):
#     # user_location and destination can be address or coordinates
#     r = requests.get(f"http://dev.virtualearth.net/REST/v1/Routes?wayPoint.1={user_location}&wayPoint.2={destination}&key={BingMapsKey}&distanceUnit=mi&durationUnit=Minute&trafficDataUsed=FlowAndClosure")
#     route = r.json()
#     directions = []
#     for direction in route['resourceSets'][0]['resources'][0]['routeLegs'][0]['itineraryItems']:
#         directions.append(direction['instruction']['text'])
#     return directions


# def find_distance(user_location, destination):
#     # user_location and destination can be address or coordinates
#     r = requests.get(f"http://dev.virtualearth.net/REST/v1/Routes?wayPoint.1={user_location}&wayPoint.2={destination}&key={BingMapsKey}&distanceUnit=mi")
#     route = r.json()
#     travelDistance=0
#     travelDuration=0
#     if len(route['resourceSets']) != 0:
#         for leg in route['resourceSets'][0]['resources'][0]['routeLegs'][0]['itineraryItems']:
#             travelDistance += (leg['travelDistance'])
#             travelDuration += (leg['travelDuration'])
#         return round(travelDistance, 2), travelDuration
#     else:
#         return -1, -1


# def get_map(user_location, destination):
#     # user_location and destination can be address or coordinates
#     r = requests.get(f"https://dev.virtualearth.net/REST/v1/Imagery/Map/imagerySet/centerPoint/zoomLevel/Routes/travelMode?waypoint.1={user_location}&waypoint.2={destination}&format={format}&key={BingMapsKey}")
#     print(r)


def get_coordinates(location):
    BingMapsKey = "AhkZGTzNUxseN5Tb-IxxOzQZ2k2IkXksXBua-LbD0FO_L-vXwg4yshTifpr0BF9H"
    r = requests.get(
        f"http://dev.virtualearth.net/REST/v1/Locations/{location}?includeNeighborhood=1&maxResults=1&key={BingMapsKey}")

    coordinates = r.json()
    xcoordinate = coordinates['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
    ycoordinate = coordinates['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
    return xcoordinate, ycoordinate

def get_bird_eye(location):
    longitude, latitude = get_coordinates(location)
    print(longitude)
    BingMapsKey = "AhkZGTzNUxseN5Tb-IxxOzQZ2k2IkXksXBua-LbD0FO_L-vXwg4yshTifpr0BF9H"
    r = f"https://dev.virtualearth.net/REST/V1/Imagery/Map/Birdseye/{longitude},{latitude}/20?dir=270&ms=900,700&key={BingMapsKey}"
    return r

print(get_coordinates("tower Hill school"))
print(get_bird_eye("jansons market"))

# xcoordinate, ycoordinate = get_coordinates("Tower Hill School")
# print(xcoordinate)
# print(ycoordinate)


# for direction in find_directions("Tower Hill School", "39.7571907, -75.56382751"):
#     print(direction)
# # finding grocery around Christiana mall
# for store in find_grocery_stores(f"{xcoordinate}, {ycoordinate}, 5000"):
#     print(store, end="\n")
#     print(store[2])
#     travelDistance, travelDuration = find_distance("39.76536934795396, -75.57746900413086", store[1])
#     if(travelDuration!=-1):
#         print(f"{travelDistance} miles" , f"in {travelDuration} seconds")
#     else:
#         print("No route found")


spoonacular_key = "97c986fad9454d9198188fa867964a6f"

def find_recipes(query, diet, intolerances, number):
    options = "query=" + query + "&diet=" + diet + "&intolerances=" + intolerances + "&number=" + number + "&apiKey=" + spoonacular_key
    request = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?{options}")
    if request.status_code != 204:
        return request.json()
    return "mega fail"

def return_image(id):
    spoonacular_key = "97c986fad9454d9198188fa867964a6f"
    return f"https://api.spoonacular.com/recipes/{id}/nutritionLabel.png?apiKey={spoonacular_key}"

recipe_data = find_recipes('cookie', 'vegitarian', 'lactose', '5')
print(return_image(641166))