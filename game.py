import player
import inquirer
from poker import *

class Game:
        def __init__(player):
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
                print("you have bet")

        def setBet(self, bet):
                self.bet = bet

        def getPot(self):
                return self.pot

        def setPot(self, pot):
                self.pot = pot

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
        def showdown(self):
                #this is where all of the hands of the players are evaluated. 
        def start(self):
                #maybe have a while loop where the size is greater than 1? 
                while (len(self.players) > 1)
                        #this is the Hole Cards
                        Game.giveCardsBeg(self)
                        #this is the Flop
                        flop = Game.getCards(3)
                        self.comCards = flop
                        for player in self.players:
                                player.mainMenu()
                        #this is the Turn
                        self.comCards.append(Game.getCards(1))
                        for player in self.players:
                                player.mainMenu()
                        #this is the River
                        self.comCards.append(Game.getCards(1))
                        for player in self.players:
                                player.mainMenu()

                        #this is the end of the game evaluating
                        Game.showdown(self)




        

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


                                