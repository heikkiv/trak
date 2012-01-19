#!/usr/bin/env python
import queryproc
from definitions import *


""" Interpreter for the database.
Run this from the command line with ./minidb.py or python minidb
"""

usage = """Usage:
    (All commands are case insensitive. In fact, they are converted to lowercase before
    being parsed, which is also why all column, table and index names are always lowercase,
    as well as any text strings inserted into the database)

    To create a table named <table_name> with columns named <col1_name>, <col2_name>
    of type <col1_type>, <col2_type>:
        create table <table_name> (<col1_name> <col1_type>, <col2_name> <col2_type>, ...)
    To create an index named <index_name> on table <table_name> column <col_name>:
        create index <index_name> on <table_name> (<col_name>)

    To insert a row into table <table_name>, you can either specify values for all columns in the table,
    making sure to give the values in the correct order:
        insert into <table_name> values (<val1>, <val2>, ...)
    or you can specify which columns you are giving values for, and in which order, adn the rest of the columns
    will be given default values:
        insert into <table_name> (<col1_name>, <col2_name>, ...) values (<val1>, <val2>, ...)

    To select values from the table <table_name>, you can either choose to print values for all columns:
        select * from <table_name>
    or only selected columns:
        select (<col1_name>, <col2_name>, ...) from <table_name>
    Additionally, you can choose to order the results by column <col_name> in either asc or desc <direction>:
        select * from <table_name> order by <col_name> <direction>
    Also, you can select only specific rows:
        select * from <table_name> where <col_name><op><value>
    Supported operations <op> are =, ==, !=, <, <=, >, >=. You can also chain these with: and, or.
    Some where-clauses can't be satisfied by the indexes, so they are parsed manually, in which case,
    the database will tell you "Unable to use any index".
    Some examples of selecting values from a table created with 'create table t1 (id int, name string, val int)':
        select * from t1 order by id asc
        select (id, name) from t1 where val>=3 order by val desc
        select * from t1 where id>3 and val!=4

    To delete rows from <table_name> you use 'where' to specify which rows, just like when selecting rows.
    For example:
        delete from <table_name> where <col_name><op><value>

    To drop a table named <table_name>:
        drop table <table_name>
    To drop an index <index_name> on table <table_name>:
        drop index <index_name> on <table_name>

    Additional commands:
        .exit -- exit the interpreter
        .help -- this usage information
        .factory -- generate a simple table with an index and a few rows, for testing
        .save <file_name> -- save the entire database to a file named <file_name>
        .load <file_name> -- load a previously saved database from a file named <file_name>

    Commands are usually split on whitespace. To input strings with whitespaces into the database, put the
    string inside single or double quotes (e.g. ' or ")

    Supported types for table columns are:
        int -- python integer
        double -- python float
        string -- string
        boolean -- True or False

    For more information, see the source!
"""

class DBCommandNotFound(DBError): pass

def runCommand(cmd):
    cmd.lower()
    cmds = cmd.split()
    if cmds[0] == "exit" or cmds[0] == "quit":
        return True
    elif cmds[0] == "help":
        print usage
    elif cmds[0] == "factory":
        cmds = ["create table t1 (id int, name string, val int)", \
                "create index i1 on t1 (id)", \
                "insert into t1 values (3, s, 5)", \
                "insert into t1 values (2, o, 6)", \
                "insert into t1 values (1, e, 7)", \
                "insert into t1 values (5, d, 3)", \
                "insert into t1 values (4, i, 4)", \
                "select * from t1"]
        for c in cmds:
            print "> " + c
            queryproc.processQuery(c)
    elif cmds[0] == "save":
        queryproc.saveTables(cmds[1])
    elif cmds[0] == "load":
        queryproc.loadTables(cmds[1])
    else:
        raise DBCommandNotFound()

def runInterpreter():
    print "Loading interpreter ..."
    print "Type .help for usage"

    while True:
        try:
            input = raw_input("> ")
            if input[0] == '.': # '.' -prefix means command
                if runCommand(input[1:]):
                    break
            elif input[0] == '#': pass # '#' -prefix means comment
            else: # process sql
                queryproc.processQuery(input)
        except DBError as e:
            print str(e)

if __name__ == "__main__":
    print "Loading minidb ..."
    runInterpreter()
