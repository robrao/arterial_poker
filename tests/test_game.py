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

    def test_recursive_high_card_check_pair_high(self):
        game = play_a_round.Game("QH 2D KS 3C JD")
        p1 = play_a_round.Player("test1 JH 8S")
        p2 = play_a_round.Player("test2 JS 6C")
        p1.hand_rank = 's'
        p2.hand_rank = 's'
        p1.high_card_sorted_list = [13, 12, 11, 11, 8]
        p2.high_card_sorted_list = [13, 12, 11, 11, 6]
        p1.pair_sorted_list = [(11, 2), (13, 1), (12, 1), (8, 1)]
        p2.pair_sorted_list = [(11, 2), (13, 1), (12, 1), (6, 1)]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, False)

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

    def test_recursive_high_card_check_twopair_high(self):
        game = play_a_round.Game("QH 2D 4S JC JD")
        p1 = play_a_round.Player("test1 7H QS")
        p2 = play_a_round.Player("test2 8C QC")
        p1.hand_rank = 't'
        p2.hand_rank = 't'
        p1.high_card_sorted_list = [12, 12, 11, 11, 7]
        p2.high_card_sorted_list = [12, 12, 11, 11, 8]
        p1.pair_sorted_list = [(12, 2), (11, 2), (7, 1)]
        p2.pair_sorted_list = [(12, 2), (11, 2), (8, 1)]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, True)

    def test_recursive_high_card_check_trips(self):
        game = play_a_round.Game("QH 2D KS 3C 3D")
        p1 = play_a_round.Player("test1 2H 2S")
        p2 = play_a_round.Player("test2 3H JC")
        p1.hand_rank = 'u'
        p2.hand_rank = 'u'
        p1.high_card_sorted_list = [13, 12, 2, 2, 2]
        p2.high_card_sorted_list = [13, 12, 3, 3, 3]
        p1.pair_sorted_list = [(2, 3), (13, 1), (12, 1)]
        p2.pair_sorted_list = [(3, 3), (13, 2), (12, 1)]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, True)

    def test_recursive_high_card_check_trips_split(self):
        game = play_a_round.Game("QH 2D KS 3C 3D")
        p1 = play_a_round.Player("test1 3S TS")
        p2 = play_a_round.Player("test2 3H JC")
        p1.hand_rank = 'u'
        p2.hand_rank = 'u'
        p1.high_card_sorted_list = [13, 12, 3, 3, 3]
        p2.high_card_sorted_list = [13, 12, 3, 3, 3]
        p1.pair_sorted_list = [(3, 3), (13, 1), (12, 1)]
        p2.pair_sorted_list = [(3, 3), (13, 2), (12, 1)]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, "split pot")

    def test_recursive_high_card_check_trips_high(self):
        game = play_a_round.Game("9H 2D KS AC AD")
        p1 = play_a_round.Player("test1 AS TS")
        p2 = play_a_round.Player("test2 AH JC")
        p1.hand_rank = 'u'
        p2.hand_rank = 'u'
        p1.high_card_sorted_list = [14, 14, 14, 13, 10]
        p2.high_card_sorted_list = [14, 14, 14, 13, 11]
        p1.pair_sorted_list = [(14, 3), (13, 1), (10, 1)]
        p2.pair_sorted_list = [(14, 3), (13, 1), (11, 1)]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, True)

    def test_recursive_high_card_check_straight(self):
        game = play_a_round.Game("TH 9D 8S 7C 6D")
        p1 = play_a_round.Player("test1 JH 3S")
        p2 = play_a_round.Player("test2 5H QC")
        p1.hand_rank = 'v'
        p2.hand_rank = 'v'
        p1.high_card_sorted_list = [11, 10, 9, 8, 7]
        p2.high_card_sorted_list = [10, 9, 8, 7, 6]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, False)

    def test_recursive_high_card_check_straight_split(self):
        game = play_a_round.Game("TH 9D 8S 7C 6D")
        p1 = play_a_round.Player("test1 JH 3S")
        p2 = play_a_round.Player("test2 JD QC")
        p1.hand_rank = 'v'
        p2.hand_rank = 'v'
        p1.high_card_sorted_list = [11, 10, 9, 8, 7]
        p2.high_card_sorted_list = [11, 10, 9, 8, 7]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, "split pot")

    def test_recursive_high_card_check_flush(self):
        game = play_a_round.Game("QH 2D KD 3C 8D")
        p1 = play_a_round.Player("test1 7D 6S")
        p2 = play_a_round.Player("test2 6D 6C")
        p1.hand_rank = 'w'
        p2.hand_rank = 'w'
        p1.high_card_sorted_list = [13, 12, 8, 7, 2]
        p2.high_card_sorted_list = [13, 12, 8, 8, 2]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, True)

    def test_recursive_high_card_check_full(self):
        game = play_a_round.Game("6H 7S 7C 3C 3D")
        p1 = play_a_round.Player("test1 7D 6S")
        p2 = play_a_round.Player("test2 6D 6C")
        p1.hand_rank = 'x'
        p2.hand_rank = 'x'
        p1.high_card_sorted_list = [7, 7, 7, 3, 3]
        p2.high_card_sorted_list = [6, 6, 6, 3, 3]
        p1.pair_sorted_list = [(7, 3), (3, 2)]
        p2.pair_sorted_list = [(6, 3), (3, 2)]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, False)

    def test_recursive_high_card_check_four(self):
        game = play_a_round.Game("6H 7S 7C 6C 3D")
        p1 = play_a_round.Player("test1 7D 7H")
        p2 = play_a_round.Player("test2 6D 6S")
        p1.hand_rank = 'y'
        p2.hand_rank = 'y'
        p1.high_card_sorted_list = [7, 7, 7, 7, 3]
        p2.high_card_sorted_list = [6, 6, 6, 6, 3]
        p1.pair_sorted_list = [(7, 4), (3, 1)]
        p2.pair_sorted_list = [(6, 4), (3, 1)]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, False)

    def test_recursive_high_card_check_straight_flush(self):
        game = play_a_round.Game("KH QH JH TH 3D")
        p1 = play_a_round.Player("test1 7D AH")
        p2 = play_a_round.Player("test2 9H 6S")
        p1.hand_rank = 'z'
        p2.hand_rank = 'z'
        p1.high_card_sorted_list = [14, 13, 12, 11, 10]
        p2.high_card_sorted_list = [13, 12, 11, 10, 9]

        res = game.recursive_high_card_check(p1, p2)

        self.assertEqual(res, False)

    def test_find_hand_rank_high_card(self):
        game = play_a_round.Game("KH QH JH TH 3D")
        hand = "9H 12D 6S 7D 14S".split(" ")
        hand_rank, hand_type, pair_sorted_list, high_card_sorted_list = game.find_hand_rank_and_high_card(hand)

        self.assertEqual(hand_rank, 'r')
        self.assertEqual(hand_type, 'Ace High')
        self.assertEqual(pair_sorted_list, [])
        self.assertEqual(high_card_sorted_list, [14, 12, 9, 7, 6])

    def test_find_hand_rank_pair(self):
        game = play_a_round.Game("KH QH JH TH 3D")
        hand = "9H 12D 6S 6D 14S".split(" ")
        hand_rank, hand_type, pair_sorted_list, high_card_sorted_list = game.find_hand_rank_and_high_card(hand)

        self.assertEqual(hand_rank, 's')
        self.assertEqual(hand_type, 'A Pair of 6\'s')
        self.assertEqual(pair_sorted_list, [(6, 2), (14, 1), (12, 1), (9, 1)])
        self.assertEqual(high_card_sorted_list, [14, 12, 9, 6, 6])

    def test_find_hand_rank_two_pair(self):
        game = play_a_round.Game("KH QH JH TH 3D")
        hand = "9H 4D 6S 6D 4S".split(" ")
        hand_rank, hand_type, pair_sorted_list, high_card_sorted_list = game.find_hand_rank_and_high_card(hand)

        self.assertEqual(hand_rank, 't')
        self.assertEqual(hand_type, 'Two Pairs: 6\'s and 4\'s')
        self.assertEqual(pair_sorted_list, [(6, 2), (4, 2), (9, 1)])
        self.assertEqual(high_card_sorted_list, [9, 6, 6, 4, 4])

    def test_find_hand_rank_three_pair(self):
        game = play_a_round.Game("KH QH JH TH 3D")
        hand = "9H 4D 6S 4C 4S".split(" ")
        hand_rank, hand_type, pair_sorted_list, high_card_sorted_list = game.find_hand_rank_and_high_card(hand)

        self.assertEqual(hand_rank, 'u')
        self.assertEqual(hand_type, 'Three 4\'s')
        self.assertEqual(pair_sorted_list, [(4, 3), (9, 1), (6, 1)])
        self.assertEqual(high_card_sorted_list, [9, 6, 4, 4, 4])

    def test_find_hand_rank_straight(self):
        game = play_a_round.Game("KH QH JH TH 3D")
        hand = "5H 14D 2S 3C 4S".split(" ")
        hand_rank, hand_type, pair_sorted_list, high_card_sorted_list = game.find_hand_rank_and_high_card(hand)

        self.assertEqual(hand_rank, 'v')
        self.assertEqual(hand_type, '5 High Straight')
        self.assertEqual(pair_sorted_list, [])
        self.assertEqual(high_card_sorted_list, [5, 4, 3, 2, 14])

    def test_find_hand_rank_flush(self):
        game = play_a_round.Game("KH QH JH TH 3D")
        hand = "5S 8S 2S 3S 4S".split(" ")
        hand_rank, hand_type, pair_sorted_list, high_card_sorted_list = game.find_hand_rank_and_high_card(hand)

        self.assertEqual(hand_rank, 'w')
        self.assertEqual(hand_type, '8 High Flush')
        self.assertEqual(pair_sorted_list, [])
        self.assertEqual(high_card_sorted_list, [8, 5, 4, 3, 2])

    def test_find_hand_rank_fully(self):
        game = play_a_round.Game("KH QH JH TH 3D")
        hand = "7D 7C 3C 3S 3D".split(" ")
        hand_rank, hand_type, pair_sorted_list, high_card_sorted_list = game.find_hand_rank_and_high_card(hand)

        self.assertEqual(hand_rank, 'x')
        self.assertEqual(hand_type, 'Full House: 3\'s over 7\'s')
        self.assertEqual(pair_sorted_list, [(3, 3), (7, 2)])
        self.assertEqual(high_card_sorted_list, [7, 7, 3, 3, 3])

if __name__ == '__main__':
    unittest.main()
