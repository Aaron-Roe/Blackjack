import random

class Card:
    Suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    Ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = Card.Ranks[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    # Adds all cards to a list and shuffles them
    def __init__(self, decks=2):
        self.game_cards = []
        for i in range(decks):
            for suit in Card.Suits:
                for rank in Card.Ranks:
                    self.game_cards.append(Card(suit, rank))
        random.shuffle(self.game_cards)
    # Returns the last card in the list and removes it from the list
    def deal(self):
        return self.game_cards.pop()


class Player:
    def __init__(self, player_balance=1500):
        self.player_balance = player_balance
        self.hand = [[]]  # Support for multiple hands
        self.player_wager = []

    # Adds the new wager amount to the wager list
    def place_wager(self, wager):
        if wager <= self.player_balance:
            self.player_wager.append(wager)
            self.player_balance -= wager
            return True
        return False

    # Adds a card to the player's hand
    def receive_card(self, game_card, index):
        self.hand[index].append(game_card)

    # Increases the amount of Aces count and if there is an ace and the hand value is over 21, then Aces are reduced to 1 in value
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
    
    # Checks hand for blackjacks
    def has_blackjack(self, index):
        if len(self.hand[index]) == 2 and self.get_hand_value(index) == 21:
            return True
        return False

    # checks to see if the Player's first two cards are the same number and available to split
    def can_split(self, index):
        if len(self.hand[index]) == 2 and self.hand[index][0].rank == self.hand[index][1].rank:
            return True
        return False

    # This splits the hand into two different hands to play with
    def split_hand(self, index):
        if self.can_split(index):
            card = self.hand[index].pop()
            self.hand.append([card])
            return True
        return False

    # Resets the hand and wagers to an empty list
    def clear_hand(self):
        self.hand = [[]] # Reset to one hand initially
        self.player_wager = []

    # Checks to see if Player or Dealer hand is greater than 21 in value
    def is_busted(self, index):
        return self.get_hand_value(index) > 21


class Game(Player):
    def __init__(self):
        super().__init__()
        self.deck = Deck()
        # self.player = Player
        self.dealer = Player()

    # Deals the first 2 cards to the player and dealer and returns both hands
    def deal_initial_cards(self):
        for _ in range(2):
            self.receive_card(self.deck.deal(), 0)
            self.dealer.receive_card(self.deck.deal(), 0)
        return self.hand[0], self.dealer.hand[0]

    # Gives player a card 
    def player_hit(self, index=0):
        card = self.deck.deal()
        self.receive_card(card, index)
        return card, self.get_hand_value(index), self.is_busted(index)

    # Gives dealer a card
    def dealer_turn(self):
        actions = []
        while self.dealer.get_hand_value(0) < 17:
            drawn_card = self.deck.deal()
            self.dealer.receive_card(drawn_card, 0)
            actions.append(drawn_card)
        return self.dealer.hand[0], self.dealer.get_hand_value(0), self.dealer.is_busted(0), actions

    # Updates the balance based on the win or loss condition and returns the result and player balance
    def handle_payouts(self, hand_index, bet):
        player_value = self.get_hand_value(hand_index)
        dealer_value = self.dealer.get_hand_value(0)
        result = "push"

        if player_value > 21:
            result = "lose"
        elif dealer_value > 21 or player_value > dealer_value:
            self.player_balance += bet * 2
            result = "win"
        elif player_value == dealer_value:
            self.player_balance += bet
            result = "push"
        else:
            result = "lose"

        return result, self.player_balance

    # clears player and dealer hands and creates new instance of the deck if there are less than 20 cards
    def reset_round(self):
        self.clear_hand()
        self.dealer.clear_hand()
        if len(self.deck.game_cards) < 20:
            self.deck = Deck()

    # Returns the players hand
    def get_player_hand(self):
        return self.hand[0]

    # Returns the dealers hand
    def get_dealer_hand(self):
        return self.dealer.hand[0]