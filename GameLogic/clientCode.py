import inquirer
import json
import requests
import sys
from time import sleep

sys.path.append("..")

from encryption import (
	generateKeys,
	rsa_decrypt,
	ASCII_to_binary as a2b,
	binary_to_ASCII as b2a
	)

# Needed for Windows support :(
try:
		import PyInquirer
except:
		pass

# Promt the player for username, get public key and send POST request
# set local username, balnace, session key

# PoST(sessionKey) -> player Table. 
# set the balance, betBalance...


# serverName = "https://go.warnold.dev/api/"
serverName = "http://localhost:5000/api/"

apiUserAdmin = serverName + "useradmin"
apiPlayer = serverName + "player"
apiUser = serverName + "user"
apiGame = serverName + "game"
apiUpdate = serverName + "update"

def getGame():
	result = requests.get(apiGame + '/1')
	# print(result)
	gameData = result.json()
	return json.loads(gameData["data"])

GAME_EX = {
  "cards": None, 
  "game": {
	"data": "{\"pot\": 110, \"bet\": 30, \"comCards\": [\"J\\u2660\", \"9\\u2660\", \"7\\u2666\"], \"players\": [\"wearnold\", \"ksbains\", \"junlan66\", \"smannan\"], \"playerTurn\": \"wearnold\"}", 
	"id": 1
  }, 
  "gameid": 1, 
  "hands": None, 
  "id": 1, 
  "user_token": "uw469OnyKfqY9OHSLSTWEA==\n", 
  "username": "wearnold"
}

playerMove = {}



# this is the code to prompt the user if it is thier turn. 
def startScript():
	query = "Welcome to Royal Straight Casino! Would you like to play some poker?"

	questions = {
		'type':'list',
		'choices' : ['yes', 'exit'],
		'message':query,
		'name':'begin'
	}
	answer = PyInquirer.prompt(questions)

	if answer["begin"] == 'yes':
		username, sessionKey = userNamePrompt()
	else:
		print("Goodbye!")
		sys.exit()
	
	return username, sessionKey

def userNamePrompt():
	query = "please enter a username to be used in the game"
	questions = {
		'type': 'input',
		"message": query,
		"name": 'username'
	}
	answer = PyInquirer.prompt(questions)
	username = answer["username"]
	if not requests.get(apiUser + '/' + username).ok:
		print('Registering new user')
	else:
		print("Looks like you already have a username. Continuing")

	#generate keys, store private key and send over public key. 


	try:
		with open('pubkey_%s' % username, 'rb') as f:
			pubkey = f.read()
			b64_pubkey = b2a(pubkey)
		with open('prikey_%s' % username, 'rb') as f:
			prikey = f.read()
			b64_p = b2a(pubkey)
	except:
		prikey, pubkey = generateKeys()
		with open('prikey_%s' % username, 'wb') as f:
			f.write(prikey)
		with open('pubkey_%s' % username, 'wb') as f:
			f.write(pubkey)
		b64_pubkey = b2a(pubkey)
	user_dict = {
		'username':username,
		'pubkey':b64_pubkey
	}

	# POST username
	try:
		user_obj = requests.post(apiUser, json=user_dict).json()
		enc_key = user_obj['enc_token']
		print(enc_key)
		sessionKey = rsa_decrypt(enc_key, prikey)
		print(sessionKey)
	except:
		# Just for testing
		sessionKey = 'whatever'
	# GET game, probably game=1
	game_id = 1

	# POST player
	player_dict = {
		'username':username,
		'gameid':game_id
	}
	requests.post(apiPlayer, json=player_dict)

	#then also se the balance, sessio key, and ammount
	balance = 500
	sessionKey = ""
	
	data = getGame()
	print("The pot is: %d" % data['pot'])
	print("The bet is: %d" % data['bet'])
	
	print("The comCards are: ")
	print(data['comCards'])
	
	print("The players are: ")
	print(data['players'])

	print("It is " + data["playerTurn"] + "'s Turn")
	
	return username, sessionKey


def getTurn():
	data = getGame()
	
	#set local from DB?
	return data['playerTurn']

def postTurn(data):
	result = requests.post(apiUpdate, json=data)
	print('Post update result:')
	print(result)
	print('Post update response:')
	print(result.json())

	#do some logic here to post turn.
	#post(DBJSON object?)
	# POST api/username? 
	return


def runner(username, sessionKey):
	# instead of true, should be as long as game is active
	while True:
		turn = ''
		# needs to print whose turn it is and is interactig with the game server
		while turn != username:
			sleep(1)
			turn = getTurn()
			print("It's %s's turn" % turn)
			# sleep for a bit, and then keep checking if it is their turn 
			
		
		# this is the code to prompt the user if it is thier turn. 
		query = "Hey there " + username + " what would you like to do?"
		try:
			questions = [inquirer.List('options', message = query, choices = ['bet', 'check', 'raise', 'fold', 'call'],),]
			answer = inquirer.prompt(questions)
		except:
			questions = {
				'type':'list',
				'choices' : ['bet', 'check', 'raise', 'fold', 'call'],
				'message':query,
				'name':'options'
			}
			answer = PyInquirer.prompt(questions)

		if answer["options"] == "bet":
			print("bet")
			#do game logic
		elif answer["options"] == "check":
			print("check")
			#do game logic
		elif answer["options"] == "raise":
			print("raise")
			#do game logic
			#should be same to bet
		elif answer["options"] == "call":
			print("call")
			#do some game logic, should be same as check
		elif answer["options"] == "fold":
			print("fold")
			#do some game logic
			#set the inROund to False
		else:
			print("this is an error!!!")
		
		action = answer["options"]
		if action in ('bet', 'raise'):
			amount = 50
		else:
			amount = 0

		print('Betting %d' % amount)
		
		data = {
			'username':username,
			'amount':amount,
			'action':action,
			'token':sessionKey
		}

		postTurn(data)







def main():
	username, sessionKey = startScript()
	print('vars')
	print(username)
	print(sessionKey)
	runner(username, sessionKey)

main()