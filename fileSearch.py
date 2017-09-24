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

    # clean up the downloads folder by getting rid of the zip file
    os.remove(join(UPLOADS, file))

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
                        print "python django testing"

                        if(isdir(join(PROJECTS, p, 'apps'))):
                            print "apps folder exists"
                            
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
                            shutil.rmtree(join(PROJECTS, p))

    # return the output from testing
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