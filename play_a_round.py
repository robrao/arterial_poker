import itertools

from copy import deepcopy
from collections import Counter


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
UNIQUE_PLAYER_NAMES = Counter()


def validate_cards(*cards):
    """ Ensure that card inputs are unique and valid """
    all_card_vals = ["A", "K", "Q", "J", "T"] + [str(i) for i in range(2, 10)]
    all_suit_vals = ["H", "D", "S", "C"]

    for card in cards:
        card = card.upper()

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
    """ Handles all the game logic, and holds all cards on the board """

    def __init__(self, board):
        self.board = self.__parseBoard__(board)

    def __parseBoard__(self, data):
        """ Ensure information entered for board is valid """
        updated_cards = []
        cards = data.split(" ")

        if not len(cards) == 5:
            msg = "** Expecting 5 cards, but got {}. **".format(len(cards))
            raise ValueError(msg)

        validate_cards(*cards)

        for card in cards:
            val = FACE_VALUE_DICT.get(card[0], False)
            if val:
                card = card.replace(card[0], val)
            updated_cards.append(card)

        return updated_cards

    def recursive_high_card_check(self, p1, p2, stack_level=0):
        """ Compares hands that have a matching rank

        Start comparison from most valuable card to least valuable.

        input:
            p1 = Player
            p2 = Player

        output:
            p1 < p2 = True
            p1 > p2 = False
            p1 == p2 = "split pot"
        """
        stack_level += 1
        if p1.hand_rank in ["v", "z"]:  # straight
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
        elif "x" == p1.hand_rank:  # full house
            if p1.pair_sorted_list[0][0] < p2.pair_sorted_list[0][0]:
                return True
            else:
                return False
        elif "y" == p1.hand_rank:  # four of a kind
            if p1.pair_sorted_list[1][0] < p2.pair_sorted_list[1][0]:
                return True
            else:
                return False
        elif p1.hand_rank in ["u", "s"]:  # three of a kind or a pair
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
        else:  # two pair
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
        highest and 'a' being the lowest. Two lists will be
        returned along side the rank and label for the hand. One
        list will be a list of sorted pairs, if there are any,
        and a list of cards sorted by descending value.

        input:
            hand = ['5H', '6D', '5C', '7C', '6H']

        output:
            ['t', "Two Pairs: 6's and 5's", [(6, 2), (5, 2), (7, 1)], [7, 6, 6, 5, 5]

        """
        no_suit_hand = [int(x[:-1]) for x in hand]
        sorted_hand = sorted(no_suit_hand,  reverse=True)

        flush = hand[0][-1] == hand[1][-1] == hand[2][-1] == hand[3][-1] == hand[4][-1]
        regular_straight = sum([(sorted_hand[idx] - val) == 1 for idx, val in enumerate(sorted_hand[1:])]) == 4
        bicycle_straight = sum([0 if x == sorted_hand[idx] else 1 for idx, x in enumerate([14, 5, 4, 3, 2])]) == 0

        if bicycle_straight:
            sorted_hand = [x for x in sorted_hand[1:]]
            sorted_hand.append(14)

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
            sorted_pairs = sorted(pairs, reverse=True, key=lambda x: (x[1], x[0]))

            if sorted_pairs[0][1] == 4:
                pair = sorted_pairs[0][0]
                face_val = VALUE_FACE_DICT.get(pair, pair)
                label = "Four {}'s".format(face_val)
                hand_value = ['y', label, sorted_pairs, sorted_hand]
            elif sorted_pairs[0][1] == 3 and sorted_pairs[1][1] == 2:
                pair1 = sorted_pairs[0][0]
                pair2 = sorted_pairs[1][0]
                face_val1 = VALUE_FACE_DICT.get(pair1, pair1)
                face_val2 = VALUE_FACE_DICT.get(pair2, pair2)
                label = "Full House: {}'s over {}'s".format(face_val1, face_val2)
                hand_value = ['x', label, sorted_pairs, sorted_hand]
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

    def best_hand(self, player):
        """Find best hand it list of possible hands

        Update Player with best hand and associated values
        based on all possible hands s/he can play.

        input:
            Player

        output:
            Player.hand_rank
            Player.hand_type
            Player.pair_sorted_list
            Player.high_card_sorted_list
        """

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
        """ Using merge sort to find winner

        Recusively iterate through all players and order
        them by most value hand to least valuable.

        input:
            players = [Player1, ..., Player5]

        output:
            ordered_list = [Player3, Player5, ...]
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
        """ Display results of the game

        List players from first to last place. If there is a
        draw the players will be listed as finishing in the
        same position.

        eg.

        1 Dave A Royal Flush
        2 Rob Two Pairs: 7's and 3's
        2 Mike Two pairs: 7's and 3's
        3 Greg Ace High

        """
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
    """ Maintains player logic and hand value """

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

    def __validate_player_name__(self, name):
        """ Ensure each player has a unique name to prevent confusion. """
        if UNIQUE_PLAYER_NAMES[name] > 0:
            msg = "** Each player must have a unique name to prevent confusion.\n{} has been used more than once **".format(name)
            raise ValueError(msg)
        else:
            UNIQUE_PLAYER_NAMES[name] += 1

    def __parsePlayerData__(self, data):
        """ Parse all Player input data """
        updated_cards = []

        try:
            name, card1, card2 = data.split(" ")
        except Exception as err:
            msg = "** Invalid data entered for a player. **"
            raise ValueError(msg)

        self.__validate_player_name__(name)
        validate_cards(card1, card2)

        for card in [card1, card2]:
            val = FACE_VALUE_DICT.get(card[0], False)
            if val:
                card = card.replace(card[0], val)
            updated_cards.append(card)

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

    board = raw_input("Enter the board: ").strip().upper()

    players = []
    try:
        for i in range(int(number_of_players)):
            player_input = raw_input("Player {}: ".format(i+1)).strip().upper()
            players.append(Player(player_input))

        game = Game(board)
    except Exception as err:
        print err
        return

    for player in players:
        game.best_hand(player)

    winner_list = game.find_winner(players)
    game.display_results(winner_list)

if __name__ == "__main__":
    main()
