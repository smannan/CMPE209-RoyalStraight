import sqlite3
from uuid import uuid4
from Crypto.PublicKey import RSA
# this is the connection to the database, if Db does not exsist it will create.
conn = sqlite3.connect('house.db')
conn.execute("PRAGMA forign_keys =1")
# this is the object that you call to make changes to the DB
c = conn.cursor()

# wrap SQL in methods to make it easier to execute


def create_tables():
    # use the cursor object to call SQL
    # User text,FOREIGN KEY (User) REFERENCES users(UserID)))""")
    createUser = "CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, pubkey TEXT UNIQUE)"
    # createPlayer = "CREATE TABLE IF NOT EXISTS players(username TEXT, seskey TEXT PRIMARY KEY, balance INTEGER DEFAULT 500, FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE)"
    createPlayer = "CREATE TABLE IF NOT EXISTS players(username TEXT, seskey TEXT PRIMARY KEY, balance INTEGER DEFAULT 500, betBalance INTEGER DEFAULT 0, inRound INTEGER DEFAULT 1, inBet INTEGER DEFAULT 0, FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE)"
    createGame = "CREATE TABLE IF NOT EXISTS game(create INTEGER, bet INTEGER, pot INTEGER, FOREIGN KEY(player1) REFERENCES players(username), FOREIGN KEY(player2) REFERENCES players(username), FOREIGN KEY(player3) REFERENCES players(username), FOREIGN KEY(player4) REFERENCES players(username), FOREIGN KEY(card1) REFERENCES cards(card), FOREIGN KEY(card2) REFERENCES cards(card), FOREIGN KEY(card3) REFERENCES cards(card), FOREIGN KEY(card4) REFERENCES cards(card), FOREIGN KEY(card5) REFERENCES cards(card)"
    createCard = "CREATE TABLE IF NOT EXISTS cards(rank INTEGER, suit TEXT, card PRIMARY KEY (rank, suit)"
    
    c.execute(createUser)
    c.execute(createPlayer)
    c.execute(createCard)
    c.execute(createGame)
    
    

# Dynamically INSERT into tables
def insert_user(userName, pubKey):
    sql_insert_query = "INSERT INTO users VALUES(?,?)"
    c.execute(sql_insert_query, (userName, pubKey))
    conn.commit()


def insert_new_player(playerName, sesKey):
    sql_insert_query = "INSERT INTO players(username, sesKey) VALUES(?,?)"
    c.execute(sql_insert_query, (playerName, sesKey))
    conn.commit()

def insert_card(rank, suit):
    sql_insert_query = "INSERT INTO cards VALUES(?, ?)"
    c.execute(sql_insert_query, (rank, suit))

def insert_game(bet, pot):
    sql_insert_query = "INSERT INTO game(create, bet, pot) VALUES(1, ?, ?)"
    c.execute(sql_insert_query, (bet, pot))

def insert_player_game(player):
    sql_insert_query = ""
    player1 = None
    player2 = None
    player3 = None
    player4 = None
    
    if player1 == None:
        sql_insert_query = "INSERT INTO game(player1) VALUES(?)"
    elif player2 == None:
        sql_insert_query = "INSERT INTO game(player2) VALUES(?)"
    elif player3 == None:
        sql_insert_query = "INSERT INTO game(player3) VALUES(?)"
    elif player4 == None:
        sql_insert_query = "INSERT INTO game(player4) VALUES(?)"
    else:
        print("The game is full, you cannot be added")
        return

    c.execute(sql_select_query, player)

def insert_card_game(card):
    sql_insert_query = ""
    card1 = None
    card2 = None
    card3 = None
    card4 = None
    card5 = None
    
    if card1 == None:
        sql_insert_query = "INSERT INTO game(card1) VALUES(?)"
    elif card2 == None:
        sql_insert_query = "INSERT INTO game(card2) VALUES(?)"
    elif card3 == None:
        sql_insert_query = "INSERT INTO game(card3) VALUES(?)"
    elif card4 == None:
        sql_insert_query = "INSERT INTO game(card4) VALUES(?)"
    elif card5 == None:
        sql_insert_query = "INSERT INTO game(card5) VALUES(?)"
    else:
        print("This is an error as the cards are full!!!")

    c.execute(sql_insert_query, card)

