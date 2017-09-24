import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import fileSearch

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'Could this key be any more secret?'

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
    fileSearch.unzipProjects()
    t = fileSearch.testProjects()
    flash(t)

    # save these results to a db
        # user table -> retrieve the name from their upload
        # assignment table -> store information about the specific test
        # user_assignments -> record of student's assignment uploads
            # make it store what features the assignment passes

    # some sort of api to tell the app to fetch student files

    return redirect('/')

app.run(debug=True)