import unittest
import play_a_round

from collections import Counter


class TestPlayerMethods(unittest.TestCase):

    def setUp(self):
        play_a_round.UNIQUE_CARD_COUNT = Counter()
        play_a_round.UNIQUE_PLAYER_NAMES = Counter()

    def test_parseBoard_too_much_input(self):
        with self.assertRaises(ValueError):
            play_a_round.Player("ab cd ef j l p q")

    def test_parseBoard_too_little_input(self):
        with self.assertRaises(ValueError):
            play_a_round.Player("ab cd ef")

    def test_parseBoard_face_to_val(self):
        p1 = play_a_round.Player("test1 AS KD")
        p2 = play_a_round.Player("test2 QD JD")
        p3 = play_a_round.Player("test3 TS 9D")

        self.assertEqual(p1.hand[0], "14S")
        self.assertEqual(p1.hand[1], "13D")
        self.assertEqual(p2.hand[0], "12D")
        self.assertEqual(p2.hand[1], "11D")
        self.assertEqual(p3.hand[0], "10S")

    def test_parseBoard_valid_names(self):
        with self.assertRaises(ValueError):
            play_a_round.Player("test AS KD")
            play_a_round.Player("test QD JD")
