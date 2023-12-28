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
import random as rnd

import requests
from aoc import *
from dotenv import load_dotenv

load_dotenv()

DEV = False
PART2 = False

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
        self.nodes = set()
        self.edges = defaultdict(set)
        for line in data:
            node, *children = nodes = re.split(r": | ", line)
            self.nodes.update(nodes)
            for child in children:
                self.edges[node].add(child)
                self.edges[child].add(node)
        self.node_list = list(self.nodes)
        return data

    def bfs_all_nodes(self, edges, start):
        q = deque()
        q.append(start)
        seen = set()
        while q:
            node = q.popleft()
            if node in seen:
                continue
            seen.add(node)
            for child in edges[node]:
                q.append(child)
        return seen


    def bfs(self, edges, start, destination):
        q = deque()
        q.append(([start],set()))
        while q:
            path, seen = q.popleft()
            node = path[-1]
            if node == destination:
                return path
            if node in seen:
                continue
            seen.add(node)
            for child in edges[node]:
                q.append(([*path, child], seen))
        return None

    def first_part(self):
        result = 0
        # print(self.node_list)
        c = Counter()
        for i in range(1000):
            a, b = rnd.sample(self.node_list, 2)
            path = self.bfs(self.edges, a, b)
            edges = [(min(path[0], path[1]), max(path[0], path[1])) for path in zip(path[:-1], path[1:])]
            c.update(edges)
            # print(a,b, path)
        print(c.most_common(3))
        for path, qty in c.most_common(3):
            a, b = path
            self.edges[a].remove(b)
            self.edges[b].remove(a)


        # test sizes of subgraphs of all nodes in the three removed edges
        for path, qty in c.most_common(3):
            a, b = path
            product = len(self.bfs_all_nodes(self.edges, a)) * len(self.bfs_all_nodes(self.edges, b))
            if result != 0: # in all cases the result should be identical
                assert result == product
            result = product

        return result

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
