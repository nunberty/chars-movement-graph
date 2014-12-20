from persona import datasets, object_detector

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app
app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<book_name>')
def book_info(book_name=None):
    return render_template('book_info.html', book_name=book_name)

if __name__=='__main__':
    app.run(debug=True)
