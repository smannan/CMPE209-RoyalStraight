import secrets
import flask
import flask_sqlalchemy
import flask_restless
from sqlalchemy.orm import validates

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
# app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poker.db'
db = flask_sqlalchemy.SQLAlchemy(app)


def encrypt_token(context):
    token = context.get_current_parameters()['token']
    pubkey = context.get_current_parameters()['pubkey']
    # TODO: pseudocode, should take the RSA pubkey and encrypt the token.
    # return rsa_encrypt(token, pubkey)
    return token+pubkey

gs_default = {
    "bet":0,
    "pool":0,
}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True)
    pubkey = db.Column(db.Unicode, unique=True)
    token = db.Column(db.Unicode, default=secrets.token_hex(16))
    enc_token = db.Column(db.Unicode, default=encrypt_token)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, default=gs_default)

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
# manager.create_api(Update, methods=['POST'], exclude_columns=['token'])

# start the flask loop
if __name__ == "__main__":

    # Create the database tables.
    db.create_all()

    app.run(debug=True)