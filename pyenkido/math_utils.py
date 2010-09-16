## Project: pyEnkido
## Module: math_utils
## Author: Salwan

import math
import random

# Dealing with py2exe bug
import pyenkido.font

def linear_interpolate(val1, val2, delta):
    return (float(val2 - val1) * delta) + val1

# [(value, percent), ...]
def get_random_percent(rlist):
    if len(rlist) == 0:
        return 0
    perc = 0
    for r in rlist:
        perc += r[1]
    n = random.randint(0, perc)
    test = 0
    for r in rlist:
        test += r[1]
        if n <= test:
            return r[0]

# Format of line equation item
# (m, (x1, y1), (x2,y2))
# (m, start, end)
class LinearEquation:
    def __init__(self):
        self.lines = []

    def addLine(self, start, end):
        fstart = (float(start[0]), float(start[1]))
        fend = (float(end[0]), float(end[1]))
        m = (fend[1] - fstart[1]) / (fend[0] - fstart[0])
        self.lines.append((m, fstart, fend))

    def getY(self, x):
        line = None
        for l in self.lines:
            if x <= l[2][0]:
                line = l
                break
        if line == None:
            raise "DUDE!!! you gave a value above equation in LinearEquation X("
        return (l[0] * (float(x) - line[1][0])) + line[1][1]

