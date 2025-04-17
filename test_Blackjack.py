import unittest
from Blackjack import Player, Card, Game, Deck


class Player_Testing(unittest.TestCase):
# Player Class 
  # place_wager Function:
    # Testing invalid wager amount 
    def test_invalid_wager(self):
        p1 = Player(1000)
        instance = p1.place_wager(2000)
        self.assertFalse(instance)

    # Testing valid wager amount
    def test_valid_wager(self):
        p1 = Player(1000)
        p1.player_wager = []
        self.assertTrue(p1.place_wager(500))

    # Testing the storage of valid wagers 
    def test_adding_valid_wagers1(self):
        p1 = Player(1000)
        p1.player_wager = []
        p1.place_wager(500)
        self.assertEqual(p1.player_wager, [500])
    
    # Testing the storage of multiple valid wagers
    def test_adding_valid_wagers2(self):
        p1 = Player(2000)
        p1.player_wager = []
        p1.place_wager(1000)
        p1.place_wager(500)
        p1.place_wager(400)
        self.assertEqual(p1.player_wager, [1000, 500, 400])

    # Testing the non-storage of invalid wagers 
    def test_adding_invalid_wagers(self):
        p1 = Player(1000)
        p1.player_wager = []
        p1.place_wager(1100)
        self.assertEqual(p1.player_wager, [])

    def test_valid_balance_subtractor(self):
        p1 = Player(1000)
        p1.player_wager = []
        p1.place_wager(500) 
        self.assertEqual(p1.player_balance, 500)
    
    def test_invalid_balance_subtractor(self):
        p1 = Player(1000)
        p1.player_wager = []
        p1.place_wager(1100)
        self.assertEqual(p1.player_balance, 1000)

    def test_recieve_card_rank(self):
        p = Player()
        p.receive_card(Card('Diamonds', '10'), 0)
        self.assertEqual(p.hand[0][0].rank, '10')
    
    def test_recieve_card_suit(self):
        p = Player()
        p.receive_card(Card('Diamonds', '10'), 0)
        self.assertEqual(p.hand[0][0].suit, 'Diamonds')
    
    def test_recieve_card_value(self):
        p = Player()
        p.receive_card(Card('Diamonds', '10'), 0)
        self.assertEqual(p.hand[0][0].value, 10)

    # Testing count for the number of aces 
    def test_num_ace_is1(self):
        p1 = Player(1000)
        c1 = Card('Diamonds', 'A')
        c2 = Card('Spades', '8')
        c3 = Card('Clubs', 'K')
        p1.hand[0] = [c1, c2, c3]
        self.assertEqual(p1.get_hand_value(0), 19)

  # has_blackjack
    # Testing for valid blackjack 
    def test_blackjack_True(self):
        p1 = Player(1000)
        c1 = Card('Diamonds', 'A')
        c2 = Card('Clubs', 'K')
        p1.hand[0] = [c1, c2]
        self.assertTrue(p1.has_blackjack(0))

    # Testing for invalid blackjack
    def test_blackjack_False(self):
        p1 = Player(1000)
        c1 = Card('Diamonds', '4')
        c2 = Card('Clubs', 'K')
        p1.hand[0] = [c1, c2]
        self.assertFalse(p1.has_blackjack(0))

  # can_split Function:
    # Testing to see if there is an avaliable split
    def test_split_check_true(self):
        p1 = Player(1000)
        c1 = Card('Diamonds', '4')
        c2 = Card('Clubs', '4')
        p1.hand[0] = [c1, c2]
        self.assertTrue(p1.can_split(0))

    # Testing to see if there is no avaliable split
    def test_split_check_false(self):
        p1 = Player(1000)
        c1 = Card('Diamonds', '4')
        c2 = Card('Clubs', '10')
        p1.hand[0] = [c1, c2]
        self.assertFalse(p1.can_split(0))

    # Testing invalid split action
    def test_split_action_false(self):
        p1 = Player(1000)
        c1 = Card('Diamonds', '8')
        p1.hand = [[c1]]
        self.assertFalse(p1.split_hand(0))
    
    # Testing hand value split
    def test_split_hand_value(self):
        p1 = Player(1000)
        c1 = Card('Diamonds', '7')
        c2 = Card('Clubs', '7')
        p1.hand[0] = [c1, c2]
        p1.split_hand(0)
        self.assertEqual(p1.hand, [[c1], [c2]])
    #testing clear_hand function to make sure player wager updates correctly
    def test_clear_hand(self):
        p = Player()
        p.place_wager(500)
        p.place_wager(1000)
        p.place_wager(268)
        p.place_wager(117)
        p.clear_hand()
        self.assertEqual(p.player_wager, [])


# Class Card
    # __str__ function 
    
    def test_str1(self):
        c1 = Card('Diamonds', 'K')
        self.assertEqual(c1.__str__(), 'K of Diamonds')

    # Testing __str__ function #2
    def test__str2(self):
        c1 = Card('Hearts', '3')
        self.assertEqual(c1.__str__(), '3 of Hearts')
    
   # handle_payouts Function:
    def test_payouts(self):
        p1 = Player(1000)
        g1 = Game()
        c1 = Card('Diamonds', 'K')
        c2 = Card('Diamonds', '5')
        c3 = Card('Clubs', 'K')
        p1.hand = [[c1, c2, c3]]
        self.assertEqual(g1.handle_payouts(0, 500), None)

