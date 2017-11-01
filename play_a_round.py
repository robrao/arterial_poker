import itertools

from collections import defaultdict

'''
NOTES:
    - a lot input validation required
        --> need at least two players
        --> no card values that are not in deck
    - best method to find hand
    - best method to decipher card > 9
        --> probably best to just use regex looking for K etc
    - best method to determine winner
        --> assign point system to hands; eg. Royal Flush = 15
        --> if tie in type of hand check high card
        --> also need to be aware if board has high card and its a draw
    - best method to find hard
        --> probably regex: may not work the best...
        how to search for straight, need atleast 5 cards/matches...
    - regex to ignore case
    - Best speed would need a lookup table which would require 7936 entries...
    - Prime number idea makes sense
        --> how would value of flush be accounted for?
        --> how do you what hand they have?
    - are all imports being used
'''

FACE_VALUE_DICT = {
        'A': "14",
        'K': "13",
        'Q': "12",
        'J': "11",
        'T': "10",
        }


class Game(object):
    flush_regex = ""
    straight_regex = ""
    pair_count_regex = ""

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
        '''

        # alot of these are doing redundant checks
        # each assigns point value, hand_type, and
        # calls function to find high card
        # high card function adds additonal value
        # high card is not necessairly highest card, but
        # card(s) that give most value ie. 3 3s in a full house

        # ** for a full house probably want to display full hand
        for hand in all_hands:
            sorted_hand = sorted(hand, key=int(x[:-1]), reverse=True) # SORTING NOT WORKING!!!
            print "{} --> {}".format(hand, sorted_hand)
            # flush = hand[0][1] and hand[1][1] and hand[2][1] and hand[3][1] and hand[4][1]
            # straight = [int(hand[idx-1][:-1]) - int(val[:-1]) for idx, val in enumerate(hand[1:])]
            # print "{} -- {}".format(hand, straight)
        # if straight_flush:
            # pass
        # elif four_of_a_kind:
            # pass
        # elif full_house:
            # pass
        # elif flush:
            # pass
        # elif straight:
            # pass
        # elif three_pair:
            # pass
        # elif two_pair:
            # pass
        # elif pair:
            # pass
        # else:
            # #high card
            # pass
        pass

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
        self.hand_value = 0
        self.high_card = ""
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

    number_of_players = "3"
    board = "2C 3D 4S 9H JH"
    player1 = Player("Rob QH QD")
    player2 = Player("Bob 2C 2S")
    player3 = Player("Buns 7D 8C")

    players = [player1, player2, player3]

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

        break

    # now looking over each players best hand find winner
        
