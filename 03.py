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
        result = 0
        seen = set()
        for y in range(len(self.data)):
            row = self.data[y]
            for x in range(len(row)):
                c = row[x]
                if c == '.':
                    continue
                if c.isdigit():
                    continue
                print(f"found symbol {c} at ({x},{y})")
                for p in all_adjacent_iter((x,y)):
                    if p in seen:
                        continue
                    d = self.data[p[1]][p[0]]
                    if d.isdigit():
                        adjacent_number = d
                        seen.add(p)
                        dx = p[0]-1
                        while dx >= 0:
                            d = self.data[p[1]][dx]
                            if d.isdigit():
                                seen.add(Point(dx ,p[1]))
                                adjacent_number = f"{d}{adjacent_number}"
                                dx -= 1
                            else:
                                break
                        dx = p[0] + 1
                        while dx < len(self.data[p[1]]):
                            d = self.data[p[1]][dx]
                            if d.isdigit():
                                seen.add(Point(dx, p[1]))
                                adjacent_number = f"{adjacent_number}{d}"
                                dx += 1
                            else:
                                break

                        print(f"found adjacent number {adjacent_number}")
                        result += int(adjacent_number)

        return result

    def second_part(self):
        result = 0
        seen = set()
        for y in range(len(self.data)):
            row = self.data[y]
            for x in range(len(row)):
                c = row[x]
                if c != '*':
                    continue
                print(f"found gear symbol {c} at ({x},{y})")
                adjacent_numbers = []
                for p in all_adjacent_iter((x, y)):
                    if p in seen:
                        continue
                    d = self.data[p[1]][p[0]]
                    if d.isdigit():
                        adjacent_number = d
                        seen.add(p)
                        dx = p[0] - 1
                        while dx >= 0:
                            d = self.data[p[1]][dx]
                            if d.isdigit():
                                seen.add(Point(dx, p[1]))
                                adjacent_number = f"{d}{adjacent_number}"
                                dx -= 1
                            else:
                                break
                        dx = p[0] + 1
                        while dx < len(self.data[p[1]]):
                            d = self.data[p[1]][dx]
                            if d.isdigit():
                                seen.add(Point(dx, p[1]))
                                adjacent_number = f"{adjacent_number}{d}"
                                dx += 1
                            else:
                                break

                        print(f"found adjacent number {adjacent_number}")
                        adjacent_numbers.append(int(adjacent_number))
                print(f"in total {len(adjacent_numbers)} adjacen numbers")
                if len(adjacent_numbers) == 2:
                    result += reduce(operator.mul, adjacent_numbers, 1)
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
