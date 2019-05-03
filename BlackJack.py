'''
THIS SCRIPT STIMULATES THE 
BLACKJACK GAME THAT IS PLAYED BETWEEN THE COMPUTER AND A PLAYER
'''

import random

# GLOBAL VARIABLES TO HOLD THE SUIT , DESK AND RANK

suits = ('heart', 'diamonds', 'space', 'clubs')
ranks = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace')
values = { 
		'one' : 1,
	    'two' : 2, 
	    'three' : 3, 
	    'four' : 4, 
	    'five' : 5, 
	    'six' : 6, 
	    'seven' : 7, 
	    'eight' : 8, 
	    'nine' : 9, 
	    'ten' : 10,
	    'jack' : 10, 
	    'king' : 10, 
	    'queen' : 10,
	    'ace'  : 11
	    }
playing = True


# A CARD CLASS THAT REPRESENTS A CARD
# HAS TWO ATTRIBUTES ( SUIT AND RANK )
class Card(object):

	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank


	def __str__(self):
		return self.rank + ' of ' + self.suit



# A CLASS DECK THAT HOLD A DECK OF ALL THE CARDS
class Deck(object):

	def __init__(self):
		self.deck = []

		# CREATING CARDS OF ALL RANKS FOR EACH SUIT AND STORING THE CARD OBJECT IN THE DECK ARRAY
		for suit in suits :
			for rank in ranks :
				self.deck.append(Card(suit, rank))


	def __str__(self):
		complete_deck = ''
		for card in self.deck :
			complete_deck += str(card)+'\n'
		return ' the deck has : \n'+complete_deck	

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		return self.deck.pop()


# A HAND CLASS REPRESENTS THE PLAYERS OF THE GAME
# ONE INSTANCE REPRESENTS THE COMPUTER
# ONE INSTANCE REPRESENTS THE PLAYER

class Hand(object):

	def __init__(self):
		self.cards = [] # to store all the cards a player holds
		self.value = 0 # to store the sum of values of all ranks the player holds
		self.aces = 0 # to store the num of aces that the player holds

	def add_card(self, card):
		# card is a object returned from Deck.deal()
		self.cards.append(card)
		self.value += values[card.rank]
		if card.rank == 'ace':
			self.aces += 1

	def adjust_for_ace(self):

		while self.value > 21 and self.aces > 0 :
			self.value -= 10
			self.aces -= 1

class Chip(object):

	def __init__(self):
		self.total = 100
		self.bet = 0 

	def won_bet(self):
		self.total += self.bet

	def lost_bet(self):
		self.total -= self.bet



class GameInterface :

	def take_bet(self, chips):

		while True:

			try:
				chips.bet = int(input(' enter your bet : '))

			except:
				print(' do provide an integer ')

			else :
				if chips.bet > chips.total :
					print(f' sorry your available bet is : {chips.total}' )
				else :
					break

	def hit(self, deck, hand):

		hand.add_card(deck.deal())
		hand.adjust_for_ace()

	def hit_or_stand(self, deck, hand):

		global playing

		while True:

			choice = input(' hit or stand ? enter \'h\' or \'s\' : ')

			if choice[0].lower() == 'h':
				self.hit(deck, hand)

			elif choice[0].lower() == 's':
				print(' player stands dealer\'s turn ')
				playing = False

			else :
				print(' do enter \'h\' or \'s\' : ')
				continue

			break	

	def show_some(self, player, dealer):
		print('\ndealer hand : ')
		print('< card hidden >')
		print(' ', dealer.cards[1])
		print('\n player hand : ', *player.cards , sep = '\n')

	def show_all(self, player, dealer):
		print('\ndealer hand : ', *dealer.cards, sep='\n')
		print('dealer hand : ', dealer.value)
		print('\nplayer hand : ', *player.cards, sep='\n')
		print('player hand : ', player.value)

	def player_busts(self, player, dealer, chips):
		print(' player busts')
		chips.lost_bet()

	def player_wins(self, player, dealer, chips):
		print(' player wins')
		chips.won_bet()

	def dealer_busts(self, player, dealer, chips):
		print(' dealer busts')
		chips.lost_bet()

	def dealer_wins(self, player, dealer, chips):
		print(' dealer wins')
		chips.won_bet()

	def push(self, player, dealer, chips):
		print(' the game is a tie ')


class Game(object):

	game = GameInterface()

	print(' welcome to the BlackJack game : ')

	deck = Deck()
	deck.shuffle()

	player_hand = Hand()
	player_hand.add_card(deck.deal())
	player_hand.add_card(deck.deal())

	dealer_hand = Hand()
	dealer_hand.add_card(deck.deal())
	dealer_hand.add_card(deck.deal())

	player_chip = Chip()

	game.take_bet(player_chip)
	game.show_some(player_hand, dealer_hand)


	while playing:

		game.hit_or_stand(deck, player_hand)
		game.show_some(player_hand, dealer_hand)

		if player_hand.value > 21:
			game.player_busts(player_hand, dealer_hand, player_chip)
			break


		if player_hand.value <= 21 :

			while dealer_hand.value < 17 :
				game.hit(deck, dealer_hand)

			game.show_all(player_hand, dealer_hand)

			if dealer_hand.value > 21 :
				game.dealer_busts(player_hand, dealer_hand, player_chip)
				break

			elif dealer_hand.value > player_hand.value :
				game.dealer_wins(player_hand, dealer_hand, player_chip)
				break

			elif dealer_hand.value < player_hand.value :
				game.player_wins(player_hand, dealer_hand, player_chip)
				break

			else :
				game.push(player_hand, dealer_hand, player_chip)
				break



	print(' thanks for playing ')










