import flask_restless
from poker_classes import (
    app,
    db,
    User,
    Game,
    Player,
    Update,
)

# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename>
manager.create_api(User, methods=['GET', 'POST'], exclude_columns=['token'])
# Only for testing
# manager.create_api(User, methods=['GET'], collection_name='useradmin')
manager.create_api(Game, methods=['GET'])
manager.create_api(Update, methods=['POST'])


manager.create_api(Player, methods=['GET'], exclude_columns=['user_token'])
manager.create_api(Player, methods=['POST'], exclude_columns=['balance'])
manager.create_api(Player, methods=['GET'], collection_name='playeradmin')

# start the flask loop
if __name__ == "__main__":
    # TODO: player makes an update


    app.run(debug=True)