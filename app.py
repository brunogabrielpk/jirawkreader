import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from fmain1 import runxml

app = Flask(__name__)
app.secret_key = "secret key"

#It will allow below 16MB contents only, you can change it
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
STATIC_FOLDER = os.path.join(path, 'static')
IMAGES_FOLDER = os.path.join(path, 'static/images')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
if not os.path.isdir(STATIC_FOLDER):
    os.mkdir(STATIC_FOLDER)
if not os.path.isdir(IMAGES_FOLDER):
    os.mkdir(IMAGES_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['xml'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            filepath= runxml(fname = os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # img_path = os.path.join(app.config['IMAGES_FOLDER'], img_filename)
            return render_template('upload.html', filename = filepath)
        else:
            flash('Allowed file types are xml')
            return redirect(request.url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
