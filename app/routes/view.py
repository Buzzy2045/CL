from flask import render_template
from . import main

@main.route('/')
def home():
    return "Hello, Flask is running!"
