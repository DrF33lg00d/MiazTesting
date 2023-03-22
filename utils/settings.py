import logging
import os

from peewee import SqliteDatabase


FORMAT = '%(asctime)s\t%(levelname)s\t%(message)s'
logging.basicConfig(format=FORMAT, filename='log.log')
logger = logging.getLogger()
logger.setLevel('INFO')

db_settings = {
    'name': 'result.db'
}
db = SqliteDatabase(os.path.join(os.getcwd(), db_settings['name']))

URL = 'https://sobaka[.]babaka[.]xyz'
POSCAT_ID = 100
POSITION_FORMAT: str = '{posid}-{catid} | {pos} | {cat}'

try:
    from utils.local_settings import *
    logger.info('Local settings imported')
except ImportError:
    logger.warning('Local settings did not import')
