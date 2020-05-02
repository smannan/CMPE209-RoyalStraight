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
                #There should be no SQL here because the username is uses as teh Primary key, so should just get the local copy of the username and then use it for SQL calls

        def getHand(self):
                return self.hand
                #!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
                #handDB = PlayerDB.get_hand(self.getUsername(PK))
                #hand = PlayerDB.string_to_hand(handDB)
                #return hand

        def setHand(self, hand):
                self.hand = hand
                #!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
                #handDB = PlayerDB.hand_to_string(hand)
                #PlayerDB.set_hand(self.getUsername(PK), handDB)

        def getFinalHand(self):
                return self.finalHand
                #!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
                #handDB = PlayerDB.get_final_hand(self.getUsername(PK))
                #return PlayerDB.string_to_hand(handDB)

        def setFinalHand(self, hand):
                self.finalHand = hand
                #!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
                #handDB = PlayerDB.hand_to_string(hand)
                #PlayerDB.set_final_hand(self.getUsername(PK), handDB)
        
        def getBalance(self):
                return self.balance
                #!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
                #return PlayerDB.get_balance(self.getUsername(PK))

        def setBalance(self, balance):
                self.balance = balance
                #!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
                #PlayerDB.set_balance(self.getUsername(PK), balance)

        def getInRound(self):
                return self.inRound
                #!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
                #return PlayerDB.get_in_round(self.getUsername(PK))

        def setInRound(self, inRound):
                self.inRound = inRound
                #!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
                #PlayerDB.set_in_round(self.getUsername(PK), inRound)
        
        def getInBet(self):
                return self.inBet
                #!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
                #return PlayerDB.get_in_bet(self.getUsername(PK))

        def setInBet(self, inBet):
                self.inBet = inBet
                #!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
                #PlayerDB.set_in_bet(self.getUsername(PK), inBet)

        def getBetBalance(self):
                return self.betBalance
                #!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
                #return PlayerDB.get_bet_balance(self.getUsername(PK))

        def setBetBalance(self, Bet):
                self.betBalance = Bet
                #!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
                #PlayerDB.set_bet_balance(self.getUsername(PK), Bet)

        def leaveGame(self):
                self.Game.removePlayer(self.username)
                #!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
                #PlayerDB.remove_player(self.getUsername(PK))
        
        def mainMenu(self):
                if self.inRound:
                        query = "Hey there " + self.getUsername() + " what would you like to do?"
                        questions = [inquirer.List('options', message = query, choices = ['Leave Game', 'Join Round', 'Fold' ],),]
                        answer = inquirer.prompt(questions)

                        if answer["options"] == "Join Round":
                                print(self.username + ", you have been added to this round")
                                #do game logic
                                self.roundMenu()
                        elif answer["options"] == "Fold":
                                self.fold()
                        else: 
                                #player leaves game
                                self.setInRound(False)
                                self.game.removePlayer(self.username)
                        
                
        def roundMenu(self):
                gameInfo = "The current pot is: " + str(self.game.getPot()) + " the current bet is: " + str(self.game.getBet()) + " your cards are: " + str(self.getHand()[0]) + " " + str(self.getHand()[1]) 
                questions = [inquirer.List('options', message = gameInfo, choices = ['Bet/Raise', 'Check/Call', 'Fold'],),]
                answer = inquirer.prompt(questions)

                if answer["options"] == "Bet/Raise":
                        self.bet()
                elif answer["options"] == "Check/Call":
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
                        # self.balance = self.balance - playerDiff
                        self.setBalance(self.getBalance() - playerDiff)
                        self.game.setBet(bet)
                        self.setBetBalance(bet)
                        self.game.setPot(self.game.getPot() + playerDiff)
                        self.game.betFalse()
                        self.setInBet(True)
                else:
                        print("Your bet is lower than current Bet, Up the ante!! Or you have not more funds:(  ")
                        self.bet()

        def check(self):
                #do some game logic here
                bet = self.game.getBet()
                playerDiff = bet - self.getBetBalance()
                if self.balance >= playerDiff:
                        # self.setbalance = self.balance - playerDiff
                        self.setBalance(self.getBalance() - playerDiff) 
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
                print(self.getUsername()  + ", you have folded " + ", see ya next round!")


                







        