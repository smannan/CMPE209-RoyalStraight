import json
import random
from pprint import pprint
import inquirer
# from poker import *
from SQLite import *
from itertools import combinations
from time import sleep
from sqlalchemy.orm import validates, relationship
from poker import Card

# import sys
# sys.path.append("..")

from encryption import (
    generateB64SessionKey,
    rsa_encrypt,
    ASCII_to_binary as a2b,
    binary_to_ASCII as b2a,
    )

# Relative import
from sql_objects import app, db

def encrypt_token(context):
    b64_token = context.get_current_parameters()['token']
    b64_pubkey = context.get_current_parameters()['pubkey']

    # Convert to binary for the rsa_encrypt function
    bin_token = a2b(b64_token)
    bin_pubkey = a2b(b64_pubkey)
    b64_enc_key = rsa_encrypt(bin_token, bin_pubkey)

    # Convert back to utf8 for storage
    return b64_enc_key

def populate_token(context):
    username = context.get_current_parameters()['username']
    row = db.session.query(User).filter_by(username=username).first()
    key = row.token
    return key

gs_default = {
    "bet":0,
    "pot":0,
}

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.Unicode, primary_key=True)
    pubkey = db.Column(db.String, unique=True)
    token = db.Column(db.Unicode, default=generateB64SessionKey)
    enc_token = db.Column(db.Unicode, default=encrypt_token)

class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode)
    betround = db.Column(db.Integer, default=0)
    action = db.Column(db.Unicode)
    amount = db.Column(db.Integer, default=0)
    user_token = db.Column(db.Unicode, default=populate_token)
    token = db.Column(db.Unicode)

    # TODO try validating user token with second session
    

    @validates('action')
    def validate_action(self, key, value):
        assert value in (
            'bet', 
            'check', 
            'raise',
            'fold',
            'call'
        )

        return value

    @validates('amount')
    def validate_amount(self, key, value):
        if self.action in ('bet', 'raise'):
            assert int(value) > 0
        return value

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, db.ForeignKey('user.username'))
    gameid = db.Column(db.Integer, db.ForeignKey('game.id'))
    # Player's private cards represented as a JSON value
    cards = db.Column(db.JSON)
    hands = db.Column(db.JSON)
    user_token = db.Column(db.Unicode, default=populate_token)
    # game = relationship("Game", back_populates="playerz")

    # def __init__(self, username, balance, game):
    # def __init__(self):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        # self.username = username
        self.hand = []
        # self.balance = balance
        # self.game = game
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

    def getHand(self):
        return self.hand

    def setHand(self, hand):
        self.hand = hand

    def getFinalHand(self):
        return self.finalHand

    def setFinalHand(self, hand):
        self.finalHand = hand
        
    def getBalance(self):
        return self.balance

    def setBalance(self, balance):
        self.balance = balance

    def getInRound(self):
        return self.inRound

    def setInRound(self, inRound):
        self.inRound = inRound
        
    def getInBet(self):
        return self.inBet

    def setInBet(self, inBet):
        self.inBet = inBet

    def getBetBalance(self):
        return self.betBalance

    def setBetBalance(self, Bet):
        self.betBalance = Bet

    def leaveGame(self):
        self.Game.removePlayer(self.username)
        
    def mainMenu(self):
        if self.inRound:
            query = "Hey there " + self.username + " what would you like to do?"
            try:
                questions = [inquirer.List('options', message = query, choices = ['Leave Game', 'Fold', 'Join Round'],),]
                answer = inquirer.prompt(questions)
            except:
                questions = {
                    'type':'list',
                    'choices' : ['Leave Game', 'Fold', 'Join Round'],
                    'message':query,
                    'name':'options'
                }
                answer = PyInquirer.prompt(questions)
            if answer["options"] == "Join Round":
                print(self.username + ", you have been added to this round")
                #do game logic
                self.roundMenu()
            elif answer["options"] == "Fold":
                self.fold()
            else: 
                #player leaves game
                self.inRound = False
                self.game.removePlayer(self.username)
                        
                
    def roundMenu(self):
        gameInfo = "The current pot is: " + str(self.game.getPot()) + " the current bet is: " + str(self.game.getBet()) + " your cards are: " + str(self.hand[0]) + " " + str(self.hand[1]) 
        try:
            questions = [inquirer.List('options', message = gameInfo, choices = ['Bet/Raise', 'Check/Match', 'Fold'],),]
            answer = inquirer.prompt(questions)
        except:
            questions = {
                'type':'list',
                'choices' : ['Bet/Raise','Check/Match', 'Fold'],
                'message':gameInfo,
                'name':'options'
            }
            answer = PyInquirer.prompt(questions)
        if answer["options"] == "Bet/Raise":
            self.bet()
        elif answer["options"] == "Check/Match":
            self.check()
        else: 
            self.fold()

    def bet(self):
        query = "How much would you like to bet? bet value needs to be greater than current bet of " + str(self.game.getBet())
        try:
            question = [inquirer.Text('bet', query)]
            answer = inquirer.prompt(question)
        except:
            questions = {
                'type': 'input',
                'name': 'bet',
                'message': query,
            }
            answer = PyInquirer.prompt(questions)
        bet = int(answer["bet"])
        #do some game logic here
        playerDiff = bet-self.getBetBalance()
        if bet > self.game.getBet() and self.balance >= playerDiff:
            self.balance = self.balance - playerDiff
            self.game.setBet(bet)
            self.setBetBalance(bet)
            self.game.setPot(self.game.getPot() + playerDiff)
            self.game.betFalse()
            self.setInBet(True)
        else:
            print("Your bet is lower than current Bet, Up the ante!! Or you have not more funds:(  ")
            self.bet(self)

    def check(self):
        #do some game logic here
        bet = self.game.getBet()
        playerDiff = bet - self.getBetBalance()
        if self.balance >= playerDiff:
            self.balance = self.balance - playerDiff
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
        print(self.username  + ", you have folded " + ", see ya next round!")

