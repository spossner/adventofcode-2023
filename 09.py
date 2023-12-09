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
PART2 = False

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

    def first_part(self):
        result_n = 0
        result_p = 0

        for row in self.data:
            numbers = get_ints(row)
            stack = deque()
            stack.append(numbers)
            only_zeros = False
            while not only_zeros:
                only_zeros = True
                seq = stack[-1]
                diffs = []
                for i in range(len(seq)-1):
                    v = seq[i+1]-seq[i]
                    if v != 0:
                        only_zeros = False
                    diffs.append(v)
                if not only_zeros:
                    stack.append(diffs)

            v_n = 0
            v_p = 0
            while stack:
                seq = stack.pop()
                v_n = v_n + seq[-1]
                v_p = seq[0] - v_p
                seq.insert(0, v_p)
                seq.append(v_n)
            print(seq, v_p, v_n)
            result_n += v_n
            result_p += v_p


        return (result_n, result_p)

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
