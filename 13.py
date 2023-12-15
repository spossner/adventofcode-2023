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
from typing import List

import requests
from aoc import *
from dotenv import load_dotenv

load_dotenv()

DEV = False
PART2 = True

STRIP = True
SPLIT_LINES = False
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


    def transpose(self, matrix):
        return [list(x) for x in zip(*matrix)]

    def is_complete_reflection(self, pattern, i):
        return all(pattern[a] == pattern[b] for a, b in zip(range(i, -1, -1), range(i + 1, len(pattern))))

    def reflexion(self, pattern):
        for i in range(len(pattern) - 1):
            if self.is_complete_reflection(pattern, i):
                return i + 1
        return 0

    def reflexions_iter(self, pattern):
        for i in range(len(pattern) - 1):
            if self.is_complete_reflection(pattern, i):
                yield i + 1 # now we may have multiple reflexions in corrected patterns - use iterator

    def corrections_iter(self, pattern):
        for y in range(len(pattern)):
            for x in range(len(pattern[0])):
                pattern2 = [row[:] for row in pattern]
                pattern2[y][x] = "#" if pattern2[y][x] == "." else "."
                yield pattern2

    def correct(self, pattern):
        for pattern2 in self.corrections_iter(pattern):
            for new_reflexion in self.reflexions_iter(pattern2):
                if new_reflexion != self.reflexion(pattern):
                    return new_reflexion
        return 0

    def first_part(self):
        result = 0

        patterns = [[[c for c in row] for row in pattern.splitlines()] for pattern in self.data.split("\n\n")]
        for pattern in patterns:
            result += self.reflexion(self.transpose(pattern)) + 100 * self.reflexion(pattern)

        return result

    def second_part(self):
        result = 0

        patterns = [[[c for c in row] for row in pattern.splitlines()] for pattern in self.data.split("\n\n")]
        for pattern in patterns:
            result += self.correct(self.transpose(pattern)) + 100 * self.correct(pattern)

        return result
        # 20277 too low
        # 34795 -> multiple reflexions in modified patterns


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
