import sys
import os

############################## for how to import func in this dir ################################

# first add path of this dir to python search path, so func/script in this dir could be improted for use
# this only need to be done once for a master script (e.g. driver script)

pyUtils_dirpath = os.path.dirname(os.path.realpath(__file__).split('/'))
# append pyUtils_dirpath to search path
sys.path.append(pyUtils_dirpath)


############################## example use of funcs in logger ####################################
from pyUtils.logger import get_module_logger

# this will set up the logger for this file
logger = get_module_logger(__name__)

# to log information, in script call
logger.info('this will add logger info to file')

# example output
# MacBook-Pro:rep-location jiajingxu$ python anchor_accuracy_report_driver.py
# 2018-07-25 13:32:11,711 module_1 INFO     finish calculating percentage of sugs taken and in predict circle
# 2018-07-25 13:32:11,712 module_1 INFO     finish adding columns for facilicty records for later use
# 2018-07-25 13:32:13,506 module_2 INFO     write results to DB


############################## example use of funcs in database_utils ####################################
from pyUtils.database_utils import DatabasePoolConnection, DatabasePoolOpContextManager, DatabaseOpContextManager, other_database_op

# initialize DB connection pool instance
dbuser = 'root'
dbpassword = ''
dbhost = 'localhost'
port = 3306
dbname = 'test_schema'
db_conn_pool = DatabasePoolConnection(max_overflow=5, pool_size=1, dbuser=dbuser,dbpassword=dbpassword, dbhost=dbhost, port=port, dbname=dbname)

# use with pandas
import pandas as pd
data = pd.read_sql(SQL_QUERY, con=db_conn_pool.get_engine())
data_df.to_sql(tablename,con=db_conn_pool.get_engine(),index=False, if_exists='append')

# use with other DB query
other_database_op(sql_query, db_conn_pool)

# directly use pool connection to do some sql operations
with DatabasePoolOpContextManager(db_conn_pool) as conn:
	# your sql operations here

# directly use connection checkout from the DB pool
conn_checkout = db_conn_pool.get_conn()
with DatabaseOpContextManager(conn_checkout) as conn:
	# your sql operations here

# close connection pool at the end of execution
db_conn_pool.close_all_conn()
