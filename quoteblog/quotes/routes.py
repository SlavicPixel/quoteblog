from random import choice
import csv
from flask import render_template, url_for, flash, redirect, request, session, abort, Blueprint
from quoteblog.quotes.forms import QuoteForm

quotes = Blueprint('quotes', __name__)                            

with open('quoteblog/static/quotes.csv', "r") as file:
    data = csv.reader(file, delimiter=',')
    first_line = True
    quotes_init = []
    for row in data:
        if not first_line:
            quotes_init.append({
                "text": row[0],
                "author": row[1],
                "bio-link": row[2]
            })
        else:
            first_line=False


@quotes.route('/allquotes')
def allquotes():
    all_quotes=quotes_init
    return render_template('allquotes.html', all_quotes=all_quotes)

@quotes.route('/random')
def random_pick():
    random_quote = choice(quotes_init)
    session['random_quote'] = random_quote
    return render_template('random.html', title='Random', random_quote=random_quote)

@quotes.route('/guess', methods=['GET', 'POST'])
def guess():
    if request.method!='POST':
        random_pick()
    game_quote = session['random_quote']
    form = QuoteForm()
    if form.author_guess.data:
        if form.author_guess.data == game_quote["author"]:
            flash('Correct!', 'success')
            return redirect(url_for('quotes.result'))
        else:
            flash(f'Wrong! The answer was {game_quote["author"]}.', 'danger')
            return redirect(url_for('quotes.result'))
    return render_template('game.html', title='Game', form=form, random_quote=game_quote)

@quotes.route('/result')
def result():
    random_pick()
    return render_template('result.html', title='Result')