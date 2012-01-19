from index import AbstractIndex, DBIndexError

class LinearIndex(AbstractIndex):
    """ A primitive index using linear search"""

    def __init__(self, name, col):
        """ Initialize index.
        Arguments:
        name -- name of the index, used to identify it
        col -- the column the index is on
        """

        self.name = name
        self.col = col
        self.keys = []
        self.rows = []

    def searchExact(self, key):
        """ Return a list of rows matching key key or
        an empty list if none match.
        """

        # TODO: Implement this using a linear search of the sorted list self.keys
        # The index of the matching key in self.keys is also the index for the row in self.rows
        # that matches the search, so once you've found the index for the matching key, you can
        # just return self.rows[index] (or [] if no match is found)

        raise DBIndexError("Searching this index has not been implemented yet!")

    def clear(self):
        """ Empty the entire index. """

        self.keys = []
        self.rows = []

    def insert(self, row):
        """ Insert the given row into the index at the correct position, to keep
        the index sorted. Generate the key based on the column specified
        when the index was initialized.
        """
    
        key = row[self.col]

        if self.keys and self.rows:
            length = len(self.keys)
            i = 0
            while i < length and self.keys[i] < key:
                i += 1

            if i < length and self.keys[i] == key:
                self.rows[i].append(row)
            else:
                self.keys.insert(i, key)
                self.rows.insert(i, [row])
        else:
            self.keys.append(key)
            self.rows.append([row])

    def delete(self, row):
        """ Delete the given row from the index. """
    
        r = self.searchExact(row)
        if len(r) > 1:
            r.remove(row)
        else:
            try:
                self.rows.remove(r)
            except ValueError:
                raise DBIndexError("Delete failed! Row not found!")
