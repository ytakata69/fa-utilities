# fa-utilities

Simple utility programs for manipulating DFA/NFAs.

- `determinize.py` -- Convert NFA to DFA.
- `minimize.py` -- Construct a DFA with the minimum number of states.
- `reverse.py` -- Construct an NFA recognizing the set of reversed words.
- `equal.py` -- Test whether two DFAs are equivalent.
- `draw.py` -- Draw a state-transition diagram in Graphviz dot format.

These programs use [PyYAML](https://pypi.org/project/PyYAML/).
You need to install it with `pip install PyYAML`.
If you like to install it locally using
[venv](https://docs.python.org/ja/3/library/venv.html),
perform the following steps:

```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install PyYAML
```

## Input format

The programs accept NFA/DFA descriptions in the following YAML format.

```yaml
# a sample dfa (accepting a word with even number of 1's)
Q: [q0, q1]
Sigma: [0, 1]
start: q0
F: [q0]
delta:
  - [q0, 0, q0]
  - [q0, 1, q1]
  - [q1, 0, q1]
  - [q1, 1, q0]
```

```yaml
# a sample nfa (accepting a*b*)
Q: [q0, q1]
Sigma: [a, b]
start: q0
F: [q1]
delta:
  - [q0, a, q0]
  - [q0, eps, q1]
  - [q1, b, q1]
```

