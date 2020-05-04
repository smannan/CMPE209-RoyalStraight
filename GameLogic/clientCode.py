import inquirer
import json
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

game = {}

playerMove = {}



def apiCall():
	# game = json.loads()
	GET api/username?

def getTurn():
	#json.p
	return "DB turn"
	#set local from DB?

def postTurn():
	#do some logic here to post turn.
	#post(DBJSON object?)
	POST api/username? 


# instead of true, should be as long as game is active
while True:
	turn = getTurn()
	# needs to print whose turn it is and is interactig with the game server
	while turn != username:
		# sleep for a bit, and then keep checking if it is their turn 
		sleep(1)


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
        #do game logic
    elif answer["options"] == "check":
        #do game logic
    elif answer["options"] == "raise":
	    #do game logic
	    #should be same to bet
	elif answer["options"] == "call":
		#do some game logic, should be same as check
	elif answer["options"] == "fold":
		#do some game logic
		#set the inROund to False
	else:
		print("this is an error!!!")
	
	posTturn()








	

