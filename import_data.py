import re

import requests
import time
from app import db, Repository, app

GITHUB_API_ENDPOINT = 'https://api.github.com/search/repositories'
DEFAULT_LANG = 'Python'
DEFAULT_KEYWORD = 'rest'
DEFAULT_IMPORT_FIELDS = ('full_name', 'html_url', 'description',
                         'stargazers_count', 'language')


def import_data(lang=DEFAULT_LANG, keyword=DEFAULT_KEYWORD):
    params = (('language', lang),)
    headers = {'Accept': 'application/vnd.github.mercy-preview+json'}
    link = GITHUB_API_ENDPOINT + '?q=' + build_query(keyword, *params)

    while link:
        app.logger.debug('Requesting link %s', link)

        response = requests.get(link, headers=headers)

        sleep_if_needed(response.headers)

        fill_db(response.json().get('items', []))

        link = get_next_link(response.headers.get('Link'))


def build_query(*args):
    def stringify(x):
        if isinstance(x, str):
            return x

        return ':'.join(str(el) for el in x)

    return '+'.join(list(map(stringify, args)))


def sleep_if_needed(headers):
    ratelimit_remaining = headers.get('X-RateLimit-Remaining', 0)

    if int(ratelimit_remaining) == 0:
        # Sleep until the time at which the current rate limit window resets
        ratelimit_reset = headers['X-RateLimit-Reset']
        to_sleep = int(ratelimit_reset) - int(time.time())
        app.logger.debug('Rate limit exceeded, will sleep for %i seconds',
                         to_sleep)
        time.sleep(to_sleep)


def fill_db(items):
    for item in items:
        repo = Repository()
        for field_name in DEFAULT_IMPORT_FIELDS:
            setattr(repo, field_name, item[field_name])
        db.session.add(repo)
        db.session.commit()


def get_next_link(s):
    # Very basic regex for url
    url_pattern = re.compile(r'<([a-zA-Z0-9_:/.?=+&%]+)>')
    rel_pattern = re.compile(r'rel="([a-z]+)"')

    if s is not None:
        for item in s.split(', '):
            url, rel = item.split('; ')
            m = re.match(rel_pattern, rel)
            if m:
                if 'next' == m.group(1):
                    match = re.match(url_pattern, url)
                    if match:
                        return match.group(1)

    return None

if __name__ == '__main__':
    try:
        import_data()
    except Exception as e:
        app.logger.debug(e)
