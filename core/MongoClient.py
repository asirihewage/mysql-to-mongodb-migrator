import pymongo
from Config import Conf

'''
@author Asiri Hewage
date : 31 May 2020
Class : DBHelper
Objective : Manage Database connections
'''

class MongoClient(object):
    def __init__(self, param):
        self.Config = Conf()
        db = self.Config.get_configs('MONGODB', 'mongodb_database')
        table = param['table']
        self._column = param['column']
        self._cli = pymongo.MongoClient(host=self.Config.get_configs('MONGODB', 'mongodb_host'),
                                        port=int(self.Config.get_configs('MONGODB', 'mongodb_port')))
        self._db = self._cli[db]
        self._table = self._db[table]

    def write(self, resobj):
        r = {}
        for k in self._column:
            r[k] = getattr(resobj, k, None)
        try:
            self._table.insert(r)
        except:
            import traceback
            traceback.print_exc()
            return False

        return True

    def read(self):
        yield
