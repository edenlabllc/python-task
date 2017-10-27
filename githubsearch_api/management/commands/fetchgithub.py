import time
import datetime

import requests
import json

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from githubsearch_api.serializers import RepositorySerializer


# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1


class Command(BaseCommand):
    help = 'Imports the repos from GitHub Search API v3.'

    def add_arguments(self, parser):
        # Positional arguments
        #parser.add_argument('--last')

        parser.add_argument(
            '--last',
            action='store_true',
            dest='last',
            default=False,
            help='Fetch last GitHub repositories',
        )

        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Fetch all GitHub repositories',
        )

    def handle(self, *args, **options):
        if options['last']:
            self.fetch_last_github_repos()
        elif options['all']:
            self.fetch_last_github_repos()
        else:
            raise CommandError("Option `--last or --all` must be specified.")

    def fetch_github_repos(self, dt_start, dt_end, per_page=100, page=1, keyword='rest', lang='Python'):
        '''

        Fetch GitHub repositories for period
        '''

        payload = {
            'q': '{keyword} language:{lang} created:{dt_start}..{dt_end}'.format(keyword=keyword, lang=lang,
                                                                                 dt_start=dt_start, dt_end=dt_end),
            'per_page': per_page, 'page': page,
            'access_token': settings.GITHUB_OAUTH}
        headers = {'Accept': 'application/vnd.github.v3+json'}

        connect_timeout, read_timeout = 2.0, 30.0

        r = requests.get(settings.API_URL,
                         params=payload,
                         headers=headers,
                         timeout=(connect_timeout, read_timeout))
        if r.status_code == 200:
            #print (json.loads(r.text))
            return r
        else:
            print('sleep for 60 seconds')
            time.sleep(60)
            r = requests.get(settings.API_URL,
                             params=payload,
                             headers=headers,
                             timeout=(connect_timeout, read_timeout))
            return r

    def save_repos_to_db(self, item):
        '''
         Save data to database
        '''
        repos = {}
        repos['full_name'] = item['full_name']
        repos['html_url'] = item['html_url']
        repos['description'] = item['description']
        repos['stargazers_count'] = item['stargazers_count']
        repos['lang'] = item['language']

        serializer = RepositorySerializer(data=repos)
        if serializer.is_valid():
            serializer.save()
        else:
            print("Item has invalid fields: {}".format(repos))
            print("Errors: {}".format(serializer.errors))

    def fetch_all_github_repos(self):
        '''
        Fetch all GitHub repositories

        '''

        self.stdout.write('Start to fetch all GitHub repositories')
        dt_end = datetime.datetime.now()
        dt_start = datetime.datetime(2008, 2, 8, 0, 0, 0)  # Date of founded GitHub

        days = 50
        all_count = 0

        while dt_start >= datetime.datetime(2008, 2, 8, 0, 0, 0):
            delta = datetime.timedelta(days=days)
            dt_start = dt_end - delta
            dt_start_str = dt_start.strftime('%Y-%m-%dT%H:%M:%SZ')
            dt_end_str = dt_end.strftime('%Y-%m-%dT%H:%M:%SZ')

            response = self.fetch_github_repos(dt_start_str, dt_end_str)
            total_count = json.loads(response.text)['total_count']

            if total_count <= 100:
                repos_list = json.loads(response.text)['items']
                for item in response['items']:
                    self.save_repos_to_db(item)

                all_count += total_count
            else:
                left_count = total_count
                per_page = 100
                page = 1
                while left_count >= 0:
                    response = self.fetch_github_repos(dt_start_str, dt_end_str, per_page, page)
                    repos_list = json.loads(response.text)['items']
                    for item in repos_list:
                        self.save_repos_to_db(item)

                    page += 1
                    left_count -= 100
                    if left_count < 100:
                        per_page = left_count

            all_count += total_count
            per_day = (total_count / days)
            diff = 1000 - total_count
            diff_per_days = diff / per_day
            days = days + diff_per_days
            print('{}-{} - total_count={}, all_count={} save to datebase'.format(dt_start_str, dt_end_str, total_count,
                                                                                 all_count))
            dt_end = dt_start + datetime.timedelta(seconds=1)

        self.stdout.write('End to fetch GitHub repositories')

    def fetch_last_github_repos(self):
        '''
        Fetch repositories for last 50 days

        '''

        days = 50
        self.stdout.write('Start to fetch GitHub repositories per last {} days'.format(days))
        dt_end = datetime.datetime.now()
        delta = datetime.timedelta(days=days)
        dt_start = (dt_end - delta)
        dt_end = dt_end.strftime('%Y-%m-%dT%H:%M:%SZ')
        dt_start = dt_start.strftime('%Y-%m-%dT%H:%M:%SZ')

        response = self.fetch_github_repos(dt_start, dt_end, 1, 1)
        total_count = json.loads(response.text)['total_count']
        count_pages = (total_count // 100) + 2
        for i in range(1, count_pages):
            response = self.fetch_github_repos(dt_start, dt_end, 100, i)
            repos_list = json.loads(response.text)['items']
            for item in repos_list:
                self.save_repos_to_db(item)
        self.stdout.write('End to fetch GitHub repositories')