import os
import sys
import math
import operator
import re
from collections import *
from functools import *
from itertools import *
from os.path import exists
import bisect

import requests
from aoc import *
from dotenv import load_dotenv

load_dotenv()

DEV = False
PART2 = True

STRIP = True
SPLIT_LINES = True
SPLIT_CHAR = None
DATA = None
AOC_SESSION = os.environ.get('AOC_SESSION')
YEAR = 2023

CARD_RANKS = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2
}

CARD_RANKS_MODIFIED = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 1,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2
}

Hand = namedtuple('Hand', 'cards,bid,pairs')

class Solution:
    def __init__(self, data):
        if data and STRIP and type(data) == str:
            data = data.strip()
        if data and SPLIT_LINES and type(data) == str:
            data = data.splitlines()
        if data and SPLIT_CHAR is not None:
            if SPLIT_CHAR == '':
                data = [list(row) for row in data] if SPLIT_LINES else list(data)
            else:
                data = [row.split(SPLIT_CHAR) for row in data] if SPLIT_LINES else data.split(SPLIT_CHAR)
        self.data = data

    def _cmp_cards(self, hand1: Hand, hand2: Hand, most_common_1, most_common_2, RANKING):
        for i in range(len(most_common_1)):
            if most_common_1[i][1] == most_common_2[i][1]:
                continue
            return most_common_1[i][1] - most_common_2[i][1]

        for i in range(len(hand1.cards)):
            if hand1.cards[i] == hand2.cards[i]:
                continue
            return RANKING[hand1.cards[i]] - RANKING[hand2.cards[i]]

        return 0

    def cmp_cards(self, hand1: Hand, hand2: Hand):
        return self._cmp_cards(hand1, hand2, hand1.pairs.most_common(), hand2.pairs.most_common(), CARD_RANKS)

    def cmp_cards_modified(self, hand1: Hand, hand2: Hand):
        return self._cmp_cards(hand1, hand2, self.optimized_pairs(hand1).most_common(), self.optimized_pairs(hand2).most_common(), CARD_RANKS_MODIFIED)

    def optimized_pairs(self, hand: Hand):
        j = hand.pairs['J']
        if j == 0 or j == 5:
            return hand.pairs
        most_common = hand.pairs.most_common()
        for i in range(len(most_common)):
            if most_common[i][0] == 'J':
                continue
            return Counter(hand.cards.replace('J', most_common[i][0]))

        print('NO REPLACEMENT FOUND - SHOULD NOT HAPPEN', hand)
        return hand.pairs

    def first_part(self):
        result = 0
        hands = []
        for row in self.data:
            cards, bid = row.split()
            pairs = Counter(cards)
            hands.append(Hand(cards, int(bid), pairs))

        ranked = sorted(hands, key=cmp_to_key(self.cmp_cards_modified if PART2 else self.cmp_cards))
        for rank, hand in enumerate(ranked):
            print(rank+1, hand.cards, hand.bid)
            result += (rank+1)*hand.bid
        return result

    def second_part(self):
        return self.first_part()

if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DATA_URL = f"https://adventofcode.com/{YEAR}/day/{int(script)}/input"

    if not DATA:
        file_name = f"{script}-dev{DEV if type(DEV) != bool else ''}.txt" if DEV else f"{script}.txt"
        if exists(file_name):
            with open(file_name) as f:
                DATA = f.read()
        elif AOC_SESSION and DATA_URL:
            DATA = requests.get(DATA_URL, headers={'Cookie': f"session={AOC_SESSION}"}).text
            with open(file_name, "w") as f:
                f.write(DATA)

    print(f"DAY {int(script)}")
    s = Solution(DATA)
    print("RESULT", s.first_part() if not PART2 else s.second_part())
