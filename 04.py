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

    def parse_numbers(self, row):
        row_id, numbers = row.split(':')
        row_id = get_ints(row_id)[0]
        my_numbers, winning_numbers = map(set, map(get_ints, numbers.split('|')))
        return (row_id, my_numbers, winning_numbers, my_numbers.intersection(winning_numbers))

    def first_part(self):
        result = 0

        for row in self.data:
            row_id, my_numbers, winning_numbers, matching_numbers = self.parse_numbers(row)
            points = int(pow(2,len(matching_numbers)-1))
            result += points

        return result

    def second_part(self):
        cards = defaultdict(int)
        max_card = len(self.data)
        for row in self.data:
            row_id, my_numbers, winning_numbers, matching_numbers = self.parse_numbers(row)
            cards[row_id] += 1
            for i in range(row_id+1,row_id+1+len(matching_numbers)):
                if i > max_card:
                    continue
                cards[i] += cards[row_id]

        return sum(cards.values())


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
