import os
import sys
import math
import operator
import re
from collections import *
from decimal import Decimal
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
GET_INTS = True
DATA = None
AOC_SESSION = os.environ.get('AOC_SESSION')
YEAR = 2023

Vector=namedtuple("Vector","x,y,z,vx,vy,vz")


class Hail:
    def __init__(self, vec):
        self.px, self.py, self.pz, self.vx, self.vy, self.vz = vec
        self.XYslope = Decimal('inf') if self.vx == 0 else self.vy / self.vx
        self.ax, self.ay, self.az = 0, 0, 0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'<{self.px}, {self.py}, {self.pz} @ {self.vx}, {self.vy}, {self.vz}>'

    def intersectXY(self, other):
        # returns None, if parallel / intersect in a past
        if self.XYslope == other.XYslope:
            return None
        if self.XYslope == Decimal('inf'):  # self is vertical
            intX = self.px
            intY = other.XYslope * (intX - other.px) + other.py
        elif other.XYslope == Decimal('inf'):  # other is vertical
            intX = other.px
            intY = self.XYslope * (intX - self.px) + self.py
        else:
            # y - y1 = m1 * ( x - x1 ) reduced to solve for x
            intX = (self.py - other.py - self.px * self.XYslope + other.px * other.XYslope) / (other.XYslope - self.XYslope)
            intY = self.py + self.XYslope * (intX - self.px)
        intX, intY = intX.quantize(Decimal(".1")), intY.quantize(Decimal(".1"))
        # intY = round(intY)

        selfFuture = np.sign(intX - self.px) == np.sign(self.vx)
        otherFuture = np.sign(intX - other.px) == np.sign(other.vx)
        if not (selfFuture and otherFuture):
            return None
        return (intX, intY)

    def adjust(self, ax, ay, az):
        self.vx -= ax - self.ax
        self.vy -= ay - self.ay
        self.vz -= az - self.az
        # assert type(self.vx) is Decimal
        self.XYslope = Decimal('inf') if self.vx == 0 else self.vy / self.vx
        self.ax, self.ay, self.az = ax, ay, az

    def getT(self, p):  # if both vx and vy are 0... good luck
        if self.vx == 0:
            return (p[1] - self.py) / self.vy
        return (p[0] - self.px) / self.vx

    def getZ(self, other, inter):  # given an intersection point and an other Hail
        # now we KNOW: z = pz_i + t_i*(vz_i-aZ)   [t = (inter[0]-px_i)/(vx_i)]
        #              z = pz_j + t_j*(vz_j-aZ)
        # (pz_i - pz_j + t_i*vz_i - t_j*vz_j)/(t_i - t_j) =  aZ
        tS = self.getT(inter)
        tO = other.getT(inter)
        if tS == tO:
            assert self.pz + tS * self.vz == other.pz + tO * other.vz
            return None
        return (self.pz - other.pz + tS * self.vz - tO * other.vz) / (tS - tO)

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
        return [[Decimal(n) for n in row] for row in data]
        # return list(map(lambda p: Vector(*p), data))

    def first_part(self):
        result = 0
        MIN = 7 if DEV else 200_000_000_000_000
        MAX = 27 if DEV else 400_000_000_000_000

        for a, b in combinations(self.data, 2):
            # steigungen
            ma = (a.vy / a.vx)
            mb = (b.vy / b.vx)

            if ma == mb: # parallel - keine zwei Hagelkörner übereinander
                continue

            # y = m * x + c  -->  c = y - m * x
            ca = a.y - (ma * a.x)
            cb = b.y - (mb * b.x)

            # a und b gleichsetzen
            x = (cb-ca)/(ma-mb)
            # x in eine einsetzen für y
            y = (ma * x) + ca

            if (x < a.x and a.vx > 0) or (x > a.x and a.vx < 0) or (x < b.x and b.vx > 0) or (x > b.x and b.vx < 0): # different directions
                continue
            if MIN <= x <= MAX and MIN <= y <= MAX:
                result += 1

        return result

    def second_part(self):
        hailstones = []
        for vec in self.data:
            hailstones.append(Hail(vec))

        N = 0
        while True:
            print('.', end='')
            for X in range(N + 1):
                Y = N - X
                for negX in (-1, 1):
                    for negY in (-1, 1):
                        aX = X * negX
                        aY = Y * negY
                        if DEV: print(f'checking v=<{aX},{aY},?>')
                        H1 = hailstones[0]
                        H1.adjust(aX, aY, 0)
                        inter = None
                        if DEV: print(f'comparing v {H1}')
                        for H2 in hailstones[1:]:
                            H2.adjust(aX, aY, 0)
                            p = H1.intersectXY(H2)
                            if p is None:
                                if DEV: print(f'v {H2} — NONEE')
                                break
                            if inter is None:
                                if DEV: print(f'v {H2} — setting to {p}')
                                inter = p
                                continue
                            if p != inter:
                                if DEV: print(f'v {H2} — NOT SAME P {p}')
                                break
                            if DEV: print(f'v {H2} — continuing{p}')
                        if p is None or p != inter:
                            continue
                        if DEV: print(f'FOUND COMMON INTERSECTION {p}')
                        # we escaped intersecting everything with H1 with a single valid XY point!
                        print(f'potential intersector found with v=<{aX},{aY},?>' \
                              + f', p=<{inter[0]},{inter[1]},?>')
                        aZ = None
                        H1 = hailstones[0]
                        # print(f'v {H1}')
                        for H2 in hailstones[1:]:
                            nZ = H1.getZ(H2, inter)
                            if aZ is None:
                                print(f'first aZ is {aZ} from {H2}')
                                aZ = nZ
                                continue
                            elif nZ != aZ:
                                print(f'invalidated! by {nZ} from {H1}')
                                return
                                break
                        if aZ == nZ:
                            H = hailstones[0]
                            Z = H.pz + H.getT(inter) * (H.vz - aZ)
                            print(f'found solution :) v=<{aX},{aY},{aZ}>, p=<{inter[0]},{inter[1]},{Z}>, s = {Z + inter[0] + inter[1]}')
                            return

            N += 1
            # 716599937560132 too high
            # 716599937560106 too high
            # 716599937560103 correct.. finally


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
