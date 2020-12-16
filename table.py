import random

class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        if self.rank == 'A':
            self.value = 11
        elif self.rank in ['J', 'Q', 'K']:
            self.value = 10
        else:
            self.value = int(self.rank)

    def __str__(self):
        return str(self.rank) + ' ' + self.suit

    def __repr__(self):
        return str(self.rank) + ' ' + self.suit

class Deck(object):
    def __init__(self, number_of_decks):
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        ranks = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
        self.deck = []
        for _ in range (number_of_decks)
            for suit in suits:
                for rank in ranks:
                    self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

class Hand(object):
    def __init__(self, bet):
        self.bet = bet
        self.cards = []
        self.active = True
        self.value = 0

class Player(object):
    def __init__(self, wallet, name='Dealer'):
        self.name = name
        if name == 'Dealer':
            self.type = 'dealer'
        else:
            self.type = 'player'
        self.wallet = wallet
        self.hands = []

    def __str__(self):
        return self.name

class Table(object):
    def __init__(self,number_of_decks):
        self.dealer = Player('Dealer',0)
        self.deck = Deck(number_of_decks)
        self.deck.shuffle()
        self.players = []
        self.cut = random.randint(1,int(len(self.deck.deck)/2))