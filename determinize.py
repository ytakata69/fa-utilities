#!/usr/bin/env python3

# Determinize an nfa
#
# You need to install PyYAML module:
# $ pip install pyyaml
#
# Usage:
# $ ./determize.py < m22.yml
#
# This program reads a description of an NFA in YAML format
# from stdin.

import yaml
import sys
from collections import deque

nfa = yaml.safe_load(sys.stdin)

# Reform the data structure (from a list to a dict).
delta = {}
for q, a, q2 in nfa['delta']:
    if (q, a) not in delta:
        delta[(q, a)] = set()
    delta[(q, a)].add(q2)

# Epsilon closure
def bfs(q):
    cls = {q}
    worklist = deque()
    worklist.append(q)
    while len(worklist) > 0:
        q = worklist.popleft()
        if (q, 'eps') in delta:
            for q2 in delta[(q, 'eps')]:
                if q2 not in cls:
                    cls.add(q2)
                    worklist.append(q2)
    return cls

eclosure = {q: bfs(q) for q in nfa['Q']}

def eps_closure(qs):
    cl = set()
    for q in qs:
        cl.update(eclosure[q])
    return cl

# Construct a dfa
start = eps_closure(set([nfa['start']]))
dfa = {
    'Q': set(),
    'Sigma': nfa['Sigma'],
    'delta': {},
    'start': tuple(sorted(start)),
    'F': set()
}

worklist = deque()
worklist.append(dfa['start'])

while len(worklist) > 0:
    qd = worklist.popleft()
    if qd not in dfa['Q']:
        dfa['Q'].add(qd)
        for a in nfa['Sigma']:
            dest = set()
            for q in qd:
                if (q, a) in delta:
                    dest |= delta[(q, a)]
            dest = eps_closure(dest)
            dest = tuple(sorted(dest))
            dfa['delta'][(qd, a)] = dest
            worklist.append(dest)

dfa['F'] = [qd for qd in dfa['Q'] if not set(qd).isdisjoint(set(nfa['F']))]

# Reform the data structure (from tuples & sets to lists)
dfa['Q'] = [list(qd) for qd in dfa['Q']]
dfa['F'] = [list(qd) for qd in dfa['F']]
dfa['start'] = list(dfa['start'])
dfa['delta'] = [(list(q), a, list(dfa['delta'][(q, a)]))
    for (q, a) in dfa['delta']]

def tuple_representer(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data,
        flow_style=True)
yaml.add_representer(tuple, tuple_representer)

print(yaml.dump(dfa,
      default_flow_style=None, sort_keys=False))
