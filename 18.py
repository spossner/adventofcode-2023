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
from PIL import Image

load_dotenv()

DEV = False
PART2 = True

STRIP = True
SPLIT_LINES = True
SPLIT_CHAR = None
DATA = None
AOC_SESSION = os.environ.get('AOC_SESSION')
YEAR = 2023

ABSOLUT_DIRECTIONS = {
    'R': EAST,
    'U': NORTH,
    'D': SOUTH,
    'L': WEST,
}

ENCODED_DIRECTIONS = {
    '0': EAST,
    '3': NORTH,
    '1': SOUTH,
    '2': WEST,
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

    def gauss_area(self, points):
        # doing the stuff with math and gauss (https://www.geodose.com/2021/09/how-calculate-polygon-area-unordered-coordinates-points-python.html)
        # ...after second part was revealed :-D
        result = 0
        for i in range(len(points)):
            p = points[i]
            q = points[(i+1) % len(points)]
            result += (p.x*q.y - p.y*q.x)
        return result // 2

    def first_part(self):
        # refactored to math approach..
        pos = Point(0, 0)
        points = [pos]
        outline = 0
        data = [re.match(r"(\w) (\d+) \(#(\w*)\)", row).groups() for row in self.data]
        for direction, steps, color in data:
            n = int(steps)
            pos = translate(pos, ABSOLUT_DIRECTIONS[direction], n)
            points.append(pos)
            outline += n

        print(points)
        return self.gauss_area(points) + outline // 2 + 1

    def second_part(self):
        pos = Point(0,0)
        points = [pos]
        outline = 0
        data = [re.match(r"(\w) (\d+) \(#(\w*)\)", row).groups() for row in self.data]
        for i, v in enumerate(data):
            color = v[2]
            steps = int(color[:-1], 16)
            outline += steps
            direction = ENCODED_DIRECTIONS[color[-1]]
            pos = translate(pos, direction, steps)
            points.append(pos)

        print(points)
        return self.gauss_area(points) + (outline // 2) + 1 # inner area + outline which was also digged out


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
