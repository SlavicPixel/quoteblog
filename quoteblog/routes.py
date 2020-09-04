from flask import render_template, url_for, flash, redirect, request, session
from quoteblog import app, db, bcrypt
from quoteblog.forms import RegistrationForm, LoginForm, QuoteForm
from quoteblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccesful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

