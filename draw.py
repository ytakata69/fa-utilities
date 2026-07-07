#!/usr/bin/env python3

# Draw a DFA or an NFA using Dot.
#
# You need to install PyYAML module:
# $ pip install pyyaml
#
# Usage:
# $ ./draw.py < m22.yml | dot -Tpdf > m22.pdf
#
# This program reads a description of an NFA in YAML format
# from stdin.

import yaml
import sys
from collections import deque

finalNodeStyle = "[style=filled, fillcolor=gray]"
eps = "eps"

nfa = yaml.safe_load(sys.stdin)

# Reform the states if they are lists.
if type(nfa['Q'][0]) is list:
    nfa['Q'] = [''.join(qs) for qs in nfa['Q']]
    nfa['F'] = [''.join(qs) for qs in nfa['F']]
    nfa['start'] = ''.join(nfa['start'])
    nfa['delta'] = [[''.join(q), a, ''.join(q2)] for q, a, q2 in nfa['delta']]

# List to set
nfa['F'] = set(nfa['F'])

# Reform the data structure (from a list to a dict).
delta = {}
for q, a, q2 in nfa['delta']:
    assert q in nfa['Q']
    assert a == eps or a in nfa['Sigma']
    if q not in delta:
        delta[q] = {}
    if q2 not in delta[q]:
        delta[q][q2] = []
    delta[q][q2].append(str(a))

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
        print(f'  "{q}"', finalNodeStyle if q in nfa['F'] else "")
        worklist.extend(sorted(delta[q].keys()))

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
        for q2 in delta[q]:
            act = ",".join(delta[q][q2])
            print(f'  "{q}" -> "{q2}" [label = "{act}"]')
        worklist.extend(sorted(delta[q].keys()))

# Trailer
print()
print("}")

