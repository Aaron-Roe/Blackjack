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

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Player()  

    def deal_initial_cards(self):
        for _ in range(2):
            self.player.deal_card(self.deck.deal())
            self.dealer.deal_card(self.deck.deal())

    def player_turn(self):
        for i in range(len(self.player.player_hand)):
            while self.player.get_hand_value(i) < 21:
                action = input("Hit, Stand, or Split? (h/s/p): ").lower()
                if action == 'h':
                    self.player.deal_card(self.deck.deal(), i)
                elif action == 'p' and self.player.can_split(i):
                    if self.player.split_hand(i):
                        self.player.deal_card(self.deck.deal(), i)
                        self.player.deal_card(self.deck.deal(), -1)
                    else:
                        print("Cannot split.")
                else:
                    break
        return True
    
    def dealer_turn(self):
        while self.dealer.get_hand_value() < 17:
            self.dealer.deal_card(self.deck.deal())
        print(f"Dealer's hand: {[str(card) for card in self.dealer.player_hand[0]]} - Value: {self.dealer.get_hand_value()}")
        return self.dealer.get_hand_value() <= 21
    
    def determine_winner(self):
        dealer_value = self.dealer.get_hand_value()
        for i, bet in enumerate(self.player.bets):
            player_value = self.player.get_hand_value(i)
            if player_value > 21:
                print("Player busts! Dealer wins.")
            elif dealer_value > 21 or player_value > dealer_value:
                print("Player wins!")
                self.player.player_balance += bet * 2
            elif player_value == dealer_value:
                print("It's a push!")
                self.player.player_balance += bet
            else:
                print("Dealer wins!")

    def play(self):
        while self.player.player_balance > 0:
            print(f"Player's balance: {self.player.player_balance}")
            bet = int(input("Enter bet amount: "))
            if not self.player.place_bet(bet):
                print("Insufficient balance!")
                continue

            self.player.clear_hands()
            self.dealer.clear_hands()
            self.deal_initial_cards()

            print(f"Dealer's hand: [{self.dealer.player_hand[0][0]}, ?]")
            print(f"Player's hand: {[str(card) for card in self.player.player_hand[0]]} - Value: {self.player.get_hand_value()}")

            if self.player.get_hand_value() == 21:
                print("Blackjack! Player wins double!")
                self.player.player_balance += bet * 2
                continue

            if not self.player_turn():
                continue

            if not self.dealer_turn():
                continue

            self.determine_winner()

        print("Game Over! Player is out of money.")


if __name__ == "__main__":
    game = Game()
    game.play()