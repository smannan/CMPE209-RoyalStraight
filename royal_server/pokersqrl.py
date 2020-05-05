import sys
import binascii
import random
import flask
import flask_sqlalchemy
import flask_restless
from sqlalchemy.orm import validates, relationship
from poker import Card

sys.path.append("..")
from encryption import (
    generateKeys,
    generateSessionKey,
    generateB64SessionKey,
    rsa_encrypt,
    )
from encryption import ASCII_to_binary as a2b
from encryption import binary_to_ASCII as b2a

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
# app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poker.db'
# Clears a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    "pot":0,
}

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.Unicode, primary_key=True)
    pubkey = db.Column(db.String, unique=True)
    token = db.Column(db.Unicode, default=generateB64SessionKey)
    enc_token = db.Column(db.Unicode, default=encrypt_token)

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, default=gs_default)
    playerz = relationship("Player", back_populates='game',
                        cascade="all, delete, delete-orphan")

    # def __init__(self, data=gs_default):
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
        # self.data = data
    
    def addPlayer(self, player):
        self.players.append(player)
        db.session.add(player1)
        db.session.commit() 

def populate_token(context):
    username = context.get_current_parameters()['username']
    row = db.session.query(User).filter_by(username=username).first()
    key = row.token
    return key

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, db.ForeignKey('user.username'))
    gameid = db.Column(db.Integer, db.ForeignKey('game.id'))
    # Player's private cards represented as a JSON value
    cards = db.Column(db.JSON)
    hands = db.Column(db.JSON)
    user_token = db.Column(db.Unicode, default=populate_token)
    game = relationship("Game", back_populates="playerz")

class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode)
    betround = db.Column(db.Integer, default=0)
    action = db.Column(db.Unicode)
    amount = db.Column(db.Integer, default=0)
    token = db.Column(db.Unicode)
    user_token = db.Column(db.Unicode, default=populate_token)

    # TODO try validating user token with second session
    

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
manager.create_api(User, methods=['GET', 'POST'], collection_name='useradmin')
# TODO: Remove POST, API doesn't need to expose game post, this is just for testing.
manager.create_api(Game, methods=['GET', 'POST'])
manager.create_api(Update, methods=['GET','POST'])


manager.create_api(Player, methods=['GET', 'POST'])
# manager.create_api(Update, methods=['POST'], exclude_columns=['token'])

# start the flask loop
if __name__ == "__main__":

    # Run a bunch of commands if this is called as __main__

    # 1. Cleanup database
    # db.drop_all()

    # 2. (Re)create the database tables.
    # db.create_all()

    # 3. Add test data to the db's.

    # 3a. Add users
    usernames = ['wearnold','ksbains','junlan66','smannan']
    users = []
    for un in usernames:
        # Try and read the file for speed
        try:
            with open('pubkey_%s' % un, 'rb') as f:
                pubkey = f.read()
                b64_pubkey = b2a(pubkey)
        except:
            prikey, pubkey = generateKeys()
            with open('prikey_%s' % un, 'wb') as f:
                f.write(prikey)
            with open('pubkey_%s' % un, 'wb') as f:
                f.write(pubkey)
            b64_pubkey = b2a(pubkey)
        user_dict = {
            'username':un,
            'pubkey':b64_pubkey
        }
        user = User(**user_dict)
        db.session.add(user)
        users.append(user)
    db.session.commit()
            
    # 3b. Create a game
    game = Game()
    db.session.add(game)
    db.session.commit()
    # print(game.data)
    # game.data['pot'] = 50

    # Just an example of a query
    our_game = db.session.query(Game).filter_by(id='1').first()

    # 3c. Add a player to the game
    for user in users:
        player = Player(username=user.username, gameid=game.id)
        db.session.add(player)
    db.session.commit()
    print(game.playerz)
   
    # TODO: player makes an update


    app.run(debug=True)