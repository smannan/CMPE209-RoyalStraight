import json
from player import Player
from royal_server.pokersqrl import Update
import random
from pprint import pprint
import inquirer
import requests
from poker import *
from SQLite import *
from itertools import combinations

import sys
import binascii
import random
import flask
import flask_sqlalchemy
import flask_restless
from sqlalchemy.orm import validates
from poker import Card

sys.path.append("..")
from encryption import (
    generateKeys,
    generateSessionKey,
    rsa_encrypt,
    )
from encryption import ASCII_to_binary as a2b
from encryption import binary_to_ASCII as b2a

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
# app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poker.db'
# Clears a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)


def encrypt_token(context):
    b64_token = context.get_current_parameters()['token']
    b64_pubkey = context.get_current_parameters()['pubkey']

    # Convert to binary for the rsa_encrypt function
    bin_token = a2b(b64_token)
    bin_pubkey = a2b(b64_pubkey)
    b64_enc_key = rsa_encrypt(bin_token, bin_pubkey)

    # Convert back to utf8 for storage
    return b64_enc_key
    # return token+pubkey



gs_default = {
    "bet":0,
    "pot":0,
}

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.Unicode, primary_key=True)
    pubkey = db.Column(db.String, unique=True)
    token = db.Column(db.Unicode, default=generateSessionKey(output='base64'))
    enc_token = db.Column(db.Unicode, default=encrypt_token)

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, default=gs_default)

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
        self.playerTurn = self.players[0].getUsername()

    def update_game_db(self):
        player_names = []
        for player in self.players:
            player_names.append(player.getUsername()) 
        
        data = {
            'pot':self.pot,
            'bet':self.bet,
            'comCards':self.comCards,
            'players':player_names
            'playerTurn':self.playerTurn
            # Nice to have: data about who's in/out
        }
        pprint(data)
        json_data = json.dumps(data)

        # TODO: Write to Database

    # TODO
    def update_player_db(self):
        pass

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

        self.update_game_db()

        #check if everyone folds
        playerCount = len(self.players)
        foldCount = 0
        winner = self.players[0]
        for player in self.players:
            if not player.inRound:
                foldCount = foldCount +1
            else:
                winner = player

        if foldCount == playerCount - 1:
            #break while loop and call winner as only person in game
            Game.declareWinner(self, self.players.index(winner))

            return 'gameover'
            # break
        return 'continue'
                    
    def giveCardsBeg(self):
        cardsNeeded = 2 * len(self.players)
        cards = Game.getCards(self, cardsNeeded)
        hand = []
        for player in self.players:
            hand.append(cards.pop())
            hand.append(cards.pop())
            # TODO: Write this to the DB
            player.setHand(hand)

    def getCards(self, need):
        toReturn = []
        for _ in range(need):
            #get a random card
            card = self.deck.pop()
            toReturn.append(card)

            # card = Card.make_random()
            # if card in self.deck:
            #   toReturn.append(card)
            #     self.deck.remove(card)
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
        #3 and 2 Rank
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
                contenders[player] = Game.check_hand(self, self.players[player].getFinalHand())
        print("The contenders are: ")
        print(contenders)
        winner = contenders.index(max(contenders))
        Game.declareWinner(self, winner)

    def declareWinner(self, winner):
        #here the index of the winner in self.palyers will be passed. the balnaces need to be adjusted. 
        winnings = self.players[winner].getBalance() + self.getPot()
        self.players[winner].setBalance(winnings)
        print("The winner is: " + self.players[winner].getUsername())
        print("The winner's balance is: " + str(self.players[winner].getBalance()))
        Game.getNewDeck(self)
        Game.ShuffleDeck(self)
        Game.setPot(self, 0)
        self.setBet(0)
        for player in self.players:
            player.setInBet(False)
            player.setBetBalance(0)
            player.setFinalHand([])
            self.update_player_db(player)
        self.update_game_db()


    def showdown(self):
        #this is where all of the hands of the players are evaluated. 
        Game.finalHand(self)
        Game.findWinner(self)



            


    def start(self):
        #maybe have a while loop where the size is greater than 1? count(inRound > 1?) 
        # while (len(self.players) > 1):
        #this is the Hole Cards
        Game.giveCardsBeg(self)

        #this is the Flop
        flop = Game.getCards(self, 3)
        self.comCards = []
        self.comCards = flop
        self.setBet(0)

        # Update DB here
        # TODO: just prints json right now
        self.update_game_db()

        # Get the latest transaction ID and start from here
        # TODO: correct function for the maxid
        self.update_processor = Update.maxid + 1

        for gameRound in ['Flop','Turn','River']:

            print('Start of %s' % gameRound)

            if gameRound in ['Turn','River']:
                result = self.resetRound()
                # TODO: game.commit()
                if result == 'gameover':
                    return

            while  not Game.checkBet(self):
                for player in self.players:
                    # Wait for player response
                    if player.inRound and not player.getInBet():
                        self.playerTurn = player.getUsername()
                        self.update_game_db()
                        while True:
                            status = db.session.query(Update).filter_by(id=str(self.update_processor))
                            if status['username'] == player.getUsername():
                                if status['token'] == status['user_token']:
                                    self.pot += status['amount']-player.getBetBalance()
                                    self.bet = status['amount']
                                    self.update_player_db()
                                    self.update_game_db()
                                    break
                                else:
                                    # Got a post for the correct user, but
                                    # the token they posted does not match.
                                    self.update_processor +=1

                            elif not status:
                                # TODO: Test this
                                continue
                            self.update_processor +=1



            # while  not Game.checkBet(self):
            #     for player in self.players:
            #         if player.inRound and not player.getInBet():
            #             print("The community cards are: ")
            #             print(self.comCards)
            #             print(str(player))
            #             print("The current pot is: " + str(self.getPot()) + " the current bet is: " + str(self.getBet()))
            #             player.mainMenu()

        #this is the end of the game evaluating
        self.showdown()


    def manageGame(self):
        while len(self.players) > 1:
            self.start()
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

main()
