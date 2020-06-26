import pymysql as _mysql
from Config import Conf

'''
@author Asiri Hewage
date : 31 May 2020
Class : DBHelper
Objective : Manage Database connections
'''

class MysqlClient(object):
    def __init__(self, param):
        self.Config = Conf()
        db = self.Config.get_configs('MONGODB', 'mongodb_database')
        table = param['table']
        self._column = param['column']
        self._db = _mysql.connect(host=self.Config.get_configs('MYSQL', 'mysql_host'),
                                  user=self.Config.get_configs('MYSQL', 'mysql_username'),
                                  password=self.Config.get_configs('MYSQL', 'mysql_password'),
                                  db=self.Config.get_configs('MYSQL', 'mysql_database'))
        self._table = '%s.%s' % (db, table)

        if isinstance(self._column, list) and len(self._column):
            column_str = map(lambda x: "`%s`" % x, self._column)
            self._column_str = ' ,'.join(column_str)

    def tuple2dict(self, sql_data):
        r = {}
        for i, col in enumerate(self._column):
            r[col] = sql_data[i]

        return r

    def read(self):
        c = self._db.cursor()
        sql = "select %s from %s ;" % (self._column_str, self._table)
        print '[MySQL]<in>: ', sql
        c.execute(sql)
        r = c.fetchone()
        while r:
            yield self.tuple2dict(r)
            r = c.fetchone()

    def write(self):
        pass
