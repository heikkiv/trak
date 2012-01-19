from index import AbstractIndex, DBIndexError

# !! If you are not using the specific index.py given for this round, remember to change 
# the index being used either with the by modifying line 53 of the index.py -file
# e.g. line 55: indexClass = BinaryIndex

class BinaryIndex(AbstractIndex):
    """ An index implemented using a binary tree """

    def __init__(self, name, col):
        """ Initialize index.
        Arguments:
        name -- name of the index, used to identify it
        col -- the column the index is on
        """

        # TODO: Implement this
        pass

    def searchExact(self, key):
        """ Return a list of rows matching key key or
        an empty list if none match.
        """
        
        # TODO: Implement this
        pass

    def searchRange(self, low, high):
        """ Return a list of rows, where low <= key <= high 
        A value of None for low simply means key <= high and
        likewise a value of None for high means key >= low
        """

        # TODO: Implement this
        pass

    def clear(self):
        """ Empty the entire index. """

        # TODO: Implement this
        pass

    def insert(self, row):
        """ Insert the given row into the index. Generate
        the key based on the column specified
        when the index was initialized.
        """
    
        # TODO: Implement this
        pass

    def delete(self, row):
        """ Delete the given row from the index. """
    
        # TODO: Implement this
        pass
