from .logger import get_module_logger
from .database_config import DatabaseConfig
from .database_utils import DatabasePoolConnection

logger = get_module_logger(__name__)


def connect_to_db_all(max_overflow=5, pool_size=1):
    """
    get pool conneciton to database that could access all dbs (e.g. pfizerusdev, pfizerusdev_learning, etc)
    :param max_overflow:
    :param pool_size:
    :return:
    """
    dbconfig = DatabaseConfig.instance()
    pool_connection = DatabasePoolConnection(max_overflow=max_overflow, pool_size=pool_size, dbuser=dbconfig.dbuser,dbpassword=dbconfig.dbpassword, dbhost=dbconfig.dbhost, port=dbconfig.dbport)
    return pool_connection
