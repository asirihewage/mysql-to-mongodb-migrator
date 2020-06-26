import pymysql
from Logger import Logger
from pymongo import MongoClient
from MySQLClient import MysqlClient
from MongoClient import MongoClient

'''
@author Asiri Hewage
date : 31 May 2020
Class : DBHelper
Objective : Manage Database connections
'''

DB_MAP = {'mysql': MysqlClient,
          'mongo': MongoClient}


class ResultObj(object):
    def __init__(self, vattr):
        self.raw_attr = vattr
        self._attrs = {}
        for k,v in vattr.iteritems():
            self._attrs[k] = v

    def __getattr__(self, k):
        if k not in self._attrs:
            return None
        else:
            return self._attrs[k]


class DatabaseObj(object):
    def __init__(self, param):
        self._client = DB_MAP[param['name']](param)
        self._reader = self._client.read()

    def read(self):
        return ResultObj(self._reader.next())

    def write(self, resobj):
        return self._client.write(resobj)


class DBHelper:

    def __init__(self):
        self.logging = Logger()
        self.vm_obj_list = []

    # connect mysql
    def connect_mysql(self, host, user, password, db):
        # mysql connection
        try:

            con = pymysql.connect(host=host,
                                  user=user,
                                  password=password,
                                  db=db,
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)

            if con:
                print 'MySQL Database connected'
            else:
                print 'MySQL Database connection None'
            return con
        except Exception as e:
            self.logging.error('Exception while connecting mysql : ' + str(e))
            print e
            return None

    # initialize new mongodb connection
    def connect_mongodb(self, host, port):
        try:
            mongodb_con = MongoClient(host, port)
            if mongodb_con:
                print 'MongoDB connected'
            else:
                print 'MongoDB connection None'
            return mongodb_con

        except Exception as e2:
            self.logging.error('Exception while connecting mongoDB : ' + str(e2))
            print e2
            return None

# json_sa = [{
#     "AUD": 1.5978,
#     "BGN": 1.9558,
#     "BRL": 4.0726,
#     "CAD": 1.5868
#  }]
# DBManager = DBManager()
# print DBManager.insert_mongodb(json_sa, 'vm_data')
# DBManager.close_mongodb_connection()
