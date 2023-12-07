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

    def bi_right(self, time, distance, lo, hi):
        while (hi-lo) > 1:
            v = (lo+hi) >> 1
            d = (time-v) * v
            if d > distance:
                lo = v
            else:
                hi = v
        return lo

    def bi_left(self, time, distance, lo, hi):
        while (hi-lo) > 1:
            v = (lo+hi) >> 1
            d = (time-v)*v
            if d > distance:
                hi = v
            else:
                lo = v
        return hi


    def first_part(self):
        results = []
        times, distances = map(get_ints, self.data)

        for race in range(len(times)):
            options = []
            max_t = times[race]
            d = distances[race]
            q = deque([x for x in range(1,max_t)])
            while q:
                for i in range(len(q)):
                    t = q.popleft()
                    distance = (max_t-t)*t
                    if distance > d:
                        options.append(t)

            results.append(len(options))


        return reduce(operator.mul, results, 1)


    def parse_ints_as_single_number(self, s):
        return get_ints(s.replace(' ',''))[0]

    def second_part(self):
        time, distance = map(self.parse_ints_as_single_number, self.data)
        t = time >> 1
        l2 = self.bi_left(time, distance, 0, t)
        r2 = self.bi_right(time, distance, t, time)
        return r2-l2+1


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
