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
from typing import List, Dict

import requests
from aoc import *
from dotenv import load_dotenv

import numpy as np

load_dotenv()

DEV = False
PART2 = True

STRIP = True
SPLIT_LINES = True
SPLIT_CHAR = None
DATA = None
AOC_SESSION = os.environ.get('AOC_SESSION')
YEAR = 2023

@dataclass
class Node:
    type: str | None
    name: str
    inputs: List
    outputs: List
    state: int | Dict

    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.inputs = []
        self.outputs = []
        self.state = 0 if type != "&" else {}

    def connect_children(self, node):
        self.outputs.append(node)
        node.add_input(self)

    def add_input(self, node):
        self.inputs.append(node)
        if self.type == "&":
            self.state[node.name] = 0

    def eval_signal(self, signal, source):
        if self.type is None:
            return [] # just consume

        if self.type == "":
            return [(signal, self, o) for o in self.outputs]

        if self.type == "%":
            if signal == 0:
                self.state = 1-self.state
                return [(self.state, self, o) for o in self.outputs]
            return []

        if self.type == "&":
            self.state[source.name] = signal
            output_value = 0 if signal and all(value == 1 for value in self.state.values()) else 1
            return [(output_value, self, o) for o in self.outputs]


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
        self.data = self.parse_rows(data)

    def parse_rows(self, rows):
        data = {}
        unconnected_outputs = {}
        for row in rows:
            type, name, outputs = re.match(r"([%&]?)(\w+) -> (.*)", row).groups()
            data[name] = Node(type, name)
            unconnected_outputs[name] = map(str.strip, outputs.split(','))

        for name, outputs in unconnected_outputs.items():
            node = data[name]
            for child_name in outputs:
                if child_name not in data:
                    print(child_name, "not a know node -> create a consume node")
                    data[child_name] = Node(None, child_name) # create a consuming node on the fly for unknown outputs
                node.connect_children(data[child_name])

        return data

    def first_part(self):
        low = 0
        high = 0

        for loop in range(1_000):
            q = deque([(0, Node(None, "button"), self.data["broadcaster"])]) # send low (=0) pulse from Button to broadcaster
            while q:
                for i in range(len(q)): # round by round
                    signal, source, destination = q.popleft()
                    # print(f"{source.name} {signal}-> {destination.name}")
                    if signal == 0:
                        low += 1
                    else:
                        high += 1
                    q.extend(destination.eval_signal(signal, source))

        return low, high, low * high

    def second_part(self):
        starts = ("gz", "xg", "cd", "sg")
        destinations = ("dd", "fh", "xp", "fc")
        loops = {}

        for start in starts:
            print("testing", start)
            found_destination = False
            for loop in count(1):
                q = deque([(0, Node(None, "button"), self.data[start])])  # send low (=0) pulse from Button to broadcaster
                while q:
                    for i in range(len(q)):  # round by round
                        signal, source, destination = q.popleft()
                        if destination.name in destinations:
                            if signal == 0:
                                print(loop, start, destination.name, signal)
                                loops[start] = loop
                                found_destination = True
                                break
                        q.extend(destination.eval_signal(signal, source))
                    if found_destination:
                        break
                if found_destination:
                    break

        return np.lcm.reduce(list(loops.values()))


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
