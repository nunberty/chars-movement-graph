from persona import datasets, object_detector
from flask import (Flask, render_template, request, redirect,
                    send_from_directory, url_for)
from werkzeug import secure_filename
from flask_bootstrap import Bootstrap
import os

UPLOAD_FOLDER = '/home/alina/test/'
ALLOWED_EXTENSIONS = {'fb2'}

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    return app
app = create_app()

def allowed_file(filename):
    return ('.' in filename) and (
            filename.split('.')[1] in ALLOWED_EXTENSIONS
    )

@app.route('/<filename>', endpoint='with_filename')
@app.route('/', methods=['GET', 'POST'], endpoint='index')
def index(filename=None):
    if request.method == 'POST':
        print(request)
        print(request.files)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            return redirect(url_for('with_filename', filename=filename))
    return render_template(
        'index.html',
        filename=filename,
        supported_formats=','.join(sorted(ALLOWED_EXTENSIONS))
    )

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/<book_name>')
def book_info(book_name=None):
    return render_template('book_info.html', book_name=book_name)

if __name__=='__main__':
    app.run(debug=True)
