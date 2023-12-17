import heapq
import os
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

Node = namedtuple('Node', 'heat,pos,directions')

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

    def valid_directions(self, p, last_directions):
        last_direction = last_directions[-1]
        directions = DIRECT_ADJACENTS
        if last_direction is None:
            return directions
        directions = filter(lambda d: d != OPPOSITE_DIRECTION[last_direction], directions)
        if all(map(lambda x: x == last_direction, last_directions)):
            directions = filter(lambda x: x != last_direction, directions)
        return tuple(directions)

    def is_valid_tail(self, directions):
        return all(map(lambda x: x == directions[-1], directions[-4:]))

    def valid_directions_ultra(self, p, last_directions):
        directions = DIRECT_ADJACENTS
        last_direction = last_directions[-1]
        if last_direction is None:
            return directions


        valid = self.is_valid_tail(last_directions)
        if not valid:
            return (last_direction,)


        directions = filter(lambda p: p.x+last_direction.x != 0 or p.y+last_direction.y!=0, DIRECT_ADJACENTS)
        if all(map(lambda x: x == last_direction, last_directions)):
            directions = filter(lambda x: x != last_direction, directions)
        return tuple(directions)

    def dump_path(self, field, path):
        bounds = Rect(0, 0, len(field[0]), len(field))
        for y in range(bounds.h):
            for x in range(bounds.w):
                if (x,y) in path:
                    print('#', end='')
                else:
                    print(field[y][x], end='')
            print()

    def dijkstra(self, field, start, destination, history, valid_directions, is_valid_solution):
        start_time = time.time()
        bounds = Rect(0, 0, len(field[0]), len(field))
        paths = []
        heapq.heappush(paths, Node(0, start, (history * (None,))))
        seen = set()
        i = 0
        while paths:
            if i % 10_000 == 0:
                print(len(paths))
            heat, pos, last_directions =  heapq.heappop(paths)
            if pos == destination:
                if is_valid_solution(last_directions):
                    end_time = time.time()
                    print(f"took {(end_time - start_time) * 1_000} ms")
                    return heat
                continue # invalid solution

            for direction in valid_directions(pos, last_directions):
                new_pos = translate(pos, direction)
                if new_pos not in bounds:
                    continue

                new_directions = (*last_directions[1:], direction)
                check = (new_pos, new_directions)
                if check in seen:
                    continue
                seen.add(check)

                heapq.heappush(paths, Node(heat + field[new_pos.y][new_pos.x], new_pos, new_directions))
            i += 1

    def first_part(self):
        field = [list(map(int, list(s))) for s in self.data]

        bounds = Rect(0, 0, len(field[0]), len(field))
        return self.dijkstra(field, Point(0,0), Point(bounds.w - 1, bounds.h - 1), 3, self.valid_directions, lambda *_: True)


    def second_part(self):
        field = [list(map(int, list(s))) for s in self.data]

        bounds = Rect(0, 0, len(field[0]), len(field))
        return self.dijkstra(field, Point(0, 0), Point(bounds.w - 1, bounds.h - 1), 10, self.valid_directions_ultra, self.is_valid_tail)


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
