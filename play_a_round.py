import itertools

from copy import deepcopy
from collections import Counter

'''
NOTES:
    - function docstring
    - README.md
    - Tests
'''

FACE_VALUE_DICT = {
        'A': "14",
        'K': "13",
        'Q': "12",
        'J': "11",
        'T': "10",
        }

VALUE_FACE_DICT = {
        14: "Ace",
        13: "King",
        12: "Queen",
        11: "Jack",
        10: "10",
        }

UNIQUE_CARD_COUNT = Counter()


def validate_cards(*cards):
    all_card_vals = ["A", "K", "Q", "J", "T"] + [str(i) for i in range(2, 10)]
    all_suit_vals = ["H", "D", "S", "C"]
    for card in cards:
        if UNIQUE_CARD_COUNT[card] > 0:
            msg = "{} card has been played more than once.".format(card)
            raise ValueError(msg)
        else:
            UNIQUE_CARD_COUNT[card] += 1

        if not card[0] in all_card_vals:
            msg = "'{}' is not a valid card value".format(card[0])
            raise ValueError(msg)

        if not card[1] in all_suit_vals:
            msg = "'{}' is not a valid card suit".format(card[1])
            raise ValueError(msg)


class Game(object):

    def __init__(self, board, players):
        self.board = self.__parseBoard__(board)
        self.players = players

    def __parseBoard__(self, data):
        updated_cards = []
        cards = data.split(" ")
        validate_cards(*cards)

        for card in cards:
            val = FACE_VALUE_DICT.get(card[0], False)
            if val:
                card = card.replace(card[0], val)
            updated_cards.append(card)
            # validate cards are as expected len 2 one char
            # one string, or two string means 10 or up

        return updated_cards

    def recursive_high_card_check(self, p1, p2, stack_level=0):
        """ Docstring Required """
        stack_level += 1
        if "v" in p1.hand_type:  # straight
            if p1.high_card_sorted_list[0] < p2.high_card_sorted_list[0]:
                return True
            elif p1.high_card_sorted_list[0] > p2.high_card_sorted_list[0]:
                return False
            else:
                return "split pot"
        elif p1.hand_rank in ["w", "r"]:  # Full House or High card
            for idx, card1 in enumerate(p1.high_card_sorted_list):
                p1.kicker = p1.high_card_sorted_list[0]
                p2.kicker = p2.high_card_sorted_list[0]
                if card1 < p2.high_card_sorted_list[idx]:
                    return True
                elif p2.high_card_sorted_list[idx] < card1:
                    return False

            return "split pot"
        elif "x" == p1.hand_type:  # full house
            if p1.pair_sorted_list[0][0] < p2.pair_sorted_list[0][0]:
                return True
            else:
                return False
        elif "y" == p1.hand_type:  # four of a kind
            if p1.pair_sorted_list[1][0] < p2.pair_sorted_list[1][0]:
                return True
            else:
                return False
        elif p1.hand_rank in ["u", "s"]:  # three of a kind
            if stack_level == 1:
                if p1.pair_sorted_list[0][0] < p2.pair_sorted_list[0][0]:
                    return True
                elif p1.pair_sorted_list[0][0] > p2.pair_sorted_list[0][0]:
                    return False
                else:
                    return self.recursive_high_card_check(p1, p2, stack_level)
            else:
                idx = stack_level - 2
                if stack_level > 6:
                    return "split pot"
                elif p1.high_card_sorted_list[idx] < p2.high_card_sorted_list[idx]:
                    p1.kicker = p1.high_card_sorted_list[idx]
                    p2.kicker = p2.high_card_sorted_list[idx]
                    return True
                elif p1.high_card_sorted_list[idx] > p2.high_card_sorted_list[idx]:
                    p1.kicker = p1.high_card_sorted_list[idx]
                    p2.kicker = p2.high_card_sorted_list[idx]
                    return False
                else:
                    return self.recursive_high_card_check(p1, p2, stack_level)
        else:
            idx = stack_level - 1
            if stack_level <= 2:
                if p1.pair_sorted_list[idx][0] < p2.pair_sorted_list[idx][0]:
                    return True
                elif p1.pair_sorted_list[idx][0] > p2.pair_sorted_list[idx][0]:
                    return False
                else:
                    return self.recursive_high_card_check(p1, p2, stack_level)
            else:
                idx = stack_level - 3
                if stack_level > 7:
                    return "split pot"
                elif p1.high_card_sorted_list[idx] < p2.high_card_sorted_list[idx]:
                    p1.kicker = p1.high_card_sorted_list[idx]
                    p2.kicker = p2.high_card_sorted_list[idx]
                    return True
                elif p1.high_card_sorted_list[idx] > p2.high_card_sorted_list[idx]:
                    p1.kicker = p1.high_card_sorted_list[idx]
                    p2.kicker = p2.high_card_sorted_list[idx]
                    return False
                else:
                    return self.recursive_high_card_check(p1, p2, stack_level)

    def find_hand_rank_and_high_card(self, hand):
        """Discover hand type and return rank and high card

        The rank of a hand is given by a letter. 'z' being the
        highest and 'a' being the lowest. Depending on the hand
        rank, one or two lists will be returned along with the
        rank.

        eg. if the hand is "Two Pair" it will have a list sorting
        the pairs by value and a list sorting all cards by value.

        """
        no_suit_hand = [int(x[:-1]) for x in hand]
        sorted_hand = sorted(no_suit_hand,  reverse=True)

        flush = hand[0][-1] == hand[1][-1] == hand[2][-1] == hand[3][-1] == hand[4][-1]
        regular_straight = sum([sorted_hand[idx] - val for idx, val in enumerate(sorted_hand[1:])]) == 4
        bicycle_straight = sum([0 if x == sorted_hand[idx] else 1 for idx, x in enumerate([14, 5, 4, 3, 2])]) == 0
        straight = regular_straight or bicycle_straight

        if straight and flush:
            if sorted_hand[0] == 14:
                label = "A Royal Flush"
            else:
                val = sorted_hand[0]
                face_val = VALUE_FACE_DICT.get(val, val)
                label = "{} High Straight Flush".format(face_val)
            hand_value = ['z', label, [], sorted_hand]
        elif flush:
            val = sorted_hand[0]
            face_val = VALUE_FACE_DICT.get(val, val)
            label = "{} High Flush".format(face_val)
            hand_value = ['w', label, [], sorted_hand]
        elif straight:
            val = sorted_hand[0]
            face_val = VALUE_FACE_DICT.get(val, val)
            label = "{} High Straight".format(face_val)
            hand_value = ['v', label, [], sorted_hand]
        else:
            pairs = Counter(sorted_hand).items()
            sorted_pairs = sorted(pairs, reverse=True, key=lambda x: x[1])

            if sorted_pairs[0][1] == 4:
                pair = sorted_pairs[0][0]
                face_val = VALUE_FACE_DICT.get(pair, pair)
                label = "Four {}'s".format(face_val)
                hand_value = ['y', label, sorted_pairs]
            elif sorted_pairs[0][1] == 3 and sorted_pairs[1][1] == 2:
                pair1 = sorted_pairs[0][0]
                pair2 = sorted_pairs[1][0]
                face_val1 = VALUE_FACE_DICT.get(pair1, pair1)
                face_val2 = VALUE_FACE_DICT.get(pair2, pair2)
                label = "Full House: {}'s over {}".format(face_val1, face_val2)
                hand_value = ['x', label, sorted_pairs]
            elif sorted_pairs[0][1] == 3:
                pair = sorted_pairs[0][0]
                face_val = VALUE_FACE_DICT.get(pair, pair)
                label = "Three {}'s".format(face_val)
                hand_value = ['u', label, sorted_pairs, sorted_hand]
            elif sorted_pairs[0][1] == 2 and sorted_pairs[1][1] == 2:
                pair1 = sorted_pairs[0][0]
                pair2 = sorted_pairs[1][0]
                face_val1 = VALUE_FACE_DICT.get(pair1, pair1)
                face_val2 = VALUE_FACE_DICT.get(pair2, pair2)
                label = "Two Pairs: {}'s and {}'s".format(face_val1, face_val2)
                hand_value = ['t', label, sorted_pairs, sorted_hand]
            elif sorted_pairs[0][1] == 2:
                pair = sorted_pairs[0][0]
                face_val = VALUE_FACE_DICT.get(pair, pair)
                label = "A Pair of {}'s".format(face_val)
                hand_value = ['s', label, sorted_pairs, sorted_hand]
            else:
                high_card = sorted_hand[0]
                face_val = VALUE_FACE_DICT.get(high_card, high_card)
                label = "{} High".format(face_val)
                hand_value = ['r', label, [], sorted_hand]

        return hand_value

    def best_hand(self, player):  # Rename to WINNING HAND
        '''Find best hand it list of possible hands

        Assign value to hand_type by creating arbitrary value system.
        straight flush most points, and then bonus for high card. Need
        to figure out this bonus for high card more specifically...

        Add proper doc string!!!

        rank, sorted_hand; 'z' is the highest rank and 'a' is the lowest.
        '''

        if player.hand_rank == "":
            player.hand_rank = "a"
            temp = deepcopy(player)
            players_cards = self.board + player.hand
            all_hands = itertools.combinations(players_cards, 5)

            for hand in all_hands:
                temp.hand_rank, temp.hand_type, temp.pair_sorted_list, temp.high_card_sorted_list = self.find_hand_rank_and_high_card(hand)

                if player.hand_rank < temp.hand_rank:
                    player.hand_rank = temp.hand_rank
                    player.hand_type = temp.hand_type
                    player.pair_sorted_list = temp.pair_sorted_list
                    player.high_card_sorted_list = temp.high_card_sorted_list
                elif player.hand_rank == temp.hand_rank and self.recursive_high_card_check(player, temp):
                    player.hand_rank = temp.hand_rank
                    player.hand_type = temp.hand_type
                    player.pair_sorted_list = temp.pair_sorted_list
                    player.high_card_sorted_list = temp.high_card_sorted_list

            player.kicker = None

    def find_winner(self, players):
        """Implementing merge sort to find winner

        If know at the top of the stack can check if the pot is split and amoungst who
        """
        if len(players) == 1:
            return players
        else:
            first_half = self.find_winner(players[:len(players)/2])
            second_half = self.find_winner(players[len(players)/2:])

        idx1 = 0
        idx2 = 0
        ordered_list = []
        len_first = len(first_half)
        len_second = len(second_half)

        while not (idx1 + idx2) == (len_first + len_second):
            if idx1 == len_first:
                ordered_list.append(second_half[idx2])
                idx2 += 1
                continue
            elif idx2 == len_second:
                ordered_list.append(first_half[idx1])
                idx1 += 1
                continue

            if first_half[idx1].hand_rank < second_half[idx2].hand_rank:
                res = True
            elif first_half[idx1].hand_rank == second_half[idx2].hand_rank:
                res = self.recursive_high_card_check(first_half[idx1], second_half[idx2])
            else:
                res = False

            if res == "split pot":
                first_half[idx1].split = True
                ordered_list.append(first_half[idx1])
                idx1 += 1
            elif res:
                ordered_list.append(second_half[idx2])
                idx2 += 1
            else:
                ordered_list.append(first_half[idx1])
                idx1 += 1

        return ordered_list

    def display_results(self, winner_list):
        # check for split pot, and amount how many
        position = 1
        for w in winner_list:
            output = "{} {} {}".format(position, w.name, w.hand_type)

            if w.kicker:
                face = VALUE_FACE_DICT.get(w.kicker, w.kicker)
                output = output + " with a {} kicker".format(face)

            print output

            if not w.split:
                position += 1


