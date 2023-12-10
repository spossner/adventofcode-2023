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
from colorama import Fore, Back, Style

import requests
from aoc import *
from dotenv import load_dotenv

load_dotenv()

DEV = False
PART2 = True
DATA = None

STRIP = True
SPLIT_LINES = True
SPLIT_CHAR = None
AOC_SESSION = os.environ.get('AOC_SESSION')
YEAR = 2023

Node = namedtuple('Node', 'p,last_move')

TRANSLATE = {
    '|': 'NS',
    '-': 'WE',
    'L': 'NE',
    'J': 'NW',
    '7': 'SW',
    'F': 'SE',
    '.': '.',
    'S': 'S',
}

MOVES = {
    'N': NORTH,
    'E': EAST,
    'S': SOUTH,
    'W': WEST,
}

OPPOSITE = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E',
}

NEIGHBOURS = { # TYPE: ( (LEFT,..), (RIGHT,...) ) if moving in direction of first letter in type
    'WE': ((SOUTH_WEST, SOUTH, SOUTH_EAST), (NORTH_WEST, NORTH, NORTH_EAST)),
    'NS': ((SOUTH_WEST, WEST, NORTH_WEST), (SOUTH_EAST, EAST, NORTH_EAST)),
    'NW': ((NORTH_WEST,), (NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST)),
    'SE': ((SOUTH_EAST,), (NORTH_EAST,NORTH,NORTH_WEST,WEST,SOUTH_WEST)),
    'SW': ((NORTH_WEST, NORTH, NORTH_EAST, EAST, SOUTH_EAST),(SOUTH_WEST,)),
    'NE': ((SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST), (NORTH_EAST,)),
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

    def dump_grid(self, path, inner, outer):
        for y, row in enumerate(self.data):
            for x, c in enumerate(row):
                p = Point(x, y)
                color = Fore.LIGHTBLACK_EX
                if p in path:
                    color = Fore.LIGHTYELLOW_EX
                if p in outer:
                    c = 'O'
                    color = Fore.LIGHTRED_EX
                if p in inner:
                    c = 'I'
                    color = Fore.LIGHTGREEN_EX
                print(color+c, end='')
            print()

    def connected_adjacent_pipes(self, grid, p):
        connected = []
        north = translate(p, NORTH)
        if north in grid and 'S' in grid[north]:
            connected.append(Node(north, 'S'))
        east = translate(p, EAST)
        if east in grid and 'W' in grid[east]:
            connected.append(Node(east, 'W'))
        south = translate(p, SOUTH)
        if south in grid and 'N' in grid[south]:
            connected.append(Node(south, 'N'))
        west = translate(p, WEST)
        if west in grid and 'E' in grid[west]:
            connected.append(Node(west, 'E'))
        return connected

    def next_direction(self, grid, n: Node):
        connect = grid[n.p]
        return connect[1] if n.last_move == connect[0] else connect[0]

    def is_turn(self, grid, p: Point):
        return grid[p] in ['NE', 'NW', 'SW', 'SE']

    def get_left_right(self, grid, n: Node, d):
        type = grid[n.p]
        neigbours = NEIGHBOURS[type]
        idx = 0 if d == type[0] else 1
        return neigbours[idx], neigbours[1-idx]

    def first_part(self):
        grid = {}
        start = None
        for y, row in enumerate(self.data):
            for x, c in enumerate(row):
                p = Point(x, y)
                grid[p] = TRANSLATE[c]
                if c == 'S':
                    start = p

        steps = 1
        ptr = self.connected_adjacent_pipes(grid, start)[0]
        turns = [start]
        path = set()
        path.add(start)
        left = set()
        right = set()
        while ptr.p != start:
            path.add(ptr.p)
            if self.is_turn(grid, ptr.p):
                turns.append(ptr.p)

            d = self.next_direction(grid, ptr)
            l, r = self.get_left_right(grid, ptr, d)
            # print(f"{ptr.p}: {grid[ptr.p]} moving {d} - marking {l} as left and {r} as right")
            left = left.union(map(lambda d: translate(ptr.p, d), l))
            right = right.union(map(lambda d: translate(ptr.p, d), r))


            ptr = Node(translate(ptr.p, MOVES[d]), OPPOSITE[d])
            steps += 1
            # print(ptr1,ptr2,steps)

        # check if turns are in clockwise or counter clockwise
        cw_sum = 0
        n = len(turns)
        for i in range(n):
            v = (turns[(i + 1) % n].x - turns[i].x) * (turns[(i + 1) % n].y + turns[i].y)
            cw_sum += v
        cw = cw_sum < 0
        # remove path from left and right
        left = left.difference(path)
        right = right.difference(path)
        # if clockwise, mark right side as inner fields; otherwise left side
        inner = right if cw else left
        outer = left if cw else right

        # flood fill inner nodes
        q = deque(inner)
        while q:
            for i in range(len(q)):
                p = q.popleft()
                for adj in direct_adjacent_iter(p):
                    if adj in outer:
                        print("UUUPSSS", p, adj) # shoud never happen
                        return
                    if adj in inner or adj in path:
                        continue
                    inner.add(adj)
                    q.append(adj)

        self.dump_grid(path, inner, outer)

        return steps >> 1, len(inner)

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
