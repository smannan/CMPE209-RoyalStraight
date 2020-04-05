import sqlite3

#this is the connection to the database, if Db does not exsist it will create. 
conn = sqlite3.connect('house.db')

#this is the object that you call to make changes to the DB
c = conn.cursor()

#wrap SQL in methods to make it easier to execute
def create_table():
	#use the cursor object to call SQL
	c.execute("CREATE TABLE players(name VARCHAR, key Text)")

def enter_data():
	c.execute("INSERT INTO players VALUES('Joe','58snkg220983')")

def enter_dynamic_data():
	pName = input("What is the player name?")
	key = input("What key level?")
	c.execute("INSERT INTO players VALUES(?,?)", (pName,key))
	conn.commit()

def enter_dynamic_data_param(pName,, key):
	c.execute("INSERT INTO players VALUES(?,?)", (pName,key))
	conn.commit()

def read_from_database():
	sql= "SELECT * FROM players"
	for row in c.execute(sql):
		print(row)


read_from_database()

#this will close the connection. 
conn.close()