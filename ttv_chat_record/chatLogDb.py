#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from baseSdb import BaseSdb 
    
class ChatLogDb(BaseSdb):
    '''
    Generally 5 column:
    
    Index
    Time(time.time() in python)
    Username
    Message
    RawSocketData
    
    each Table corresponding to each channel
    
    '''

    def __init__(self, dbpath=None):
        super(ChatLogDb, self).__init__(dbpath)
        # use orderedDict since the sequence is important with insert by list
        self.tableFormat = OrderedDict([
            ('ID', 'INTEGER PRIMARY KEY'),
            ('TIME', 'REAL'),
            ('USERNAME', 'TEXT'),
            ('MESSAGE', 'TEXT'),
            ('RAWDATA', 'TEXT')
        ])
        
    def create_chat_table(self, tableName):
        if self.check_table_exist(tableName):
            raise 'Table already exist'
        self.create_table(tableName, self.tableFormat)
      
    # def general
        
if __name__ == "__main__":
    testdb = ChatLogDb()
    test_table_name = 'cc'
    print 'check table ' + test_table_name + ' exist:' + str(testdb.check_table_exist('cc'))
    
    testdb.create_chat_table(test_table_name)
        
    print 'check table cc exist:' + str(testdb.check_table_exist(test_table_name))
    
    print 'read table cc:'
    print testdb.read_records(test_table_name)
    
    testdb.insert_record_list(test_table_name, [None, 34234.23, 'kappa', 'ok', 'kappa: ok'])
    testdb.insert_record_list(test_table_name, [None, 3234.23, 'kappa', 'odk', 'kappa: ok'])
    testdb.insert_record_list(test_table_name, [None, 34.23, 'kappa', 'okd', 'kappa: ok'])
    
    from pprint import pprint
    pprint(testdb.read_records(test_table_name))