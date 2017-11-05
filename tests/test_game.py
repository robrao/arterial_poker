import unittest
import play_a_round

from collections import Counter


class TestGameMethods(unittest.TestCase):

    def setUp(self):
        play_a_round.UNIQUE_CARD_COUNT = Counter()

    def test_recursive_high_card_check_high(self):
        game = play_a_round.Game("QH 2D KS 3C JD")
        p1 = play_a_round.Player("test1 9H 6S")
        p2 = play_a_round.Player("test2 8H 6C")
        p1.hand_rank = 'r'
        p2.hand_rank = 'r'
        p1.high_card_sorted_list = [13, 12, 11, 9, 6]
        p2.high_card_sorted_list = [13, 12, 11, 8, 6]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, False)

    def test_recursive_high_card_check_high_split(self):
        game = play_a_round.Game("QH 2D KS 3C JD")
        p1 = play_a_round.Player("test1 8C 6S")
        p2 = play_a_round.Player("test2 8H 6C")
        p1.hand_rank = 'r'
        p2.hand_rank = 'r'
        p1.high_card_sorted_list = [13, 12, 11, 8, 6]
        p2.high_card_sorted_list = [13, 12, 11, 8, 6]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, "split pot")

    def test_recursive_high_card_check_pair(self):
        game = play_a_round.Game("QH 2D KS 3C JD")
        p1 = play_a_round.Player("test1 2H 6S")
        p2 = play_a_round.Player("test2 3H 6C")
        p1.hand_rank = 's'
        p2.hand_rank = 's'
        p1.high_card_sorted_list = [13, 12, 11, 2, 2]
        p2.high_card_sorted_list = [13, 12, 11, 3, 3]
        p1.pair_sorted_list = [(2, 2), (13, 1), (12, 1), (11, 1)]
        p2.pair_sorted_list = [(3, 2), (13, 1), (12, 1), (11, 1)]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, True)

    def test_recursive_high_card_check_pair_split(self):
        game = play_a_round.Game("QH 2D KS 3C JD")
        p1 = play_a_round.Player("test1 6H 6S")
        p2 = play_a_round.Player("test2 6D 6C")
        p1.hand_rank = 's'
        p2.hand_rank = 's'
        p1.high_card_sorted_list = [13, 12, 11, 6, 6]
        p2.high_card_sorted_list = [13, 12, 11, 6, 6]
        p1.pair_sorted_list = [(6, 2), (13, 1), (12, 1), (11, 1)]
        p2.pair_sorted_list = [(6, 2), (13, 1), (12, 1), (11, 1)]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, "split pot")

    def test_recursive_high_card_check_twopair(self):
        game = play_a_round.Game("QH 2D KS 3C JD")
        p1 = play_a_round.Player("test1 2H QS")
        p2 = play_a_round.Player("test2 2C JC")
        p1.hand_rank = 't'
        p2.hand_rank = 't'
        p1.high_card_sorted_list = [13, 12, 12, 2, 2]
        p2.high_card_sorted_list = [13, 11, 11, 2, 2]
        p1.pair_sorted_list = [(12, 2), (2, 2), (13, 1)]
        p2.pair_sorted_list = [(11, 2), (2, 2), (13, 1)]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, False)

    def test_recursive_high_card_check_twopair_split(self):
        game = play_a_round.Game("QH 2D KS 3C JD")
        p1 = play_a_round.Player("test1 2H QS")
        p2 = play_a_round.Player("test2 2C QC")
        p1.hand_rank = 't'
        p2.hand_rank = 't'
        p1.high_card_sorted_list = [13, 12, 12, 2, 2]
        p2.high_card_sorted_list = [13, 12, 12, 2, 2]
        p1.pair_sorted_list = [(12, 2), (2, 2), (13, 1)]
        p2.pair_sorted_list = [(12, 2), (2, 2), (13, 1)]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, "split pot")

if __name__ == '__main__':
    unittest.main()
