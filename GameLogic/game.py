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

		#!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
		#GameDB.set_deck(self.deck)

		# create a list of players in the game. 
		self.players = []
		self.pot = 0
		self.bet = 0
		self.comCards = []


	
	def addPlayer(self, player):
		self.players.append(player)
		#!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
		#GameDB.insert_player(player.getUsername()
		# Have to do some logic here to make sure that the NULL column is filled with new player


	def removePlayer(self, playerUsername):
		for player in self.players:
			if playerUsername == player.getUsername():
				self.players.remove(player)
				#!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
				#GameDB.remove_player(player.getUsername(PK))
				# Have to do some logic here to make sure that the player column is now NULL
	def getPlayers():
		return self.getPlayers
		#!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
		#playersDB = GameDB.get_players()
		#return GameDB.string_to_players(playersDB)



	
	def ShuffleDeck(self):
		random.shuffle(self.deck)
	
	def getNewDeck(self):
		self.deck = list(Card)
		#!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
		#self.ShuffleDeck()
		# self.set_deck(self.deck)

	
	def getDeck(self):
		return self.deck
		#!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
		#deckDB = GameDB.get_deck()
		#return GameDB.string_to_deck(deckDB)
	
	def setDeck(self, deck):
		self.deck = deck
		#!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
		#deckDB = GameDB.deck_to_string(deck)
		#GameDB.set_deck(deckDB)

	def getBet(self):
		#!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
		#return GameDB.get_bet()
		return self.bet

	def setBet(self, bet):
		self.bet = bet
		#!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
		#GameDB.set_bet(bet)

	def getPot(self):
		#!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
		#return GameDB.get_pot()
		return self.pot

	def setPot(self, pot):
		self.pot = pot
		#!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
		#GameDB.set_pot(pot)
	
	def betFalse(self):
		for player in self.players:
			player.setInBet(False)
			#PlayerDB should be invoked in player.setInBet() so SQL changes happen in player. 

	def inRoundReset(self):
		for player in self.players:
			player.setInRound(True)
			#PlayerDB should be invoked in player.setInRound() so SQL changes happen in player. 


	def checkBet(self):
		for player in self.players:
			#PlayerDB should be invoked in player.getInBet() so SQL changes happen in player. 
			#PlayerDB should be invoked in player.getInRound() so SQL changes happen in player. 
			inBet = player.getInBet()
			inRound = player.getInRound() 
			if not  inBet and inRound:
				return False
		return True

	def resetRound(self):
		self.comCards.append(self.getCards(1)[0])
		#!!!!!!!!!!!!!!SQL HERE!!!!!!!!!!!!!!!!!!!!!!
		#cardDB = GameDB.card_to_string(self.getCards(1)[0])
		#GameDB.insert_card(cardDB)
		#GameDB should be invoked in game.setBet() so SQL changes happen in setter.
		self.setBet(0)
		for player in self.players:
			#PlayerDB should be invoked in player.setInBet() so SQL changes happen in player. 
			#PlayerDB should be invoked in player.setBetBalance() so SQL changes happen in player. 
			player.setInBet(False)
			player.setBetBalance(0)
					
	def giveCardsBeg(self):
		cardsNeeded = 2 * len(self.players)
		cards = Game.getCards(self, cardsNeeded)
		for player in self.players:
			card1 = cards.pop()
			card2 = cards.pop()
			#PlayerDB should be invoked in player.getHand() and player.setHand() so SQL changes happen in player. 
			hand = []
			hand.append(card1)
			hand.append(card2)
			player.setHand(hand)


	def getCards(self, need):
		toReturn = []
		i = 0
		while i < need:
			#get a random card
			card = Card.make_random()
			deck = self.getDeck()
			#if card in self.deck
			if card in deck:
				toReturn.append(card)
				# self.deck.remove(card)
				deck.remove(card)
				self.setDeck(deck)
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
				possibleCombos.append(player.getHand()[0])
				possibleCombos.append(player.getHand()[1])
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
		self.getNewDeck()
		self.ShuffleDeck()
		self.setPot(0)
		self.resetRound()
		self.inRoundReset()
		self.start()


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
		players = self.getPlayers()
		while  not Game.checkBet(self):
			for player in players:
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
		winner = self.players[0]
		players = self.getPlayers()
		for player in players:
			if not player.inRound:
				foldCount = foldCount +1
			else:
				winner = player

		if foldCount == playerCount - 1:
			#break while loop and call winner as only person in game
			Game.declareWinner(self, self.players.index(winner))
			# break

		while  not Game.checkBet(self):
			for player in players:
				if player.inRound and not player.getInBet():
					print("The community cards are: ")
					print(self.comCards)
					print(str(player))
					print("The current pot is: " + str(self.getPot()) + " the current bet is: " + str(self.getBet()))
					player.mainMenu()
		
		#this is the River
		self.resetRound()
		#check if everyone folds
		playerCount = len(self.players)
		foldCount = 0
		winner = self.players[0]
		players = self.getPlayers()
		for player in players:
			if not player.inRound:
				foldCount = foldCount +1
			else:
				winner = player

		if foldCount == playerCount - 1:
			#break while loop and call winner as only person in game
			Game.declareWinner(self, self.players.index(winner))
			# break
		while  not Game.checkBet(self):
			for player in players:
				if player.inRound and not player.getInBet():
					print("The community cards are: ")
					print(self.comCards)
					print(str(player))
					print("The current pot is: " + str(self.getPot()) + " the current bet is: " + str(self.getBet()))
					player.mainMenu()

		#this is the end of the game evaluating
		self.showdown()

		if(len(self.players) > 1):
			Game.start(self)
		else:
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
