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
BUILDINGS = [SOLAR,RESIDENCE]
ARTICLES = [{ 'headline': "The sun is so bright!",
                'article':"The sun has been especially bright recently. So much so that the only, lonely flowers that we brought are now wilting."
            },{ 'headline': "Testing", 
            'article': "This is a test"
            },{ 'headline': "Spate of headaches plagues base", 
            'article':"I've got a headache, you've got a headache. Must be all this sun and the LACK OF ANY FOOD OR WATER..."
            },{ 'headline': "Royal baby something something", 
            'article' : "Blah blah blah the royal baby is something something"
            }]
RIOT_MSG = {
'headline':"Riots break out in base!",
'article':"Riots have been happening in the sector with coordinates "
}

# -----------------------------------------------------------------------------------------
# The function get_map returns the randomly generated map as an array. Used to set up the 
# game. 
#
#
# INPUTS            TYPE        DESCRIPTION
#
# size              int         The total number of tiles, i.e. width x height.
#
#
# OUTPUTS           TYPE        DESCRIPTION
# 
# map               array       The randomly generated map returned as an array. The array
#                               is ordered as row followed by row, stacked into an array,
#                               starting from the top left corner of the map and finishing
#                               at the bottom right corner of the map.
#
# -----------------------------------------------------------------------------------------

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
    # Add the randomly generated objects. 
    randomly_generate_terrain(map)

    return map


# -----------------------------------------------------------------------------------------
# The function generate_random_terrain inputs randomly generated terrain into the map. It
# sets seeds of certain types (e.g. plants, cacti, rocks, wastepiles) into the map, which 
# each have certain properties (e.g. mean number of tiles occupied and probability of this
# seed occuring). These seeds are put in random places and accepts or rejected based upon a
# checks to make sure that nothing is already in the way.
#
#
# INPUTS            TYPE        DESCRIPTION
#
# map               array       This is the map as it starts.
#
#
# OUTPUTS           TYPE        DESCRIPTION
# 
# map               array       The map is returned with randomly generated terrain inside.
#
# -----------------------------------------------------------------------------------------
def randomly_generate_terrain(map):
    # Loop over the seed generation, up to a maximum number of seeds
        # Generate seed index and its type
        # Check that seed index is further than a predefined number of tiles from anything else <-- may replace with just checking that it does not lie on top of anything else
        # Grow the seed, randomness involved in selecting 8 tiles around seed, don't grow if something else is already there
        # Grow outer layers for a certain probability if below meansize and for a different probability if greater than meansize
    return map

# -----------------------------------------------------------------------------------------
# The function list_to_xy_coords is a mapping function that converts list indices into x
# and y coordinates. 
#
#
# INPUTS            TYPE        DESCRIPTION
#
# lindex            int         The list index of the map. It starts with 0 and goes up to
#                               (width*height - 1), where 0 corresponds to the top left
#                               corner of the map and (width*height - 1) to the bottom 
#                               right corner of the map.
#
# width             int         The width of the map.
#
# height            int         The height of the map.
#
#
# OUTPUTS           TYPE        DESCRIPTION
# 
# x                 int         The x coordinate of the map list index inserted, this goes
#                               from 0 to (width - 1), where 0 corresponds to the left of 
#                               the map and (width - 1) corresponds to the right of the
#                               map.
#
# y                 int         The y coordinate of the map list index inserted, this goes
#                               from 0 to (height - 1), where 0 corresponds to the top of
#                               the map and (height - 1) corresponds to the bottom of the
#                               map (bitmap convension).
#
# -----------------------------------------------------------------------------------------
def list_to_xy_coords(lindex,width,height):
    # test to make sure that lindex is within bounds
    if (lindex >= 0 and lindex <= (width*height-1)):
        x = lindex % width
        y = (lindex - x)/width
        return x,y
    else: 
        print "ERROR in converting from list index to x,y coordinates. List index outside allowed values."
        return None, None


# -----------------------------------------------------------------------------------------
# The function xy_coords_to_list is a mapping function that converts x and y map
# coordinates into the corresponding list index. 
#
#
# INPUTS            TYPE        DESCRIPTION
#
# x                 int         The x coordinate of the map, this goes from 0 to 
#                               (width - 1), where 0 corresponds to the left of the map and
#                               (width - 1) corresponds to the right of the map.
#
# y                 int         The y coordinate of the map, this goesf rom 0 to 
#                               (height - 1), where 0 corresponds to the top of the map and
#                               (height - 1) corresponds to the bottom of the map (bitmap 
#                               convension).
#
# width             int         The width of the map.
#
# height            int         The height of the map.
#
#
# OUTPUTS           TYPE        DESCRIPTION
# 
# lindex            int         The list index that corresponds to map coordinate x,y. It
#                               starts with 0 and goes up to (width*height - 1), where 0
#                               corresponds to the top left corner of the map and
#                               (width*height - 1) to the bottom right corner of the map.
#                               
#
# -----------------------------------------------------------------------------------------
def xy_coords_to_list(x,y,width,height):
    if (x>=0 and x<=(width-1) and y>=0 and y<=(height-1)): 
        lindex = y*width + x
        return lindex
    else:
        print "ERROR in converting from x,y map coordinates to list index. x or y coordinate outside allowed values."
        return None
            
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
    data['newspaper'] = calcNewspaper(data)
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
        },
        {
         "data":[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10],
         "height":40,
         "name":"Fog",
         "opacity":1,
         "type":"tilelayer",
         "visible":True,
         "width":40,
         "x":0,
         "y":0
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
    map = data['map']
    # if (data['enough_power'] == False):
    #     happiness = randomChange(happiness, 20, False)
    if (population > max_population):
        happiness = randomChange(happiness, 20, False) # False is superfluous, but just to show it's a negative change
    if happiness < 0:
        happiness = 0 # horrible, I know, but temporary
    if happiness < 25:
        for tile in map:
            if tile['index'] in BUILDINGS and random.randint(0,100) > 70:
                tile['properties'] = { "rioting": True }
    return happiness

def calcNewspaper(data):
    happiness = data['happiness']
    population = data['population']
    map = data['map']
    articles = []
    for tile in map:
        if "rioting" in tile['properties']:
            articles.append(RIOT_MSG)
    articles.append(ARTICLES[random.randint(0,(len(ARTICLES)-1))])
    return articles

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
