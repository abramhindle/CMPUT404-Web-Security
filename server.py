#!/usr/bin/env python
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask

import flask
from flask import Flask, request
import json
import difflib
import os
import os.path
app = Flask(__name__)
app.debug = True


def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data != ''):
        return json.loads(request.data)
    else:
        return json.loads(request.form.keys()[0])


ourwords = []

def load_words():
    global ourwords
    words = file("server.py").read().split()
    x = dict()
    for word in words:
        x[word] = 1
    ourwords = x.keys()
    ourwords.sort()

def get_closest_words(entity, n):
    global ourwords
    print(ourwords)
    return difflib.get_close_matches(entity, ourwords, n, 0.1)

@app.route("/")
def hello():
    return flask.redirect("/static/index.html")

@app.route("/happybirthday")
def happy_birthday():
    name = request.args.get('name')
    return flask.render_template('happybirthday.html', name=name)

@app.route("/happybirthday2")
def happy_birthday2():
    name = request.args.get('name')
    if name is None:
        name = "World"
    str = file('templates/happybirthday2.html').read().replace("{{ name }}",name)
    return (str, 200, {"Content-type": "text/html"})

@app.route("/traverse")
def traverse():
    entity = request.args.get('entity')
    str = file(entity).read()
    return (str, 200, {"Content-type": "text/plain"})

@app.route("/traverse_sane")
def traverse_sane():
    entity = request.args.get('entity')
    path = os.path.abspath(entity)
    mycwd = os.getcwd()
    common = os.path.commonprefix([mycwd,path])
    if (len(common) >= len(mycwd)):
        str = file(entity).read()
        return (str, 200, {"Content-type": "text/plain"})
    else:
        flask.abort(403)

adcount = 0
@app.route("/ads")
def malicious_ad():
    global adcount
    adcount += 1
    if (adcount > 0 and (adcount % 3 == 0)):
        return flask.render_template('malice.html')
    else:
        return flask.render_template('worms.html')



if __name__ == "__main__":
    load_words()
    app.run()
