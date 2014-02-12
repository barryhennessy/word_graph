from unittest import TestCase
from graph import WordGraph

__author__ = 'barryhennessy'


class TestWordGraph(TestCase):
    """Tests for the word graph class"""

    def test_are_connected_throws_key_error_on_non_existent(self):
        graph = WordGraph()
        graph.add("foo")
        with self.assertRaises(KeyError):
            graph.are_connected("foo", "bar")

    def test_are_connected_if_connected(self):
        graph = WordGraph()
        graph.add("hat")
        graph.add("mat")

        self.assertTrue(graph.are_connected("hat", "mat"))

    def test_connection_with_off_length_words(self):
        graph = WordGraph()
        graph.add("boo")
        graph.add("boom")

        self.assertTrue(graph.are_connected("boo", "boom"))

    def test_are_connected_if_not_connected(self):
        graph = WordGraph()
        graph.add("foo")
        graph.add("bar")

        self.assertFalse(graph.are_connected("foo", "bar"))

    def test_add_word_connects_vertices(self):
        graph = WordGraph()
        graph.add("hat")
        graph.add("mat")

        self.assertTrue(graph.are_connected("hat", "mat"))

    def test_add_word_connects_bidirectionally(self):
        graph = WordGraph()
        graph.add("hat")
        graph.add("mat")

        self.assertTrue(graph.are_connected("hat", "mat"))
        self.assertTrue(graph.are_connected("mat", "hat"))

    def test_add_word_no_self_loop(self):
        graph = WordGraph()
        graph.add("hat")
        graph.add("mat")

        self.assertFalse(graph.are_connected("hat", "hat"))

    def test_add_word_no_self_loop_if_added_twice(self):
        graph = WordGraph()
        graph.add("hat")
        graph.add("mat")
        graph.add("hat")

        self.assertFalse(graph.are_connected("hat", "hat"))

    def test_find_path_finds_correctly(self):
        graph = WordGraph()
        graph.add("hat")
        graph.add("cat")
        graph.add("car")

        path = graph.find_path("hat", "car")

        self.assertListEqual(path, ["hat", "cat", "car"])

    def test_find_path_raises_key_error_if_word_not_in_graph(self):
        graph = WordGraph()
        graph.add("hat")
        graph.add("cat")
        graph.add("car")

        with self.assertRaises(KeyError):
            graph.find_path("hat", "tree")

    def test_find_path_finds_only_one(self):
        graph = WordGraph()
        graph.add("hat")
        graph.add("cat")
        graph.add("car")
        graph.add("bar")
        graph.add("bat")

        path = graph.find_path("hat", "car")

        self.assertTrue(len(path), 1)

    def test_find_path_executes_with_cycle(self):
        graph = WordGraph()
        graph.add("cat")
        graph.add("car")
        graph.add("bar")
        graph.add("bat")

        path = graph.find_path("cat", "bar")

        self.assertIsInstance(path, list)

    def test_find_path_to_self_raises_value_error(self):
        graph = WordGraph()
        graph.add("hat")
        graph.add("cat")

        with self.assertRaises(ValueError):
            graph.find_path("hat", "hat")

    def test_find_path_finds_none_when_none_exist(self):
        graph = WordGraph()
        graph.add("cat")
        graph.add("car")
        graph.add("man")

        path = graph.find_path("cat", "man")

        self.assertIs(path, None)

    def test_find_path_with_n_letter_combinations(self):
        graph = WordGraph()
        graph.add("cat")
        graph.add("cats")
        graph.add("bats")
        graph.add("batt")
        graph.add("batty")
        graph.add("car")

        path = graph.find_path("cat", "batty")

        self.assertListEqual(path, ["cat", "cats", "bats", "batt", "batty"])

    def test_find_all_paths_find_all_correctly(self):
        graph = WordGraph()
        graph.add("hat")
        graph.add("cat")
        graph.add("car")
        graph.add("bar")
        graph.add("bat")

        paths = graph.find_all_paths("hat", "bar")

        expected_paths = [
            ["hat", "cat", "bat", "bar"],
            ["hat", "bat", "bar"],
            ["hat", "cat", "car", "bar"],
            ["hat", "bat", "cat", "car", "bar"],
        ]

        for path in paths:
            self.assertIn(path, expected_paths)

        self.assertEqual(len(paths), len(expected_paths))

    def test_find_all_paths_to_self_raises_value_error(self):
        graph = WordGraph()
        graph.add("hat")
        graph.add("cat")

        with self.assertRaises(ValueError):
            graph.find_all_paths("hat", "hat")

    def test_find_all_paths_raises_key_error_if_word_not_in_graph(self):
        graph = WordGraph()
        graph.add("hat")
        graph.add("cat")
        graph.add("car")

        with self.assertRaises(KeyError):
            graph.find_all_paths("hat", "tree")

    def test_find_all_paths_find_none_when_none(self):
        graph = WordGraph()
        graph.add("hat")
        graph.add("cat")
        graph.add("car")
        graph.add("bar")
        graph.add("bat")
        graph.add("alone")

        paths = graph.find_all_paths("hat", "alone")

        self.assertIs(paths, None)

    def test_find_all_paths_with_n_letter_combinations(self):
        graph = WordGraph()
        graph.add("cat")
        graph.add("cats")
        graph.add("bats")
        # I'll admit, I'm no scrabble champion
        graph.add("batt")
        graph.add("batty")
        graph.add("car")
        graph.add("ate")
        graph.add("bate")

        paths = graph.find_all_paths("cat", "batty")

        expected_paths = [
            ["cat", "cats", "bats", "batt", "batty"],
            ["cat", "ate", "bate", "bats", "batt", "batty"],
            ["cat", "cats", "bats", "bate", "batt", "batty"],
            ["cat", "ate", "bate", "batt", "batty"],
        ]
        for path in paths:
            self.assertIn(path, expected_paths)

        self.assertEqual(len(paths), len(expected_paths))