#!/usr/bin/env python
import os
import zipfile
import json
import shutil
import subprocess
from os import listdir
from os.path import join, dirname, realpath, isfile, isdir

UPLOADS = join(dirname(realpath(__file__)), "uploads")
PROJECTS = join(dirname(realpath(__file__)), "projects")
TESTS = join(dirname(realpath(__file__)), "tests")
JSONS = join(dirname(realpath(__file__)), "jsons")

with open('assignments.json') as data_file:
    ASSIGNMENTS = json.load(data_file)

def unzipProjects():
    files = [f for f in listdir(UPLOADS) if isfile(join(UPLOADS, f))]
    for file in files:
        if file.endswith(".zip"):
            # print "unzipping " + file
            zip_ref = zipfile.ZipFile(join(UPLOADS, file), 'r')
            zip_ref.extractall(PROJECTS)
            zip_ref.close()

            # extract student name from upload
            names = file.split("_")
            if(len(names) > 2):
                proj = names[2].split(".")
                n = (names[0], names[1], proj[0])
            else:
                proj = file.split(".")
                n = ("unknown", "unknown", proj[0])

    # clean up the downloads folder by getting rid of the zip file
    os.remove(join(UPLOADS, file))
    return n

def testProjects():
    t = "tests not run"
    for p in listdir(PROJECTS):
        if(isdir(join(PROJECTS, p))):
            for a in ASSIGNMENTS["assignments"]:
                if a["name"] == p:
                    if a["type"] == "fundamentals":
                        print "python fundamentals testing"
                    elif a["type"] == "oop":
                        print "python oop testing"
                    elif a["type"] == "flask":
                        print "python flask testing"
                    elif a["type"] == "django":
                        # print "python django testing"

                        if(isdir(join(PROJECTS, p, 'apps'))):
                            # print "apps folder exists"
                            
                            app_not_found = True
                            
                            for f in listdir(join(PROJECTS, p, 'apps')):    
                                if(isdir(join(PROJECTS, p, 'apps', f)) and app_not_found):
                                    if(isfile(join(PROJECTS, p, 'apps', f, "tests.py"))):

                                        # avoid copying the tests into multiple apps
                                        app_not_found = False

                                        # open the file with the tests
                                        with open(join(TESTS, a["test"]), 'r') as testFile:
                                            text = testFile.read()
                                            testTarget = open(join(PROJECTS, p, 'apps', f, "tests.py"), 'w')
                                            testTarget.write(text)
                                            testTarget.close()

                            # make the manage.py in the downloaded file executable
                            os.system("chmod +x projects/{}/manage.py".format(p))
                            # for some reason tests can only be run from inside the folder... 
                            os.chdir("projects/{}".format(p))
                            # ls to see that we are in the right folder
                            # os.system("ls")
                            # run the tests we copied in, save the output to t

                            try:
                                t = subprocess.check_output("./manage.py test", stderr=subprocess.STDOUT, shell=True)
                            except subprocess.CalledProcessError as e:
                                # print "Oops... returncode: {}, output:\n {}".format(e.returncode, e.output)
                                t = e.output
                            
                            # clean up by cd'ing back and deleting the folder
                            os.chdir("../..")

    # return the output from testing
    cleanProjects()
    return t
    # consider rewriting into an object
    """
    {
        "student": {
            "first": "Example",
            "last": "Name"
        },
        "assignment": "Test Assignment",
        "optional": True,
        "passed": True,
        "tests": [
            {
                "name": "test_login_screen_exists",
                "passed": True,
                "error": ""
            },
            {
                "name": "test_register_validations",
                "passed": "True",
                "error": ""
            },
            {
                "name": "test_login_validations",
                "passed": True,
                "error": ""
            },
            {
                "name": "test_successful_login",
                "passed": True,
                "error": ""
            },
            {
                "name": "test_successful_register",
                "passed": True,
                "error": ""
            }
        ]
    }
    """

# removes all files and folders from the projects folder
def cleanProjects():
    for thing in listdir(PROJECTS):
        path_to_thing = join(PROJECTS, thing)
        if isdir(path_to_thing):
            shutil.rmtree(path_to_thing)
        if isfile(path_to_thing):
            os.remove(path_to_thing)

# function to convert all files in the project into a json object

REJECT_SUFFIX = set(["pyc", "sqlite3", "jpg", "jpeg", "png", "gif", "css"])

def recursiveFileToJSON(n):
    myjson = ['{\n\t"project": "' + n[2] + '",\n\t"student": {\n\t\t"first_name": "' + n[0] + '",\n\t\t"last_name": "' + n[1] + '"\n\t}']
    filename = "{}_{}_{}.json".format(n[0], n[1], n[2])

    def allowedFile(file):
        flag = True
        if '.' not in file:
            flag = False
        if file.endswith("DS_Store"):
            flag = False
        if file.rsplit('.', 1)[1].lower() in REJECT_SUFFIX:
            flag = False
        if file[0:2] == "__":
            flag = False
        return flag

    def helper(path, relative_path):
        for p in listdir(path):
            if isdir(join(path, p)):
                helper(join(path, p), join(relative_path, p))
            if isfile(join(path, p)) and allowedFile(p):
                with open(join(path, p), 'r') as testFile:
                    text = testFile.read().splitlines()
                    t = ''.join(text)
                    
                    # properly escape `"` characters
                    q = ''
                    for l in t:
                        if l == '"':
                            q += "\\"
                        q += l

                    myjson[0] += ',\n\t"' + join(relative_path, p) + '": {\n'
                    myjson[0] += '\t\t"raw": "' + q + '"\n\t}'

    helper(PROJECTS, "")
    myjson[0] += "\n}"

    z = open(join(JSONS, filename), 'w+')
    z.write(myjson[0])
    z.close()
