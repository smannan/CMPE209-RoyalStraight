from flask import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/game')
def game():
	return render_template('game.html')

@app.route('/players')
def players():
	return render_template('players.html')



if __name__ =='__main__':
    app.run(debug=True)
