import os

import json

import requests

from flask import Flask, flash, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    """Home Page"""
    return render_template("index.html")

#RECIPES CODE
def find_recipes(query, diet, intolerances, number):
    spoonacular_key = "ae59d5f764644a6eb6353d6186327fef"
    options = "query=" + query + "&diet=" + diet + "&intolerances=" + intolerances + "&number=" + number + "&addRecipeInfomration=true&addRecipeNutrition=true" +"&apiKey=" + spoonacular_key
    request = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?{options}")
    if request.status_code != 204:
        return request.json()
    return "mega fail"

def return_image(id):
    spoonacular_key = "ae59d5f764644a6eb6353d6186327fef"
    return f"https://api.spoonacular.com/recipes/{id}/nutritionLabel.png?apiKey={spoonacular_key}"

@app.route("/recipe_query", methods=["GET", "POST"])
def recipe_query():
        if(request.method == "GET"):
            return render_template("recipe_query.html")
        elif (request.method == "POST"):
            query = request.form.get("query")
            diet = request.form.get("selectDiet")
            intolerance = request.form.get("selectIntolerance")
            number = request.form.get("results")
            recipe_data = find_recipes(query, diet, intolerance, number)
            for recipe in recipe_data['results']:
                recipe.update({'nutrition': return_image(recipe['id'])})
            return render_template("recipes.html", recipes = recipe_data['results'])

@app.route("/recipe_info", methods=["GET"])
def recipe_info():
        spoonacular_key = "97c986fad9454d9198188fa867964a6f"
        if(request.method == "GET"):
            id = request.args.get('id')
            recipe_info = requests.get(f"https://api.spoonacular.com/recipes/{id}/information&apiKey={spoonacular_key}").json()
            return render_template("recipe_info.html", recipe = recipe_info)

#LOCATION CODE
def create_map(locationx, locationy, location, stores):
    BingMapsKey = "AhkZGTzNUxseN5Tb-IxxOzQZ2k2IkXksXBua-LbD0FO_L-vXwg4yshTifpr0BF9H"
    link = f"https://dev.virtualearth.net/REST/v1/Imagery/Map/CanvasDark/?mapSize=1000,500"
    link = link + f"&pp={locationx}, {locationy};129;{location}"
    for store in stores:
        link = link + f"&pp={store[2]};;{store[0]}"
    link = link + f"&dcl=1&key={BingMapsKey}"
    return link


def get_coordinates(location):
    BingMapsKey = "AhkZGTzNUxseN5Tb-IxxOzQZ2k2IkXksXBua-LbD0FO_L-vXwg4yshTifpr0BF9H"
    r = requests.get(
        f"http://dev.virtualearth.net/REST/v1/Locations/{location}?includeNeighborhood=1&maxResults=1&key={BingMapsKey}")

    coordinates = r.json()
    xcoordinate = coordinates['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
    ycoordinate = coordinates['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
    return xcoordinate, ycoordinate


def find_grocery_stores(parameters):
    BingMapsKey = "AhkZGTzNUxseN5Tb-IxxOzQZ2k2IkXksXBua-LbD0FO_L-vXwg4yshTifpr0BF9H"
    type = "Grocers"
    r = requests.get(
        f"https://dev.virtualearth.net/REST/v1/LocalSearch/?type=Supermarkets&userCircularMapView={parameters}&key={BingMapsKey}")

    stores = r.json()
    lst = []
    if len(stores['resourceSets']) != 0:
        for store in stores['resourceSets'][0]['resources']:
            coordinates = (str(store['point']['coordinates'])[1:-1])
            address = str(store['Address']['formattedAddress'])
            store_name = str(store['name'])
            info = (store_name, address, coordinates)
            lst.append(info)
    else:
        return
    # returns information in a tuple
    return lst

@app.route("/location_query", methods=["GET", "POST"])
def location_query():
    """Show list of nearby grocery stores!"""
    if(request.method == "GET"):
        return render_template("location_query.html")
    elif (request.method == "POST"):
        location = request.form.get("location")
        latitude, longitude = get_coordinates(location)
        stores = find_grocery_stores(f"{latitude}, {longitude}, 5000")
        map = create_map(latitude, longitude, location, stores)
        if(len(stores) == 0):
            return render_template("location_not_found.html")
        
        return render_template("stores.html", stores = stores, map = map, location = location)

