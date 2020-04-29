from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='0.1', title='Poker API',
    description='Poker API for class project',
    doc='/api/docs/'
)

# Puts the whole thing under /api/
ns = api.namespace('api', description='Top-level API')


# Defines the format of user that gets output in calls
# { "id": username, "pubkey": pubkey}
user = api.model('User', {
    "id": fields.String(required=True, description="User's unique username"),
    "pubkey" : fields.String(required=True, description="User's pubkey")
})

# Defines the players playing in game
# { "id": username, "seskey": seskey}
player = api.model('Player', {
    "id": fields.String(required=True, description="Player's unique username"),
    "seskey" : fields.String(required=True, description="Player's sessionkey"),
    "balance" : fields.String(required=True, description="Player's Balance")
})

# Just a starter to play with how to define game state
game_state = {}
game_state['whose_turn'] = fields.String()
game_state['card_pool'] = fields.List()
game_state['current_bet'] = fields.String()

game = api.model('Game', {
    "id": fields.String(require=True, description="Unique Game ID, or Table Number"),
    "playerList": fields.List(description="List of player IDs at the table"),
    "gameState": fields.Nested(game_state)
})

# Defines the data object
# TODO: Calls to database would happen here, instead of having a "users" object
class UserDAO(object):
    def __init__(self):
        self.users=[]

    def get(self, id):
        for user in self.users:
            if user['id'] == id:
                return user
        api.abort(404, "User {} doesn't exist".format(id))

    def create(self, data):
        if data['id'] not in self.users:
            user = {}
            user['id']=data['id']
            user['pubkey']=data['pubkey']
            self.users.append(user)
            return user
        else:
            api.abort(401, "User {} already exists.".format(data['id']))

    def update(self, id, data):
        user = self.get(id)
        user.update(data)
        return user

    def delete(self, id):
        user = self.get(id)
        self.users.remove(user)


DAO = UserDAO()
DAO.create({
    'id': 'warnold22',
    'pubkey':'1234567890abcdef1234567890'
})
DAO.create({
    'id': 'warnold23',
    'pubkey':'1234567890abcdef1234567891'
})
DAO.create({
    'id': 'warnold23',
    'pubkey':'1234567890abcdef1234567892'
})

# TODO: Validate user's public key before "sitting" at the table
class PlayerDAO(object):
    def __init__(self):
        pass

    def get(self, id):
        for user in self.users:
            if user['id'] == id:
                return user
        api.abort(404, "User {} doesn't exist".format(id))

class GameDAO(object):
    
    def __init__(self):
        self.games=[]
    

    def get(self, id):
        for game in self.games:
            if game['id'] == id:
                return game
        api.abort(404, "User {} doesn't exist".format(id))

    def create(self, data):
        if data['id'] not in self.games:
            game = {}
            game['id']=data['id']
            game['pubkey']=data['pubkey']
            self.games.append(game)
            return game
        else:
            api.abort(401, "User {} already exists.".format(data['id']))

    def update(self, id, data):
        game = self.get(id)
        game.update(data)
        return game

    def delete(self, id):
        game = self.get(id)
        self.games.remove(game)

# /api/users/
@ns.route('/users/')
class UserList(Resource):
    '''Shows a list of all users, and lets you POST to add new users'''
    @ns.doc('list_users')
    @ns.marshal_list_with(user)
    def get(self):
        '''List all users'''
        return DAO.users

    @ns.doc('create_user')
    @ns.expect(user)
    @ns.marshal_with(user, code=201)
    def post(self):
        '''Create a new user'''
        return DAO.create(api.payload), 201


@ns.route('/user/<id>')
@ns.response(404, 'User not found')
@ns.param('id', 'The user identifier')
class User(Resource):
    '''Show a single user item and lets you delete them'''
    @ns.doc('get_user')
    @ns.marshal_with(user)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    def delete(self, id):
        '''Delete a user given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(user)
    @ns.marshal_with(user)
    def put(self, id):
        '''Update a user given its identifier'''
        return DAO.update(id, api.payload)

if __name__ == '__main__':
    app.run(debug=True)
