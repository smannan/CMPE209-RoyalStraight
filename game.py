from player import Player
import random
import inquirer
import requests
from poker import *
from SQLite import *
from itertools import combinations
class Game:
        def __init__(self):
                #create deck with all of the cards
                self.deck = list(Card)
                #shuffle the deck
                random.shuffle(self.deck)
                # create a list of players in the game. 
                self.players = []
                self.pot = 0
                self.bet = 0
                self.comCards = []
                

        def ShuffleDeck(self):
                random.shuffle(self.deck)
        
        def getNewDeck(self):
                self.deck = list(Card)
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
                if Game.check_straight_flush(self, hand):
                        return 9
                if Game.check_four_of_a_kind(self, hand):
                        return 8
                if Game.check_full_house(self, hand):
                        return 7
                if Game.check_flush(self, hand):
                        return 6
                if Game.check_straight(self, hand):
                        return 5
                if Game.check_three_of_a_kind(self, hand):
                        return 4
                if Game.check_two_pair(self, hand):
                        return 3
                if Game.check_pair(self, hand):
                        return 2
                # this means that it will go High Card
                return 1

        def check_straight(self, hand):
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
                straightCount = 0
                for i in range(len(cards)):
                        if (cards[i] == len(cards) - 1) and cards[0] == 1 and straightCount == 4:
                                return True

                        if cards[i] == 1  and straightCount != 5:
                                straightCount = straightCount + 1
                        else:
                                if straightCount > 0 and straightCount != 5:
                                        straightCount -= 1
                                        
                if straightCount == 5:
                         return True
                else: 
                        return False

                

        def check_straight_flush(self, hand):
                if Game.check_flush(self, hand) and Game.check_straight(self, hand):
                        return True
                else:
                        return False
        def check_full_house(self, hand):
                #3 and 2 Rank
                suits = [h.suit for h in hand]
                if len(set(suits)) == 2:
                        return True
                else:
                        return False

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
                                # use thiis to get rid of duplicates for performance imporments
                                # combo = list(set(list(combinations(possibleCombos, 5)))) 
                                # Use this for know for Proof Of Concept
                                combo = list(combinations(possibleCombos, 5))
                                bestHand = combo[0]
                                for hand in combo:
                                        if Game.check_hand(self, hand) > Game.check_hand(self, bestHand):
                                                bestHand = hand
                                        elif Game.check_hand(self, hand) == Game.check_hand(self, bestHand):
                                                # need to implement this by sorting cards, and seeing which one is the greatest. for now just blindly take the next 
                                                bestHand = hand
                                
                                player.setHand(list(bestHand))
                                print("for the player " + player.getUsername() + " the best hand is: " )
                                print(player.hand)
                                                

                                                        



        def showdown(self):
                #this is where all of the hands of the players are evaluated. 
                Game.finalHand(self)
                Game.getNewDeck(self)
                for player in self.players:
                        player.hand = []

                # for player in self.players:
                #         username = player.getUsername()
                #         self.removePlayer(username)

                
                
                print("the numbers of playres is: ")
                print(self.players)
                


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



def getSessionKey(user_set):
    url = 'https://go.warnold.dev/api/register'
    for row in user_set:
        myobj = {'username': row[0], 'publickey': row[1]}
        x = requests.post(url, data=myobj)
        print(x)
        

def main():
        #create the Game
        poker = Game()
        clearDB()
        startup()
        user_set = users()
        getSessionKey(user_set)
        # Todo - add session keys to dbs and to game functions
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
        # #start the game
        poker.start()
        # test the methods
        # # print(poker.deck)
        # four = []
        # four.append(poker.deck[1])
        # four.append(poker.deck[5])
        # four.append(poker.deck[9])
        # four.append(poker.deck[13])
        # four.append(poker.deck[17])
        # print("this is hand")
        # print(four)
        # if poker.check_straight(four):
        #         print("yay")
        # else:
        #         print("you are failure")
main()
