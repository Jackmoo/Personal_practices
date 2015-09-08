#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

class BaseSdb:
    '''
    SQLlite db, generally 5 column as 
    
    Index
    Time(time.time() in python)
    Username
    Message
    RawSocketData
    
    '''
    def __init__(self, dbpath=None):
        if dbpath is None:
            self.dbpath = ':memory:'  # in memory
        else:
            self.dbpath = dbpath
        self.conn = sqlite3.connect(self.dbpath)
        # self.cur = self.conn.cursor()
    
    def check_table_exist(self, table):
        sql = "SELECT name from sqlite_master WHERE type='table' AND name='%s'" % table
        cursor = self.conn.cursor()
        print sql
        cursor.execute(sql)
        self.conn.commit()
        try:
            sqlResult = cursor.fetchone()
            if sqlResult:
                return True
            else:
                return False
        except:
            print 'check_table_exist error'

    def create_table(self, tableName, columnFormat):
        '''
        tableName is the table name
        recordFormat is the table element in dict
            i.e.
                Person(
                    PersonName text
                    PersonPhone integer
                    PersonAddress text
                )
                
                should input a dict as
                {'PersonName': 'text', 'PersonPhone': 'integer', 'PersonAddress': 'text'}
                other special format could also apply like 
                'PersonIndex': 'INTEGER PRIMARY KEY AUTOINCREMENT'
                
                data type in sqlite and python
                https://docs.python.org/2/library/sqlite3.html#sqlite-and-python-types
                only 5 type in sqlite3
                NULL     => Python None
                INTEGER  => Python int/long
                REAL     => Python float
                TEXT     => Python str (default unicode utf8)
                BLOB     => buffer (??)
        '''
        formatStr = ''
        for columnName, columnDataType in columnFormat.iteritems():
            formatStr += str(columnName) + ' ' + str(columnDataType) + ','
        
        formatStr = formatStr[:-1]  # remove last ','
        
        sql = "CREATE TABLE %s(%s)" % (tableName, formatStr)
        
        cursor = self.conn.cursor()
        print sql
        cursor.execute(sql)
        self.conn.commit()
        
    
    # not working yet
    def read_dict(self, table, row=6):
        '''
        read single record
        improved security with sqlite placeholder
        '''
        sql = "SELECT * FROM ?1 ORDER BY TIME LIMIT " + str(row) 
        
        ret = []
        
        with self.conn.cursor() as cursor:
            cursor.execute(cursor, sql)
            self.conn.commit()
            try:
                sqlResult = cursor.fetchone()
                # info[0] = keys() = names of column 
                fields = [info[0] for info in cursor.description]
                for sqlLine in sqlResult:
                    entry = dict(zip(fields, sql_result))
                    for key in entry:
                        if entry[key] == 'None' or entry[key] is None:
                            entry[key] = ''
                    ret.append(entry)
            except:
                pass
                ret = None
        
        return ret

    def read_records(self, table, where=None, limit=0, offset=0, orderby=None, columns=None):
        '''
        NOT SAVE, might have SQL INJECTION risk
        read whole table
        '''
        ret = []
        
        whereStr = ' WHERE %s' % where if where else ''
        limitStr = ' LIMIT %d' % limit if limit else ''
        offsetStr = ' OFFSET %d' % offset if offset else ''
        orderStr = ' ORDER BY %s %s' % orderby if orderby else ''
        
        if not columns:
            columns = "*"
        sql = "SELECT %s FROM %s%s%s%s%s" % (columns,
                                             table,
                                             whereStr,
                                             orderStr,
                                             limitStr,
                                             offsetStr)
        
        cursor = self.conn.cursor()
        
        cursor = self.exec_sql(cursor, sql)
        self.conn.commit()
        try:
            sqlResult = cursor.fetchall()
            # info[0] = keys() = names of column 
            fields = [info[0] for info in cursor.description]
            for sqlLine in sqlResult:
                entry = dict(zip(fields, sqlLine))
                for key in entry:
                    if entry[key] == 'None' or entry[key] is None:
                        entry[key] = ''
                ret.append(entry)
        except:
            pass
            ret = None
        
        return ret
     
    #def write_row(self):
    
    #def insert_row(self):
 
    
    def exec_sql(self, cursor, sql):
        sql = sql.replace("%", "%%")
        cursor = self.run_sql(cursor, sql)
        return cursor
    
    def run_sql(self, cursor, sql):
        retryTimes = 3
        while retryTimes > 0:
            retryTimes = retryTimes - 1
            try:
                cursor.execute(sql)
                break
            except:
                self.conn.close()
                self.conn = sqlite3.connect(self.dbpath)
                cursor = self.conn.cursor()
                
        return cursor
        
if __name__ == "__main__":
    testdb = BaseSdb()
    test_table_name = 'cc'
    print 'check table ' + test_table_name + ' exist:' + str(testdb.check_table_exist('cc'))
    
    table_template = {'this_is_num': 'NUM', 'this_is_str': 'TEXT'}
    testdb.create_table(test_table_name, table_template)
    print 'check table cc exist:' + str(testdb.check_table_exist(test_table_name))
    
    print 'read table cc:'
    print testdb.read_records(test_table_name)
