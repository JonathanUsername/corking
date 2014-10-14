#!/usr/bin/python

from flask import Flask, request, abort, Response, jsonify, make_response, current_app, g
import ipdb
app = Flask(__name__)
app.config['DEBUG'] = True

def check_name(newname):
	# Later on add a database access to see if the name is already taken
	# Assuming that there is no problem:
	return newname

@app.route("/newname")
def new_name():
#	ipdb.set_trace()
	name = request.url.split("?")[1]
	return name

if __name__ == "__main__":
    app.run()