# Dynamically UPDATE data in tables
def update_user_pubkey(userName, pubKey):
    sql_update_query = "UPDATE users SET pubkey = ? WHERE username = ?"
    c.execute(sql_update_query, (pubKey, userName))
    conn.commit()


#------------------------------player Updates------------------------------
def update_player_seskey(userName, sesKey):
    sql_update_query = "UPDATE players SET seskey = ? WHERE username = ?"
    c.execute(sql_update_query, (sesKey, userName))
    conn.commit()


def update_player_balance(userName, balance):
    sql_update_query = "UPDATE players SET balance = ? WHERE username = ?"
    try: 
        c.execute(sql_update_query, (balance, userName))
        conn.commit()
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))

def update_player_betBalance(userName, balance):
    sql_update_query = "UPDATE players SET betBalance = ? WHERE username = ?"
    try: 
        c.execute(sql_update_query, (balance, userName))
        conn.commit()
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))

def update_player_inBet(userName, inBet):
    dbVal = 0
    if inBet:
        dbVal = 1

    sql_update_query = "UPDATE players SET inBet = ? WHERE username = ?"
    try:
        c.execute(sql_update_query,(dbVal, userName))
        conn.commit()
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))

def update_player_inRound(userName, inRound):
    dbVal = 0
    if inRound:
        dbVal = 1

    sql_update_query = "UPDATE players SET inRound = ? WHERE username = ?"
    try:
        c.execute(sql_update_query,(dbVal, userName))
        conn.commit()
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))


#------------------------------game Updates------------------------------
def update_game_bet(bet):
    sql_update_query = "UPDATE game SET bet = ? WHERE create = 1"
    c.execute(sql_update_query, (bet, ))
    conn.commit()

def update_game_pot(pot):
    sql_update_query = "UPDATE game SET pot = ? WHERE create = 1"
    c.execute(sql_update_query, (pot, ))
    conn.commit()

# Dynamically DELETE data in tables


def delete_user(userName):
    sql_delete_query = "DELETE FROM users WHERE username = ?"
    c.execute(sql_delete_query, (userName,))
    conn.commit()


def delete_player(userName):
    sql_delete_query = "DELETE FROM players WHERE username = ?"
    c.execute(sql_delete_query, (userName,))
    conn.commit()

# Dynamically SELECT data from tables
#------------------Get from users-------------------
def getPublicKey(username):
    sql_select_query = "SELECT pubkey FROM users WHERE username = ?"
    try:
        c.execute(sql_select_query, (username,))
        result = c.fetchone()[0]
        return result
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))

#------------------Get from players-------------------
def getSesKey(username):
    sql_select_query = "SELECT seskey FROM players where username = ?"
    try:
        c.execute(sql_select_query, (username,))
        result = c.fetchone()[0]
        return result
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))
                


def getBalance(username):
    sql_select_query = "SELECT balance FROM players where username = ?"
    try:
        c.execute(sql_select_query, (username,))
        result = c.fetchone()[0]
        return result
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))

def get_betBalance(username):
    sql_select_query = "SELECT betBalance FROM players where username = ?"
    try:
        c.execute(sql_select_query, (username,))
        result = c.fetchone()[0]
        return result
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))


def get_inBet(username):
    sql_select_query = "SELECT inBet FROM players where username = ?"
    try:
        c.execute(sql_select_query, (username,))
        result = c.fetchone()[0]
        return result
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))

def get_inRound(username):
    sql_select_query = "SELECT inRound FROM players where username = ?"
    try:
        c.execute(sql_select_query, (username,))
        result = c.fetchone()[0]
        return result
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))


