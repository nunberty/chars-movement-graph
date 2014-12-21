import itertools
import os
import json
import functools

from flask import (Flask, render_template, request, redirect,
                    send_from_directory, url_for, Response)
from werkzeug import secure_filename
from flask_bootstrap import Bootstrap

from persona import datasets, object_detector



UPLOAD_FOLDER = '/tmp'
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

class BookInfo(object):
    def __init__(self, filename):
        self.filename = filename
        self._cache = None

    @property
    def title(self):
        return datasets.get_book_name(self._path)

    @property
    def visits(self):
        return [(i, str(l), str(p)) for i, l, p in
                object_detector.generate_schema(*self._persons_locations)]

    @property
    def persons(self):
        return [str(x) for x in self._persons_locations[0]]

    @property
    def locations(self):
        return [str(x) for x in self._persons_locations[1]]

    @property
    def _persons_locations(self):
        if self._cache is None:
            characters = datasets.fetch_character_list(self.title)
            sentences = datasets.fetch_file(self._path)
            persons, locations = object_detector.analyze(characters, sentences)
            self._cache = persons, locations
        return self._cache

    @property
    def _path(self):
        return path_to_file(self.filename)

@app.route('/api/<filename>')
def api(filename):
    bi = BookInfo(filename)
    locations = bi.locations
    groups = []
    for k, g in itertools.groupby(sorted(bi.visits), lambda x: x[0]):
        persons_for_loc = [[] for _ in locations]
        for (_, l, p) in g:
            for ll, ps in zip(locations, persons_for_loc):
                if l == ll:
                    ps.append(p)

        groups.append(persons_for_loc)

    data = {
        'title': bi.title,
        'persons': bi.persons,
        'locations': locations,
        'visits': groups
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

@app.route('/<filename>')
def schema(filename):
    bi = BookInfo(filename)
    return render_template('schema.html',
                           title=bi.title,
                           filename=filename
    )

if __name__=='__main__':
    app.run(debug=True)
