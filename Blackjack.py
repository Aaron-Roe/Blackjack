import random


class Card:
    Suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    Ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = Card.Ranks[rank]
    
    def __str__(self):
        return f"{self.rank} of {self.suit}" # Ex Ace of Hearts


class Deck:
    def __init__(self, decks = 2):
        self.game_cards = []
        for i in range(decks):
            for suit in Card.Suits:
                for rank in Card.Ranks:
                    self.game_cards.append(Card(suit, rank))

        random.shuffle(self.game_cards)

    def deal(self):
        return self.game_cards.pop()

class Player: # player values like hand and balance 
    pass

class Game: #Blackjack game checks and play loop
    pass