#------------------Get from game-------------------
def getBet():
    sql_select_query = "SELECT bet FROM game where create = 1"
    try:
        c.execute(sql_select_query)
        result = c.fetchone()[0]
        return result
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))

def getPot():
    sql_select_query = "SELECT pot FROM game where create = 1"
    try:
        c.execute(sql_select_query)
        result = c.fetchone()[0]
        return result
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))




# Database Operations
def inUsers(username):
    sql = "SELECT username FROM users"
    try:
        c.execute(sql)
        result = c.fetchall()
        for row in result:
            if username == row[0]:
                return true
            else:
                return false
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))


def users():
    sql = "SELECT * FROM users"
    try:
        c.execute(sql)
        result = c.fetchall()
        return result
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))
#-----------------------------------------GAME------------------------------------------------------

def inGamePlayer1():
    sql = "SELECT player1 from game where create = 1"
    try: 
        c.execute(sql)
        result = c.fetchone()
        return result
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))

# def inGamePlayer2():
# def inGamePlayer3():
# def inGamePlayer4():

def inGameCard1():    
    sql = "SELECT card1 from game where create = 1"
    try: 
        c.execute(sql)
        result = c.fetchone()
        return result
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))

# def inGameCard2():
# def inGameCard3():
# def inGameCard4():
# def inGameCard5():

#-----------------------------------------PLAYERS------------------------------------------------------
def players():
    sql = "SELECT * FROM players"
    try:
        c.execute(sql)
        result = c.fetchall()
        return result
    except sqlite3.DatabaseError as e:
        print("Error: %s" % (e.args[0]))


def startup():
    create_tables()
    players = ["ksbains", "wearnold", "smannan", "junlan66"]
    for player in players:
        insert_user(player, generateKeys())
    for player in players:
        insert_new_player(player, generateId())

    # player1 = "ksbains"
    # player2 = "wearnold"
    # player3 = "smannan"
    # player4 = "junlan66"

    # # random id of type uuid
    # rand_token1 = uuid4().urn
    # rand_token2 = uuid4().urn
    # rand_token3 = uuid4().urn
    # rand_token4 = uuid4().urn

    # # session Keys
    # sesKey1 = uuid4().urn
    # sesKey2 = uuid4().urn
    # sesKey3 = uuid4().urn
    # sesKey4 = uuid4().urn

    # insert into tables

    # insert_user(player1, generateId, generateKeys)
    # insert_new_player(player1, generateId)

    # insert_user(player2, generateId, generateKeys)
    # insert_new_player(player2, generateId)

    # insert_user(player3, generateId, generateKeys)
    # insert_new_player(player3, generateId)

    # insert_user(player4, generateId, generateKeys)
    # insert_new_player(player4, generateId)


def clearDB():
    sql = "DROP TABLE IF EXISTS players"
    sql2 = "DROP TABLE IF EXISTS users"
    c.execute(sql)
    c.execute(sql2)
    conn.commit()


def generateKeys():
    pri_key = RSA.generate(1024)
    pub_key = pri_key.publickey()
    return pub_key.exportKey('PEM')


def generateId():
    return uuid4().urn


# def main():
#     # this is the main function
#     print("This is the start of the script")
#     clearDB()
#     startup()
#     print("--------------------------This is the Users Table----------------------------")
#     print("-USERNAME--------------PUBLIC KEY-----------------------------------------")
#     users()
#     print("--------------------------This is the Players Table----------------------------")
#     print("-USERNAME--------------SESSION KEY-------------------------BALANCE-----")
#     players()
#     print("--------------------------This is the TEST----------------------------")
#     username = "ksbains"
#     delete_player(username)
#     delete_user("wearnold")
#     print("-USERNAME--------------PUBLIC KEY-----------------------------------------")
#     users()
#     print("-USERNAME--------------SESSION KEY-------------------------BALANCE-----")
#     players()


# # this is where the script starts and ends.
# main()
