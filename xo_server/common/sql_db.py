#!/usr/bin/python
# coding: utf-8

import logging

import MySQLdb.cursors
from twisted.enterprise import adbapi
from twisted.internet import defer

class ConnectionPool (object):
    """
    Wrapper for twisted.enterprise.adbapi.ConnectionPool 
    with SQL query logging and supporting for returning new 
    inserted IDs.
    """
    def __init__ (self, host, port, db, user, password, cp_min=3, cp_max=50):
        self.db_host = host
        self.db_port = port
        self.db_name = db
        self.db_user = user
        self.db_passwd = password
        self.cp_min = cp_min
        self.cp_max = cp_max
        self._connect()        
    
    def _connect(self):
        self.dbpool = adbapi.ConnectionPool("MySQLdb", cursorclass=MySQLdb.cursors.DictCursor,
                                            host=self.db_host, port=self.db_port,
                                            db=self.db_name, user=self.db_user, 
                                            passwd=self.db_passwd, use_unicode=True,
                                            charset='utf8', cp_min=self.cp_min, 
                                            cp_max=self.cp_max) 
            
    
    @defer.inlineCallbacks
    def runQuery (self, strSQL, *args, **kw):
        """ runQuery wrapper """        
        logging.debug(" *> sql: %s, args are `%s`" % (strSQL, str(args)))
        res = yield self.dbpool.runQuery(strSQL, *args, **kw)
            
        defer.returnValue(res)

    @defer.inlineCallbacks
    def runOperation (self, strSQL, *args, **kw):
        """ runOperation wrapper """        
        logging.debug(" *> sql: %s, args are `%s`" % (strSQL, str(args)))
        res = yield self.dbpool.runOperation(strSQL, *args, **kw)
        defer.returnValue(res)

    @defer.inlineCallbacks
    def runInteraction (self, strSQL, *args, **kw):
        """ runInteraction wrapper and new inserted ID retrieving """ 
        logging.debug(" *> sql: %s, args are `%s`" % (strSQL, str(args)))
        ret_id = yield self.dbpool.runInteraction(self._returnID, strSQL, *args, **kw)
        defer.returnValue(ret_id)
    

    def _returnID (self, cursor, strSQL, *args, **kw):
        """new inserted ID retrieving"""
        cursor.execute(strSQL, *args, **kw)
        new_row_id = int(cursor.lastrowid)
        return new_row_id
        
