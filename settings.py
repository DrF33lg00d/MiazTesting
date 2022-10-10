from contextlib import suppress

db_settings = {
    'name': 'result.db'
}

url = 'https://sobaka[.]babaka[.]xyz'
id = 100

with suppress(ImportError):
    from local_settings import *
