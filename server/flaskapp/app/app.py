from utils.path import fix_path
import os

# this fix allows us to import modues/packages found in 'lib'
fix_path(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, render_template
from blueprints.example.views import bp as example_blueprint


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/maps')
def maps():
    return render_template('map.html')
@app.route('/login')
def login():
	return render_template('login.html')


# register Blueprints
app.register_blueprint(example_blueprint)
