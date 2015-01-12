import os, json, re
import flask

from flask import (
	Flask, 
	session, 
	render_template, 
	redirect, 
	url_for, 
	request, 
	make_response,
)

app = Flask(__name__)

app.config['SECRET_KEY'] = '876sdfuisdfn23qr';

"""Game Logic Code Below (controller)"""

@app.route('/')
def index():
	session.clear()
	return render_template("Hangman.html", score=0)

@app.route('/game', methods=['GET', 'POST'])
def game():
	session['word'] = request.form['word']
	word = session['word']
	session['reveal'] = list('X'*len(word))
	reveal = session['reveal']
	session['score'] = 0
	if request.method == 'POST':
		return render_template("Game.html", word=word, \
											reveal=reveal, \
											score=0
											)
	else:
		return redirect(url_for('index'))

@app.route('/guess', methods=['GET', 'POST'])
def guess():
	"""Game View Code Below"""
	word = session['word']
	session['letter'] = request.form['letter']
	letter = session['letter']
	if letter not in word:
		session['score'] += 1
	locations = [m.start() for m in re.finditer(letter, word)]
	for i in locations:
		session['reveal'][i] = letter
	try:
		session['allguesses'].append(letter)
	except:
		session['allguesses'] = [letter]
	if request.method == 'POST':
		return render_template("Game.html", letter=letter, \
											word=word, \
											reveal=session['reveal'], \
											allguesses=session['allguesses'],\
											locations=locations,\
											score=session['score']
											)
	else:
		return redirect(url_for('index'))

app.run()

