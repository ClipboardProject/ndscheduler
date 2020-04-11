"""A job to send a HTTP (GET or DELETE) periodically."""

import logging
import requests

from ndscheduler.corescheduler import job

logger = logging.getLogger(__name__)


class CurlJob(job.JobBase):
    TIMEOUT = 30

    @classmethod
    def meta_info(cls):
        return {
            'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
            'notes': 'This sends a HTTP request to a particular URL',
            'arguments': [
                # url
                {'type': 'string', 'description': 'What URL you want to make a GET call?'},
                # Request Type
                {'type': 'string', 'description': 'What request type do you want? '
                                                  '(currently supported: GET/POST/DELETE)'},
                {'type': 'string', 'description': 'Username'},
                {'type': 'string', 'description': 'Password'},
                {'type': 'string', 'description': 'Login endpoint'}

            ],
            'example_arguments': ('["http://localhost:8888/api/v1/jobs", "GET"]'
                                  '["http://localhost:8888/api/v1/jobs/ba12e", "DELETE"]')
        }

    def run(self, url, request_type, username, password, login_endpoint, data={}):
        print('Calling %s on url: %s' % (request_type, url))

        session = requests.Session()
        authorization = None
        if username != None and password != None:
            token = session.post(login_endpoint, json={'email': username, 'password': password}).content.decode()
            authorization = f'Bearer {token}'
        if request_type == 'POST':
            result = session.request(request_type, url,
                                     timeout=self.TIMEOUT,
                                     headers={'Content-Type': 'application/json', 'Authorization': authorization},
                                     json=data)
            return result.text
        else:
            result = session.request(request_type, url, timeout=self.TIMEOUT, headers={'Authorization': authorization})
            return result.text


if __name__ == "__main__":
    job = CurlJob.create_test_instance()
    job.run('http://localhost:8888/api/v1/jobs', 'GET', {})
