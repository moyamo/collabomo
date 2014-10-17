#!/usr/bin/env python

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/collabomo')
def collabomo():
    return render_template('omo_collab.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', app_name="Collabomo")

@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
