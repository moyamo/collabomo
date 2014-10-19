#!/usr/bin/env python

# Copyright (c) 2014 Mohammed Yaseen Mowzer
#
# This Software is subject to the terms of the MIT License which can be found
# LICENSE file.

from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)

@app.route('/collabomo', methods=["GET", "POST"])
def collabomo():
    if 'username' in session and session['username'] in members:
        if request.method == 'POST':
            user = session['username']
            for i in range(1, NUM_OF_QUESTIONS + 1):
                new_ans = request.form['answer' + str(i)]
                answers[user][i] = new_ans
            with open(ANSWERS_FILE, 'w') as f:
                f.write(str(answers))
        return render_template('collabomo.html', names = members,
                username = session['username'],
                NUM_OF_QUESTIONS = NUM_OF_QUESTIONS,
                answers = answers)
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
answers = dict()
NUM_OF_QUESTIONS = 30
ANSWERS_FILE = 'answerdict'
with open('secrets') as f:
    secret = f.readline()
    app.secret_key = secret
    for i in range(4):
        members.append(f.readline().strip())
    with open(ANSWERS_FILE) as f2:
        try:
            answers = eval(f2.readline())
            if not isinstance(answers, dict):
                for m in members:
                    answers[m] = [None for i in range(NUM_OF_QUESTIONS + 1)]
        except SyntaxError:
            for m in members:
                answers[m] = [None for i in range(NUM_OF_QUESTIONS + 1)]

    password = f.readline().strip()


if __name__ == '__main__':
    app.run(debug=True)
