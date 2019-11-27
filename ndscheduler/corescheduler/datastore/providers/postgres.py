"""Represents Postgres datastore."""

from ndscheduler.corescheduler.datastore import base


class DatastorePostgres(base.DatastoreBase):

    def get_db_url(self):
        """Returns the db url to establish a Postgres connection, where db_config is passed in
        on initialization as:
        {
            'user': 'my_user',
            'password': 'my_password',
            'hostname': 'db.hostname.com',
            'port': 8888,
            'database': 'my_db',
            'sslmode': 'disable'
        }
        :return: string db url
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
