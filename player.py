from poker import *

class Player:
        def __init__(username):
                self.username = username
                self.hand = []

        def getHand(self, username):
                return self.hand

        def setHand(self, hand):
                self.hand = hand