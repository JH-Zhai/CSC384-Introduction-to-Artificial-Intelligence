from constraints import *
from backtracking import bt_search, GacEnforce
from csp import Variable, CSP
from csp_problems import nQueens, sudokuCSP, solve_planes
from sudoku import b1, b5, b6
from plane_scheduling import p1, p2, p3, p4, p5, p6, p7, check_plane_solution
import argparse
import csp_problems
import backtracking
import argparse

import itertools

titles = ["Q1. Table Constraint for nQueens (4 points)",
          "Q2. Forward Checking implementation (5 points)",
          "Q3. GacEnforce and GAC implementation (5 points)",
          "Q4. AllDiff for Sudoku (2 points)",
          "Q5. NValues Constraint implementation (4 points)",
          "Q6. Plane Scheduling (10 points)"]

m=1
n=20
p8=csp_problems.PlaneProblem(
    #planes
    ['AC-' + str(i) for i in range(m)],

    #the flights
    ['AC' + str(i) for i in range(n)],

    #flights each plane can fly
    [['AC-' + str(j)] + ['AC' + str(i) for i in range(n)] for j in range(m)],

    #flights each plane can start with
    [['AC-' + str(j)] + ['AC' + str(i) for i in range(n)] for j in range(m)],

    #Flights that can follow each other
    [(x, y) for x, y in
     list(itertools.permutations(
         ['AC' + str(i) for i in range(n)], r=2)) if x != y],
    #maintenance depots at end of these flights
    ['AC' + str(i) for i in range(n)],
    #Min maintenance frequency
    n)


def do_test(n, cmd, pi, nsolns, complete=True):
    fail = False
    solns = solve_planes(pi, 'GAC', complete, 'mrv', True)
    if len(solns) != nsolns:
        fail = True
        print("Error: expected {} solution()s got {}".format(nsolns,len(solns)))
    for s in solns:
        if not check_plane_solution(pi, s):
            print("Error: got invalid solution")
            fail = True
            break

    if fail:
        print("\nFail Q6 test {}\nErrors were generated on the following code:".format(n+1))
        print(cmd)
    else:
        print("Pass Q6 test {}".format(n+1))
    print_sep()

def print_sep(c='-'):
    l = max([len(t) for t in titles])
    print(c*l)

if __name__ == '__main__':
    do_test(7, "python plane_scheduling.py -a GAC 7 -c", p7, 192)
