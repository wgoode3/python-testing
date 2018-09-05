# Python Assignment Testing

<img src="https://raw.githubusercontent.com/wgoode3/python-testing/master/demo.gif" alt="demo.gif" />

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
