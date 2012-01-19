from definitions import DBTypeError

class DBGenericValue(object):
    """ Base class for DBValues.
    Overrides lots of built-in methods to ease
    usage of DBValues.
    """

    def __str__(self):
        return str(self.val)

    def __hash__(self):
        """ Override in subclasses for customized hashing. """

        return hash(self.val)

    """ The following six rich comparison methods need to be
    implemented to allow DBValues to be used as keys in dicts.
    """
    def __lt__(self, other):
        return self.val < other

    def __le__(self, other):
        return self.val <= other

    def __eq__(self, other):
        return self.val == other

    def __ne__(self, other):
        return self.val != other

    def __ge__(self, other):
        return self.val >= other

    def __gt__(self, other):
        return self.val > other
    
class DBInt(DBGenericValue):
    type = "int"

    def __init__(self, val, type):
        if val == None:
            self.val = 0
        else:
            try:
                self.val = int(val)
            except ValueError:
                raise DBTypeError("Not integer!")

class DBDouble(DBGenericValue):
    type = "double"

    def __init__(self, val, type):
        if val == None:
            self.val = 0.0
        else:
            try:
                self.val = float(val)
            except ValueError:
                raise DBTypeError("Not double!")

class DBString(DBGenericValue):
    type = "string"

    def __init__(self, val, type):
        if val == None:
            self.val = ""
        else:
            self.val = val

class DBBoolean(DBGenericValue):
    type = "boolean"

    def __init__(self, val, type):
        if val == "true":
            self.val = True
        elif val == "false" or val == None:
            self.val = False
        else:
            raise DBTypeError("Not boolean!")
