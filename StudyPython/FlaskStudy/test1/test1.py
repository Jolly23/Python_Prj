#!/usr/bin/env python
import sys
from flask import Flask
from flask import render_template

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/fuck')
def fuck():
    return render_template('base.html')


if __name__ == '__main__':
    app.run()
