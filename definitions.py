class DBRow():
    """ Class for representing rows in tables. """

    def __init__(self, row, givenCols, cols, types):
        """ Initialize a new row.
        Arguments:
        row -- a list of values to form the new row
        givenCols -- a list of columns that values have been
            specified for, columns not in this list will get
            default values
        cols -- a list of all the columns for the row
        types -- a list of types for the columns, where
            types[i] is the type for column cols[i]
        """

        self.values = []
        self.cols = []
        given = dict(zip(givenCols, row))
        for col, type in zip(cols, types):
            try:
                val = DBValue(given[col], type)
            except KeyError:
                val = DBValue(None, type)
            self.values.append(val)
            self.cols.append(col)

    def __hash__(self):
        """ Override for more complex hashing. """

        return hash(self.v)

    def toString(self, cols=None):
        """ Print row. cols specifies which columns to print, or all if cols=None. """

        s = ""
        for val, col in zip(self.values, self.cols):
            if not cols or col in cols:
                s += " | " + str(col) + ": " + str(val)

        return s[3:]

    def __str__(self):
        return self.toString()

    def __getitem__(self, key):
        """ Implemented so DBRows can be accessed like dictionaries. """

        return self.values[self.cols.index(key)]

def DBValue(val, type):
    """ Factory function for generating DBValues.
    Chooses actual class depending on specified type.
    """

    for cls in DBGenericValue.__subclasses__():
        if cls.type == type:
            return cls(val, type)
    raise ValueError()

class DBError(Exception):
    """ Base class for database errors.
    Can be given a message to be printed with the error.
    """

    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.__class__.__name__ + (": " + self.msg if self.msg else "")

class DBTypeError(DBError): pass

from dbvalue import *
