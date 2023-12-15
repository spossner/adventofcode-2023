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

    def calculate_total(self, field):
        result = 0
        n = len(field)
        for y, row in enumerate(field):
            for c in row:
                if c == 'O':
                    result += n - y
        return result

    def roll_north(self, field):
        bounds = Rect(0,0,len(field[0]),len(field))
        for y, x in product(range(1,bounds.h), range(bounds.w)):
            c = field[y][x]
            if c == '.' or c == '#':
                continue

            new_y = y - 1
            if field[new_y][x] == '.': # there is space to roll
                while True:
                    check_y = new_y - 1
                    if check_y < 0 or field[check_y][x] != ".":
                        break
                    new_y = check_y

                field[new_y][x] = field[y][x]
                field[y][x] = "."

    def roll_south(self, field):
        bounds = Rect(0, 0, len(field[0]), len(field))
        for y, x in product(range(bounds.h-2, -1, -1), range(bounds.w)):
            c = field[y][x]
            if c == '.' or c == '#':
                continue

            new_y = y + 1
            if field[new_y][x] == '.':  # there is space to roll
                while True:
                    check_y = new_y + 1
                    if check_y >= bounds.h or field[check_y][x] != ".":
                        break
                    new_y = check_y

                field[new_y][x] = field[y][x]
                field[y][x] = "."

    def roll_west(self, field):
        bounds = Rect(0, 0, len(field[0]), len(field))
        for y, x in product(range(bounds.h), range(1,bounds.w)):
            c = field[y][x]
            if c == '.' or c == '#':
                continue

            new_x = x - 1
            if field[y][new_x] == '.':  # there is space to roll
                while True:
                    check_x = new_x - 1
                    if check_x < 0 or field[y][check_x] != ".":
                        break
                    new_x = check_x

                field[y][new_x] = field[y][x]
                field[y][x] = "."

    def roll_east(self, field):
        bounds = Rect(0, 0, len(field[0]), len(field))
        for y, x in product(range(bounds.h), range(bounds.w-2,-1,-1)):
            c = field[y][x]
            if c == '.' or c == '#':
                continue

            new_x = x + 1
            if field[y][new_x] == '.':  # there is space to roll
                while True:
                    check_x = new_x + 1
                    if check_x >= bounds.w or field[y][check_x] != ".":
                        break
                    new_x = check_x

                field[y][new_x] = field[y][x]
                field[y][x] = "."

    def dump_field(self, field):
        for row in field:
            print("".join(row))
        print()

    def first_part(self):
        field = [[c for c in row] for row in self.data]
        self.roll_north(field)

        for row in field:
            print(row)

        return self.calculate_total(field)

    def second_part(self):
        field = [[c for c in row] for row in self.data]
        seen = {}
        i = 0
        TOTAL = 1_000_000_000
        while i < TOTAL:
            self.roll_north(field)
            self.roll_west(field)
            self.roll_south(field)
            self.roll_east(field)
            checksum = "".join(chain(*field))
            if checksum in seen:
                # print(i, checksum, "\nALREADY SEEN", seen[checksum], TOTAL-i, i-seen[checksum])
                cycle = i - seen[checksum]
                d = int((TOTAL - i) / cycle) * cycle
                if d > 0:
                    i += d
                    print("SKIP", d, "CONTINUE WITH", i)
            else:
                print(i, checksum)
                seen[checksum] = i
            i += 1

        return self.calculate_total(field)


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
