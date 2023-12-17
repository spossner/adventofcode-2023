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
SPLIT_CHAR = ''
DATA = None
AOC_SESSION = os.environ.get('AOC_SESSION')
YEAR = 2023

REFLEXIONS = {
    ('/', EAST): NORTH,
    ('/', NORTH): EAST,
    ('/', WEST): SOUTH,
    ('/', SOUTH): WEST,

    ('\\', EAST): SOUTH,
    ('\\', SOUTH): EAST,
    ('\\', WEST): NORTH,
    ('\\', NORTH): WEST,
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

    def simulate(self, start, direction):
        bounds = Rect(0, 0, len(self.data[0]), len(self.data))
        q = deque()
        seen = set()
        energized = set()
        q.append((start, direction))
        while q:
            for i in range(len(q)):
                pos, direction = item = q.popleft()
                if pos not in bounds or item in seen:
                    continue
                seen.add(item)
                c = self.data[pos.y][pos.x]
                if c == '.':
                    q.append((translate(pos, direction), direction))
                elif c == '/' or c == '\\':
                    new_direction = REFLEXIONS[(c, direction)]
                    q.append((translate(pos, new_direction), new_direction))
                elif c == '-':
                    if direction == EAST or direction == WEST:
                        q.append((translate(pos, direction), direction))
                    else:
                        q.append((translate(pos, EAST), EAST))
                        q.append((translate(pos, WEST), WEST))
                elif c == '|':
                    if direction == NORTH or direction == SOUTH:
                        q.append((translate(pos, direction), direction))
                    else:
                        q.append((translate(pos, NORTH), NORTH))
                        q.append((translate(pos, SOUTH), SOUTH))
                energized.add(pos)

        return len(energized)

    def first_part(self):
        return self.simulate(Point(0,0), EAST)


    def second_part(self):
        result = 0
        bounds = Rect(0, 0, len(self.data[0]), len(self.data))
        for y in range(len(self.data)):
            result = max(result, self.simulate(Point(0,y), EAST))
            result = max(result, self.simulate(Point(bounds.w-1,y), WEST))

        for x in range(len(self.data[0])):
            result = max(result, self.simulate(Point(x,0), SOUTH))
            result = max(result, self.simulate(Point(x,bounds.h-1), NORTH))

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
