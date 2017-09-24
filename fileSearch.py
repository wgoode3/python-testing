#!/usr/bin/env python
import os
import zipfile
import json
import shutil
import subprocess
from os import listdir
from os.path import join, dirname, realpath, isfile, isdir

uploads = join(dirname(realpath(__file__)), "uploads")
projects = join(dirname(realpath(__file__)), "projects")
tests = join(dirname(realpath(__file__)), "tests")

def unzipProjects():
    files = [f for f in listdir(uploads) if isfile(join(uploads, f))]
    for file in files:
        if file.endswith(".zip"):
            # print "unzipping " + file
            zip_ref = zipfile.ZipFile(join(uploads, file), 'r')
            zip_ref.extractall(projects)
            zip_ref.close()

    # clean up the downloads folder by getting rid of the zip file
    os.remove(join(uploads, file))

def testProjects():
    t = "tests not run"
    for p in listdir(projects):
        if(isdir(join(projects, p))):
            with open('assignments.json') as data_file:
                assignments = json.load(data_file)
                for a in assignments["assignments"]:
                    if a["name"] == p:
                        if a["type"] == "fundamentals":
                            print "python fundamentals testing"
                        elif a["type"] == "oop":
                            print "python oop testing"
                        elif a["type"] == "flask":
                            print "python flask testing"
                        elif a["type"] == "django":
                            print "python django testing"

                            if(isdir(join(projects, p, 'apps'))):
                                print "apps folder exists"
                                
                                app_not_found = True
                                
                                """
                                find one of the apps at least
                                may need to overwrite all other testing files to 
                                avoid errors if student is already testing their code. 
                                I don't think students really do that... 
                                test their code I mean  
                                """

                                for f in listdir(join(projects, p, 'apps')):    
                                    if(isdir(join(projects, p, 'apps', f)) and app_not_found):
                                        if(isfile(join(projects, p, 'apps', f, "tests.py"))):

                                            # avoid copying the tests into multiple apps
                                            app_not_found = False

                                            # open the file with the tests
                                            with open(join(tests, a["test"]), 'r') as testFile:
                                                text = testFile.read()
                                                testTarget = open(join(projects, p, 'apps', f, "tests.py"), 'w')
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
                                    print "Oops... returncode: {}, output:\n {}".format(e.returncode, e.output)
                                    t = e.output
                                

                                # let's cd back out again
                                os.chdir("../..")
                                # this deletes the file from the folder
                                shutil.rmtree(join(projects, p))

    # return the output from the testing
    return t