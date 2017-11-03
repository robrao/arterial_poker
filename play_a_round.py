import itertools

from collections import defaultdict, Counter

'''
NOTES:
    - a lot input validation required
        --> need at least two players
        --> no card values that are not in deck
        --> no card suits that are not in deck
        --> need check to ensure same card is not used more than once in a game
    - Gamer winner / Tie breaker logic
        --> BEST HAND logic can be reused only needs method to recursively check high card if necessary
        --> Handle ties
        --> hand may need to be its own class, then might be a way to compare objects?
    - game output
    - function docstring
    - CATCH RAISED EXCEPTIONS in main, PRINT, AND EXIT GRACEFULLY
    - how to deal with a tie? both rank tie and full tie
    - README.md?
'''

FACE_VALUE_DICT = {
        'A': "14",
        'K': "13",
        'Q': "12",
        'J': "11",
        'T': "10",
        }


class Game(object):

    def __init__(self, board, number_of_players, players):
        self.board = self.__parseBoard__(board)
        self.num_players = number_of_players
        self.players = players

    def __parseBoard__(self, data):
        try:
            updated_cards = []
            cards = data.split(" ")

            for card in cards:
                val = FACE_VALUE_DICT.get(card[0], False)
                if val:
                    card = card.replace(card[0], val)
                updated_cards.append(card)
            # validate cards are as expected len 2 one char
            # one string, or two string means 10 or up
        except Exception as e:
            raise("The dealer is not playing by the rules!")

        return updated_cards

    def recursive_high_card_check(self, p1, p2):
        # Since recursive now need verify hand length before checking
        # needs tests asap.
        if "Straight" in p1.hand_type:
            # WHAT ABOUT TIES??
            if p1.high_card_sorted_list[0] < p2.high_card_sorted_list[0]:
                return True
            elif p1.high_card_sorted_list[0] == p2.high_card_sorted_list[0]:
                return "split pot"  # will eval as true for best_hand (because irrelevant if player ties self)
            else:
                return False
        elif "Flush" == p1.hand_type or "High Card" == p1.hand_type:
            if len(p1.high_card_sorted_list) == 0:
                return "split pot"
            elif p1.high_card_sorted_list[0] < p2.high_cardd_sorted_list[0]:
                return True
            elif p1.high_card_sorted_list[0] == p2.high_cardd_sorted_list[0]:
                p1.high_card_sorted_list.pop(0)
                p2.high_card_sorted_list.pop(0)
                return self.recursive_high_card_check(p1, p2)  # unnecessary recurrsion; turn in to a while loop
            else:
                return False
        elif "Full House" == p1.hand_type:
            if p1.pair_sorted_list[0][0] < p2.pair_sorted_list[0][0]:
                return True
            else:
                return False
        elif "Four of a kind" == p1.hand_type:
            if p1.pair_sorted_list[1][0] < p2.pair_sorted_list[1][0]:
                return True
            else:
                return False
        elif "Three of a kind" == p1.hand_type:
            if len(p1.pair_sorted_list) == 3:
                if p1.pair_sorted_list[0][0] < p2.pair_sorted_list[0][0]:
                    return True
                elif p1.pair_sorted_list[0][0] == p2.pair_sorted_list[0][0]:
                    p1.pair_sorted_list.pop(0)
                    p2.pair_sorted_list.pop(0)
                    return self.recursive_high_card_check(p1, p2)
                else:
                    return False
            else:
                if len(p1.high_card_sorted_list) == 0:
                    return "split pot"
                elif p1.high_card_sorted_list[0] < p2.high_card_sorted_list[0]:
                    return True
                elif p1.high_card_sorted_list[0] == p2.high_card_sorted_list[0]:
                    p1.high_card_sorted_list.pop(0)
                    p2.high_card_sorted_list.pop(0)
                    return self.recursive_high_card_check(p1, p2)
                else:
                    return False
        elif "Two Pair" == p1.hand_type:
            if len(p1.pair_sorted_list) > 2:
                if p1.pair_sorted_list[0][0] < p2.pair_sorted_list[0][0]:
                    return True
                elif p1.pair_sorted_list[0][0] == p2.pair_sorted_list[0][0]:
                    p1.pair_sorted_list.pop(0)
                    p2.pair_sorted_list.pop(0)
                    return self.recursive_high_card_check(p1, p2)
                else:
                    return False
            else:
                if len(p1.high_card_sorted_list) == 0:
                    return "split pot"
                elif p1.high_card_sorted_list[0] < p2.high_card_sorted_list[0]:
                    return True
                elif p1.high_card_sorted_list[0] == p2.high_card_sorted_list[0]:
                    p1.high_card_sorted_list.pop(0)
                    p2.high_card_sorted_list.pop(0)
                    return self.recursive_high_card_check(p1, p2)
                else:
                    return False
        elif "A Pair" == p1.hand_type:
            if len(p1.pair_sorted_list) == 4:
                if p1.pair_sorted_list[0][0] < p2.pair_sorted_list[0][0]:
                    return True
                elif p1.pair_sorted_list[0][0] == p2.pair_sorted_list[0][0]:
                    p1.pair_sorted_list.pop(0)
                    p2.pair_sorted_list.pop(0)
                    return self.recursive_high_card_check(p1, p2)
                else:
                    return False
            else:
                if len(p1.high_card_sorted_list) == 0:
                    return "split pot"
                elif p1.high_card_sorted_list[0] < p2.high_card_sorted_list[0]:
                    return True
                elif p1.high_card_sorted_list[0] == p2.high_card_sorted_list[0]:
                    p1.high_card_sorted_list.pop(0)
                    p2.high_card_sorted_list.pop(0)
                    return self.recursive_high_card_check(p1, p2)
                else:
                    return False


        # PAIRS -- check length of pair list and if shorted than expected means
        # pair has already been checked, so check high cards. This might result
        # in redundant checks, because pair value will be checked again, but its
        # negligible because only one check and it has already tied so no effect

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
            hand_value = ['z', "Straight Flush", [], sorted_hand]
        elif flush:
            hand_value = ['w', "Flush", [], sorted_hand]
        elif straight:
            hand_value = ['v', "Straight", [], sorted_hand]
        else:
            pairs = Counter(sorted_hand).items()
            sorted_pairs = sorted(pairs, reverse=True, key=lambda x: x[1])

            if sorted_pairs[0][1] == 4:
                hand_value = ['y', "Four of a kind", sorted_pairs]
            elif sorted_pairs[0][1] == 3 and sorted_pairs[1][1] == 2:
                hand_value = ['x', "Full House", sorted_pairs]
            elif sorted_pairs[0][1] == 3:
                hand_value = ['u', "Three of a kind", sorted_pairs, sorted_hand]
            elif sorted_pairs[0][1] == 2 and sorted_pairs[1][1] == 2:
                hand_value = ['t', "Two Pairs", sorted_pairs, sorted_hand]
            elif sorted_pairs[0][1] == 2:
                hand_value = ['s', "A Pair", sorted_pairs, sorted_hand]
            else:
                hand_value = ['r', "High card", [], sorted_hand]

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
            temp = Player("temp 2D 2H")  # random initialization; will be over written
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
            elif first_half[idx1].hand_rank < second_half[idx2].hand_rank:
                res = self.recursive_high_card_check(first_half[idx1], second_half[idx2])
            else:
                res = False

            if res == "split pot":
                ordered_list.append(first_half[idx1])
                ordered_list.append(second_half[idx2])
                idx1 += 1
                idx2 += 1
            elif res:
                ordered_list.append(second_half[idx2])
                idx2 += 1
            else:
                ordered_list.append(first_half[idx1])
                idx1 += 1

        return ordered_list


