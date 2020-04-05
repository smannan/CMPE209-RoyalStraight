import mysql.connector
  
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="",
)
cursor = mydb.cursor()

def read_from_database():
	sql = "SELECT * FROM department"
	for row in cursor.execute(sql):
		print(row)

def insert(value):
	sql = "INSERT INTO table VALUES(%s)"
	cursor.execute(sql, (value))
	mydb.commit()




