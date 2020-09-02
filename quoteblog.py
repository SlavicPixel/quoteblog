from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, QuoteForm
from random import choice
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a14ca7f30abdb6b81e94e8866d205738'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}', '{self.content}')"

@app.route('/')
@app.route('/home')
def home():
    with open('static/quotes.csv', "r") as file:
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
    return render_template('home.html', quotes=quotes)

@app.route('/random')
def random_pick():
    with open('static/quotes.csv', "r") as file:
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

if __name__ == '__main__':
    app.run(debug=True)