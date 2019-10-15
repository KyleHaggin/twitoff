# import important packages
from flask import Flask, render_template

# Create Flask web server
app = Flask(__name__)

# Routes determine location
@app.route('/')

# Define simple function
def home():
    return render_template()
