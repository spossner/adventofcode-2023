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
import numpy as np

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

Node = namedtuple('Node', 'value,left,right')

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

    def parse_nodes(self):
        re_node = re.compile(r"(\w+) = \((\w+), (\w+)\)")
        network = {}
        for row in self.data[2:]:
            id, l, r = re_node.match(row).groups()
            network[id] = Node(id, l, r)
        return (list(self.data[0]), network)

    def first_part(self):
        result = 0

        instr, network = self.parse_nodes()

        node = network['AAA']
        ptr = 0
        while node.value != 'ZZZ':
            node = network[node.left if instr[ptr] == 'L' else node.right]
            ptr = (ptr + 1) % len(instr)
            result += 1

        return result

    def is_starting_node(self, node: Node):
        return node.value[-1] == 'A'

    def is_finish_node(self, node: Node):
        return node.value[-1] == 'Z'

    def second_part(self):
        instr, network = self.parse_nodes()

        nodes = list(filter(self.is_starting_node, network.values()))

        # steps_to_z = defaultdict(set) # node-name: {steps,}
        steps_to_z = []

        for node in nodes:
            ptr = 0
            steps = 0

            # id = node.value
            # end_nodes_seen = set()
            while True:
                if self.is_finish_node(node):
                    # all paths have exact one end node and therefore only one path
                    # -> ignore complex set building...
                    # marker = (node.value, ptr)
                    # if marker in end_nodes_seen:
                    #     break # found all end node / direction combinations
                    # end_nodes_seen.add(marker)
                    # steps_to_z[id].add(steps)

                    # ... but use just a simple list of steps needed
                    steps_to_z.append(steps)
                    break;
                node = network[node.left if instr[ptr] == 'L' else node.right]
                ptr = (ptr + 1) % len(instr)
                steps += 1
        return np.lcm.reduce(steps_to_z)


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
