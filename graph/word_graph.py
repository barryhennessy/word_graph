__author__ = 'barryhennessy'
from difflib import SequenceMatcher


class WordGraph(object):
    """Models a graph of words, providing functionality for searching over the
    graph for connections"""

    def __init__(self):
        """Initialises the graph"""
        self._graph = {}

    def are_connected(self, node_a, node_b):
        """Determines whether node_a and node_b are directly connected

        :param node_a: One of the nodes to check for a connection
        :param node_b: The other node to check for a connection

        :return: Bool. True if connected, false otherwise
        """
        node_a = node_a.lower()
        node_b = node_b.lower()

        return node_a in self._graph[node_b]

    def add(self, word):
        """Adds word to the graph

        :param word: The word to add

        :return: None
        """

        word = word.lower()

        if word not in self._graph:
            pre_existing_keys = self._graph.keys()
            self._graph[word] = []
            for existing_word in pre_existing_keys:
                if self._is_neighbouring(word, existing_word):
                    self._connect_nodes(word, existing_word)

    def _is_neighbouring(self, word_a, word_b):
        """Determines whether word_a and word_b are to be considered neighbours

        In this context being neighbours refers to having exactly 1 letter not
        in common.

        :param word_a: A word to check
        :param word_b: The other word to check

        :return: Bool True if word_a and word_b are neighbours. I.e. 1 letter
                      apart
        """

        # If they are to be neighbours they can have at most 1 letter out of
        # place, therefore if their lengths differ by more than 1 they're not
        # connected
        if abs(len(word_a) - len(word_b)) > 1:
            return False

        matches = SequenceMatcher(a=word_a, b=word_b).get_matching_blocks()

        # The number of matching chars will be the size of all the matching
        # pieces
        num_matches = 0
        for match in matches:
            num_matches += match.size

        longest_word_length = max(len(word_a), len(word_b))
        if longest_word_length - num_matches == 1:
            return True
        else:
            return False

    def _connect_nodes(self, node_a, node_b):
        """Connects the nodes a and b

        :param node_a: One of the words to be connected
        :param node_b: The other word to be connected

        :return: None
        """
        self._graph[node_a].append(node_b)
        self._graph[node_b].append(node_a)

    def find_path(self, from_node, to_node, path=[]):
        """Finds a path from from_node to to_node (if any exist)

        :param from_node: The node to initiate a search from
        :param to_node:   The destination node
        :param path:      The path previously traveled. Used to keep track of
                          marked nodes when calling recursively so as not to
                          re-trace steps and get stuck in a loop

        :raise ValueError: If the source and destination nodes are the same
        :raise KeyError:   If either the source or destination nodes are not in
                           the graph

        :return: List of strings, the path, if a path has been found,
                 None, if no path has been found
                 List of strings, a partial path may be returned during
                 intermediary recursive steps
        """
        self._ensure_common_path_traversal_requirements(from_node, to_node,
                                                        path)

        # Marking the current node and putting it in place in our path.
        path = path + [from_node]

        # We've reached our destination, stop recursing and return the path
        if from_node == to_node:
            return path

        for node in self._graph[from_node]:
            if node not in path:
                new_path = self.find_path(node, to_node, path)
                if new_path:
                    return new_path

        return None

    def find_all_paths(self, from_node, to_node, path=[]):
        """Finds all paths from from_node to to_node (if any exist)

        :param from_node: The node to initiate the search from
        :param to_node:   The destination node
        :param path:      The path previously travelled on this particular
                          path. This is used to keep track of nodes already
                          visited to avoid re-tracing steps and getting stuck.
                          It also serves as part output, since when it contains
                          the destination it is one of the paths we're looking
                          for.

        :raise ValueError: If the source and destination nodes are the same
        :raise KeyError:   If either the source or destination nodes are not in
                           the graph

        :return: List of a list of strings, the paths, if paths have been found
                 None, if no paths have been found
                 A list of strings may be returned from intermediary steps in
                 the recursive process when one of the paths have been found
        """

        self._ensure_common_path_traversal_requirements(from_node, to_node,
                                                        path)

        # Marking the current node and putting it in place in our current path.
        path = path + [from_node]

        if from_node == to_node:
            return [path]

        paths = []

        for node in self._graph[from_node]:
            if node not in path:
                new_paths = self.find_all_paths(node, to_node, path)
                if new_paths:
                    for new_path in new_paths:
                        paths.append(new_path)

        if len(paths) == 0:
            return None
        else:
            return paths

    def _ensure_common_path_traversal_requirements(self, from_node, to_node,
                                                   path):
        """Runs a number of checks to determine if the call to traverse the
        graph makes sense and should be run

        :param from_node: The node we're starting our search from
        :param to_node:   The destination node
        :param path:      The current path

        :raise ValueError: If the source and destination nodes are the same
        :raise KeyError:   If either the source or destination nodes are not in
                           the graph
        """

        if from_node not in self._graph:
            raise KeyError("The source node must be in the graph")

        if to_node not in self._graph:
            raise KeyError("The destination node must be in the graph")

        # If our initial call is to find a path from one node to itself we
        # raise an error to flag the nonsensical call.
        if len(path) == 0 and from_node == to_node:
            raise ValueError(
                "Nodes cannot be connected to themselves. \
                There are no self loops"
            )
