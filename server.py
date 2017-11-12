#!/usr/bin/env python
import os
import json
import bson
import fileSearch
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo

app            = Flask(__name__)
app.secret_key = "b7nmhjyuki8lop0zxscdefrv76yu8"
app.name       = "py_test" # app.name is the mongod database name
mongo          = PyMongo(app)

# route to show the main page
@app.route('/')
def index():
    return render_template('index.html')

# file upload, unzipping, generating a json, and runnung tests on the exam
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        fileSearch.uploadZipfile(request.files['file'])
        fileSearch.unzipProjects()
        fileSearch.recursiveFileToJSON()
        session["output"] = fileSearch.testProjects()
    return redirect('/')

# clear the most recent exam data from the screen
@app.route('/clear')
def clear():
    session.clear()
    return redirect('/')

# A route to test out using a Mongo Database
@app.route('/results', methods=["GET", "POST"])
def results():
    if request.method == "POST":
        mongo.db.results.insert({
            "status": "ok",
            "tests": request.form["thing"],
            "bool": True
        })
        return redirect('/results')
    else:
        return render_template("results.html", results=mongo.db.results.find())

# Another route to test out using a Mongo Database
@app.route('/delete/<_id>')
def delete(_id):
    mongo.db.results.remove({"_id": bson.objectid.ObjectId(_id)})
    return redirect('/results')

app.run(port=5001, debug=True)