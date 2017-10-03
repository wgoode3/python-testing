import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import fileSearch

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "b7nmhjyuki8 .lo-/';[p0zxscdefr v76yu8'"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    n = fileSearch.unzipProjects()
    fileSearch.recursiveFileToJSON(n)
    t = fileSearch.testProjects()
    flash(t)

    # let's try parsing the resonse

    if t == "tests not run":
        print "cannot find tests for the given upload"
    else:
        results = t.split("\n")
        results = [r for r in results if len(r) > 0]

        tests = []
        for result in results[0]:
            tests.append(result == ".")

        print tests

    # need to associate this boolean array with the validations that need to be passed

    # save these results to a db
        # user table -> retrieve the name from their upload
        # assignment table -> store information about the specific test
        # user_assignments -> record of student's assignment uploads
            # make it store what features the assignment passes

    return redirect('/')

app.run(debug=True)