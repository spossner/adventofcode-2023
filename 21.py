import os
import sys
import math
import operator
import re
import time
from collections import *
from functools import *
from itertools import *
from os.path import exists
import bisect
import numpy as np

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
        self.data = self.parse_data(data)

    def parse_data(self, data):
        return data

    def dump_grid(self, seen):
        print()
        for y in range(len(self.data)):
            row = self.data[y]
            for x in range(len(row)):
                if (x,y) in seen:
                    print('O', end='')
                else:
                    print(row[x], end='')
            print()

    def reachable(self, n=64):
        if n > 64:
            data = []
            for i in range(5):
                for line in self.data:
                    data.append(5 * line.replace("S", "."))
        else:
            data = self.data

        bounds = Rect(0, 0, len(data[0]), len(data))
        start = Point(bounds.w // 2, bounds.h // 2)
        q = deque([start])

        for loop in range(n):
            seen = set()
            for i in range(len(q)):
                p = q.popleft()
                for adj in direct_adjacent_iter(p):
                    if adj not in bounds:
                        continue
                    if adj in seen:
                        continue
                    seen.add(adj)
                    if data[adj.y][adj.x] != '#':
                        q.append(adj)

            # self.dump_grid(q)
        return len(q)

    def first_part(self):
        return self.reachable_fields(64)

    def second_part(self):
        points = [(i, self.reachable(65 + i * 131)) for i in range(3)]
        # [(0, 3797), (1, 34009), (2, 94353)]
        print(points)
        return

        # Fit a quadratic polynomial (degree=2) through the points
        coefficients = np.polyfit(*zip(*points), 2)

        # Evaluate the quadratic equation at the given x value
        return round(np.polyval(coefficients, 202300))
        # 616583483179597 is correct

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
