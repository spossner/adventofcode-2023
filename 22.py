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
GET_INTS = True
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
        if GET_INTS:
            if type(data) == str:
                data = get_ints(data)
            else:
                data = list(map(lambda e: get_ints(e) if type(e) == str else [get_ints(v) for v in e], data))
        self.data = self.parse_data(data)

    def parse_data(self, data):
        return sorted(data, key=lambda brick: brick[2]) # sort by 1st z value

    def dropped_brick(self, heights, cube):
        # find the max peak below this cube
        peak = max(heights[(x, y)] for x, y in product(range(cube[0], cube[3] + 1), range(cube[1], cube[4] + 1)))
        dz = max(cube[2] - peak - 1, 0)
        # translate cube down by dz if dz > 0
        return (cube[0], cube[1], cube[2] - dz, cube[3], cube[4], cube[5] - dz) if dz else cube

    def drop(self, tower):
        heights = defaultdict(int) # stores height for every (x, y)
        new_tower = []
        drop_count = 0
        for brick in tower:
            new_brick = self.dropped_brick(heights, brick)
            if new_brick[2] != brick[2]:
                drop_count += 1
            new_tower.append(new_brick)
            for x, y in product(range(brick[0], brick[3] + 1), range(brick[1], brick[4] + 1)):
                heights[(x, y)] = new_brick[5] # take 2nd z as new highest for this (x, y)
        return drop_count, new_tower

    def first_part(self):
        result = 0
        _, tower = self.drop(self.data) # initially creation of tower with all cubes dropped
        for i in range(len(tower)):
            removed = tower[:i] + tower[i + 1:] # remove the cube i
            drop_count, _ = self.drop(removed) # count number of cubes which are falling down
            if not drop_count:
                result += 1
        return result

    def second_part(self):
        result = 0
        _, tower = self.drop(self.data)  # initially creation of tower with all cubes sinked in
        for i in range(len(tower)):
            removed = tower[:i] + tower[i + 1:]  # remove the cube i
            drop_count, _ = self.drop(removed)  # count number of cubes which are falling down
            result += drop_count
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
