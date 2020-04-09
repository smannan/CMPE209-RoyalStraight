import sqlite3
from uuid import uuid4
#this is the connection to the database, if Db does not exsist it will create. 
conn = sqlite3.connect('house.db')
conn.execute("PRAGMA forign_keys =1")
#this is the object that you call to make changes to the DB
c = conn.cursor()

#wrap SQL in methods to make it easier to execute
def create_tables():
	#use the cursor object to call SQL
	#User text,FOREIGN KEY (User) REFERENCES users(UserID)))""")
	createUser = "CREATE TABLE IF NOT EXISTS users(username VARCHAR PRIMARY KEY, pubkey TEXT UNIQUE)"
	createPlayer = "CREATE TABLE IF NOT EXISTS players(username VARCHAR, seskey TEXT PRIMARY KEY, balance INTEGER DEFAULT 500, FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE)"
	c.execute(createUser)
	c.execute(createPlayer)

#Dynamically INSERT into tables
def insert_user(userName, pubKey):
	sql_insert_query = "INSERT INTO users VALUES(?,?)"
	c.execute(sql_insert_query, (userName,pubKey))
	conn.commit()

def insert_new_player(playerName, sesKey):
	sql_insert_query = "INSERT INTO players VALUES(?,?, 500)"
	c.execute(sql_insert_query, (playerName, sesKey))
	conn.commit()

def insert_custom_player(playerName, sesKey,  balance):
	sql_insert_query = "INSERT INTO players VALUES(?,?,?)"
	c.execute(sql_insert_query, (playerName, sesKey, balance))
	conn.commit()


#Dynamically UPDATE data in tables
def update_user_pubkey(userName, pubKey):
	sql_update_query = "UPDATE users SET pubkey = ? WHERE username = ?"
	c.execute(sql_update_query, (pubKey, userName))
	conn.commit()

def update_player_seskey(userName, sesKey):
	sql_update_query = "UPDATE players SET seskey = ? WHERE username = ?"
	c.execute(sql_update_query, (sesKey, userName))
	conn.commit()

def update_player_balance(userName, balance):
	sql_update_query = "UPDATE players SET balance = ? WHERE username = ?"
	c.execute(sql_update_query, (balance, userName))
	conn.commit()

#Dynamically DELETE data in tables
def delete_user(userName):
	sql_delete_query = "DELETE FROM users WHERE username = ?"
	c.execute(sql_delete_query, (userName,))
	conn.commit()

def delete_player(userName):
	sql_delete_query = "DELETE FROM players WHERE username = ?"
	c.execute(sql_delete_query, (userName,))
	conn.commit()


#Dynamically SELECT data from tables
def getPublicKey(username):
	sql_select_query= "SELECT pubkey FROM users WHERE username = ?"	
	try:
		c.execute(sql_select_query, (username,))
		result = c.fetchone()[0]
		return result
	except sqlite3.DatabaseError as e:
		print("Error: %s" % (e.args[0]))


def getSesKey(username):
	sql_select_query= "SELECT seskey FROM players where username = ?"
	try:
		c.execute(sql_select_query, (username,))
		result = c.fetchone()[0]
		return result
	except sqlite3.DatabaseError as e:
		print("Error: %s" % (e.args[0]))


def getBalance(username):
	sql_select_query= "SELECT balance FROM players where username = ?"
	try:
		c.execute(sql_select_query, (username,))
		result = c.fetchone()[0]
		return result
	except sqlite3.DatabaseError as e:
		print("Error: %s" % (e.args[0]))


#Database Operations
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
		for row in result:
			print(row)
	except sqlite3.DatabaseError as e:
		print("Error: %s" % (e.args[0]))


def players():
	sql = "SELECT * FROM players"
	try:
		c.execute(sql)
		result = c.fetchall()
		for row in result:
			print(row)
	except sqlite3.DatabaseError as e:
		print("Error: %s" % (e.args[0]))

def startup():
	create_tables()
	player1 = "ksbains"
	player2 = "wearnold"
	player3 = "smannan"
	player4 = "junlan66"
	
	#random id of type uuid
	rand_token1 = uuid4().urn
	rand_token2 = uuid4().urn
	rand_token3 = uuid4().urn
	rand_token4 = uuid4().urn
	
	#session Keys
	sesKey1 = uuid4().urn
	sesKey2 = uuid4().urn
	sesKey3 = uuid4().urn
	sesKey4 = uuid4().urn
	
	#insert into tables
	insert_user(player1, rand_token1)
	insert_new_player(player1, sesKey1)

	insert_user(player2, rand_token2)
	insert_new_player(player2,sesKey2)

	insert_user(player3, rand_token3)
	insert_new_player(player3,sesKey3)

	insert_user(player4, rand_token4)
	insert_new_player(player4,sesKey4)

def clearDB():
	sql = "DROP TABLE IF EXISTS players"
	sql2 = "DROP TABLE IF EXISTS users"
	c.execute(sql)
	c.execute(sql2)
	conn.commit()

def main():
	#this is the main function
	print("This is the start of the script")
	#clearDB()
	#startup()
	print("--------------------------This is the Users Table----------------------------")
	print("-USERNAME--------------PUBLIC KEY-----------------------------------------")
	users()
	print("--------------------------This is the Players Table----------------------------")
	print("-USERNAME--------------SESSION KEY-------------------------BALANCE-----")
	players()
	print("--------------------------This is the TEST----------------------------")
	username = "ksbains"
	delete_player(username)
	delete_user("wearnold")
	print("-USERNAME--------------PUBLIC KEY-----------------------------------------")
	users()
	print("-USERNAME--------------SESSION KEY-------------------------BALANCE-----")
	players()

#this is where the script starts and ends. 
main()

# clearDB()
# startup()


