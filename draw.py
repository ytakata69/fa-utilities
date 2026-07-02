#!/usr/bin/env python3

# Draw a DFA or an NFA using Dot.
#
# You need to install PyYAML module:
# $ pip install pyyaml
#
# Usage:
# $ ./draw.py < m22.yml > m22.dot
# $ dot -Tpdf m22.dot > m22.pdf
#
# This program reads a description of an NFA in YAML format
# from stdin.

import yaml
import sys
from collections import deque

nfa = yaml.safe_load(sys.stdin)

# Reform the states if they are lists.
if type(nfa['Q'][0]) is list:
    nfa['Q'] = [''.join(qs) for qs in nfa['Q']]
    nfa['F'] = [''.join(qs) for qs in nfa['F']]
    nfa['start'] = ''.join(nfa['start'])
    nfa['delta'] = [[''.join(q), a, ''.join(q2)] for q, a, q2 in nfa['delta']]

# Reform the data structure (from a list to a dict).
delta = {}
for q, a, q2 in nfa['delta']:
    assert q in nfa['Q']
    assert a == "eps" or a in nfa['Sigma']
    if (q, a) not in delta:
        delta[(q, a)] = set()
    delta[(q, a)].add(q2)

# Header
print("digraph nfa {")

# Nodes
print("  // node definitions")

worklist = deque()
worklist.append(nfa['start'])

visited = set()

while len(worklist) > 0:
    q = worklist.popleft()
    if q not in visited:
        visited.add(q)
        print(f'  "{q}"')
        for a in nfa['Sigma'] + ["eps"]:
            if (q, a) in delta:
                worklist.extend(sorted(delta[(q, a)]))

# Edges
print()
print("  // edge definitions")

worklist = deque()
worklist.append(nfa['start'])

visited = set()

while len(worklist) > 0:
    q = worklist.popleft()
    if q not in visited:
        visited.add(q)
        for a in nfa['Sigma'] + ["eps"]:
            if (q, a) in delta:
                for qt in delta[(q, a)]:
                    print(f'  "{q}" -> "{qt}" [label = "{a}"]')
                worklist.extend(sorted(delta[(q, a)]))

# Trailer
print()
print("}")

