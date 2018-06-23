#! /usr/bin/python3

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/', methods=['POST'])
def processing():
    return '585a8a6c'
