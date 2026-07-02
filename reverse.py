#!/usr/bin/env python3

# Reverse an nfa
#
# You need to install PyYAML module:
# $ pip install pyyaml
#
# Usage:
# $ ./reverse.py < m22.yml
#
# This program reads a description of an NFA in YAML format
# from stdin.

import yaml
import sys

nfa = yaml.safe_load(sys.stdin)

eps = "eps"

# Reform the states if they are lists.
if type(nfa['Q'][0]) is list:
    nfa['Q'] = [''.join(qs) for qs in nfa['Q']]
    nfa['F'] = [''.join(qs) for qs in nfa['F']]
    nfa['start'] = ''.join(nfa['start'])
    nfa['delta'] = [[''.join(q), a, ''.join(q2)] for q, a, q2 in nfa['delta']]

# Add a new initial state
qnamelens = set(map(len, nfa['Q'])) # the set of lengths of state names
l = min(i for i in range(1, len(nfa['Q']) + 1) if i not in qnamelens)
init = 'q' + ('0' * (l - 1))

# Construct the reversed nfa
rnfa = {
    'Q': nfa['Q'] + [init],
    'Sigma': nfa['Sigma'],
    'delta': [[q2, a, q1] for q1, a, q2 in nfa['delta']],
    'start': init,
    'F': [nfa['start']]
}

for qf in nfa['F']:
    rnfa['delta'].append((init, eps, qf))

def tuple_representer(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data,
        flow_style=True)
yaml.add_representer(tuple, tuple_representer)

print(yaml.dump(rnfa,
      default_flow_style=None, sort_keys=False))
