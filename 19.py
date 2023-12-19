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

DEV = True
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

    def parse_rule(self, row):
        name, rule_list = re.match(r'^(\w+){(.*)}', row).groups()
        rules = list(map(lambda r: (r[1], r[2], int(r[3]), r[4]) if r[0] is None else r[0], map(lambda x: re.match(r"^(\w+)$|(\w+)([<>])(\d+):(\w+)", x).groups(), rule_list.split(','))))
        return (name, rules)

    def simplify_rule(self, rule):
        fallback = rule[-1]
        for i in range(len(rule) - 2, -1, -1):
            step = rule[i]
            if step[3] != fallback: # can not simplify
                break
            rule.pop(i)
        return rule

    def parse_part(self, row):
        x,m,a,s = get_ints(row)
        return {'x': x, 'm': m, 'a': a, 's': s}

    def eval_rule(self, rule, part):
        for step in rule:
            if type(step) == str:
                return step # final rule

            category, op, threshold, cond_name = step

            part_value = part[category]
            if part_value < threshold:
                if op == '<':
                    return cond_name
            elif part_value > threshold:
                if op == '>':
                    return cond_name
        print(f"UUPSS.. found illegal rule {rule}")

    def parse_data(self):
        rules = {}
        parts = []
        i = 0
        while len(self.data[i]) > 0:
            rule = self.parse_rule(self.data[i])
            rules[rule[0]] = self.simplify_rule(rule[1])
            i += 1

        for j in range(i+1, len(self.data)):
            parts.append(self.parse_part(self.data[j]))

        return rules, parts



    def first_part(self):
        x = 0
        m = 0
        a = 0
        s = 0

        rules, parts = self.parse_data()

        for part in parts:
            step = 'in'
            print(part, end=': ')
            while step not in ("A", "R"):
                print(step, end=' -> ')
                step = self.eval_rule(rules[step], part)
            if step == 'A':
                x += part['x']
                m += part['m']
                a += part['a']
                s += part['s']
            print(step)

        return x+m+a+s

    def second_part(self):
        rules, parts = self.parse_data()

        # find ranges of category values which get accepted
        valid_parts = []
        # start part with max range for each category
        part = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}

        # traverse the workflow tree
        nodes = deque([("in", part)])
        while nodes:
            name, part = nodes.popleft()

            print(name, rules[name])
            for rule in rules[name]:
                if type(rule) == tuple: # conditional rule
                    category, op, threshold, cond_name = rule

                    # part which will fulfill the condition
                    cond_part = part.copy()

                    if op == '<':
                        cond_part[category] = (cond_part[category][0], threshold - 1)
                        part[category] = (threshold, part[category][1])
                    elif op == '>':
                        cond_part[category] = (threshold + 1, cond_part[category][1])
                        part[category] = (part[category][0], threshold)


                    if cond_name == "A": # found a valid part
                        valid_parts.append(cond_part)
                    elif cond_name != "R": # not rejected -> continue workflow
                        # queue this potential path with adapted part
                        nodes.append((cond_name, cond_part))
                else: # last fallback rule
                    if rule == "A":
                        valid_parts.append(part) # found a valid part
                    elif rule != "R": # queue the non rejecting fallback path
                        nodes.append((rule, part))

        # sum all possible combinations
        return sum(reduce(lambda current, part: current * (part[1] - part[0] + 1), part.values(), 1) for part in valid_parts)


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
