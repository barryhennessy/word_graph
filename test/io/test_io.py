from unittest import TestCase
from io import IO

__author__ = 'barryhennessy'


class TestIO(TestCase):
    """Tests for IO operations and reading dictionaries"""

    # This assumes tests are being run from the project root directory
    valid_path = "test/io/dummy_dictionary.csv"
    valid_path_with_blanks = "test/io/dictionary_with_blanks.csv"

    def test_raises_on_non_readable_path(self):
        io = IO()
        with self.assertRaises(IOError):
            reader = io.read_dictionary("path/that/doesnt/exist")

            for line in reader:
                pass

    def test_reads_correct_entries(self):
        io = IO()
        reader = io.read_dictionary(self.valid_path)

        values = list(reader)

        self.assertListEqual(values, ["foo", "bar", "baz"])

    def test_reads_correct_entries_despite_blanks(self):
        io = IO()
        reader = io.read_dictionary(self.valid_path_with_blanks)

        values = list(reader)

        self.assertListEqual(values, ["foo", "bar", "baz"])

    def test_reads_entries_as_strings(self):
        io = IO()
        reader = io.read_dictionary(self.valid_path_with_blanks)

        values = list(reader)

        for value in values:
            self.assertIsInstance(value, str)