class Player(object):

    def __init__(self, data):
        name, card1, card2 = self.__parsePlayerData__(data)
        self.name = name
        self.hand = [card1, card2]
        self.hand_type = ""
        self.hand_rank = ""
        self.high_card_sorted_list = []
        self.pair_sorted_list = []
        self.flush = False
        self.straight = False
        self.pairs = defaultdict(int)
        self.high_card = None

    def __str__(self):
        return "{} {}".format(self.name, self.hand_type)

    def __parsePlayerData__(self, data):
        try:
            updated_cards = []
            name, card1, card2 = data.split(" ")

            for card in [card1, card2]:
                val = FACE_VALUE_DICT.get(card[0], False)
                if val:
                    card = card.replace(card[0], val)
                updated_cards.append(card)
            # validate cards are as expected len 2 one char
            # one string, or two string means 10 or up
        except Exception as err:
            msg = "Someone is not playing by the rules!\n{}".format(err)
            raise(msg)

        return name, updated_cards[0], updated_cards[1]

if __name__ == "__main__":
    # need to validate all input
    #TESTING number_of_players = raw_input("How many players do we have? ")
    #TESTING board = raw_input("Enter the board: ")

    number_of_players = "4"
    board = "2C 3D 4S 9H JH"
    player2 = Player("Mike 5S AD")
    player1 = Player("Rob QH QD")
    # player1 = Player("Rob 5H AC")
    player0 = Player("Bob 2C 2S")
    player3 = Player("Buns 7D 8C")

    players = [player0, player1, player2, player3]

    # players = []
    # for i in range(int(number_of_players)):
        # player_input = raw_input("Player {}: ".format(i+1))
        # players.append(Player(player_input))

    game = Game(board, number_of_players, players)

    # each player goes over board and finds best hand
    # https://docs.python.org/2/library/itertools.html#itertools.combinations
    for player in players:
        game.best_hand(player)


    # for player in players:
        # print player

    winner_list = game.find_winner(players)

    for w in winner_list:
        print w
