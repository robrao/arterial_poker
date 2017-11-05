import unittest
import itertools
import play_a_round

from collections import Counter

SUITS = 'CDHS'
RANKS = '23456789TJQKA'
DECK = tuple(''.join(card) for card in itertools.product(RANKS, SUITS))


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        play_a_round.UNIQUE_CARD_COUNT = Counter()

    def test_all_valid_cards(self):
        play_a_round.validate_cards(*DECK)

    def test_all_valid_cards_lower_case_suit(self):
        lower_deck = [c.lower() for c in DECK]
        play_a_round.validate_cards(*lower_deck)

    def test_same_card_played_twice(self):
        cards = ["2H", "2H"]

        with self.assertRaises(ValueError):
            play_a_round.validate_cards(*cards)

    def test_invalid_card_value(self):
        cards = ["2H", "1D"]

        with self.assertRaises(ValueError):
            play_a_round.validate_cards(*cards)

    def test_invalid_card_suit(self):
        cards = ["2H", "2T"]

        with self.assertRaises(ValueError):
            play_a_round.validate_cards(*cards)

if __name__ == '__main__':
    unittest.main()
