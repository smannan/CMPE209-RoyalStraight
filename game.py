from player import Player
import random
import inquirer
from poker import *
from itertools import combinations


class Game:
        def __init__(self):
                #create deck with all of the cards
                self.deck = list(Card)
                #shuffle teh deck
                # random.shuffle(self.deck)
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
        # THESE ARE ALL OF THE METHODS TO CHECK THE VALUE OF THE HANDS FOR PLAYERS.
        
        def check_hand(self, hand):
                if check_straight_flush(hand):
                        return 9
                if check__four_of_a_kind(hand):
                        return 8
                if check_full_house(hand):
                        return 7
                if check_flush(hand):
                        return 6
                if check_straight(hand):
                        return 5
                if check_three_of_a_kind(hand):
                        return 4
                if check_two_pair(hand):
                        return 3
                if check_pair(hand):
                        return 2
                # this means that it will go High Card
                return 1

        

        def check_flush(self, hand):
                suits = [h.suit for h in hand]
                if len(set(suits)) == 1:
                        return True
                else:
                        return False

        def check_four_of_a_kind(self, hand):
                cards = [0] * 13
                idx = 0
                for card in hand:
                        if card.is_broadway:
                                switch={
                                "A":1,
                                "T":10,
                                "J":11,
                                "Q":12,
                                "K":13,
                                "no":14
                                }
                                idx = switch.get(str(card.rank), "no") - 1
                        else:
                                idx = int(str(card.rank)) - 1
                        cards[idx] = cards[idx] + 1
                for count in cards:
                        if cards[count] == 4:
                                return True
                return False
        def check_three_of_a_kind(self, hand):
                cards = [0] * 13
                idx = 0
                for card in hand:
                        if card.is_broadway:
                                switch={
                                "A":1,
                                "T":10,
                                "J":11,
                                "Q":12,
                                "K":13,
                                "no":14
                                }
                                idx = switch.get(str(card.rank), "no") - 1
                        else:
                                idx = int(str(card.rank)) - 1
                        cards[idx] = cards[idx] + 1
                for count in cards:
                        if cards[count] == 3:
                                return True
                return False
        def check_pair(self, hand):
                cards = [0] * 13
                idx = 0
                for card in hand:
                        if card.is_broadway:
                                switch={
                                "A":1,
                                "T":10,
                                "J":11,
                                "Q":12,
                                "K":13,
                                "no":14
                                }
                                idx = switch.get(str(card.rank), "no") - 1
                        else:
                                idx = int(str(card.rank)) - 1
                        cards[idx] = cards[idx] + 1
                for count in cards:
                        if cards[count] == 2:
                                return True
                return False

        def check_two_pair(self, hand):
                cards = [0] * 13
                idx = 0
                for card in hand:
                        if card.is_broadway:
                                switch={
                                "A":1,
                                "T":10,
                                "J":11,
                                "Q":12,
                                "K":13,
                                "no":14
                                }
                                idx = switch.get(str(card.rank), "no") - 1
                        else:
                                idx = int(str(card.rank)) - 1
                        cards[idx] = cards[idx] + 1
                pair = 0
                print(cards)
                for count in cards:
                        if count == 2:
                                pair += 1
                
                if pair == 2:
                        return True
                else:
                        return False
        
        def finalHand(self):
                for player in self.players:
                                        if player.inRound:
                                                possibleCombos = self.comCards
                                                possibleCombos.append(player.hand[0])
                                                possibleCombos.append(player.hand[1])
                                                combo = combinations(possibleCombos, 5)
                                                for cards in combo:
                                                        print("A hand of cards for " + player.username + " is: ")
                                                        print(cards)



        def showdown(self):
                #this is where all of the hands of the players are evaluated. 
                Game.finalHand(self)
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
                        #check if everyone folds
                        playerCount = len(self.players)
                        foldCount = 0
                        for player in self.players:
                                if not player.inRound:
                                        foldCount = foldCount +1

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
        print(poker.deck)
        four = []
        four.append(poker.deck[0])
        four.append(poker.deck[4])
        four.append(poker.deck[8])
        four.append(poker.deck[12])
        four.append(poker.deck[16])
        print("this is hand")
        print(four)
        if poker.check_flush(four):
                print("yay")
        else:
                print("you are failure")
        #start the game
        # poker.start()
        # test the methods
main()


                                