import itertools

from collections import defaultdict, Counter

'''
NOTES:
    - a lot input validation required
        --> need at least two players
        --> no card values that are not in deck
        --> need check to ensure same card is not used more than once in a game
    - Gamer winner / Tie breaker logic
        --> BEST HAND logic can be reused only needs method to recursively check high card if necessary
    - game output
    - function docstring
    - CATCH RAISED EXCEPTIONS in main, PRINT, AND EXIT GRACEFULLY
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

    def best_hand(self, all_hands):
        '''Find best hand it list of possible hands

        Assign value to hand_type by creating arbitrary value system.
        straight flush most points, and then bonus for high card. Need
        to figure out this bonus for high card more specifically...

        Add proper doc string!!!

        rank, sorted_hand; 'z' is the highest rank and 'a' is the lowest.
        '''

        best_hand = ('a')

        for hand in all_hands:
            no_suit_hand = [int(x[:-1]) for x in hand]
            sorted_hand = sorted(no_suit_hand,  reverse=True)

            flush = hand[0][-1] == hand[1][-1] == hand[2][-1] == hand[3][-1] == hand[4][-1]
            regular_straight = sum([sorted_hand[idx] - val for idx, val in enumerate(sorted_hand[1:])]) == 4
            bicycle_straight = sum([0 if x == sorted_hand[idx] else 1 for idx, x in enumerate([14, 5, 4, 3, 2])]) == 0
            straight = regular_straight or bicycle_straight

            if straight and flush:
                if best_hand[0] < 'z':
                    best_hand = ('z', "Straight Flush", sorted_hand)
                elif best_hand[0] == 'z' and best_hand[1][0] < sorted_hand[0]:
                    best_hand = ('z', "Straight Flush", sorted_hand)
            elif flush:
                if best_hand[0] < 'w':
                    best_hand = ('w', "Flush", sorted_hand)
                elif best_hand[0] == 'w' and best_hand[1][0] < sorted_hand[0]:
                    best_hand = ('w', "Flush", sorted_hand)
            elif straight:
                if best_hand[0] < 'v':
                    best_hand = ('v', "Straight", sorted_hand)
                elif best_hand[0] == 'v' and best_hand[1][0] < sorted_hand[0]:
                    best_hand = ('v', "Straight", sorted_hand)
            else:
                pairs = Counter(sorted_hand).items()
                sorted_pairs = sorted(pairs, reverse=True, key=lambda x: x[1])

                if sorted_pairs[0][1] == 4:
                    if best_hand[0] < 'y':
                        best_hand = ('y', "Four of a kind", sorted_pairs)
                    elif best_hand == 'y' and best_hand[1][0] < sorted_pairs[0][0]:
                        best_hand = ('y', "Four of a kind", sorted_pairs)
                elif sorted_pairs[0][1] == 3 and sorted_pairs[1][1] == 2:
                    if best_hand[0] < 'x':
                        best_hand = ('x', "Full House", sorted_pairs)
                    elif best_hand == 'x' and best_hand[1][0] < sorted_pairs[0][0]:
                        best_hand = ('x', "Full House", sorted_pairs)
                elif sorted_pairs[0][1] == 3:
                    if best_hand[0] < 'u':
                        best_hand = ('u', "Three of a kind", sorted_pairs, sorted_hand)
                    elif best_hand == 'u' and best_hand[1][0] < sorted_pairs[0][0]:
                        best_hand = ('u', "Three of a kind", sorted_pairs, sorted_hand)
                elif sorted_pairs[0][1] == 2:
                    if best_hand[0] < 't':
                        best_hand = ('t', "A Pair", sorted_pairs, sorted_hand)
                    elif best_hand == 't' and best_hand[1][0] < sorted_pairs[0][0]:
                        best_hand = ('t', "A Pair", sorted_pairs, sorted_hand)
                else:
                    if best_hand[0] < 's':
                        best_hand = ('s', "High Card", sorted_hand)
                    elif best_hand == 's' and best_hand[1][0] < sorted_pairs[0][0]:
                        best_hand = ('s', "High Card", sorted_hand)

        return best_hand

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


class Player(object):

    def __init__(self, data):
        name, card1, card2 = self.__parsePlayerData__(data)
        self.name = name
        self.hand = [card1, card2]
        self.hand_type = ""
        self.hand_rank = ""
        self.high_card = 0
        self.flush = False
        self.straight = False
        self.pairs = defaultdict(int)
        self.high_card = None

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
        players_cards = game.board + player.hand
        all_possible_hands = itertools.combinations(players_cards, 5)

        player.hand = game.best_hand(all_possible_hands)

    print players[0].hand
        
