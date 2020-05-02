import sqlite3
import os,binascii
import json

USER = 'warnold'
PUBKEY = '1234567890abcdef1234567890'
AUTH_TOKEN = binascii.b2a_hex(os.urandom(15))

#############################################
# Borrowed from SQLite.py and modified
#############################################
def create_tables(conn):
    # use the cursor object to call SQL
    # User text,FOREIGN KEY (User) REFERENCES users(UserID)))""")
    createUser = '''CREATE TABLE IF NOT EXISTS users(username VARCHAR PRIMARY KEY,
        pubkey TEXT UNIQUE)'''
    # Thought it might be good to 
    createPlayer = '''CREATE TABLE IF NOT EXISTS players(username VARCHAR, 
        seskey TEXT PRIMARY KEY, 
        balance INTEGER DEFAULT 500, 
        FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE)'''
    c = conn.cursor()
    c.execute(createUser)
    c.execute(createPlayer)
def insert_user(conn, userName, pubKey):
    sql_insert_query = "INSERT INTO users VALUES(?,?)"
    c = conn.cursor()
    c.execute(sql_insert_query, (userName, pubKey))
    conn.commit()
def insert_new_player(conn, playerName, sesKey):
    sql_insert_query = "INSERT INTO players VALUES(?,?, 500)"
    c = conn.cursor()
    c.execute(sql_insert_query, (playerName, sesKey))
    conn.commit()
#############################################


def create_jgame(conn):
    '''
    Creates a table for game with json data format
    '''
    createGame = '''CREATE TABLE IF NOT EXISTS jgames(
        gameid INTEGER PRIMARY KEY,
        data json
    )'''
    c = conn.cursor()
    c.execute(createGame)
    conn.commit()

def create_json_game(conn, data):
    '''
    Creates an instance of a game
    '''
    c = conn.cursor()
    # Have to embed it in a single item tuple
    c.execute("INSERT INTO jgames (data) VALUES (?)",(data,))
    conn.commit()

    # Returns the ID of the game created
    return c.lastrowid

def update_json_game(conn, gameid, data):
    '''
    Modifies the json blob for the game state
    '''
    c = conn.cursor()
    # Have to embed it in a single item tuple
    c.execute("UPDATE jgames set data=? where gameid=?",(data,gameid,))
    conn.commit()


def get_json_game_state(conn, gameid):
    '''
    Gets the current state of the game
    '''
    select = 'SELECT data FROM jgames WHERE gameid==?'
    c = conn.cursor()
    c.execute(select,(gameid,))
    json_blob = c.fetchone()[0]

    return json_blob

if __name__ == "__main__":
    # Setup
    conn = sqlite3.connect('poker.db')
    conn.execute("PRAGMA foreign_keys =1")

    # Note: passing the conn as an argument as good practice
    # This way other modules can import the functions.

    # Create the game table
    create_jgame(conn)

    # Create the other tables (copied from SQLite.py)
    create_tables(conn)
            
    # POST /api/user/{username}
    # Create a user
    # TODO: Just add an auth_token to the user table. We can rotate it
    #   after every game.
    insert_user(conn, USER, PUBKEY)

    # GET /api/user/{username}
    # Returns auth_token, encrypted with pubkey.

    # POST /api/games
    #   Required:
    #     userid
    #     auth_token
    # 
    # 1. Adds a player to table
    # 2. Returns status code 201 OK, 401 table is full.
    # TODO: Not sure if auth_token needs to be in this table.
    #   If it does, SELECT it from the users table.
    insert_new_player(conn, USER, AUTH_TOKEN)

    # Once players are in, two things happen.
    # 1. Game logic starts progressing (once 5 players have joined).
    # 2. Clients start GET requests for state.

    # GET /api/games
    #
    # Once a user has joined the game, they'll start performing
    # regular GET requests for state of game. They'll get an
    # indicator when it's their turn.

    # Create a game with initial game state
    #   we can fill in the other attributes later

    # json.dumps(obj) serializes the object for insert.
    #   We can move this into the get/insert functions.
    game_state = json.dumps({
        'pot':0,
        'bet':0,
        'cards':[]
    })

    game_id = create_json_game(conn, game_state)
    
    # Just demonstrating how to pull the state back
    #   from the databse.
    same_state = get_json_game_state(conn, game_id)
    print('Original state:')
    print(json.loads(same_state))

    # Now we'll update the game state.
    new_game_state = json.dumps({
        'pot':0,
        'bet':0,
        'cards':['Ks','Qd','3h']
    })
    update_json_game(conn, game_id, new_game_state)

    # Demonstrating that the state has changed.
    new_state = get_json_game_state(conn, game_id)
    print('New State:')
    print(json.loads(new_state))

    # Cleanup
    c = conn.cursor()
    for table in ["users", "players", "games", "jgames"]:
        c.execute('DROP TABLE IF EXISTS %s' % table)
    
    conn.commit()

    # TODO: At end of game, rotate auth tokens for all players.