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


    def parse_mapping(self):
        mapping = {}
        name = None
        ranges = []
        for row in self.data[2:]:
            if row == '':
                mapping[name[0]] = (name[1], self.create_range_map(ranges))
                continue

            m = re.match(f"(.*)-to-(.*) map", row)
            if m:
                name = (m.group(1), m.group(2))
                ranges = []
                continue

            ranges.append(get_ints(row))
        mapping[name[0]] = (name[1], self.create_range_map(ranges))
        return mapping

    def create_range_map(self, ranges):
        result = []
        for r in ranges:
            r_to = range(r[0],r[0]+r[2])
            r_from = range(r[1],r[1]+r[2])
            result.append((r_from, r_to, r_to.start - r_from.start))
        return result

    def map_value(self, source, v, mapping):
        range_map = mapping[source]
        destination = range_map[0]
        for r_from, r_to, delta in range_map[1]:
            if v in r_from:
                d = v-r_from.start
                return (destination, r_to[d])
        return (destination, v)

    def first_part(self):
        result = None
        seeds = get_ints(self.data[0])
        mapping = self.parse_mapping()

        for seed in seeds:
            v = seed
            step = 'seed'
            while step != 'location':
                step, v = self.map_value(step, v, mapping)
            if result == None or v < result:
                result = v

        return result

    # return overlap range for two range objects (with step = 1 !!) or None if no overlap
    def range_intersect(self, r1, r2):
        return range(max(r1.start, r2.start), min(r1.stop, r2.stop)) or None


    def second_part(self):
        result = None

        seeds = get_ints(self.data[0])
        mapping = self.parse_mapping()

        print(seeds)
        q = deque()
        for i in range(0, len(seeds), 2):
            s_from = seeds[i]
            s_to = seeds[i+1]+s_from
            print(s_from, s_to)
            q.append(('seed', range(s_from, s_to)))
        while q:
            for i in range(len(q)):
                step, r1 = q.popleft()
                # print(step, r1)
                if step == 'location':
                    if result == None or r1.start < result:
                        result = r1.start
                        # print(result)
                    continue
                destination, shifts = mapping[step]
                touched = False
                for r2_from, r2_to, r2_d in shifts:
                    overlap = self.range_intersect(r1, r2_from)

                    if overlap == None:
                        continue

                    touched = True
                    if overlap == r1: # full overlap
                        print('full shift', step, destination, r1, r2_d)
                        q.append((destination, range(r1.start+r2_d, r1.stop+r2_d)))
                    else:
                        r_left = range(r1.start, overlap.start) or None
                        r_right = range(overlap.stop, r1.stop) or None
                        print('split', step, destination, r1, overlap, r2_d, r_left, r_right, r1 != overlap, touched)
                        if r_left: # keep r_left in step
                            q.append((step, r_left))
                        if r_right:  # keep r_right in step
                            q.append((step, r_right))
                        q.append((destination, range(overlap.start+r2_d, overlap.stop+r2_d))) # overlap shifted in next step

                    break

                if not touched: # pass identical range to next step
                    q.append((destination, r1))

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
