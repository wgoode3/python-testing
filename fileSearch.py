#!/usr/bin/env python
import os
import zipfile
import json
import shutil
from os import listdir
from os.path import join, dirname, realpath, isfile, isdir

uploads = join(dirname(realpath(__file__)), "uploads")
projects = join(dirname(realpath(__file__)), "projects")
tests = join(dirname(realpath(__file__)), "tests")

def testProjects():

	files = [f for f in listdir(uploads) if isfile(join(uploads, f))]
	for file in files:
		if file.endswith(".zip"):

			print "unzipping " + file

			zip_ref = zipfile.ZipFile(join(uploads, file), 'r')
			zip_ref.extractall(projects)
			zip_ref.close()
			for p in listdir(projects):
				if(isdir(join(projects, p))):
					
					# failed approach of trying to use a shell script
					# let this comment serve as a warning to myself not to try that again

					"""
					print p
					text = open("projects/test.sh", "w")
					text.write("#!/bin/sh\n")
					text.write("echo 'from inside the shell script'\n")
					text.write("source djangoEnv/bin/activate\n")
					text.write("cd {}\n".format(p))
					text.write("chmod +x manage.py\n")
					text.write("./manage.py test > results.txt\n")
					text.write("deactivate\n")
					text.write("cd ..\n")
					text.close()
					text = open("projects/test.sh").read()
					print text
					subprocess.call(['./projects/test.sh'])
					"""

					# print "looking for project name", p

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
										find one of the apps at least may need to overwrite all other 
										testing files to avoid errors if student is already testing 
										their code. I don't think students really do that... 
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

														# for debugging the test file
														global test_file_location
														test_file_location = join(projects, p, 'apps', f, "tests.py")

										# make the manage.py in the downloaded file executable
										os.system("chmod +x projects/{}/manage.py".format(p))
										# for some reason tests can only be run from inside the folder... 
										os.chdir("projects/{}".format(p))
										# ls to see that we are in the right folder
										# os.system("ls")
										# run the tests we copied in
										os.system("./manage.py test".format(p))
										# let's cd back out again
										os.chdir("../..")
										# this deletes the file from the folder
										shutil.rmtree(join(projects, p))

					# then go into one of their apps
					# then write the tests into the student's test.py
					# then make manage.py executable
					# then run our tests

					# save these results to a db
						# user table -> retrieve the name from their upload
						# assignment table -> store information about the specific test
						# user_assignments -> record of student's assignment uploads
							# make it store what features the assignment passes

					# some sort of api to tell the app to fetch student files

		os.remove(join(uploads, file))