gs_default = {
    "bet":0,
    "pot":0,
}

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
        # self.playerTurn = self.players[0].getUsername()
        self.playerTurn = ''

    def update_game_db(self):
        player_names = []
        for player in self.players:
            player_names.append(player.getUsername()) 
        
        strComCards = []
        for card in self.comCards:
            strComCards.append(str(card))

        data = {
            'pot':self.pot,
            'bet':self.bet,
            'comCards':strComCards,
            'players':player_names,
            'playerTurn':self.playerTurn
            # Nice to have: data about who's in/out
        }
        pprint(data)
        json_data = json.dumps(data)
        self.data = json_data
        db.session.commit()
        # TODO: Write to Database

    # TODO
    def update_player_db(self):
        pass

    def addPlayer(self, player):
        self.players.append(player)

    def getPlayers(self):
        return self.players 
        #playersJSON == json.loads(Game.players)
        # players = list((playersJSON.values()))
        #return players

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
        # self.update_processor = Update.maxid + 1
        self.update_processor = 1

        for gameRound in ['Flop','Turn','River']:

            print('Start of %s' % gameRound)

            if gameRound in ['Turn','River']:
                result = self.resetRound()
                # TODO: game.commit()
                if result == 'gameover':
                    return

            while  not Game.checkBet(self):
                players = self.getPlayers()
                for player in self.players:
                    # Wait for player response
                    if player.inRound and not player.getInBet():
                        self.playerTurn = player.getUsername()
                        self.update_game_db()
                        while True:
                            print('Looking for update %d' % self.update_processor)
                            status = db.session.query(Update).filter_by(id=self.update_processor).first()
                            print(status)
                            if status is None:
                                print('Waiting for input, user should be %s' % player.getUsername())
                                sleep(5)
                                continue
                            print('Status.username = %s' % status.username)
                            if status.username == player.getUsername():
                                if True:
                                    print("Username matches, ignoring token")
                                # if status.token == status.user_token:
                                #     print('Found matching token')
                                    self.pot += status.amount-player.getBetBalance()
                                    self.bet = status.amount
                                    self.update_player_db()
                                    self.update_game_db()
                                    # Until I fix the update__db methods
                                    self.update_processor +=1
                                    db.session.commit()

                                    break
                                else:
                                    # Got a post for the correct user, but
                                    # the token they posted does not match.
                                    print('Found non-matching token')
                                    self.update_processor +=1
                                    db.session.commit()
                            # This shouldn't match, can probably get rid of this
                            else:
                                print("Username doesn't match")

                            self.update_processor +=1
                            db.session.commit()

        #this is the end of the game evaluating
        self.showdown()


    def manageGame(self):
        while len(self.getPlayers()) > 1:
            self.start()
        print("end of game!")

    
if __name__ == "__main__":
    pass
