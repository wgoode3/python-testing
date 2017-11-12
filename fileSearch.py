#!/usr/bin/env python
import os
import zipfile
import json
import shutil
import subprocess
import time
import hashlib
from werkzeug.utils import secure_filename
from os import listdir
from os.path import join, dirname, realpath, isfile, isdir

"""
TODO List:
1) rubric.json - belt grading rules
2) beltScore   - use rubric to determine belt score
"""

UPLOADS = join(dirname(realpath(__file__)), "uploads")
PROJECTS = join(dirname(realpath(__file__)), "projects")
TESTS = join(dirname(realpath(__file__)), "tests")
JSONS = join(dirname(realpath(__file__)), "jsons")

with open('assignments.json') as data_file:
    ASSIGNMENTS = json.load(data_file)

# for use with recursiveFileToJSON
ACCEPTED_FILES = set(["py", "html"])

# saves a file in the uploads folder
def uploadZipfile(file):
    if file and file.filename.endswith(".zip"):
        filename = secure_filename(file.filename)
        file.save(os.path.join("uploads", filename))

# removes all files and folders from the specified folder
def cleanFolder(folder):
    for thing in listdir(folder):
        path_to_thing = join(folder, thing)
        if isdir(path_to_thing):
            shutil.rmtree(path_to_thing)
        if isfile(path_to_thing):
            os.remove(path_to_thing)

# function to unzip zip files in uploads to projects
def unzipProjects():
    files = [f for f in listdir(UPLOADS) if isfile(join(UPLOADS, f))]
    for file in files:
        if file.endswith(".zip"):
            try:
                zip_ref = zipfile.ZipFile(join(UPLOADS, file), 'r')
                zip_ref.extractall(PROJECTS)
                zip_ref.close()
            except:
                print "something went wrong unzipping..."

    cleanFolder(UPLOADS)

# function to convert all files in the project into a json object
def recursiveFileToJSON():

    # we may find a way to pass student names and ids to this function later
    student_id   = None
    first_name   = "Test"
    last_name    = "McTesterson"
    project_name = listdir(PROJECTS)[0]
    timestamp    = int(time.time())

    # I have to declare this variable in a list to update it recursively in python, weird
    myjson = ['{\n\t"project": "' + project_name + '",\n\t"student": {\n\t\t"first_name": "' + first_name + '",\n\t\t"last_name": "' + last_name + '"\n\t}']
    filename = "{}_{}_{}_{}.json".format(first_name, last_name, project_name, timestamp)

    # check if the file should be one to be added to the json
    def allowedFile(file):
        if '.' not in file:
            return False
        elif file[0:2] == "__":
            return False
        elif file.rsplit('.', 1)[1].lower() not in ACCEPTED_FILES:
            return False
        else:
            return True

    def helper(path, relative_path):
        for thing in listdir(path):

            # ignore any .git folers, maybe ignore all folders that start with `.`
            if isdir(join(path, thing)) and thing != ".git":
                helper(join(path, thing), join(relative_path, thing))

            if isfile(join(path, thing)) and allowedFile(thing):
                with open(join(path, thing), 'r') as testFile:

                    # split on new lines and tabs
                    filetext = " ".join(testFile.read().split("\n"))
                    filetext = " ".join(filetext.split("\t"))

                # properly escape `"` and `\`characters && also remove unnecessary whitespace
                string = ""
                prev = ""
                for letter in filetext:
                    if letter == '"' or letter == "\\":
                        string += "\\"
                    if (letter.isspace() and not prev.isspace()) or not letter.isspace():
                        string += letter
                    prev = letter

                # add the file text as raw and a hash as hash     
                myjson[0] += ',\n\t"' + join(relative_path, thing) + '": {\n'
                myjson[0] += '\t\t"raw": "' + string + '",\n'
                myjson[0] += '\t\t"hash": "' + hashlib.sha512(string).hexdigest() + '"\n\t}'

            # to prevent: `RuntimeWarning: DateTimeField received a naive datetime`
            if thing == "settings.py":
                with open(join(path, thing), 'a') as testFile:
                    testFile.write("USE_TZ = False")
                    testFile.close()

    helper(PROJECTS, "")
    myjson[0] += "\n}"

    z = open(join(JSONS, filename), 'w+')
    z.write(myjson[0])
    z.close()

