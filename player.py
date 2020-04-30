# from game import Game
import inquirer
from poker import *

class Player:
        def __init__(self, username, balance, game):
                self.username = username
                self.hand = []
                self.balance = balance
                self.game = game
                self.inRound = True
                self.inBet = False
                self.betBalance = 0
                self.finalHand = []

        
        def __str__(self):
                if self.hand == []:
                        return self.username + " has a balance of " + str(self.balance) + " and empty hand"
                else:
                        return self.username + " has a balance of " + str(self.balance) + " AND hand of " + str(self.hand[0]) + " " + str(self.hand[1]) +" AND a betBalance of " + str(self.getBetBalance()) 
        def getUsername(self):
                return self.username

        def getHand(self):
                return self.hand

        def setHand(self, hand):
                self.hand = hand

        def getFinalHand(self):
                return self.finalHand

        def setFinalHand(self, hand):
                self.finalHand = hand
        
        def getBalance(self):
                return self.balance

        def setBalance(self, balance):
                self.balance = balance

        def getInRound(self):
                return self.inRound

        def setInRound(self, inRound):
                self.inRound = inRound
        
        def getInBet(self):
                return self.inBet

        def setInBet(self, inBet):
                self.inBet = inBet

        def getBetBalance(self):
                return self.betBalance

        def setBetBalance(self, Bet):
                self.betBalance = Bet

        def leaveGame(self):
                self.Game.removePlayer(self.username)
        
        def mainMenu(self):
                if self.inRound:
                        query = "Hey there " + self.username + " what would you like to do?"
                        questions = [inquirer.List('options', message = query, choices = ['Leave Game', 'Fold', 'Join Round'],),]
                        answer = inquirer.prompt(questions)

                        if answer["options"] == "Join Round":
                                print(self.username + ", you have been added to this round")
                                #do game logic
                                self.roundMenu()
                        elif answer["options"] == "Fold":
                                self.fold()
                        else: 
                                #player leaves game
                                self.inRound = False
                                self.game.removePlayer(self.username)
                        
                
        def roundMenu(self):
                gameInfo = "The current pot is: " + str(self.game.getPot()) + " the current bet is: " + str(self.game.getBet()) + " your cards are: " + str(self.hand[0]) + " " + str(self.hand[1]) 
                questions = [inquirer.List('options', message = gameInfo, choices = ['Bet/Raise', 'Check/Match', 'Fold'],),]
                answer = inquirer.prompt(questions)

                if answer["options"] == "Bet/Raise":
                        self.bet()
                elif answer["options"] == "Check/Match":
                        self.check()
                else: 
                        self.fold()

        def bet(self):
                query = "How much would you like to bet? bet value needs to be greater than current bet of " + str(self.game.getBet())
                question = [inquirer.Text('bet', query)]
                answer = inquirer.prompt(question)
                bet = int(answer["bet"])
                #do some game logic here
                playerDiff = bet-self.getBetBalance()
                if bet > self.game.getBet() and self.balance >= playerDiff:
                        self.balance = self.balance - playerDiff
                        self.game.setBet(bet)
                        self.setBetBalance(bet)
                        self.game.setPot(self.game.getPot() + playerDiff)
                        self.game.betFalse()
                        self.setInBet(True)
                else:
                        print("Your bet is lower than current Bet, Up the ante!! Or you have not more funds:(  ")
                        self.bet(self)

        def check(self):
                #do some game logic here
                bet = self.game.getBet()
                playerDiff = bet - self.getBetBalance()
                if self.balance >= playerDiff:
                        self.balance = self.balance - playerDiff
                        self.setBetBalance(bet)
                        #DB call 
                        self.game.setPot(self.game.getPot() + playerDiff)
                        self.setInBet(True)
                else:
                        print("Sorry! You don't have enough money to check this round, good luck next round")
                        self.setInRound(False)

        def fold(self):
                #do some game logic here
                self.setInRound(False)
                print(self.username  + ", you have folded " + ", see ya next round!")


                







        