class Player(object):

    def __init__(self, data):
        name, card1, card2 = self.__parsePlayerData__(data)
        self.name = name
        self.hand = [card1, card2]
        self.hand_type = ""
        self.hand_rank = ""
        self.high_card_sorted_list = []
        self.pair_sorted_list = []
        self.kicker = None
        self.split = False

    def __str__(self):
        return "{} {}".format(self.name, self.hand_type)

    def __parsePlayerData__(self, data):
        updated_cards = []
        name, card1, card2 = data.split(" ")
        validate_cards(card1, card2)

        for card in [card1, card2]:
            val = FACE_VALUE_DICT.get(card[0], False)
            if val:
                card = card.replace(card[0], val)
            updated_cards.append(card)
            # validate cards are as expected len 2 one char
            # one string, or two string means 10 or up

        return name, updated_cards[0], updated_cards[1]


def main():
    try:
        number_of_players = int(raw_input("How many players do we have? ").strip())
    except ValueError as err:
        print "** Ensure that the input was a number **"
        return

    if number_of_players < 2:
        print "** It takes atleast two players to play. **"
        return

    # board = raw_input("Enter the board: ").strip().upper()

    number_of_players = "5"
    board = "QD 1D 4S 9H JH"
    player_inputs = ["Mike 9S 2D", "Rob 5H JC", "Bob 2C 2S", "Buns 7D 8C", "Gisele 9D TH"]

    players = []
    try:
        for i in range(int(number_of_players)):
            # player_input = raw_input("Player {}: ".format(i+1)).strip().upper()
            player_input = player_inputs[i]
            players.append(Player(player_input))

        game = Game(board, players)
    except Exception as err:
        print err
        return

    # each player goes over board and finds best hand
    # https://docs.python.org/2/library/itertools.html#itertools.combinations
    for player in players:
        game.best_hand(player)

    # for player in players:
        # print player
    winner_list = game.find_winner(players)
    game.display_results(winner_list)

if __name__ == "__main__":
    main()
