import inquirer
import json
import sys
# Needed for Windows support :(
try:
        import PyInquirer
except:
        pass

# Promt the player for username, get public key and send POST request
# set local username, balnace, session key

# PoST(sessionKey) -> player Table. 
# set the balance, betBalance...

username = ""
amount = 50
action = ""
sessionkey = ""

apiUserAdmin = "https://go.warnold.dev/api/useradmin"
apiPlayer = "https://go.warnold.dev/api/player "
apiUser = "https://go.warnold.dev/api/user"
apiGame = "https://go.warnold.dev/api/game "
apiUpdate = "https://go.warnold.dev/api/update"

game = {
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
	
	try:
	    questions = [inquirer.List('begin', message = query, choices = ['yes', 'exit'],),]
	    answer = inquirer.prompt(questions)
	except:
	    questions = {
	        'type':'list',
	        'choices' : ['yes', 'exit'],
	        'message':query,
	        'name':'begin'
		}
	    answer = PyInquirer.prompt(questions)

	if answer["begin"] == 'yes':
		userNamePrompt()
	else:
		sys.exit()

def userNamePrompt():
	query = "please enter a username to be used in the game"

	try:
		questions = [inquirer.Text('username', message=query)]
		answer = inquirer.prompt(questions)
	except:
		questions = {
			'type': 'input',
			"message": query,
			"name": 'username'
		}
		answer = PyInquirer.prompt(questions)

	username = answer["username"]
	#generate keys, store private key and send over public key. 
	
	#then also se the balance, sessio key, and ammount
	balance = 500
	sessionKey = ""
	# print(answer["username"])
	# print(list(game["game"].values()))
	# print(list(game["game"].keys()))
	data = game["game"]
	print(data["data"])
	print("The pot is: " + str(getInfo(game["game"], "pot")))
	print("The bet is: " + str(getInfo(game["game"], "bet")))
	
	print("The comCards are: ")
	print(getInfo(game["game"], "comCards"))
	
	print("The players are: ")
	print(getInfo(game["game"], "players"))

	print("It is " + getInfo(game["game"], "playerTurn") + "'s Turn")
	
	







def getInfo(GameDictionary, key):
	JSONData = json.loads(GameDictionary["data"])

	if key == "comCards":
		return JSONData["comCards"]
	elif key == "players":
		return JSONData["players"]
	else:
		return JSONData[key]

def apiCall():
	# game = json.loads()
	# GET api/username?
	return


def getTurn():
	#json.p
	#set local from DB?
	return "DB turn"

def postTurn():
	#do some logic here to post turn.
	#post(DBJSON object?)
	# POST api/username? 
	return


def runner():
	# instead of true, should be as long as game is active
	while True:
		turn = getTurn()
		# needs to print whose turn it is and is interactig with the game server
		while turn != username:
			sleep(1)
			# sleep for a bit, and then keep checking if it is their turn 
			
		
		# this is the code to prompt the user if it is thier turn. 
		query = "Hey there " + self.username + " what would you like to do?"
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
		
		posTturn()







def main():
	startScript()
	

main()