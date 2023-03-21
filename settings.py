import os

from peewee import SqliteDatabase

from contextlib import suppress

db_settings = {
    'name': 'result.db'
}

db = SqliteDatabase(os.path.join(os.getcwd(), db_settings['name']))

url = 'https://sobaka[.]babaka[.]xyz'
id = 100


with suppress(ImportError):
    from local_settings import *
