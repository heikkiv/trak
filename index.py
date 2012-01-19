from definitions import *

class AbstractIndex:
    """ Baseclass for all indices """

    def __init__(self, name, col):
        """ Initialize index.
        Arguments:
        name -- name of the index, used to identify it
        col -- the column the index is on
        """

        pass

    def searchRange(self, low, high):
        """ Return a list of rows, where low <= key <= high """

        DBError("This index does not support range searces")

    def searchExact(self, key): 
        """ Return a list of rows matching key key or
        an empty list if none match.
        """
    
        pass

    def clear(self): 
        """ Empty the entire index. """
    
        pass

    def insert(self, row): 
        """ Insert the given row into the index.
        Generate the key based on the column specified
        when the index was initialized.
        """
    
        pass

    def delete(self, row): 
        """ Delete the given row from the index. """
    
        pass

# Exceptions related to indexes
class DBIndexError(DBError): pass

# Import your custom indices here.
# Them modify Index.create() to use them/it.

from linearindex import LinearIndex

class Index:
    """ A class to function as an interface for the actual index -classes. """
    indexClass = LinearIndex

    @classmethod
    def create(cls, name, col):
        """ Create a new index with name name on column col. """
        index = cls.indexClass(name, col)
        return index
