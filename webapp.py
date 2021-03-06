#!/usr/bin/env python

from flask import Flask, render_template, request
from serial import Serial

app = Flask(__name__)
port = Serial('/dev/ttyUSB0', 9600)

@app.route('/')
def home():
    return render_template('chrl.html')

@app.route('/update', methods=['POST'])
def update():
    port.write(''.join(''.join(chr(int(i)) for i in line.split(',')) for line in request.data.split('\n')))
    return ''

if __name__ == '__main__':
    app.run(debug=True)
