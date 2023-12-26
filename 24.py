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

DEV = True
PART2 = True

STRIP = True
SPLIT_LINES = True
SPLIT_CHAR = None
GET_INTS = True
DATA = None
AOC_SESSION = os.environ.get('AOC_SESSION')
YEAR = 2023

Vector=namedtuple("Vector","x,y,z,vx,vy,vz")

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
        return list(map(lambda p: Vector(*p), data))

    def first_part(self):
        result = 0
        MIN = 7 if DEV else 200_000_000_000_000
        MAX = 27 if DEV else 400_000_000_000_000

        for a, b in combinations(self.data, 2):
            # steigungen
            ma = (a.vy / a.vx)
            mb = (b.vy / b.vx)

            if ma == mb: # parallel - keine zwei Hagelkörner übereinander
                continue

            # y = m * x + c  -->  c = y - m * x
            ca = a.y - (ma * a.x)
            cb = b.y - (mb * b.x)

            # a und b gleichsetzen
            x = (cb-ca)/(ma-mb)
            # x in eine einsetzen für y
            y = (ma * x) + ca

            if (x < a.x and a.vx > 0) or (x > a.x and a.vx < 0) or (x < b.x and b.vx > 0) or (x > b.x and b.vx < 0): # different directions
                continue
            if MIN <= x <= MAX and MIN <= y <= MAX:
                result += 1

        return result

    def second_part(self):
        # MIN = -100_000_000
        # MAX = 100_000_000
        # potential_x_set = None
        # potential_y_set = None
        # potential_z_set = None
        # for a, b in combinations(self.data, 2):
        #     if a.vx == b.vx and abs(a.vx) > 0:
        #         new_x_set = set()
        #         diff = b.x - a.x
        #         for v in range(MIN, MAX):
        #             if v == a.vx:
        #                 continue
        #             if diff % (v - a.vx) == 0:
        #                 new_x_set.add(v)
        #         if potential_x_set is None:
        #             potential_x_set = new_x_set.copy()
        #         else:
        #             potential_x_set = potential_x_set & new_x_set
        #     if a.vy == b.vy and abs(a.vy) > 0:
        #         new_y_set = set()
        #         diff = b.y - a.y
        #         for v in range(MIN, MAX):
        #             if v == a.vy:
        #                 continue
        #             if diff % (v - a.vy) == 0:
        #                 new_y_set.add(v)
        #         if potential_y_set != None:
        #             potential_y_set = potential_y_set & new_y_set
        #         else:
        #             potential_y_set = new_y_set.copy()
        #     if a.vz == b.vz and abs(a.vz) > 0:
        #         new_z_set = set()
        #         diff = b.z - a.z
        #         for v in range(MIN, MAX):
        #             if v == a.vz:
        #                 continue
        #             if diff % (v - a.vz) == 0:
        #                 new_z_set.add(v)
        #         if potential_z_set != None:
        #             potential_z_set = potential_z_set & new_z_set
        #         else:
        #             potential_z_set = new_z_set.copy()
        #
        # print(potential_x_set, potential_y_set, potential_z_set)
        # rv = Point3d(potential_x_set.pop(), potential_y_set.pop(), potential_z_set.pop())
        #
        # a = self.data[0]
        # b = self.data[1]
        # ma = (a.vy - rv.y) / (a.vx - rv.x)
        # mb = (b.vy - rv.y) / (b.vx - rv.x)
        # ca = a.y - (ma * a.x)
        # cb = b.y - (mb * b.x)
        # x = (cb - ca) / (ma - mb)
        # y = (ma * x) + ca
        # t = (x - a.x) / (a.vx - rv.x)
        # z = a.z + (a.vz - rv.z) * t
        #
        # print(x, y, z)
        # return x + y + z
        # 716599937560132 too high
        # 716599937560106 too high
        # 289 too low
        return 0


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
