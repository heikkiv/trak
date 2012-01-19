from index import AbstractIndex, DBIndexError

class InterpolationIndex(AbstractIndex):
    """ A very basic and quite inefficient index """

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
        an empty list if none match. We do this by searching
        through the ordered list of keys in self.keys, and if
        we find a match, the index of the matching key in self.keys,
        is the index of the row in self.rows, that we want to return.
        """
    
        length = len(self.keys)

        # Initial bounds for the search
        low = 0
        high = len(self.keys) - 1

        while self.keys[low] <= key and self.keys[high] >= key: # Check if there still might be something to find
            # Calculate mid
            mid = low + ((key.val - self.keys[low].val) * (high - low)) / (self.keys[high].val - self.keys[low].val)

            if mid < 0 or mid >= length: # Check mid is not out of range
                break # Break if out of range

            # Check whether our mid is too high or too low, or maybe we already found the right key
            if self.keys[mid] < key:
                low = mid + 1
            elif self.keys[mid] > key:
                high = mid - 1
            else:
                return self.rows[mid]

        # Check if we narrowed down to a correct key
        if self.keys[low] == key:
            return self.rows[low]
        else: # No match found
            return []

    def clear(self):
        """ Empty the entire index. """
    
        self.keys = []
        self.rows = []

    def insert(self, row):
        """ Insert the given row into the index.
        Generate the key based on the column specified
        when the index was initialized. Then find the correct
        position for the key and row in the corresponding lists
        so that they stay in order.
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
