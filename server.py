#!/usr/bin/env python
import os
import json
import bson
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import fileSearch

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['zip'])

with open('assignments.json') as data_file:
    ASSIGNMENTS = json.load(data_file)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "b7nmhjyuki8 .lo-/';[p0zxscdefr v76yu8'"

# app.name will be the mongod database name
app.name = "py_test"
mongo = PyMongo(app)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    
    output = {
        "raw": "",
        "tests": []
    }

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            n = fileSearch.unzipProjects()
            fileSearch.recursiveFileToJSON(n)
            output["raw"] = fileSearch.testProjects()

            try:
                if output["raw"] != "tests not run":

                    for a in ASSIGNMENTS["assignments"]:
                        
                        results = output["raw"].split("\n")[0]


                        if a["name"] == n[2]:
                            # print "we found", n[2]
                            # print a["tests"]

                            count = 0

                            for test in a["tests"]:
                                output["tests"].append({"name": test, "result": results[count] == "."})
                                count += 1

                session["output"] = output
            except KeyError:
                print "tests not found for", n[2]

    return redirect('/')

@app.route('/clear')
def clear():
    session.clear()
    return redirect('/')

# just some test routes for using a mongo database

@app.route('/results', methods=["GET", "POST"])
def results():
    if request.method == "POST":
        val = {'status': 'ok'}
        val["tests"] = request.form["thing"]
        val["bool"] = True
        mongo.db.results.insert(val)
        return redirect('/results')
    return render_template("results.html", results=mongo.db.results.find())

@app.route('/delete/<_id>')
def delete(_id):
    mongo.db.results.remove({"_id": bson.objectid.ObjectId(_id)})
    return redirect('/results')

app.run(port=5001, debug=True)