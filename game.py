from poker import *

class Game:
        def __init__(player):
                self.deck = list[Card]
                self.players = list[Player]
                random.shuffle(self.deck)

        def ShuffleDeck(self):
                random.shuffle(self.deck)
        
        def getNewDeck(self):
                self.deck = list[Card]
                random.shuffle(self.deck)
        def addPlayer(player):