"""Settings to override default settings."""

import os
import logging

#
# Override settings
#
DEBUG = True

HTTP_PORT = 8888
HTTP_ADDRESS = '0.0.0.0'

#
# Set logging level
#
logging.getLogger().setLevel(logging.DEBUG)

JOB_CLASS_PACKAGES = ['simple_scheduler.jobs']

DATABASE_CLASS = 'ndscheduler.core.datastore.providers.postgresql.DatastorePostgresql'
DATABASE_CONFIG_DICT = {
    'user': 'postgres',
    'password': 'postgres',
    'hostname': os.getenv('HOSTNAME'),
    'port': 5432,
    'database': 'scheduler',
    'sslmode': 'disable'
}
