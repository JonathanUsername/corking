#!/usr/bin/python
from flask import Flask, request, abort, Response, jsonify, make_response, current_app, g, render_template
import json
import random
import math
import ipdb
import os
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
RESIDENT = 23

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
    map[center + 1] = RESIDENT
    map[center + WIDTH] = RESIDENT
    map[center + WIDTH + 1] = SOLAR

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
    obj = {}
    data = request.json
    data['solar_power'] = replenishPower(data['solar_power'], data['map'])
    print data
    return json.dumps(data)

@app.route("/newgame")
def give_object_coordinates():
    js = { "height":HEIGHT,
         "layers":[
                {
         "data" : get_map(no_tiles),
         "height":HEIGHT,
                 "name":"Ground",
                 "opacity":1,
                 "type":"tilelayer",
                 "visible":True,
                 "width":WIDTH,
                 "x":0,
                 "y":0
                }],"orientation":"orthogonal",
        "properties":
            {
             },
        "tileheight":32,
        "tilesets":[
                    {
                        "firstgid":1,
                        "image":"~/corking/tmw_desert_spacing.png",
                        "imageheight":199,
                        "imagewidth":265,
                        "margin":1,
                        "name":"Desert",
                        "properties":
                            {
                         },
                        "spacing":1,
                        "tileheight":32,
                        "tilewidth":32
                        }],
        "tilewidth":32,
        "version":1,
        "width":WIDTH,
        "turn":0
        }
    return Response(json.dumps(js), mimetype='application/json')


def replenishPower(amount,map_array):
    panels = 0
    for i,v in enumerate(map_array):
        print i
        if map_array[i] == 22:
            panels += 1
    return amount + (panels * 10) 


# @app.route("/test")
# def test():
#     return Response(json.dumps(get_map(1600)),mimetype='application/json')

if __name__ == "__main__":
        app.run(host="0.0.0.0", port=int("5000"))
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
