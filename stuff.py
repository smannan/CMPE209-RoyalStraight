import random
# from poker import Suit
# from poker import Rank
# from poker import Card
from poker import *

def newHand():
        card1 = Card.make_random()
        card2 = Card.make_random()
        cards = []
        cards.append(card1)
        cards.append(card2)

def showHand(cards):
        for card in cards:
                print(card)


def testRound():
        deck = list(Card)
        random.shuffle(deck)
        flop = []
        #list 3 cards
        print("The flop is:")
        flop.append(Card.make_random())
        flop.append(Card.make_random())
        flop.append(Card.make_random())
        showHand(flop)
        #list 4 cards
        print("the turn is:")
        turn = flop
        turn.append(Card.make_random())
        showHand(turn)
        print("the river is:")
        river = turn
        river.append(Card.make_random()) 
        showHand(river)

        
