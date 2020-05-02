import sys
import binascii
import random
import flask
import flask_sqlalchemy
import flask_restless
from sqlalchemy.orm import validates
from poker import Card

sys.path.append("..")
from encryption import (
    generateKeys,
    generateSessionKey,
    rsa_encrypt,
    )
from encryption import ASCII_to_binary as a2b
from encryption import binary_to_ASCII as b2a

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
# app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poker.db'
db = flask_sqlalchemy.SQLAlchemy(app)


def encrypt_token(context):
    b64_token = context.get_current_parameters()['token']
    b64_pubkey = context.get_current_parameters()['pubkey']

    # Convert to binary for the rsa_encrypt function
    bin_token = a2b(b64_token)
    bin_pubkey = a2b(b64_pubkey)
    b64_enc_key = rsa_encrypt(bin_token, bin_pubkey)

    # Convert back to utf8 for storage
    return b64_enc_key
    # return token+pubkey


gs_default = {
    "bet":0,
    "pool":0,
}

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True)
    pubkey = db.Column(db.String, unique=True)
    token = db.Column(db.Unicode, default=generateSessionKey(output='base64'))
    enc_token = db.Column(db.Unicode, default=encrypt_token)

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, default=gs_default)

    def __init__(self):
        #create deck with all of the cards
        self.deck = list(Card)
        #shuffle the deck
        random.shuffle(self.deck)
        # create a list of players in the game. 
        self.players = []
        self.pot = 0
        self.bet = 0
        self.comCards = []
    
    def addPlayer(self, player):
        self.players.append(player)
        db.session.add(player1)
        db.session.commit() 

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, db.ForeignKey('user.username'))
    gameid = db.Column(db.Integer, db.ForeignKey('game.id'))
    # Player's private cards represented as a JSON value
    cards = db.Column(db.JSON)

class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode)
    betround = db.Column(db.Integer, default=0)
    action = db.Column(db.Unicode)
    amount = db.Column(db.Integer, default=0)

    @validates('action')
    def validate_action(self, key, value):
        assert value in (
            'bet', 
            'check', 
            'raise',
            'fold',
            'call'
        )

        return value

    @validates('amount')
    def validate_amount(self, key, value):
        if self.action in ('bet', 'raise'):
            assert int(value) > 0
        return value


# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename>
manager.create_api(User, methods=['GET', 'POST'], exclude_columns=['token'])
# TODO: Remove POST, API doesn't need to expose game post, this is just for testing.
manager.create_api(Game, methods=['GET', 'POST'])
manager.create_api(Update, methods=['POST'])
manager.create_api(Player, methods=['GET', 'POST'])
# manager.create_api(Update, methods=['POST'], exclude_columns=['token'])

# start the flask loop
if __name__ == "__main__":

    # Run a bunch of commands if this is called as __main__

    # 1. Cleanup database
    db.drop_all()

    # 2. (Re)create the database tables.
    db.create_all()

    # 3. Add test data to the db's.

    # 3a. Add a user

    prikey, pubkey = generateKeys()
    b64_pubkey = b2a(pubkey)

    user_dict = {
        'username':'warnold',
        'pubkey':b64_pubkey
    }

    wayne = User(**user_dict)
    db.session.add(wayne)
    db.session.commit()
    # print(wayne.id)
    
    # 3b. Create a game
    game = Game()
    db.session.add(game)
    db.session.commit()
    # print(game.id)

    # 3c. Add a player to the game
    player1 = Player(username=wayne.username, gameid=game.id)
    db.session.add(player1)
    db.session.commit()
    # print(player1.id)
    
    # TODO: add more players

    # TODO: player makes an update


    app.run(debug=True)