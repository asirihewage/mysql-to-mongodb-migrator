from core.DBHelper import DatabaseObj
from core.Functions import Functions

'''
@author Asiri Hewage
date : 31 May 2020
Class : Main
Objective : Implementation of business logic
'''

MYSQL_SETTINGS = {'name': 'mysql',
                  'table': 'user',
                  'column': ['userid',
                             'username',
                             'firstname',
                             'lastname',
                             'teamid']}

MONGODB_SETTINGS = {'name': 'mongo',
                    'table': 'user',
                    'column': ['userid',
                               'username',
                               'firstname',
                               'lastname',
                               'teamid']}

MYSQL_SETTINGS = DatabaseObj(MYSQL_SETTINGS)
MONGODB_SETTINGS = DatabaseObj(MONGODB_SETTINGS)


def run():
    # import functions
    functions = Functions()

    # migrate a single table
    functions.migrate(MYSQL_SETTINGS, MONGODB_SETTINGS)

    # migrate all tables in mysql db in bulk
    # functions.bulk_migrate()


if __name__ == "__main__":
    run()
