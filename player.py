import game
import inquirer
from poker import *

class Player:
        def __init__(username, balance, game):
                self.username = username
                self.hand = []
                self.balance = balance
                self.game = game
        
        def getUsername(self):
                return self.username

        def getHand(self):
                return self.hand

        def setHand(self, hand):
                self.hand = hand
        
        def getBalance(self):
                return self.balance

        def setBalance(self, balance):
                self.balance = balance
        def leaveGame(self):
                self.Game.removePlayer(self.username)
        
        def mainMenu():
                query = ""
                questions = [inquirer.List('options', message = query, choices = ['Leave Game', 'Join Round'],),]
                answer = inquirer.prompt(questions)

                if answer["options"] == "Join Game":
                        print(self.username ", you have been added to this round")
                        #do game logic
                else: 
                        #player leaves game
                        self.game.removePlayer(self.username)
                        
                
        def roundMenu(self):
                gameInfo = "The current pot is: " + str(Player.game.getPot()) + "the current bet is: " + str(Player.game.getBet()) + "your cards are: "
                print(self.hand[0])
                print(self.hand[1]) 

                questions = [inquirer.List('options', message = query, choices = ['Bet', 'Check', 'Fold'],),]
                answer = inquirer.prompt(questions)

                if answer["options"] == "Bet":
                        Player.bet(self)
                elif answer["options"] == "Check":
                        Player.check(self)
                else: 
                        Player.fold(self)

        def bet(self):
                query = "How much would you like to bet? bet value needs to be greater than current bet: " + Player.game.bet()
                question = [inquirer.Text('bet', query)]
                answer = inquirer.prompt(question)

                #do some game logic here

        def check(self):
                #do some game logic here
                print(" you have checked " + self.username)

        def fold(self):
                #do some game logic here
                print(" you have folded " + self.username ", see ya next round!")
                mainMenu()

                







        