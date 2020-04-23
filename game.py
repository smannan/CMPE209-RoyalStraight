from player import Player
import random
import inquirer
from poker import *


class Game:
        def __init__(self):
                #create deck with all of the cards
                self.deck = list(Card)
                #shuffle teh deck
                random.shuffle(self.deck)
                # create a list of players in the game. 
                self.players = []
                self.pot = 0
                self.bet = 0
                self.comCards = []
                

        def ShuffleDeck(self):
                random.shuffle(self.deck)
        
        def getNewDeck(self):
                self.deck = list[Card]
                random.shuffle(self.deck)
        
        def addPlayer(self, player):
                self.players.append(player)

        def removePlayer(self, playerUsername):
                for player in self.players:
                        if playerUsername == player.getUsername():
                                self.players.remove(player)

        def getBet(self):
                return self.bet

        def setBet(self, bet):
                self.bet = bet

        def getPot(self):
                return self.pot

        def setPot(self, pot):
                self.pot = pot
        def betFalse(self):
                for player in self.players:
                        player.setInBet(False)

        def checkBet(self):
                for player in self.players:
                        if not player.getInBet() and player.getInRound():
                                return False
                return True

        def resetRound(self):
                self.comCards.append(Game.getCards(self, 1)[0])
                self.setBet(0)
                for player in self.players:
                        player.setInBet(False)
                        player.setBetBalance(0)
                        
        def giveCardsBeg(self):
                cardsNeeded = 2 * len(self.players)
                cards = Game.getCards(self, cardsNeeded)
                for player in self.players:
                        player.hand.append(cards.pop())
                        player.hand.append(cards.pop())

        def getCards(self, need):
                toReturn = []
                i = 0
                while i < need:
                        #get a random card
                        card = Card.make_random()
                        if card in self.deck:
                                toReturn.append(card)
                                self.deck.remove(card)
                                i = i+1
                return toReturn
        def showdown(self):
                #this is where all of the hands of the players are evaluated. 
                for player in self.players:
                        username = player.getUsername()
                        self.removePlayer(username)
        def start(self):
                #maybe have a while loop where the size is greater than 1? count(inRound > 1?) 
                while (len(self.players) > 1):
                        #this is the Hole Cards
                        Game.giveCardsBeg(self)

                        #this is the Flop
                        flop = Game.getCards(self, 3)
                        
                        self.comCards = flop
                        self.setBet(0)
                        while  not Game.checkBet(self):
                                for player in self.players:
                                        if player.inRound and not player.getInBet():
                                                print("The community cards are: ")
                                                print(self.comCards)
                                                print(str(player))
                                                print("The current pot is: " + str(self.getPot()) + " the current bet is: " + str(self.getBet()))
                                                player.mainMenu()
                        
                        #this is the Turn
                        self.resetRound()
                        while  not Game.checkBet(self):
                                for player in self.players:
                                        if player.inRound and not player.getInBet():
                                                print("The community cards are: ")
                                                print(self.comCards)
                                                print(str(player))
                                                print("The current pot is: " + str(self.getPot()) + " the current bet is: " + str(self.getBet()))
                                                player.mainMenu()
                        
                        #this is the River
                        self.resetRound()
                        while  not Game.checkBet(self):
                                for player in self.players:
                                        if player.inRound and not player.getInBet():
                                                print("The community cards are: ")
                                                print(self.comCards)
                                                print(str(player))
                                                print("The current pot is: " + str(self.getPot()) + " the current bet is: " + str(self.getBet()))
                                                player.mainMenu()

                        #this is the end of the game evaluating
                        self.showdown()

                print("end of game!")




        

def main():
        #create the Game
        poker = Game()

        #create players
        kb = Player("ksbains", 500, poker)
        wayne = Player("wearnold", 500, poker)
        junlan = Player("junlan", 500, poker)
        sonia = Player("smannan", 500, poker)
        
        #add the Players
        poker.addPlayer(kb)
        poker.addPlayer(wayne)
        poker.addPlayer(junlan)
        poker.addPlayer(sonia)
        #start the game
        poker.start()
main()


                                