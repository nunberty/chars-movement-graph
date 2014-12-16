from persona import datasets, object_detector

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app
app = create_app()

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/bye/')
def good_bye():
    return 'Good bye!'

@app.route('/hello/<name>')
def say_hello(name=None):
    return render_template('hello.html', name=name)

if __name__=='__main__':
    app.run(debug=True)
