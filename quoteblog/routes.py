from flask import render_template, url_for, flash, redirect, request, session
from quoteblog import app
from quoteblog.forms import RegistrationForm, LoginForm, QuoteForm
from quoteblog.models import User, Post
from random import choice
import csv

with open('quoteblog/static/quotes.csv', "r") as file:
    data = csv.reader(file, delimiter=',')
    first_line = True
    quotes = []
    for row in data:
        if not first_line:
            quotes.append({
                "text": row[0],
                "author": row[1],
                "bio-link": row[2]
            })
        else:
            first_line=False

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route('/random')
def random_pick():
    random_quote = choice(quotes)
    session['random_quote'] = random_quote
    return render_template('random.html', title='Random', random_quote=random_quote)

@app.route('/guess', methods=['GET', 'POST'])
def guess():
    if request.method!='POST':
        random_pick()
    game_quote = session['random_quote']
    form = QuoteForm()
    if form.author_guess.data:
        if form.author_guess.data == game_quote["author"]:
            flash('Correct!', 'success')
            return redirect(url_for('result'))
        else:
            flash(f'Wrong! The answer was {game_quote["author"]}.', 'danger')
            return redirect(url_for('result'))
    return render_template('game.html', title='Game', form=form, random_quote=game_quote)

@app.route('/result')
def result():
    random_pick()
    return render_template('result.html', title='Result')

@app.route('/allquotes')
def allquotes():
    all_quotes=quotes
    return render_template('allquotes.html', quotes=all_quotes)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been loggen in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccesful. Please check username and password', 'danger')
    return render_template('login.html', title='login', form=form)