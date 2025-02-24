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
    def __init__(self, player_balance = 1000):
        self.player_balance = player_balance
        self.hand = [[]]
        self.player_wager = []

    def place_wager(self, wager):
        if wager <= self.player_balance:
            self.player_wager.append(wager)
            self.player_balance -= wager
            return True
        return False
    
    def recieve_card(self, game_card, index):
        # self.hand is not updating with another list / adding 
        self.hand[index].append(game_card)

    def get_hand_value(self, index):
        hand_value = 0
        number_of_aces = 0

        for card in self.hand[index]:
            hand_value += card.value
            if card.rank == 'A':
                number_of_aces += 1
                
        while hand_value > 21 and number_of_aces > 0:
            hand_value -= 10
            number_of_aces -= 1
        
        return hand_value

    def  has_blackjack(self, index):
        if (len(self.hand[index]) == 2, self.get_hand_value(index) == 21):
            return True
        return False

    def clear_hand(self):
        self.hand = [[]]
        self.player_wager = []
        
        

            

class Game: #Blackjack game checks and play loop
    pass

