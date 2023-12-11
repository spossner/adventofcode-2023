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

    def translate(self, p: Point):
        return Point(p.x+self.offsets_x[p.x], p.y+self.offsets_y[p.y])

    def first_part(self):
        result = 0

        points = []
        m = len(self.data)
        n = len(self.data[0])
        filled_columns = set()
        filled_rows = set()
        for y, row in enumerate(self.data):
            for x, c in enumerate(row):
                if c == '#':
                    filled_columns.add(x)
                    filled_rows.add(y)
                    points.append(Point(x,y))

        expand_factor = 999_999

        self.offsets_x = []
        self.offsets_y = []
        o = 0
        for x in range(n):
            self.offsets_x.append(o)
            if x not in filled_columns:
                o += expand_factor

        o = 0
        for y in range(m):
            self.offsets_y.append(o)
            if y not in filled_rows:
                o += expand_factor

        translated_points = list(map(self.translate, points))

        # print(points, translated_points)
        for p1, p2 in combinations(translated_points, 2):
            d = manhattan_distance(p1,p2)
            # print(p1, p2, d)
            result += d

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
