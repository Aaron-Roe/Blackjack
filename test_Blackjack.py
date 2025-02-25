import unittest
from Blackjack import Player, Card, Game


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

  # recieve_card Function:
    # NEEDS MODIFICATION - FUNCTION CURRENTLY DOES NOT WORK

    # def test_valid_hand_update1(self):
    #     self.hand = [[],[]]
    #     Player.recieve_card(self, 'K', 0)
    #     Player.recieve_card(self, 'A', 1)
    #     self.assertEqual(self.hand, [['K'], ['A']])
    
    # def test_valid_hand_update2(self):
    #     self.hand = [[]]
    #     Player.recieve_card(self, 'K', 0)
    #     Player.recieve_card(self, 'A', 0)
    #     Player.recieve_card(self, '10', 1)
    #     Player.recieve_card(self, '8', 1)
    #     self.assertEqual(self.hand, [['K','A'], ['10','8']])

  # get_hand_value function
  # MAKE NU_OF_ACES and HAND_VALUE .SELF SO I CAN ACCESS
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
    


# Class Card
  # __str__ function 
    def test_str1(self):
        c1 = Card('Diamonds', 'K')
        self.assertEqual(c1.__str__(), 'K of Diamonds')

    # Testing __str__ function #2
    def test__str2(self):
        c1 = Card('Hearts', '3')
        self.assertEqual(c1.__str__(), '3 of Hearts')

    
#class Game
  # player_turn Function
    # Testing Bust
    def test_Bust(self):
        g1 = Game()
        c1 = Card('Diamonds', 'A')
        c2 = Card('Clubs', 'K')
        g1.player.hand = [[c1, c2]]
        self.assertTrue(g1.player_turn())




if __name__ == '__main__':
    unittest.main(verbosity=2)