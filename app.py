#!/usr/bin/python
from flask import Flask, request, abort, Response, jsonify, make_response, current_app, g
import json
import ipdb
app = Flask(__name__)
app.config['DEBUG'] = True

# Temporary assumptions (to be updated when we can get a json file from the front end).
screen_width=400
screen_height=400


def check_name(newname):
	# Later on add a database access to see if the name is already taken
	# Assuming that there is no problem:
	return newname

def midpoint(length):
	return length/2


@app.route("/newname")
def new_name():
#	ipdb.set_trace()
	name = request.url.split("?")[1]
	return name

@app.route("/newgame")
def give_object_coordinates():
	js = [ { "rocks" : [[10,134],[234,122]],
		 "base" : [midpoint(screen_width),midpoint(screen_height)] } ]
	return Response(json.dumps(js), mimetype='application/json')

if __name__ == "__main__":
    app.run()
