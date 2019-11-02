"""A job to send a HTTP (GET or DELETE) periodically."""

import logging
import requests
from tenacity import retry, wait_exponential
from ndscheduler import job
from ndscheduler.pubsub import PubSub

logger = logging.getLogger(__name__)

# 30 minute timeout for jobs
TIMEOUT = 30


class ScrapyJob(job.JobBase):
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
                                                  '(currently supported: GET/DELETE)'},

            ],
            'example_arguments': ('["http://localhost:8888/api/v1/jobs", "GET"]'
                                  '["http://localhost:8888/api/v1/jobs/ba12e", "DELETE"]')
        }

    @retry(wait=wait_exponential(min=1, max=16))
    def schedule_spider(self, spider_name):
        job_results = requests.post('http://event_processor:6800/schedule.json',
                                    data={'project': 'In2ItChicago', 'spider': spider_name})
        job_results_json = job_results.json()
        if 'status' in job_results_json and job_results_json['status'] == 'error':
            raise Exception('Error while scheduling spider: ' + str(job_results_json))
        return job_results_json

    @retry(wait=wait_exponential(min=1, max=16))
    def get_results(self):
        results = requests.get('http://event_processor:6800/listjobs.json',
                               params={'project': 'In2ItChicago'})
        return results.json()

    def run(self, spider_name):
        create_job_json = self.schedule_spider(spider_name)

        jobid = create_job_json['jobid']

        def timeout_callback():
            jobs_json = self.get_results()
            possible_states = ['pending', 'running', 'finished']
            job_state = next((state for state in possible_states
                              for job in jobs_json[state] if job['id'] == jobid), 'not found')
            return {
                'errored': True,
                'response': f'Timed out waiting for response from scrapy for job {jobid}. '
                            f'Scrapyd job status = {job_state}'
            }

        if 'status' not in create_job_json or create_job_json['status'] != 'ok':
            raise Exception('scrapy job failed: ' + create_job_json)

        result = PubSub.subscribe(jobid, lambda result: result, timeout=TIMEOUT*60,
                                  timeout_func=timeout_callback)
        if result['errored']:
            raise Exception('Failure during scrapy processing: ' + str(result))
        return result


if __name__ == "__main__":
    job = ScrapyJob.create_test_instance()
    job.run('history')
