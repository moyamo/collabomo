#!/usr/bin/env python

# Copyright (c) 2014 Mohammed Yaseen Mowzer
#
# This Software is subject to the terms of the MIT License which can be found
# LICENSE file.

from flask import Flask, render_template, redirect, url_for, request, session
import os
import datetime

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
                times = ["No posts" if len(t) <= 0 else str(t[-1][0]) + ' ' +  str(t[-1][2]) for t in forum_threads ],
                answers = answers)

    else:
        return 'You are not allowed to view this'

@app.route('/thread/<questnum>', methods=["GET", "POST"])
def forum(questnum):
    try:
        number = int(questnum)
        if request.method == "POST":
            text = request.form["posttext"]
            user = session['username']
            if user in members:
                post_to_forum(user, text, number)
        return render_template('thread.html',
                app_name = "Collabomo",
                question = questnum,
                posts = forum_threads[number])
    except SyntaxError:
        return "Page not found"


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

forum_path = 'posts/'
def read_forum_data():
    forum_data = list()
    for i in range(NUM_OF_QUESTIONS + 1):
        filename = forum_path + str(i)
        if os.path.exists(filename):
            with open(filename) as f:
                forum_data.append(eval(f.readline()))
        else:
            forum_data.append(list())
    return forum_data

def post_to_forum(user, text, thread):
    forum_threads[thread].append((user, text, datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))))
    with open(forum_path + str(thread), 'w') as f:
        f.write(str(forum_threads[thread]))
        

members = list()
password = ''
answers = dict()
NUM_OF_QUESTIONS = 30
ANSWERS_FILE = 'answerdict'

forum_threads = read_forum_data()

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
