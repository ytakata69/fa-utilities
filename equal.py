#!/usr/bin/env python3

# Check the equality of two dfa's
#
# You need to install PyYAML module:
# $ pip install pyyaml
#
# Usage:
# $ ./equal.py m28.yaml < m29.yml
#
# This program reads descriptions of two DFA's in YAML format
# one from a file and the other from stdin.

import yaml
import sys

if len(sys.argv) != 2:
    print("Usage: ./equal.py file1 < file2", file=sys.stderr)
    exit(2)

with open(sys.argv[1]) as f:
    dfa1 = yaml.safe_load(f)
dfa2 = yaml.safe_load(sys.stdin)

def reform(dfa):
    """Reform the data structure."""

    # Reform the states if they are lists.
    if type(dfa['Q'][0]) is list:
        dfa['Q'] = [''.join(qs) for qs in dfa['Q']]
        dfa['F'] = [''.join(qs) for qs in dfa['F']]
        dfa['start'] = ''.join(dfa['start'])
        dfa['delta'] = [[''.join(q), a, ''.join(q2)] for q, a, q2
                        in dfa['delta']]

    # Reform the data structure (from a list to a dict).
    delta = {}
    for q, a, q2 in dfa['delta']:
        assert (q, a) not in delta, "not a dfa"
        assert q in dfa['Q']
        assert a in dfa['Sigma']
        delta[(q, a)] = q2
    dfa['delta'] = delta

    dfa['Sigma'] = set(dfa['Sigma'])
    dfa['Q'] = set(dfa['Q'])
    dfa['F'] = set(dfa['F'])

    assert dfa['F'] <= dfa['Q']
    for q in dfa['Q']:
        for a in dfa['Sigma']:
            assert (q, a) in delta, f"no transition for {(q, a)}"

reform(dfa1)
reform(dfa2)

assert dfa1['Sigma'] == dfa2['Sigma']

# Search for (F, nonF)
visited = set()
stack = [(dfa1['start'], dfa2['start'], "")]

while len(stack) > 0:
    (p, q, path) = stack.pop()
    if (p, q) not in visited:
        visited.add((p, q))
        if (p in dfa1['F']) != (q in dfa2['F']):
            print(f"Different with path={path}")
            exit(1)
        for a in dfa1['Sigma']:
            pn = dfa1['delta'][(p, a)]
            qn = dfa2['delta'][(q, a)]
            stack.append((pn, qn, path + str(a)))
print("Equal")
