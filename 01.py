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

NUMS = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

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

    def first_part(self):
        result = 0
        for row in self.data:
            d1, d2 = None, None
            for i in range(len(row)):
                if not d1 and row[i].isnumeric():
                    d1 = int(row[i])
                if not d2 and row[-i-1].isnumeric():
                    d2 = int(row[-i-1])
                if d1 and d2:
                    break
            n = d1*10+d2
            result += n
            print(n)


        return result



    def parseNumber(self, text, start):
        for digit, value in NUMS.items():
            if text.find(digit, start) == start:
                return value
        return None

    def second_part(self):
        result = 0
        for row in self.data:
            d1, d2 = None, None
            for i in range(len(row)):
                if not d1:
                    if row[i].isnumeric():
                        d1 = int(row[i])
                    else:
                        spelled_number = self.parseNumber(row, i)
                        if spelled_number:
                            d1 = spelled_number
                if not d2:
                    if row[-i - 1].isnumeric():
                        d2 = int(row[-i - 1])
                    else:
                        spelled_number = self.parseNumber(row, len(row)-i-1)
                        if spelled_number:
                            d2 = spelled_number
                if d1 and d2:
                    break
            n = d1 * 10 + d2
            result += n
            print(row, n)

        return result


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
