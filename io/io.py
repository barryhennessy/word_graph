__author__ = 'barryhennessy'


class IO(object):
    """Handles all IO for word graph related operations"""

    def read_dictionary(self, path):
        """Reads the dictionary from path

        :param path: The path to the dictionary of words

        :return: A generator that reads the dictionary line by line
        """
        with open(path, "rU") as dictionary_file:
            for line in dictionary_file:
                line = line.strip()
                if line:
                    yield str(line)

