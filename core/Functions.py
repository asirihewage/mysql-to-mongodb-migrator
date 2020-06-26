from Config import Conf
from DBHelper import DBHelper, DatabaseObj
from Logger import Logger

'''
@author Asiri Hewage
date : 31 May 2020
Class : Functions
Objective : All functions related with Migrator
'''


class Functions:

    def __init__(self):
        self.logging = Logger()
        self.Config = Conf()
        self.db_helper = DBHelper()
        self.mysql_con = self.db_helper.connect_mysql(host=self.Config.get_configs('MYSQL', 'mysql_host'),
                                                      user=self.Config.get_configs('MYSQL', 'mysql_username'),
                                                      password=self.Config.get_configs('MYSQL', 'mysql_password'),
                                                      db=self.Config.get_configs('MYSQL', 'mysql_database'))
        self.mongo_con = self.db_helper.connect_mongodb(host=self.Config.get_configs('MONGODB', 'mongodb_host'),
                                                        port=int(self.Config.get_configs('MONGODB', 'mongodb_port')))

    # Run MYSQL query on database - no return
    def run_mysql(self, query):
        try:
            with self.mysql_con.cursor() as cursor:
                result = cursor.execute(query)
                if result is not None:
                    self.logging.debug('MYSQL  transaction success.' + str(result))
                    return result
                else:
                    self.logging.debug('MYSQL transaction error.')
                    return None
        except Exception as e:
            self.logging.error('Exception while running MYSQL query : ' + str(e))
            return None

    # Run MYSQL query on database - with returns
    def return_mysql(self, query):
        try:
            with self.mysql_con.cursor() as cursor:
                result = cursor.execute(query)
                data = cursor.fetchall()
                if data is not None:
                    self.logging.debug('MYSQL  transaction success.' + str(result))
                    return data
                else:
                    self.logging.debug('MYSQL transaction error.')
                    return None
        except Exception as e:
            self.logging.error('Exception while running MYSQL query : ' + str(e))
            return None

    # commit transaction
    def commit(self):
        if self.mysql_con:
            self.mysql_con.commit()
            # self.logging.info('Transaction committed')
        else:
            self.logging.debug('Transaction not committed. DB connection not found.')

    # close DB connection
    def close(self, con):
        if con:
            con.close()
            self.logging.info('DB Connection Closed')
        else:
            self.logging.info('DB Connection already Closed')

    # insert data into mongodb database
    def insert_mongodb(self, json_doc, collection):
        try:
            if self.mongo_con is None:
                db_conn = self.db_helper.connect_mongodb()
                mongodb_database = db_conn[self.Config.get_configs('mongoDB_CREDENTIALS', 'mongodb_database')]
            else:
                mongodb_database = self.mongo_con[self.Config.get_configs('mongoDB_CREDENTIALS', 'mongodb_database')]

            collection_vm_data = mongodb_database[collection]
            file_data = json_doc
            collection_vm_data.insert_many(file_data)
            return True

        except Exception as mongoException:
            self.logging.error('Exception while inserting mongodb record  : ' + str(mongoException))
            print mongoException
            return False

        finally:
            self.close_mongodb_connection()

    # Close mongodb database connection
    def close_mongodb_connection(self):
        if self.mongo_con is not None:
            self.logging.debug('Mongodb connection closed.')
            self.mongo_con.close()

    # get mysql table headers
    def get_mysql_table_headers(self):
        cursor = self.mysql_con.cursor()
        cursor.execute("select column_name from information_schema.columns where table_name = 'user' ")
        records = cursor.fetchall()
        print ("Displaying column name from table ")
        for column in records:
            print (column)

    def custom_rules(self, resobj):
        # resobj.mysql_id = resobj.userid
        return resobj

    def migrate(self, MYSQL_SETTINGS, MONGODB_SETTINGS):
        print 'MySQL to MongoDB Migration Started.'
        counter = 0
        finished = True

        while True:
            r = None
            try:
                r = MYSQL_SETTINGS.read()
                if not r:
                    print "Read failed %s counter=%s" % (r, counter)
                    break
            except StopIteration:
                break
            except Exception, e:
                print str(e)
                finished = False
                break

            try:
                ok = MONGODB_SETTINGS.write(self.custom_rules(r))
                if not ok:
                    print "Write failed result=%s!" % r
                    finished = False
                    break
            except Exception, e:
                print str(e)
                finished = False
                break

            counter += 1

        print "%d data have been Finished. finished=%s" % (counter, finished)
        return finished

    def bulk_migrate(self):
        try:
            connection = self.mysql_con
            cursor = connection.cursor()
            cursor.execute("USE {0}".format(self.Config.get_configs('MYSQL', 'mysql_database')))
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print "Found " + str(len(tables)) + " Tables in the database " + str(self.Config.get_configs('MYSQL', 'mysql_database'))
            for table in tables:
                print 'MySQL to MongoDB Migration Started for ' + str(table['Tables_in_shot'])

                cursor.execute("SHOW COLUMNS FROM "+str(table['Tables_in_shot'])+";")

                columns_arr = []

                for col in cursor.fetchall():
                    columns_arr.append(col['Field'])

                print columns_arr
                DB_SRC = {'name': 'mysql',
                          'table': str(table['Tables_in_shot']),  # table name
                          'column': columns_arr}

                DB_DST = {'name': 'mongo',
                          'table': str(table['Tables_in_shot']),
                          'column': columns_arr}

                DB_SRC = DatabaseObj(DB_SRC)
                DB_DST = DatabaseObj(DB_DST)

                counter = 0
                finished = True
                while True:
                    r = None
                    try:
                        r = DB_SRC.read()
                        if not r:
                            print "Read failed %s counter=%s" % (r, counter)
                            break
                    except StopIteration:
                        break
                    except Exception, e:
                        print str(e)
                        finished = False
                        break

                    try:
                        ok = DB_DST.write(self.custom_rules(r))
                        if not ok:
                            print "Write failed result=%s!" % r
                            finished = False
                            break
                    except Exception, e:
                        print str(e)
                        finished = False
                        break

                    counter += 1

                print "%d data have been Finished. finished=%s" % (counter, finished)
                return finished
        except Exception as er:
            print er
            self.logging.error(str(er))
