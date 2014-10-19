#!/usr/bin/env python

# Copyright (c) 2014 Mohammed Yaseen Mowzer
#
# This Software is subject to the terms of the MIT License which can be found
# LICENSE file.

from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)


def save_answers():
    with open(ANSWERS_FILE, 'w') as f:
        f.write(str(answers))


@app.route('/collabomo', methods=["GET", "POST"])
def collabomo():
    if 'username' in session and session['username'] in members:

        if request.method == 'POST':
            user = session['username']
            for i in range(1, NUM_OF_QUESTIONS + 1):
                answers[user][i] = request.form['answer' + str(i)]
            save_answers()

        return render_template('collabomo.html',
                names = members,
                username = session['username'],
                NUM_OF_QUESTIONS = NUM_OF_QUESTIONS,
                answers = answers)

    else:
        return 'You are not allowed to view this'


def authenticate(form):
    correct_password = 'password' in form and form['password'] == password
    correct_username  = 'username' in form and form['username'] in members
    return correct_password and correct_username


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        if authenticate(request.form):
            session['username'] = request.form['username']
            return redirect(url_for('collabomo'))

        else:
            return render_template('login.html',
                    app_name="Collabomo Access Denied")

    else:
        return render_template('login.html', app_name="Collabomo")


@app.route('/')
def index():
    return redirect(url_for('login'))

def init_answers():
    for m in members:
        answers[m] = [None for i in range(NUM_OF_QUESTIONS + 1)]

members = list()
password = ''
answers = dict()
NUM_OF_QUESTIONS = 30
ANSWERS_FILE = 'answerdict'

with open('secrets') as f:

    app.secret_key = f.readline()

    for i in range(4):
        members.append(f.readline().strip())

    with open(ANSWERS_FILE) as f2:
        try:
            answers = eval(f2.readline())
            if not isinstance(answers, dict):
                raise SyntaxError()
        except SyntaxError:
            init_answers()

    password = f.readline().strip()

if __name__ == '__main__':
    app.run(debug=True)
