from definitions import *
from table import Table
from index import Index, DBIndexError
from functools import partial
import re

def tokenize(q):
    """ Split given query into tokens for further processing.
    Should be split on whitespace, unless inside quotes.
    Anything inside parentheses should become a nested list.
    """

    global s 
    s = q
    tokens = [""]
    quote = False
    while s:
        if s[0] == " " or s[0] == ",":
            if quote:
                tokens[-1] += s[0]
            else:
                tokens.append("")
                if s[1] == " ":
                    s = s[1:]
        elif s[0] == "'" or s[0] == '"':
            if quote:
                quote = False
            else:
                quote = True
        elif s[0] == "(":
            s = s[1:]
            tokens[-1] = tokenize(s)
        elif s[0] == ")":
            return tokens
        elif s[0] == ";":
            return tokens
        else:
            tokens[-1] += s[0]

        s = s[1:]

    return tokens

def _functionize(fn, q):
    """ Semi-recursively go through the tokens, building a partial
    function that will eventually be called to actually modify the database.
    """

    if not q:
        pass
    elif q[0] == "create":
        if q[1] == "table":
            fn = partial(createTable, table=q[2], cols=q[3])
        elif q[1] == "index":
            fn = partial(createIndex, index=q[2], table=q[4], cols=q[5])
        else:
            raise QueryError("Specify whether to create a table or an index!")
    elif q[0] == "drop":
        if q[1] == "table":
            fn = partial(dropTable, table=q[2])
        elif q[1] == "index":
            fn = partial(dropIndex, index=q[2], table=q[4])
        else:
            raise QueryError("Specify whether to drop a table or an index!")
    elif q[0] == "insert":
        if q[3] == "values":
            fn = partial(insert, table=q[2], row=q[4])
        else:
            fn = partial(insert, table=q[2], cols=q[3], row=q[5])
    elif q[0] == "select":
        fn = partial(select, select=q[1], table=q[3])
        q = q[4:] if len(q) > 4 else []
        fn = _functionize(fn, q)
    elif q[0] == "delete":
        fn = partial(delete, table=q[2])
        q = q[3:] if len(q) > 3 else []
        fn = _functionize(fn, q)
    elif q[0] == "where":
        q.pop(0)
        conds = []
        while len(q) > 0 and not q[0] == "order":
            conds.append(q.pop(0))
        fn = _functionize(partial(fn, where=conds), q)
    elif q[0] == "order":
        q = q[2:]
        order = (q.pop(0), False)
        if q:
            if q[0] == "desc":
                q.pop(0)
                order = (order[0], True)
            elif q[0] == "asc":
                q.pop(0)
        fn = _functionize(partial(fn, order=order), q)
    else:
        raise DBQueryError("Unknown token in query!")

    return fn

def functionize(q):
    fn = _functionize(None, q)

    return fn

def processQuery(q):
    q = q.lower()
    q = tokenize(q)
    q = functionize(q)
    q()

def select(table, select, where=None, order=None):
    """ Called for SELECT -queries. """

    table = Table.get(table)
    rows = _select(table, where)

    if order:
        rows = table.sort(order[0], order[1], rows[:])
    
    if select == '*':
        for r in rows:
            print r.toString()
    else:
        for r in rows:
            print r.toString(select)

def _select(table, where):
    """ Called for any query requiring specific rows. """

    if where:
        # First clean up excess whitespace, to simplify parsing
        where = re.split(r"(\w+ ?[<>!=][=<]? ?\w+|\w+)", ' '.join(where))
        where = [t.replace(' ', '') for t in where if t and not t.isspace()]
        try:
            rows = parseWhere(table, where)
        except DBIndexError as e:
            rows = []
            print str(e)

        if not rows:
            print "Unable to use any index"
            for r in table.rows:
                if _where(r, table, conds=where):
                    rows.append(r)
    else:
        rows = table.rows

    if not rows: # Check if we found anything
        raise DBRowNotFound("No matching rows found!")

    return rows

