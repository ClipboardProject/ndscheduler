"""Represents Postgres datastore."""

from ndscheduler.corescheduler.datastore import base


class DatastorePostgres(base.DatastoreBase):

    def get_db_url(self):
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

        user = self.db_config['user']
        password = self.db_config['password']
        hostname = self.db_config['hostname']
        port = self.db_config['port']
        database = self.db_config['database']
        sslmode = self.db_config['sslmode']

        if hostname.startswith('/'):
            # socket
            return f'postgresql://{user}:{password}@/{database}?host={hostname}'
        else:
            return f'postgresql://{user}:{password}@{hostname}:{port}/{database}?sslmode={sslmode}'
