# storage.table
from definitions import *
from index import Index
import pickle

class BasicTable:
    """ Basic database table class. """

    def __init__(self, name, cols, types): 
        """ Initialize table.
        Arguments:
        name -- name of the table, used to identify it
        cols -- names of the columns in the table
        types -- types of the columns in the table, such that
            types[i] is the type for column cols[i] 
        """

        self.cols = cols
        self.types = types
        self.name = name
        self.rows = []
        self.indexes = []

    def createIndex(self, name, col): 
        """ Create an index on the table.
        Arguments:
        name -- name of the index, used to identify it
        col -- name of column to be used as key for the index
        """
    
        index = Index.create(name, col)
        self.indexes.append(index)
        for row in self.rows:
            index.insert(row)

    def dropIndex(self, name): 
        """ Drop the index named name. """
    
        index = None
        for i in self.indexes:
            if i.name == name:
                index = i
                break

        if index:
            self.indexes.remove(index)
        else:
            raise DBTableError("No such index found!")

    def getIndexes(self): 
        """ Return a list of all the indices for the table.
        Shouldn't probably be used any time other than when saving
        the database to disk. In other cases getIndex() is probably
        the correct method to call.
        """
    
        return self.indexes

    def insert(self, row, cols): 
        """ Insert the given row into the table.
        Arguments:
        row -- a list of values for the columns, should be converted
            to a DBRow before adding it to the table
        cols -- a list of the columns that values have been specified for
        """
    
        row = DBRow(row, cols, self.cols, self.types)
        self.rows.append(row)
        for i in self.indexes:
            i.insert(row)

    def delete(self, row): 
        """ Delete from the table and indices the DBRow specified by row. """
        
        self.rows.remove(row)
        for i in self.indexes:
            i.delete(row)

    def getIndex(self, col): 
        """ Return the first index for column col. """
        
        for i in self.indexes:
            if i.col == col:
                return i

        return None

    @classmethod
    def sort(cls, col, reverse, rows):
        """ Return a list of the given rows sorted on column col.
        Arguments:
        cls -- class for which the method is called, like self for instance mehtods
        col -- column on which to sort
        reverse -- whether the order should be reversed
        rows -- a list of the rows to sort
        """

        # TODO: Implement this method using the search algorithm you designed

        raise DBError("Sorting has not been implemented!")

# Exceptions related to tables
class DBTableError(DBError): pass

class Table:
    """ A class to function as an interface for the actual table -classes. """
    tables = [] # A list of all tables in the database

    @classmethod
    def create(cls, name, cols, types):
        """ Create a new table and add it to list of tables currently
        in the database.
        Arguments:
        name -- the name used to identify the table
        cols -- names of the columns in the table
        types -- types for the columns of the table
        """

        table = BasicTable(name, cols, types) # Modify this line to use your custom table
        cls.tables.append(table)
        return table

    @classmethod
    def list(cls):
        """ Return a list of the tables in the database """

        return cls.tables

    @classmethod
    def saveTables(cls, filename):
        """ Save the database to a file named filename. """

        file = open(filename, 'wb')
        pickle.dump(cls.tables, file)

    @classmethod
    def loadTables(cls, filename):
        """ Load the database from a file named filename. """

        file = open(filename, 'rb')
        cls.tables = pickle.load(file)

    @classmethod
    def get(cls, name):
        """ Get the table named name or raise DBTableError if
        no such table is found.
        """

        for t in cls.tables:
            if t.name == name:
                return t
        raise DBTableError("Table not found!")

    @classmethod
    def drop(cls, name):
        """ Drop the table named name or raise DBTableError if
        no such table is found.
        """

        for t in cls.tables:
            if t.name == name:
                cls.tables.remove(t)
                return
        raise DBTableError("Table not found!")

