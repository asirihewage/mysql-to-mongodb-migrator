MySQL to MongoDB Migrator v0.1.0
-
This python 2.7 script will be useful to migrate MySQL Database into MongoDB.
 
## Setup
Do the necessary changes in config/config.ini with your database credentials
Make sure the user is having read/write access into the databases 
```bash
[MONGODB]
mongodb_host=
mongodb_port=
mongodb_database=
mongodb_username=
mongodb_password=

[MYSQL]
mysql_host=
mysql_port=
mysql_database=
mysql_username=
mysql_password=
```

If you are using bulk migration, make sure to comment out/remove single migration function.
```python
    # import functions
    functions = Functions()

    # migrate a single table
    # functions.migrate(MYSQL_SETTINGS, MONGODB_SETTINGS)

    # migrate all tables in mysql db in bulk
    functions.bulk_migrate()
``` 
 
If you are not using Bulk Migration function, please change the following setting with your table details.
```bash
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
```

To add custom rules, you can change the following function in Functions.py
```python
    def custom_rules(self, resobj):
        resobj.mysql_id = "PTOps_" + resobj.userid
        resobj.number = int(resobj.userid)
        return resobj
```
### Install Requirements
```bash
pip install -r requirments.txt
```
### Execute
```bash
python Main.py
```

### Medium Article
https://medium.com/@asiriofficial/sample-project-mysql-to-mongodb-migration-e7b10b2e9d6b?sk=77366640e4c4aaa749c61da3b75f6503

Contact me for more details.