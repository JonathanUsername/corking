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
screen_width=400
screen_height=400
no_tiles=1600
DESERT = 30
SOLAR = 22
RESIDENT = 23

def generate_desert(size):
    desertmap = []
    for i in range(size):
        desertmap.append(DESERT)
    # Add the initial solar panels
    #   S|R
    #   -+-
    #   R|S
    desertmap[no_tiles/2] = SOLAR
    desertmap[no_tiles/2 + 1 ] = RESIDENT
    desertmap[no_tiles/2 + screen_width] = RESIDENT
    desertmap[no_tiles/2 + screen_width + 1] = SOLAR

    return desertmap
            
                
            
                    

def check_name(newname):
    # Later on add a database access to see if the name is already taken
    # Assuming that there is no problem:
    return newname

def midpoint(length):
    return length/2

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/newname")
def new_name():
#    ipdb.set_trace()
    name = request.url.split("?")[1]
    return name

@app.route("/newgame")
def give_object_coordinates():
    js = { "height":40,
         "layers":[
                {
         "data" : generate_desert(no_tiles),
         "height":40,
                 "name":"Ground",
                 "opacity":1,
                 "type":"tilelayer",
                 "visible":True,
                 "width":40,
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
        "width":40
        }
    return Response(json.dumps(js), mimetype='application/json')



# @app.route("/test")
# def test():
#     return Response(json.dumps(generate_desert(1600)),mimetype='application/json')

if __name__ == "__main__":
        app.run(host="0.0.0.0", port=int("5000"))
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
