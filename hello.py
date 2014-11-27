#!/usr/bin/python
from flask import Flask, request, abort, Response, jsonify, make_response, current_app, g, render_template
import json
import random
import math
import ipdb
import os
import string
app = Flask(__name__, static_folder='', static_url_path='')
app.config['DEBUG'] = True
#current_directory = os.getcwd()
#app._static_folder=current_directory
# Temporary assumptions (to be updated when we can get a json file from the front end).
no_tiles = 1600
WIDTH = 40
HEIGHT = 40
DESERT = 30
SOLAR = 22
RESIDENCE = 23

def get_map(size):
    #ipdb.set_trace()
    map = []
    for i in range(size):
        map.append(DESERT)
    # Add the initial solar panels
    #   S|R
    #   -+-
    #   R|S
    row_length = 1
    center = midpoint(WIDTH)+midpoint(WIDTH*HEIGHT)
    map[center] = SOLAR
    map[center + 1] = RESIDENCE
    map[center + WIDTH] = RESIDENCE
    map[center + WIDTH + 1] = SOLAR
    return map
            
def get_empty_map(size):
    map = []
    for i in range(size):
        map.append(None)
    return map

def check_name(newname):
    # Later on add a database access to see if the name is already taken
    # Assuming that there is no problem:
    return newname

def midpoint(length):
    return length/2

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/endturn", methods = ['POST'])
def end_turn():
    data = request.json
    data['solar_power'] = calcPower(data)
    popObj = calcPop(data)
    data['population'] = popObj['population']
    data['max_population'] = popObj['max_population']
    data['solar_power'] = popObj['solar_power']
    data['enough_power'] = popObj['enough_power']
    data['happiness'] = calcHappy(data)
    return json.dumps(data)

@app.route("/newgame")
def give_object_coordinates():
    js = {
        "height": HEIGHT,
        "layers": [{
            "data": get_map(no_tiles),
            "height": HEIGHT,
            "name": "Ground",
            "opacity": 1,
            "type": "tilelayer",
            "visible": True,
            "width": WIDTH,
            "x": 0,
            "y": 0
        }],
        "orientation": "orthogonal",
        "properties": {},
        "tileheight": 32,
        "tilesets": [{
            "firstgid": 1,
            "image": "~/corking/tmw_desert_spacing.png",
            "imageheight": 199,
            "imagewidth": 265,
            "margin": 1,
            "name": "Desert",
            "properties": {},
            "spacing": 1,
            "tileheight": 32,
            "tilewidth": 32
        }],
        "tilewidth": 32,
        "version": 1,
        "width": WIDTH,
        "turn": 0,
        "game_id": id_generator()
    }
    return Response(json.dumps(js), mimetype='application/json')

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))



# Functions to call on ended turn data. Basically, this is where the gameplay engine is. I've just made something as an example, but it would be good to keep everything as constants or a simple config object for easy tweaking later

def calcPower(data):
    amount = data['solar_power']
    map = data['map']
    panels = 0
    for tile in map:
        if tile['index'] == SOLAR:
            panels += 1
    return amount + (panels * 10)

def calcPop(data):
    population = data['population']
    max_population = data['max_population']
    map = data['map']
    solar = data['solar_power']
    residences = 0
    obj = { 
        'max_population': max_population, 
        'population': population,
        'solar_power': solar,
        'enough_power': False
    }
    for tile in map:
        if tile['index'] == RESIDENCE:
            residences += 1
    obj['max_population'] = (residences * 4)
    if solar > 100:
        obj['solar_power'] = solar - 30
        obj['population'] = randomChange(population, residences, True)
        obj['enough_power'] = True
    return obj

def calcHappy(data):
    happiness = data['happiness']
    population = data['population']
    max_population = data['max_population']
    # if (data['enough_power'] == False):
    #     happiness = randomChange(happiness, 20, False)
    if (population > max_population):
        happiness = randomChange(happiness, 20, False) # False is superfluous, but just to show it's a negative change
    if happiness < 0:
        happiness = 0 # horrible, I know, but temporary
    return happiness

def randomChange(current, reasonable_max, positive):
    #reasonable_max = current / 5
    if positive:
        inc = random.randint(current, current + reasonable_max)
    else:
        inc = random.randint(current - reasonable_max, current)
    return inc 

def percentof(whole, amount):
    return amount * (float(whole)/100 )




if __name__ == "__main__":
        app.run(host="0.0.0.0", port=int("5000"))
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
