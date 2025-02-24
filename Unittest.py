import unittest
from Blackjack import Player, Card


class Blackjack_Testing(unittest.TestCase):
# Player Class 
  # place_wager Function:
    # Testing invalid wager amount 
    def test_invalid_wager(self):
        self.player_balance = 1000
        self.assertFalse(Player.place_wager(self, 2000))

    # Testing valid wager amount
    def test_valid_wager(self):
        self.player_wager = []
        self.player_balance = 1000
        self.assertTrue(Player.place_wager(self, 500))

    # Testing the storage of valid wagers 
    def test_adding_valid_wagers1(self):
        self.player_wager = []
        self.player_balance = 1000
        Player.place_wager(self, 500)
        self.assertEqual(self.player_wager, [500])
    
    # Testing the storage of multiple valid wagers
    def test_adding_valid_wagers2(self):
        self.player_wager = []
        self.player_balance = 2000
        Player.place_wager(self, 1000)
        Player.place_wager(self, 500)
        Player.place_wager(self, 400)
        self.assertEqual(self.player_wager, [1000, 500, 400])

    # Testing the non-storage of invalid wagers 
    def test_adding_invalid_wagers(self):
        self.player_wager = []
        self.player_balance = 1000
        Player.place_wager(self, 1100)
        self.assertEqual(self.player_wager, [])

    def test_valid_balance_subtractor(self):
        self.player_wager = []
        self.player_balance = 1000
        Player.place_wager(self, 500) 
        self.assertEqual(self.player_balance, 500)
    
    def test_invalid_balance_subtractor(self):
        self.player_wager = []
        self.player_balance = 1000
        Player.place_wager(self, 1100) 
        self.assertEqual(self.player_balance, 1000)

  # recieve_card Function:
    # Testing 
    def test_valid_hand_update1(self):
        self.hand = [[],[]]
        Player.recieve_card(self, 'K', 0)
        Player.recieve_card(self, 'A', 1)
        self.assertEqual(self.hand, [['K'], ['A']])
    
    def test_valid_hand_update2(self):
        self.hand = [[]]
        Player.recieve_card(self, 'K', 0)
        Player.recieve_card(self, 'A', 0)
        Player.recieve_card(self, '10', 1)
        Player.recieve_card(self, '8', 1)
        self.assertEqual(self.hand, [['K','A'], ['10','8']])

# Class Card
    #Testing __str__ function
    def test_valid_str1(self):
        self.rank = 'K'
        self.suit = 'Diamonds'
        self.assertEqual(Card.__str__(self), 'K of Diamonds')

    def test_valid_str2(self):
        self.rank = '3'
        self.suit = 'Hearts'
        self.assertEqual(Card.__str__(self), '3 of Hearts')







if __name__ == '__main__':

    unittest.main()