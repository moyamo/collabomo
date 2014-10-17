#!/usr/bin/env python

from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)

@app.route('/collabomo')
def collabomo():
    if 'username' in session and session['username'] in members:
        return render_template('omo_collab.html')
    else:
        return 'You are not allowed to view this'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if ('password' in request.form and
                'username' in request.form and
                request.form['password'] == password and
                request.form['username'] in members):
            username = request.form['username']
            session['username'] = username
            return redirect(url_for('collabomo'))
        else:
            return render_template('login.html', app_name="Collabomo Access Denied")
    else:
        return render_template('login.html', app_name="Collabomo")

@app.route('/')
def index():
    return redirect(url_for('login'))

members = list()
password = ''
with open('secrets') as f:
    secret = f.readline()
    app.secret_key = secret
    for i in range(4):
        members.append(f.readline().strip())
    password = f.readline().strip()

if __name__ == '__main__':
    app.run(debug=True)
