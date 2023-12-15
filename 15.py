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
from aoc.linked_list import ListNode
from dotenv import load_dotenv

load_dotenv()

DEV = False
PART2 = True

STRIP = True
SPLIT_LINES = False
SPLIT_CHAR = ','
DATA = None
AOC_SESSION = os.environ.get('AOC_SESSION')
YEAR = 2023

class Box:
    def __init__(self):
        self.head = None
        self.tail = None
        self.lenses = {}

    def append(self, label, focal: int):
        if label in self.lenses:
            self.lenses[label].val = focal
        else:
            node = None
            if self.tail:
                node = self.tail = self.tail.insert_after(focal)
            else:
                node = self.head = self.tail = ListNode(focal)
            self.lenses[label] = node

    def remove(self, label):
        if label not in self.lenses:
            return
        node = self.lenses.pop(label)
        if node:
            node.pop()
            if node == self.head:
                self.head = node.next_node
            if node == self.tail:
                self.tail = node.prev_node
        return node

    def dump(self, id=None):
        print(id if id is not None else '', self.lenses, list(self.head) if self.head else '[]')


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

    def my_hash(self, label):
        current = 0
        for c in label:
            current = ((current + ord(c)) * 17) % 256
        return current

    def first_part(self):
        result = 0

        for row in self.data:
            result += self.my_hash(row)
        return result

    def second_part(self):
        result = 0

        boxes = defaultdict(Box)

        for row in self.data:
            _,label,op,focal,_ = re.split(r"(\w+)([=-])(\d*)", row)
            id = self.my_hash(label)
            box = boxes[id]

            if op == '=':
                box.append(label, int(focal))
            else:
                box.remove(label)

        for id, box in boxes.items():
            if not box.head:
                continue
            sum = 0
            for i, val in enumerate(box.head):
                sum += (id+1) * (i+1) * val
            result += sum

        # 222450 too high
        # 210906 after fixing my linked list insert_after...
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