def parseWhere(table, where):
    """ Parse WHERE for use with an index. """

    keys, rows = [], []
    col, low, high = None, None, None
    for t in where:
        if t == "and":
            if keys: # Only try to and for range searches
                return []
        elif t == "or":
            index = table.getIndex(col)
            if index:
                type = table.types[table.cols.index(col)]
                if low or high:
                    if low:
                        low = DBValue(low, type)
                    if high:
                        high = DBValue(high, type)
                    for r in index.searchRange(low, high):
                        if not r in rows:
                            rows.append(r)
                else:
                    for i in range(len(keys)):
                        for r in index.searchExact(DBValue(keys[i], type)):
                            if not r in rows:
                                rows.append(r)
                col, low, high = None, None, None
                keys = []
            else:
                return []
        else:
            c, op, val = re.match(r"(\w+)([<>!=][=<]?)(.+)", t).groups()
            if op == "=" or op == "==":
                if not col:
                    col = c
                elif not col == c:
                    return []
                keys.append(val)
            elif op == "<":
                if not col:
                    col = c
                elif not col == c:
                    return []
                type = table.types[table.cols.index(col)]
                try:
                    if type == "double":
                        high = str(float(val) - 0.01)
                    elif type == "int":
                        high = str(int(val) - 1)
                    else:
                        return []
                except ValueError:
                    raise DBError("Incorrect argument in WHERE -clause")
            elif op == ">":
                if not col:
                    col = c
                elif not col == c:
                    return []
                type = table.types[table.cols.index(col)]
                try:
                    if type == "double":
                        low = str(float(val) + 0.01)
                    elif type == "int":
                        low = str(int(val) + 1)
                    else:
                        return []
                except ValueError:
                    raise DBError("Incorrect argument in WHERE -clause")
            elif op == "<=":
                if not col:
                    col = c
                elif not col == c:
                    return []
                high = val
            elif op == ">=":
                if not col:
                    col = c
                elif not col == c:
                    return []
                low = val
            else:
                return ([], [])

    index = table.getIndex(col)
    if index:
        type = table.types[table.cols.index(col)]
        if low or high:
            if low:
                low = DBValue(low, type)
            if high:
                high = DBValue(high, type)
            for r in index.searchRange(low, high):
                if not r in rows:
                    rows.append(r)
        else:
            for i in range(len(keys)):
                for r in index.searchExact(DBValue(keys[i], type)):
                    if not r in rows:
                        rows.append(r)
    else:
        return []

    return rows

def _where(row, table, **kwargs):
    """ Parse WHERE when no suitable index is found. """

    conds = []
    ops = []
    for t in kwargs['conds']:
        if t == "and":
            ops.append(lambda x,y: x and y)
        elif t == "or":
            ops.append(lambda x,y: x or y)
        else:
            key, op, val = re.match(r"(\w+)([<>!=][=<]?)(.+)", t).groups()
            val = DBValue(val, table.types[table.cols.index(key)]).val
            if op == "=" or op == "==":
                conds.append((key, lambda x, val=val: x == val))
            elif op == "!=":
                conds.append((key, lambda x, val=val: not x == val))
            elif op == "<":
                conds.append((key, lambda x, val=val: x < val))
            elif op == "<=":
                conds.append((key, lambda x, val=val: x <= val))
            elif op == ">":
                conds.append((key, lambda x, val=val: x > val))
            elif op == ">=":
                conds.append((key, lambda x, val=val: x >= val))
            else:
                raise DBQueryError("Unknown comparison operator!")

    bool = lambda x: False or x
    for (key, val), op in map(None, conds, ops):
            
        if op == None:
            bool = bool(val(row[key].val))
            break
        else:
            bool = bool(val(row[key].val))
            bool = partial(op, bool)
    
    return bool

def insert(**kwargs):
    """ Called for INSERT -queries. """

    table = Table.get(kwargs['table'])
    del kwargs['table']
    if not 'cols' in kwargs:
        kwargs['cols'] = table.cols
    table.insert(**kwargs)

def delete(table, where=None):
    """ Called for DELETE -queries. """

    table = Table.get(table)
    rows = _select(table, where)
    
    for row in rows:
        table.delete(row)

def createTable(**kwargs):
    """ CREATE table.
    kwargs['cols'] is a list of consecutive column name - type pairs
    i.e. [col1_name, col1_type, col2_name, col2_type, ...] which is why
    it gets split when calling Table.create()
    """

    Table.create(kwargs['table'], kwargs['cols'][::2], kwargs['cols'][1::2])

def createIndex(**kwargs):
    table = Table.get(kwargs['table'])
    table.createIndex(kwargs['index'], kwargs['cols'][0])

def dropTable(**kwargs):
    Table.drop(kwargs['table'])

def dropIndex(**kwargs):
    table = Table.get(kwargs['table'])
    table.dropIndex(kwargs['index'])

def saveTables(filename):
    Table.saveTables(filename)

def loadTables(filename):
    Table.loadTables(filename)

def getIndexClassName():
    return Index.indexClass

class DBQueryError(DBError): pass
class DBRowNotFound(DBError): pass
