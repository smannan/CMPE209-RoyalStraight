from player import Player
import random
import inquirer
import requests
from poker import *
from SQLite import *
from encryption import *
import os
from itertools import combinations

import binascii


class Game:
    def __init__(self):
        # create deck with all of the cards
        self.deck = list(Card)
        # shuffle the deck
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

    def ShuffleDeck(self):
        random.shuffle(self.deck)

    def getNewDeck(self):
        self.deck = list(Card)

    def getDeck(self):
        return self.deck

    def setDeck(self, deck):
        self.deck = deck

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
            # get a random card
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
                switch = {
                    "A": 1,
                    "T": 10,
                    "J": 11,
                    "Q": 12,
                    "K": 13,
                    "no": 14
                }
                idx = switch.get(str(card.rank), "no") - 1
            else:
                idx = int(str(card.rank)) - 1
            cards[idx] = cards[idx] + 1

        straightCount = 0
        for i in range(len(cards)):
            if (cards[i] == len(cards) - 1) and cards[0] == 1 and straightCount == 4:
                return True

            if cards[i] == 1 and straightCount != 5:
                straightCount += 1
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
        # 3 and 2 Rank
        cards = [0] * 13
        idx = 0
        for card in hand:
            if card.is_broadway:
                switch = {
                    "A": 1,
                    "T": 10,
                    "J": 11,
                    "Q": 12,
                    "K": 13,
                    "no": 14
                }
                idx = switch.get(str(card.rank), "no") - 1
            else:
                idx = int(str(card.rank)) - 1
            cards[idx] = cards[idx] + 1

        fullHouse = 0
        for count in cards:
            if count == 2:
                fullHouse = fullHouse + 1
            if count == 3:
                fullHouse = fullHouse + 1
        if fullHouse == 2:
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
                switch = {
                    "A": 1,
                    "T": 10,
                    "J": 11,
                    "Q": 12,
                    "K": 13,
                    "no": 14
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
                switch = {
                    "A": 1,
                    "T": 10,
                    "J": 11,
                    "Q": 12,
                    "K": 13,
                    "no": 14
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
                switch = {
                    "A": 1,
                    "T": 10,
                    "J": 11,
                    "Q": 12,
                    "K": 13,
                    "no": 14
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
                switch = {
                    "A": 1,
                    "T": 10,
                    "J": 11,
                    "Q": 12,
                    "K": 13,
                    "no": 14
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
                combo = list(combinations(possibleCombos, 5))
                bestHand = combo[0]
                for hand in combo:
                    if Game.check_hand(self, hand) > Game.check_hand(self, bestHand):
                        bestHand = hand
                    elif Game.check_hand(self, hand) == Game.check_hand(self, bestHand):
                        # need to implement this by sorting cards, and seeing which one is the greatest. for now just blindly take the next
                        bestHand = hand
                player.setFinalHand(list(bestHand))
                print("the player: " + player.getUsername() + "has a hand of: ")
                print(player.getFinalHand())

    def findWinner(self):
        playerSize = len(self.players)
        contenders = [0] * playerSize
        for player in range(playerSize):
            if self.players[player].getFinalHand():
                contenders[player] = Game.check_hand(
                    self, self.players[player].getFinalHand())
        print("The contenders are: ")
        print(contenders)
        winner = contenders.index(max(contenders))
        Game.declareWinner(self, winner)

    def declareWinner(self, winner):
        # here the index of the winner in self.palyers will be passed. the balnaces need to be adjusted.
        winnings = self.players[winner].getBalance() + self.getPot()
        self.players[winner].setBalance(winnings)
        print("The winner is: " + self.players[winner].getUsername())
        print("The winner's balance is: " +
              str(self.players[winner].getBalance()))
        Game.getNewDeck(self)
        Game.ShuffleDeck(self)
        Game.setPot(self, 0)
        self.resetRound()
        Game.start(self)

    def showdown(self):
        # this is where all of the hands of the players are evaluated.
        Game.finalHand(self)
        Game.findWinner(self)

    def start(self):
        # maybe have a while loop where the size is greater than 1? count(inRound > 1?)
        # while (len(self.players) > 1):
        # this is the Hole Cards
        Game.giveCardsBeg(self)

        # this is the Flop
        flop = Game.getCards(self, 3)
        self.comCards = []
        self.comCards = flop
        self.setBet(0)
        while not Game.checkBet(self):
            for player in self.players:
                if player.inRound and not player.getInBet():
                    print("The community cards are: ")
                    print(self.comCards)
                    print(str(player))
                    print("The current pot is: " + str(self.getPot()) +
                          " the current bet is: " + str(self.getBet()))
                    player.mainMenu()

        # this is the Turn
        self.resetRound()
        # check if everyone folds
        playerCount = len(self.players)
        foldCount = 0
        winner = self.players[0]
        for player in self.players:
            if not player.inRound:
                foldCount = foldCount + 1
            else:
                winner = player

        if foldCount == playerCount - 1:
            # break while loop and call winner as only person in game
            Game.declareWinner(self, self.players.index(winner))
            # break

        while not Game.checkBet(self):
            for player in self.players:
                if player.inRound and not player.getInBet():
                    print("The community cards are: ")
                    print(self.comCards)
                    print(str(player))
                    print("The current pot is: " + str(self.getPot()) +
                          " the current bet is: " + str(self.getBet()))
                    player.mainMenu()

        # this is the River
        self.resetRound()
        # check if everyone folds
        playerCount = len(self.players)
        foldCount = 0
        winner = self.players[0]
        for player in self.players:
            if not player.inRound:
                foldCount = foldCount + 1
            else:
                winner = player

        if foldCount == playerCount - 1:
            # break while loop and call winner as only person in game
            Game.declareWinner(self, self.players.index(winner))
            # break
        while not Game.checkBet(self):
            for player in self.players:
                if player.inRound and not player.getInBet():
                    print("The community cards are: ")
                    print(self.comCards)
                    print(str(player))
                    print("The current pot is: " + str(self.getPot()) +
                          " the current bet is: " + str(self.getBet()))
                    player.mainMenu()

        # this is the end of the game evaluating
        self.showdown()

        if(len(self.players) > 1):
            Game.start(self)
        else:
            print("end of game!")


def getSessionKey(username, pubkey):
    url = 'https://go.warnold.dev/api/user'
    data = {'username': username, 'pubkey': pubkey}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    print(data)
    x = requests.post(url, data=data, headers=headers)
    print(x.text)
    return x


def main():
    # create the Game
    poker = Game()

    # get public keys from file
    smannan_public_key = RSA.importKey(
        open('pub_pri_keys/smannan_public.pem', 'r').read()).exportKey('PEM')
    junlan66_public_key = RSA.importKey(
        open('pub_pri_keys/junlan66_public.pem', 'r').read()).exportKey('PEM')
    wearnold_public_key = RSA.importKey(
        open('pub_pri_keys/wearnold_public.pem', 'r').read()).exportKey('PEM')
    ksbains_public_key = RSA.importKey(
        open('pub_pri_keys/ksbains_public.pem', 'r').read()).exportKey('PEM')
    print(junlan66_public_key)

    # get encrypted session keys from server
    smannan_enc_sessionkey = getSessionKey('smannan', binascii.b2a_base64(
        smannan_public_key).decode('utf8'))
    junlan66_enc_sessionkey = getSessionKey('junlan6', binascii.b2a_base64(
        junlan66_public_key).decode('utf8'))
    wearnold_enc_sessionkey = getSessionKey('wearnolds', binascii.b2a_base64(
        wearnold_public_key).decode('utf8'))
    ksbains_enc_sessionkey = getSessionKey('ksbains', binascii.b2a_base64(
        ksbains_public_key).decode('utf8'))

    # get private keys from files
    smannan_pri_key = RSA.importKey(
        open('pub_pri_keys/smannan_public.pem', 'r').read()).exportKey('PEM')
    junlan66_pri_key = RSA.importKey(
        open('pub_pri_keys/junlan66_public.pem', 'r').read()).exportKey('PEM')
    wearnold_pri_key = RSA.importKey(
        open('pub_pri_keys/wearnold_public.pem', 'r').read()).exportKey('PEM')
    ksbains_pri_key = RSA.importKey(
        open('pub_pri_keys/ksbains_public.pem', 'r').read()).exportKey('PEM')
    print(junlan66_public_key)

    # decrypt session keys with private key
    smannan_dec_sessionkey = rsa_decrypt(
        ASCII_to_binary(smannan_enc_sessionkey), smannan_pri_key)
    junlan66_dec_sessionkey = rsa_decrypt(
        ASCII_to_binary(junlan66_enc_sessionkey), junlan66_pri_key)
    wearnold_dec_sessionkey = rsa_decrypt(
        ASCII_to_binary(wearnold_enc_sessionkey), wearnold_pri_key)
    ksbains_dec_sessionkey = rsa_decrypt(
        ASCII_to_binary(ksbains_enc_sessionkey), ksbains_pri_key)

    # Todo - add session keys to dbs and to game functions
    # create players
    # kb = Player("ksbains", 500, poker)
    # wayne = Player("wearnold", 500, poker)
    # junlan = Player("junlan", 500, poker)
    # sonia = Player("smannan", 500, poker)

    # # add the Players
    # poker.addPlayer(kb)
    # poker.addPlayer(wayne)
    # poker.addPlayer(junlan)
    # poker.addPlayer(sonia)
    # # #start the game
    # poker.start()


main()
