#!/usr/bin/env python3

# Minimize a dfa
#
# You need to install PyYAML module:
# $ pip install pyyaml
#
# Usage:
# $ ./minimize.py < m29.yml
#
# This program reads a description of a DFA in YAML format
# from stdin.

import yaml
import sys
from collections import deque

dfa = yaml.safe_load(sys.stdin)

# Reform the states if they are lists.
if type(dfa['Q'][0]) is list:
    dfa['Q'] = [''.join(qs) for qs in dfa['Q']]
    dfa['F'] = [''.join(qs) for qs in dfa['F']]
    dfa['start'] = ''.join(dfa['start'])
    dfa['delta'] = [[''.join(q), a, ''.join(q2)] for q, a, q2 in dfa['delta']]

# Reform the data structure (from a list to a dict).
delta = {}
for q, a, q2 in dfa['delta']:
    assert (q, a) not in delta, "not a dfa"
    assert q in dfa['Q']
    assert a in dfa['Sigma']
    delta[(q, a)] = q2

for q in dfa['Q']:
    for a in dfa['Sigma']:
        assert (q, a) in delta, f"no transition for {(q, a)}"

# from a list to a set
dfa['Q'] = frozenset(dfa['Q'])
dfa['F'] = frozenset(dfa['F'])
assert dfa['F'] <= dfa['Q'], "F is not a subset of Q"

# Construct the minimized dfa
mindfa = {
    'Q': [dfa['F'], dfa['Q'] - dfa['F']],
    'Sigma': dfa['Sigma'],
    'delta': {},
    'start': None,
    'F': set()
}
group = {}
for i, qd in enumerate(mindfa['Q']):
    for q in qd:
        group[q] = i

while True:
    tobreak = []
    for i, qd in enumerate(mindfa['Q']):
        if len(qd) <= 1:
            continue
        for a in mindfa['Sigma']:
            groupset = set()
            for q in qd:
                groupset.add(group[delta[(q, a)]])
            if len(groupset) >= 2:
                tobreak.append((i, a))
                break
        if len(tobreak) > 0:
            break
    if len(tobreak) <= 0:
        break

    i, a = tobreak.pop()
    qd = mindfa['Q'][i]
    newqd = {}
    for q in qd:
        g = group[delta[(q, a)]]
        if g not in newqd:
            newqd[g] = set()
        newqd[g].add(q)
    newqd = list(newqd.values())
    mindfa['Q'][i] = newqd[0]
    for j in range(1, len(newqd)):
        g = len(mindfa['Q'])
        for q in newqd[j]:
            group[q] = g
        mindfa['Q'].append(newqd[j])

mindfa['Q'] = [tuple(sorted(qd)) for qd in mindfa['Q']]

for qd in mindfa['Q']:
    for a in mindfa['Sigma']:
        q2g = group[delta[(qd[0], a)]]
        mindfa['delta'][(qd, a)] = mindfa['Q'][q2g]

mindfa['start'] = mindfa['Q'][group[dfa['start']]]

for q in dfa['F']:
    mindfa['F'].add(mindfa['Q'][group[q]])

# Reform the data structure (from tuples & sets to lists)
mindfa['Q'] = [list(qd) for qd in mindfa['Q']]
mindfa['F'] = [list(qd) for qd in mindfa['F']]
mindfa['start'] = list(mindfa['start'])
mindfa['delta'] = [(list(q), a, list(mindfa['delta'][(q, a)]))
    for (q, a) in mindfa['delta']]

def tuple_representer(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data,
        flow_style=True)
yaml.add_representer(tuple, tuple_representer)

print(yaml.dump(mindfa,
      default_flow_style=None, sort_keys=False))
