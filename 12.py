import os
import random
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
from typing import List

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

    def find_arrangements(self, field, sets):
        arrangements = []
        q = deque()
        q.append((0, 0, sets, ""))
        while q:
            print(field, len(q))
            for i in range(len(q)):
                ptr, length_so_far, missing_sets, pattern = q.popleft()

                if ptr >= len(field): # end reached
                    if len(missing_sets) > 1:
                        continue
                    elif not missing_sets:
                        if length_so_far:
                            continue
                    elif length_so_far != missing_sets[0]:
                        continue
                    # print("VALID", pattern, length_so_far, missing_sets)
                    arrangements.append(pattern)
                    continue

                if field[ptr] == '#':
                    if not missing_sets:
                        continue # not a solution
                    if length_so_far >= missing_sets[0]:
                        continue
                    q.appendleft((ptr + 1, length_so_far+1, missing_sets, pattern+"#"))  # matched
                elif field[ptr] == '.':
                    if length_so_far:
                        if length_so_far != missing_sets[0]:
                            continue # not a solution
                        if length_so_far == missing_sets[0]:
                            q.appendleft((ptr+1, 0, missing_sets[1:], pattern+".")) # matched group
                    else:
                        q.appendleft((ptr + 1, 0, missing_sets, pattern+"."))
                elif field[ptr] == '?':
                    if not missing_sets:
                        q.appendleft((ptr + 1, 0, missing_sets, pattern+".")) # use ? as gap
                    elif length_so_far:
                        if length_so_far < missing_sets[0]:
                            q.appendleft((ptr + 1, length_so_far + 1, missing_sets, pattern+"#"))  # matched
                        elif length_so_far == missing_sets[0]: # use a gap
                            q.appendleft((ptr + 1, 0, missing_sets[1:], pattern+"."))  # matched group
                        else:
                            continue # can not be reached
                    else:
                        q.append((ptr + 1, 0, missing_sets, pattern+"."))  # use ? as gap
                        q.append((ptr + 1, 1, missing_sets, pattern+"#"))  # use ? as marked
        return arrangements

    @cache
    def greedy_groups(self, field, sets):
        if field == "": # end
            return 1 if len(sets) == 0 else 0 # no solution if there are still groups left

        if field[0] == ".":
            # skip all operational springs to find potential new group start
            return self.greedy_groups(field.lstrip("."), sets)

        if field.startswith("#"):
            if not sets:
                return 0 # no group expected -> no solution
            if len(field) < sets[0]:
                return 0 # early exit -> not enough potential fields left to form group

            for c in field[0:sets[0]]:
                if c == ".":
                    return 0 # not a valid group containing a operational spring

            if len(sets) > 1:
                if len(field) < sets[0] + 2:
                    return 0 # early exist - can not fit any other group after this group plus a gap
                if field[sets[0]] == "#":
                    return 0  # group too long
                return self.greedy_groups(field[sets[0] + 1:], sets[1:]) # group found
            else:
                return self.greedy_groups(field[sets[0]:], sets[1:]) # group found

        if field[0] == "?":
            as_operational = self.greedy_groups("." + field[1:], sets)
            as_damaged = self.greedy_groups("#" + field[1:], sets)
            return as_operational + as_damaged

        print("UUUPPPS")
        assert False

    def first_part(self):
        result = 0

        for row in self.data:
            field, sets = row.split(" ")
            sets = get_ints(sets)
            arrangements = self.find_arrangements(field, sets)
            result += len(arrangements)

        return result

    def second_part(self):
        result = 0

        for row in self.data:
            field, sets = row.split(" ")
            sets = get_ints(sets)
            unfolded_field = "?".join(5 * [field])
            unfolded_sets = tuple(5 * sets)
            print(unfolded_field)
            # arrangements = self.find_arrangements(unfolded_field, unfolded_sets)
            # result += len(arrangements)
            n = self.greedy_groups(unfolded_field, tuple(unfolded_sets))
            result += n

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
