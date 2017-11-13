# Python Assignment Testing
Automated testing to provide students feedback on the Python assignments they submit. If the students name their project correctly and follow the wireframe's directions, they should get feedback showing what features their project passes. 
Current Version only supports testing Belt Exams.

### Requirements
* python version 2.7
* MongoDB version 2.6
* virtualenv

### How do I run this?
In a Mac/Linux environment simply run the following:
```
$ cd Testing 
$ ./run.sh
```
That's it. The script ```run.sh``` should take care of setting up the virtual environment, creating the necessary folders, and installing the requiements. When this is done, just go ahead and fire up your browser to ```http://localhost:5001/``` and you should be up and running.

### Version
Current Version: 0.7
| Core Features                                                       | Version |
|---------------------------------------------------------------------|:-------:|
| file upload (Flask server)                                          | v 0.1   |
| file unzip                                                          | v 0.1   |
| read and copy python unittest files                                 | v 0.1   |
| run python unittest and capture output (Django testing)             | v 0.3   |
| parse terminal output and display a table of tests and tests passed | v 0.5   |
| recursively generate JSON of python files and html files            | v 0.6   |
| connect to mongo database                                           | v 0.7   |
| Tests for all 6 Belt Exams                                          | v 0.7   |
| implement belt exam grading                                         | planned |
| write tests for belt exams (and redo wireframes)                    | planned |
| implement python fundamentals testing                               | planned |
| implement oop testing                                               | planned |
| implement flask testing                                             | planned |
| save results to database                                            | planned |
| howto page                                                          | planned |
| redo wireframe and instructions for those assignments               | planned |
| page to view results with search features                           | planned |