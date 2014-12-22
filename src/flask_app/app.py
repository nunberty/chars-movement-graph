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
            print("")
            print(self.title)
            print("")

            characters = datasets.fetch_character_list(self.title)
            sentences = datasets.fetch_file(self._path)
            persons, locations = object_detector.analyze(characters, sentences)
            self._cache = (sorted(persons, key=lambda x: str(x)),
                           sorted(locations, key=lambda x: str(x)))
        return self._cache

    @property
    def _path(self):
        return path_to_file(self.filename)

@app.route('/api/<filename>')
def api(filename):
    bi = BookInfo(filename)
    position_f = lambda x: x[0]
    location_f = lambda x: x[1]
    pearson_f = lambda x: x[2]

    visits = sorted(bi.visits, key=position_f)
    # visits = [v for v in visits if v[2] == "Mrs. Jones"]
    position_index = {p: i for (i, p) in
                      enumerate(sorted({x for (x, _, _) in visits}))}
    locations_index = {l: i for (i, l) in enumerate(bi.locations)}
    person_index = {p: i for (i, p) in enumerate(bi.persons)}
    groups = []
    for _, g in itertools.groupby(visits, position_f):
        persons_for_loc = [[] for _ in bi.locations]
        for (_, l, p) in g:
            persons_for_loc[locations_index[l]].append(p)

        groups.append(persons_for_loc)

    transitions = [[] for p in bi.persons]
    for p, g in itertools.groupby(sorted(visits, key=pearson_f), pearson_f):
        locs = [{'position': position_index[pos], 'location': locations_index[l]}
                for (pos, l, _) in sorted(g, key=position_f)]
        for l1, l2 in zip(locs, locs[1:]):
            transitions[person_index[p]].append((l1, l2))

    data = {
        'title': bi.title,
        'persons': bi.persons,
        'locations': bi.locations,
        'visits': groups,
        'transitions': transitions
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
