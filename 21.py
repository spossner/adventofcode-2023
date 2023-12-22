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

import requests
from aoc import *
from dotenv import load_dotenv

load_dotenv()

DEV = True
PART2 = True

STRIP = True
SPLIT_LINES = True
SPLIT_CHAR = ''
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

    def first_part(self):
        result = 0
        start = None
        bounds = Rect(0, 0, len(self.data[0]), len(self.data))
        for y, x in product(range(bounds.h), range(bounds.w)):
            if self.data[y][x] == 'S':
                start = Point(x,y)
                break

        q = deque([start])

        for loop in range(64):
            seen = set()
            for i in range(len(q)):
                p = q.popleft()
                for adj in direct_adjacent_iter(p):
                    if adj not in bounds:
                        continue
                    if adj in seen:
                        continue
                    seen.add(adj)
                    if self.data[adj.y][adj.x] != '#':
                        q.append(adj)

            # self.dump_grid(q)
        return len(q)

    def second_part(self):
        start = None
        increase = []
        bounds = Rect(0, 0, len(self.data[0]), len(self.data))
        for y, x in product(range(bounds.h), range(bounds.w)):
            if self.data[y][x] == 'S':
                start = Point(x, y)
                break

        q = deque([start])
        already_found = set()

        for loop in range(100):
            seen = set()
            for i in range(len(q)):
                p = q.popleft()
                for adj in direct_adjacent_iter(p):
                    nx = adj.x % bounds.w
                    ny = adj.y % bounds.h
                    if self.data[ny][nx] == '#':
                        continue
                    if adj in seen:
                        continue
                    seen.add(adj)
                    if self.data[ny][nx] != '#':
                        q.append(adj)

            new_found = seen.difference(already_found)
            if loop % 2 == 1:
                increase.append((loop, len(new_found)))
            # if loop % 2 == 1:
            #     print("-----------")
                # print(list(map(lambda p:(p,manhattan_distance(start, p)),new_found)))
                # c = Counter(map(lambda x:x[-1], new_found))
                # print(loop, len(new_found))
            already_found.update(seen)
            # self.dump_grid(q)

        print(increase)
        return len(q)


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
