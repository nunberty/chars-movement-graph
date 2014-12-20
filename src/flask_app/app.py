from persona import datasets, object_detector
from flask import (Flask, render_template, request, redirect,
                    send_from_directory, url_for, Response)
from werkzeug import secure_filename
from flask_bootstrap import Bootstrap
import os
import json

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

@app.route('/', methods=['GET', 'POST'], endpoint='index')
def index(filename=None):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(path_to_file(filename))
            return redirect(url_for('schema', filename=filename))
    return render_template(
        'index.html',
        supported_formats=','.join(sorted(ALLOWED_EXTENSIONS))
    )

def path_to_file(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/')
def api():
    data = {"xs": [100, 4, 8, 16]}
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

@app.route('/<filename>')
def schema(filename):
    path = path_to_file(filename)
    title = datasets.get_book_name(path)
    characters = datasets.fetch_character_list(title)

    return render_template('schema.html',
        title=title,
        characters=characters
    )

if __name__=='__main__':
    app.run(debug=True)
