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
from colorama import Fore
from dotenv import load_dotenv

load_dotenv()

DEV = False
PART2 = True

STRIP = True
SPLIT_LINES = True
SPLIT_CHAR = None
GET_INTS = False
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
        self.bounds = Rect(0, 0, len(data[0]), len(data))
        self.start = Point(data[0].index('.'), 0)
        self.destination = Point(data[self.bounds.h - 1].index('.'), self.bounds.h - 1)
        return data

    def dump_grid(self):
        print("    ", end='')
        for x in range(len(self.data[0])):
            print((x // 100)%100 if x >= 100 and x % 10 == 0 else ' ', end='')
        print("\n    ", end='')
        for x in range(len(self.data[0])):
            print((x // 10)%10 if x >= 10 and x % 10 == 0 else ' ', end='')
        print("\n    ", end='')
        for x in range(len(self.data[0])):
            print(x%10, end='')
        print()
        for y in range(len(self.data)):
            print(f"{y:3d} ", end='')
            for x in range(len(self.data[0])):
                key = (x,y)
                if key in self.junctions:
                    print(Fore.LIGHTYELLOW_EX+'❖'+Fore.RESET, end='')
                else:
                    print(self.data[y][x], end='')
            print()

    def adj(self, p, directed=not PART2):
        if directed and self.data[p.y][p.x] in DIRECTIONS:
            return [translate(p, DIRECTIONS[self.data[p.y][p.x]])]
        return list(filter(lambda a: a in self.bounds and self.data[a.y][a.x] != '#', direct_adjacent_iter(p)))

    def build_graph(self):
        self.junctions = set([self.start, self.destination])
        for x, y in product(range(self.bounds.w), range(self.bounds.h)):
            if self.data[y][x] == '#':
                continue
            p = Point(x, y)
            if len(self.adj(p)) > 2:
                self.junctions.add(p)

        self.edges = defaultdict(list)
        for j in self.junctions:
            q = deque([(j, 0)])
            seen = {j, }
            while q:
                p, dist = q.popleft()
                for a in self.adj(p):
                    if a in seen:
                        continue
                    seen.add(a)
                    if a in self.junctions:
                        self.edges[j].append((a, dist + 1))
                    else:
                        q.append((a, dist + 1))

    def dfs(self, cur, pathset, totaldist, best=0):
        if cur == self.destination:
            return max(best, totaldist)
        for a, dist in self.edges[cur]:
            if a not in pathset:
                pathset.add(a)
                best = self.dfs(a, pathset, totaldist + dist, best)
                pathset.remove(a)
        return best

    def first_part(self):
        self.build_graph()
        self.dump_grid()
        return self.dfs(self.start, set(), 0)


    def second_part(self):
        self.build_graph()
        self.dump_grid()

        return self.dfs(self.start, set(), 0)


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