# Class Deck
    # Testing Deal() function
    def test_deal(self):
        d = Deck()
        card = d.deal()
        self.assertIsInstance(card, Card)

# Class Game
    # Making sure all items in the player hands correct
    def test_initial_cards_player1(self):
        g = Game()
        dealing = g.deal_initial_cards()
        player_hand = dealing[0]
        self.assertEqual(player_hand, g.hand[0])

    # Making sure there are two cards in player hand after initial cards are dealt
    def test_initial_cards_player2(self):
        g = Game()
        g.deal_initial_cards()
        self.assertEqual(len(g.hand[0]), 2)

    # Making sure all items in the dealer hands correct
    def test_initial_cards_dealer1(self):
        g = Game()
        dealing = g.deal_initial_cards()
        dealer_hand = dealing[1]
        self.assertEqual(dealer_hand, g.dealer.hand[0])

    # Making sure there are two cards in dealer hand after initial cards are dealt
    def test_initial_cards_dealer2(self):
        g = Game()
        g.deal_initial_cards()
        self.assertEqual(len(g.dealer.hand[0]), 2)

    def test_player_hit_continue(self):
        g = Game()
        g.hand[0] = []
        g.hand[0] = [Card("Spades","10"),Card("Diamonds","5")]
        g.deck.game_cards.append(Card("Hearts","2"))
        hitting = g.player_hit()
        is_busted = hitting[2]
        hand_val = hitting[1]
        self.assertEqual(is_busted, False)
        # self.assertEqual(hand_val, 17)

    def test_player_hit_bust(self):
        g = Game()
        g.hand[0] = []
        g.hand[0] = [Card("Spades","10"),Card("Diamonds","J")]
        g.deck.game_cards.append(Card("Hearts","5"))
        hitting = g.player_hit()
        is_busted = hitting[2]
        hand_val = hitting[1]
        self.assertEqual(is_busted, True)
        # self.assertEqual(hand_val, 25)

    def test_dealer_turn_under17(self):
        g = Game()
        g.dealer.hand[0] = []
        g.dealer.hand[0] = [Card("Spades","10"),Card("Diamonds","3")]
        g.deck.game_cards = [Card("Hearts","5")]
        hitting = g.dealer_turn()
        is_busted = hitting[2]
        self.assertEqual(is_busted, False)


    def test_dealer_turn_above17(self):
        g = Game()
        g.dealer.hand[0] = []
        g.dealer.hand[0] = [Card("Spades","10"),Card("Diamonds","J")]
        hitting = g.dealer_turn()
        is_busted = hitting[2]
        self.assertEqual(is_busted, False)


    def test_handle_payouts_lose1(self):
        g = Game()
        g.hand[0] = [Card("Spades","10"),Card("Diamonds","3"),Card("hearts","10")]
        result = g.handle_payouts(0, 500)[0]
        self.assertEqual(result, "lose")

    def test_handle_payouts_win(self):
        g = Game()
        g.hand[0] = [Card("Spades","10"),Card("Diamonds","3"),Card("hearts","6")]
        g.dealer.hand[0] = [Card("Spades","10"),Card("Diamonds","3"),Card("hearts","5")]
        result = g.handle_payouts(0, 500)[0]
        self.assertEqual(result, "win")

    def test_handle_payouts_push(self):
        g = Game()
        g.hand[0] = [Card("Spades","10"),Card("Diamonds","3"),Card("hearts","6")]
        g.dealer.hand[0] = [Card("Spades","5"),Card("Diamonds","8"),Card("hearts","6")]
        result = g.handle_payouts(0, 500)[0]
        self.assertEqual(result, "push")

    def test_handle_payouts_lose2(self):
        g = Game()
        g.hand[0] = [Card("Spades","10"),Card("Diamonds","3"),Card("hearts","5")]
        g.dealer.hand[0] = [Card("Spades","10"),Card("Diamonds","3"),Card("hearts","6")]
        result = g.handle_payouts(0, 500)[0]
        self.assertEqual(result, "lose")

    def test_reset_player(self):
        g = Game()
        g.hand[0] = [Card("Spades","10"),Card("Diamonds","3"),Card("hearts","6")]
        g.reset_round()
        self.assertEqual(g.hand[0], [])

    def test_reset_dealer(self):
        g = Game()
        g.deck.game_cards = [Card("Hearts","5")]
        g.dealer.hand[0] = [Card("Spades","10"), Card("Diamonds","3"), Card("hearts","6")]
        g.reset_round()
        self.assertEqual(g.dealer.hand[0], [])

    def test_get_player_hand(self):
        g = Game()
        g.hand[0] = [Card("Spades","10"),Card("Diamonds","3"),Card("hearts","6")]
        self.assertEqual(g.hand[0], g.get_player_hand())

    def test_get_dealer_hand(self):
        g = Game()
        g.dealer.hand[0] = [Card("Spades","10"),Card("Diamonds","3"),Card("hearts","6")]
        self.assertEqual(g.dealer.hand[0], g.get_dealer_hand())

# if __name__ == '__main__':
#     unittest.main(verbosity=2)

