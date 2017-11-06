import unittest
import play_a_round

from collections import Counter


class TestGameMethods(unittest.TestCase):

    def setUp(self):
        play_a_round.UNIQUE_CARD_COUNT = Counter()

    def test_parseBoard_too_much_input(self):
        with self.assertRaises(ValueError):
            play_a_round.Game("ab cd ef j l p q")

    def test_parseBoard_too_little_input(self):
        with self.assertRaises(ValueError):
            play_a_round.Game("ab cd ef")

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

    def test_find_hand_rank_four_pair(self):
        game = play_a_round.Game("KH QH JH TH 3D")
        hand = "7D 3H 3C 3S 3D".split(" ")
        hand_rank, hand_type, pair_sorted_list, high_card_sorted_list = game.find_hand_rank_and_high_card(hand)

        self.assertEqual(hand_rank, 'y')
        self.assertEqual(hand_type, 'Four 3\'s')
        self.assertEqual(pair_sorted_list, [(3, 4), (7, 1)])
        self.assertEqual(high_card_sorted_list, [7, 3, 3, 3, 3])

    def test_find_hand_rank_straight_flush(self):
        game = play_a_round.Game("KH QH JH TH 3D")
        hand = "8H 7H 6H 5H 4H".split(" ")
        hand_rank, hand_type, pair_sorted_list, high_card_sorted_list = game.find_hand_rank_and_high_card(hand)

        self.assertEqual(hand_rank, 'z')
        self.assertEqual(hand_type, '8 High Straight Flush')
        self.assertEqual(pair_sorted_list, [])
        self.assertEqual(high_card_sorted_list, [8, 7, 6, 5, 4])

    def test_find_hand_rank_royal_flush(self):
        game = play_a_round.Game("KH QH JH TH 3D")
        hand = "14H 13H 12H 11H 10H".split(" ")
        hand_rank, hand_type, pair_sorted_list, high_card_sorted_list = game.find_hand_rank_and_high_card(hand)

        self.assertEqual(hand_rank, 'z')
        self.assertEqual(hand_type, 'A Royal Flush')
        self.assertEqual(pair_sorted_list, [])
        self.assertEqual(high_card_sorted_list, [14, 13, 12, 11, 10])

    def test_best_hand_high_card(self):
        game = play_a_round.Game("4H 3S 7S 5H 2D")
        player = play_a_round.Player("test1 9H JC")
        game.best_hand(player)

        self.assertEqual(player.hand_rank, 'r')
        self.assertEqual(player.hand_type, 'Jack High')
        self.assertEqual(player.pair_sorted_list, [])
        self.assertEqual(player.high_card_sorted_list, [11, 9, 7, 5, 4])

    def test_best_hand_pair(self):
        game = play_a_round.Game("4H 3S 7S 5C 2D")
        player = play_a_round.Player("test1 5H JC")
        game.best_hand(player)

        self.assertEqual(player.hand_rank, 's')
        self.assertEqual(player.hand_type, 'A Pair of 5\'s')
        self.assertEqual(player.pair_sorted_list, [(5, 2), (11, 1), (7, 1), (4, 1)])
        self.assertEqual(player.high_card_sorted_list, [11, 7, 5, 5, 4])

    def test_best_hand_two_pair(self):
        game = play_a_round.Game("4H 3S 7S 5C JD")
        player = play_a_round.Player("test1 5H 4C")
        game.best_hand(player)

        self.assertEqual(player.hand_rank, 't')
        self.assertEqual(player.hand_type, 'Two Pairs: 5\'s and 4\'s')
        self.assertEqual(player.pair_sorted_list, [(5, 2), (4, 2), (11, 1)])
        self.assertEqual(player.high_card_sorted_list, [11, 5, 5, 4, 4])

    def test_best_hand_trips(self):
        game = play_a_round.Game("5S 3S 7S 5C JD")
        player = play_a_round.Player("test1 5H 4C")
        game.best_hand(player)

        self.assertEqual(player.hand_rank, 'u')
        self.assertEqual(player.hand_type, 'Three 5\'s')
        self.assertEqual(player.pair_sorted_list, [(5, 3), (11, 1), (7, 1)])
        self.assertEqual(player.high_card_sorted_list, [11, 7, 5, 5, 5])

    def test_best_hand_straight(self):
        game = play_a_round.Game("KS 3S 7S 5C JD")
        player = play_a_round.Player("test1 6H 4C")
        game.best_hand(player)

        self.assertEqual(player.hand_rank, 'v')
        self.assertEqual(player.hand_type, '7 High Straight')
        self.assertEqual(player.pair_sorted_list, [])
        self.assertEqual(player.high_card_sorted_list, [7, 6, 5, 4, 3])

    def test_best_hand_flush(self):
        game = play_a_round.Game("KS QS 7S 5S JD")
        player = play_a_round.Player("test1 4S 8S")
        game.best_hand(player)

        self.assertEqual(player.hand_rank, 'w')
        self.assertEqual(player.hand_type, 'King High Flush')
        self.assertEqual(player.pair_sorted_list, [])
        self.assertEqual(player.high_card_sorted_list, [13, 12, 8, 7, 5])

    def test_best_hand_full_house(self):
        game = play_a_round.Game("QS QC 7S 5S JD")
        player = play_a_round.Player("test1 7D 7C")
        game.best_hand(player)

        self.assertEqual(player.hand_rank, 'x')
        self.assertEqual(player.hand_type, 'Full House: 7\'s over Queen\'s')
        self.assertEqual(player.pair_sorted_list, [(7, 3), (12, 2)])
        self.assertEqual(player.high_card_sorted_list, [12, 12, 7, 7, 7])

    def test_best_hand_quads(self):
        game = play_a_round.Game("QS QC 7S 7H JD")
        player = play_a_round.Player("test1 7D 7C")
        game.best_hand(player)

        self.assertEqual(player.hand_rank, 'y')
        self.assertEqual(player.hand_type, 'Four 7\'s')
        self.assertEqual(player.pair_sorted_list, [(7, 4), (12, 1)])
        self.assertEqual(player.high_card_sorted_list, [12, 7, 7, 7, 7])

    def test_best_hand_straight_flush(self):
        game = play_a_round.Game("QS JS 7S 7H TS")
        player = play_a_round.Player("test1 9S 8S")
        game.best_hand(player)

        self.assertEqual(player.hand_rank, 'z')
        self.assertEqual(player.hand_type, 'Queen High Straight Flush')
        self.assertEqual(player.pair_sorted_list, [])
        self.assertEqual(player.high_card_sorted_list, [12, 11, 10, 9, 8])

    def test_best_hand_royal_flush(self):
        game = play_a_round.Game("QS JS 7S 7H TS")
        player = play_a_round.Player("test1 KS AS")
        game.best_hand(player)

        self.assertEqual(player.hand_rank, 'z')
        self.assertEqual(player.hand_type, 'A Royal Flush')
        self.assertEqual(player.pair_sorted_list, [])
        self.assertEqual(player.high_card_sorted_list, [14, 13, 12, 11, 10])

    def test_find_winner(self):
        game = play_a_round.Game("QS JS 7S 7H TS")
        p1 = play_a_round.Player("test1 6S AS")
        p2 = play_a_round.Player("test2 7D 2S")
        p3 = play_a_round.Player("test3 8S 3S")
        p4 = play_a_round.Player("test4 9D 4S")
        p5 = play_a_round.Player("test5 TD 5S")
        p2.pair_sorted_list = [(3, 2), (2, 2)]
        p3.pair_sorted_list = [(3, 2), (2, 2)]
        p4.pair_sorted_list = [(4, 2), (2, 2)]
        p2.high_card_sorted_list = [6, 5, 5, 2, 2]
        p3.high_card_sorted_list = [6, 5, 4, 2, 2]
        p1.hand_rank = 'r'
        p2.hand_rank = 't'
        p3.hand_rank = 't'
        p4.hand_rank = 't'
        p5.hand_rank = 'x'

        winner_list = game.find_winner([p1, p2, p3, p4, p5])

        self.assertEqual(winner_list[0].name, "test5")
        self.assertEqual(winner_list[1].name, "test4")
        self.assertEqual(winner_list[2].name, "test2")
        self.assertEqual(winner_list[3].name, "test3")
        self.assertEqual(winner_list[4].name, "test1")

if __name__ == '__main__':
    unittest.main()
