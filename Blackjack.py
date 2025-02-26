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
    def __init__(self, player_balance=1000):
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
    def recieve_card(self, game_card, index):
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
        self.hand = [[]]  # Reset to one hand initially
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

    # Deals the first 2 cards to the player and dealer
    def deal_initial_cards(self):
        for _ in range(2):
            Player.recieve_card(self, self.deck.deal(), 0)
            self.dealer.recieve_card(self.deck.deal(), 0)

    # This function runs different player functions and checks for inputs from the player using 'h' or 'p' or 's'
    def player_turn(self):
        for i in range(len(self.hand)):
            while True:
                if Player.is_busted(self, i):
                    print(f"Bust! Hand {i + 1} is over 21.")
                    return False
                if Player.get_hand_value(self, i) == 21:
                    print(f"Hand {i + 1} has 21!")
                    return True
                
                self.action = input("Hit, Stand, or Split? (h/s/p): ").lower()
                if self.action == 'h':
                    drawn_card = self.deck.deal()
                    Player.recieve_card(self, drawn_card, i)
                    print(f"You drew: {drawn_card} - New hand value: {Player.get_hand_value(self, i)}")
                elif self.action == 'p' and Player.can_split(self, i):
                    if Player.split_hand(self, i):
                        Player.recieve_card(self, self.deck.deal(), i)
                        Player.recieve_card(self, self.deck.deal(), -1)  # Deal to new hand
                        print("Your hands after splitting:")
                        for hand_index in range(len(self.hand)):
                            print(f"Hand {hand_index + 1}: {[str(card) for card in self.hand[hand_index]]} - Value: {Player.get_hand_value(self, hand_index)}")
                    else:
                        print("Cannot split.")
                elif self.action == 's':
                    return True
                else:
                    print("Invalid action! Please choose 'h', 's', or 'p'.")
        return True

    # Keeps dealing to dealer until dealer is above 17 in card value and then checks to see if dealer busts
    def dealer_turn(self):
        print(f"Dealer's full hand: {[str(card) for card in self.dealer.hand[0]]} - Value: {self.dealer.get_hand_value(0)}")
        while self.dealer.get_hand_value(0) < 17:
            drawn_card = self.deck.deal()
            self.dealer.recieve_card(drawn_card, 0)
            print(f"Dealer drew: {drawn_card} - New value: {self.dealer.get_hand_value(0)}")
        return not self.dealer.is_busted(0)

    # Updates the balance if player wins or loses
    def handle_payouts(self, hand_index, bet):
        player_value = Player.get_hand_value(self, hand_index)
        dealer_value = self.dealer.get_hand_value(hand_index)
        
        # Player bust
        if player_value > 21:
            print(f"Player's hand {hand_index + 1} busted. Dealer wins.")
            return
            
        # Dealer bust
        if dealer_value > 21:
            print(f"Dealer busts! Player's hand {hand_index + 1} wins!")
            self.player_balance += bet * 2
            return
            
        # Compare hands
        if player_value > dealer_value:
            print(f"Player's hand {hand_index + 1} wins! ({player_value} vs {dealer_value})")
            self.player_balance += bet * 2
        elif player_value == dealer_value:
            print(f"Hand {hand_index + 1} pushes! ({player_value} vs {dealer_value})")
            self.player_balance += bet
        else:
            print(f"Dealer wins hand {hand_index + 1}! ({dealer_value} vs {player_value})")

    # runs play loop and calls functions to start the game
    def play(self):
        while self.player_balance > 0:
            print(f"Player's balance: {self.player_balance}")
            bet = int(input("Enter bet amount: "))
            if not Player.place_wager(self, bet):
                print("Insufficient balance!")
                continue

            Player.clear_hand(self)
            self.dealer.clear_hand()
            self.deal_initial_cards()

            # Display initial hands
            print(f"Your hand: {[str(card) for card in self.hand[0]]} - Value: {Player.get_hand_value(self, 0)}")
            print(f"Dealer's face-up card: {str(self.dealer.hand[0][0])}")

            # Player's turn
            player_not_busted = self.player_turn()

            # Only continue to dealer's turn if player hasn't busted
            if player_not_busted:
                self.dealer_turn()
                num = 0
                # Handle payouts for each hand
                for i in range(len(self.player_wager)):
                    num += 1
                Game.handle_payouts(self, num, bet)
               
                # for i, bet in enumerate(self.player_wager):
                #     Game.handle_payouts(i, bet)
            else:
                print("Player busts! Dealer wins!")

            # End of round
            print(f"Player's new balance: {self.player_balance}")
            play_again = input("Do you want to play again? (y/n): ").lower()
            if play_again != 'y':
                break

if __name__ == "__main__":
    game = Game()
    game.play()