# add python tests to the right place and capture the output
def testProjects():

    # what to pass on if nothing runs
    thing = "tests not run"
    projects = [d for d in listdir(PROJECTS) if isdir(join(PROJECTS, d))]

    for project in projects:

        # I should probably change how we do this...
        assignments = [a for a in ASSIGNMENTS["assignments"] if a["name"] == project]

        if len(assignments) > 1:
            print "error: more than one assignment matches!"
            cleanFolder(PROJECTS)
            return thing
        elif len(assignments) < 1:
            print "error: no assignment matches!"
            cleanFolder(PROJECTS)
            return thing

        assignment = assignments[0]

        if assignment["type"] == "fundamentals":
            print "python fundamentals testing"

            # copy in the appropriate test file
            """
            with open(join(TESTS, a["test"]), 'r') as testFile:
                text = testFile.read()
                z = open(join(PROJECTS, p), 'w+')
                z.write(text)
                z.close()

            os.chdir("projects/{}".format(p))

            # need to test this

            try:
                cmd = "python {}".format(a["test"])
                t = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
            except subprocess.CalledProcessError as e:
                # print "Oops... returncode: {}, output:\n {}".format(e.returncode, e.output)
                t = e.output

            os.chdir("../..")
            """

        elif assignment["type"] == "oop":
            print "python oop testing"
        elif assignment["type"] == "flask":
            print "python flask testing"
        elif assignment["type"] == "django" or assignment["type"] == "belt_exam":

            if(isdir(join(PROJECTS, project, 'apps'))):
                
                app_not_found = True
                for folder in listdir(join(PROJECTS, project, 'apps')):    
                    
                    # finding the tests.py file in a django project
                    # this will break things if they delete it for some reason...
                    if(isdir(join(PROJECTS, project, 'apps', folder)) and app_not_found):
                        if(isfile(join(PROJECTS, project, 'apps', folder, "tests.py"))):

                            # avoid copying the tests into multiple apps
                            app_not_found = False

                            # open the file with the tests
                            try:
                                with open(join(TESTS, assignment["test"]), 'r') as testFile:
                                    text = testFile.read()
                                    testTarget = open(join(PROJECTS, project, 'apps', folder, "tests.py"), 'w')
                                    testTarget.write(text)
                                    testTarget.close()
                            except IOError:
                                print "cannot find the test for", project
                
                """
                I may need to check that this file exists at all in the place we're looking
                recursive file to json could let me know
                """

                # make the manage.py in the downloaded file executable
                os.system("chmod +x projects/{}/manage.py".format(project))
                # for some reason tests can only be run from inside the folder... 
                os.chdir("projects/{}".format(project))
                # ls to see that we are in the right folder
                # os.system("ls")

                # run the tests we copied in, save the output to t
                try:
                    output = subprocess.check_output("./manage.py test", stderr=subprocess.STDOUT, shell=True)
                except subprocess.CalledProcessError as e:
                    # print "Oops... returncode: {}, output:\n {}".format(e.returncode, e.output)
                    output = e.output
                
                # clean up by cd'ing back and deleting the folder
                os.chdir("../..")

                thing = score(project + "_test.py", output)

            else:
                print "apps folder not found in the expected location"

    # return the output from testing
    cleanFolder(PROJECTS)
    return thing

# function to generate the score output of what tests passed
def score(testname, output):

    # there may be errors when grading Appointments at around 12:00 AM
    # could fix by modifying the settings.py if time close to midnight...

    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errored": 0,
        "raw": output,
        "messages": []
    }

    try:
        with open(join(TESTS, testname), 'r') as testFile:
            text = testFile.read()
    except IOError:
        results["messages"].append("cannot find the test file, {}".format(testname))

    # parses test method names from the test file
    functions = [line.lstrip()[4:].split("(")[0] for line in text.split("\n") if line.lstrip()[0:3] == "def"]
    tests = [" ".join(func.split("_")[2:]) for func in functions if func[0:4] == "test"]
    results["tests"] = [{"name": test, "outcome": None} for test in tests]

    # determines if each test passed, failed, or errored
    test_runner = output.split("\n")[0]

    if len(results["tests"]) == len(test_runner):
        for i in range(0, len(test_runner)):
            results["total"] += 1
            if test_runner[i] == ".":
                results["tests"][i]["outcome"] = "Passed"
                results["passed"] += 1
            elif test_runner[i] == "F":
                results["tests"][i]["outcome"] = "Failed"
                results["failed"] += 1
            elif test_runner[i] == "E":
                results["tests"][i]["outcome"] = "Errored"
                results["errored"] += 1
    else:
        results["messages"].append("length missmatch between tests and expected tests")

    return results