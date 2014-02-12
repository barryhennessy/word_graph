# Word graph
`word_graph.py` builds word graphs based on a given dictionary with words
connected if they're one character different. It also calculates paths from one
word to another. Optionally it can calculate all paths from one to another.
For full documentation run `word_graph.py -h` which will print help
information.

Sample data files of various sizes can be found in 'data/'.

### Unit tests
To run the unit tests simply run `python -m unittest discover` from the root
directory.