from sqlalchemy import create_engine, event
import pymysql
from .logger import get_module_logger

logger = get_module_logger(__name__)


def compose_sqlalchemy_engine_url(dbhost, dbuser, dbpassword, dbname=None, port=None, drv='mysql'):
    """
    function to establish engine_url for sqlachemy
    """
    if drv == 'mysql':
        engine_url = 'mysql+pymysql://{dbuser}:{dbpassword}@{dbhost}'.format(dbuser=dbuser,dbpassword=dbpassword,dbhost=dbhost)
        engine_url += ':{}'.format(port) if port is not None else ''
        engine_url += '/{}'.format(dbname) if dbname is not None else ''
        return engine_url


class DatabasePoolConnection:
    """
    database connneciton pool manager
    """

    def __init__(self, max_overflow=5, pool_size=1, **kwargs):

        """
        initialize the connection pool/sqlachemy engine based
        """
        if kwargs is not None:
            sqlachemy_engine_url = compose_sqlalchemy_engine_url(**kwargs)
        else:
            raise AttributeError('must key in arguments for DB connection (e.g.dbuser, dbpassword, dbhost, port, dbname')
        self.__connection_pool = create_engine(sqlachemy_engine_url, max_overflow=max_overflow, pool_size=pool_size)
        logger.debug("Initialize DB connection: {}".format(sqlachemy_engine_url))

    def get_engine(self):
        return self.__connection_pool

    def get_conn(self):
        return self.__connection_pool.connect()

    def return_conn(self, connection):
        connection.close()

    def close_all_conn(self):
        self.__connection_pool.dispose()
        logger.debug("Close DB connection")

    def get_stat(self):
        print(self.__connection_pool.pool.status())

    def customize_receive_before_cursor_execute(self):
        """
        this is to use execute many to speed up pandas.to_sql
        :return:
        """
        @event.listens_for(self.__connection_pool, 'before_cursor_execute')
        def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
            if executemany:
                cursor.fast_executemany = True
        return receive_before_cursor_execute


class DatabasePoolOpContextManager:
    """
    Context manger used of database operations starting from getting connection from connection pool;
    Example:
        with DatabaseOpContextManger(DatabasePoolConnection_instance) as conn:
            .....
    """
    def __init__(self, DatabasePoolConnection_instance):
        self.conn_pool = DatabasePoolConnection_instance
        self.conn = None

    def __enter__(self):
        self.conn = self.conn_pool.get_conn()
        return self.conn

    def __exit__(self, *exc):
        self.conn_pool.return_conn(self.conn)


class DatabaseOpContextManager:
    """
    Context manger used of database operations from connection directly;
    Example:
        with DatabaseOpContextManger(conn) as conn:
            .....
    """
    def __init__(self,conn):
        self.conn = conn

    def __enter__(self):
        return self.conn

    def __exit__(self, *exc):
        self.conn.close()


def other_database_op(sql_query, DatabasePoolConnection_instance, check_have_data=False, return_cursor=False, *multiparams):
    """
    function wrapper for other database operation through connection pool
    """
    with DatabasePoolOpContextManager(DatabasePoolConnection_instance) as connection:
        result = connection.execute(sql_query, *multiparams)
        if check_have_data:
            data = result.fetchone()
            if data is None:
                return False
            else:
                return True
        elif return_cursor:
            return result


def check_if_table_exists(table_schema, table_name, DatabasePoolConnection_instance):
    check_sql = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA ='{}' and TABLE_NAME='{}';".format(table_schema, table_name)
    count = other_database_op(check_sql, DatabasePoolConnection_instance, return_cursor=True).fetchone()[0]
    return count > 0


def check_if_column_exists(table_schema, table_name, column_name, DatabasePoolConnection_instance):
    check_sql = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA ='{}' and TABLE_NAME='{}' and COLUMN_NAME='{}';".format(table_schema, table_name, column_name)
    count = other_database_op(check_sql, DatabasePoolConnection_instance, return_cursor=True).fetchone()[0]
    return count > 0
