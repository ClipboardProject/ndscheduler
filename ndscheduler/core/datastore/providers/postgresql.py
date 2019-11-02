"""Represents PostgreSQL datastore."""

from ndscheduler import settings
from ndscheduler.core.datastore.providers import base


class DatastorePostgresql(base.DatastoreBase):

    @classmethod
    def get_db_url(cls):
        """
        DATABASE_CONFIG_DICT = {
            'user': 'myuser',
            'password': 'password',
            'hostname': 'mydb.domain.com',
            'port': 5432,
            'database': 'mydatabase',
            'sslmode': 'disable'
        }

        :return: database url
        :rtype: str
        """

        user = settings.DATABASE_CONFIG_DICT['user']
        password = settings.DATABASE_CONFIG_DICT['password']
        hostname = settings.DATABASE_CONFIG_DICT['hostname']
        port = settings.DATABASE_CONFIG_DICT['port']
        database = settings.DATABASE_CONFIG_DICT['database']
        sslmode = settings.DATABASE_CONFIG_DICT['sslmode']

        if hostname.startswith('/'):
            # socket
            return f'postgresql://{user}:{password}@/{database}?host={hostname}'
        else:
            return f'postgresql://{user}:{password}@{hostname}:{port}/{database}?sslmode={sslmode}'
