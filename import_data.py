import re

import optparse
import requests
from requests.utils import unquote
import time
from app import db, Repository, app

GITHUB_API_ENDPOINT = 'https://api.github.com/search/repositories'
DEFAULT_LANG = 'Python'
DEFAULT_KEYWORD = 'rest'
DEFAULT_IMPORT_FIELDS = 'full_name,html_url,description,stargazers_count,language'

# Configure the option parser
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-l', '--lang', dest='lang', default=DEFAULT_LANG,
                  help='Searches repositories based on the language they\'re written in.')
parser.add_option('-k', '--keyword', dest='keyword', default=DEFAULT_KEYWORD,
                  help='Search for repositories with the given word in the name, the description, or the README.')
parser.add_option('', '--import_fields', dest='import_fields', default=DEFAULT_IMPORT_FIELDS,
                  help='Comma-separated field names, which should be imported from GitHub API.')
(options, args) = parser.parse_args()


def import_data(keyword, lang, fields):
    """Import GitHub repositories, based on given criteria, into the database"""
    params = (('language', lang),)
    headers = {'Accept': 'application/vnd.github.mercy-preview+json'}
    link = GITHUB_API_ENDPOINT + '?q=' + build_query(keyword, *params)

    while link:
        app.logger.debug('Requesting link %s', link)

        response = requests.get(link, headers=headers)

        sleep_if_needed(response.headers)

        fill_db(response.json().get('items', []), fields)

        link = get_next_link(response.headers.get('Link'))


def build_query(*args):
    """Helper function to build 'q' parameter, in format, suitable for GitHub"""
    def stringify(x):
        if isinstance(x, str):
            return x

        return ':'.join(str(el) for el in x)

    return '+'.join(list(map(stringify, args)))


def sleep_if_needed(headers):
    """Decide if rate limit exceeded and sleep if needed"""
    ratelimit_remaining = headers.get('X-RateLimit-Remaining', 0)

    if int(ratelimit_remaining) == 0:
        # Sleep until the time at which the current rate limit window resets
        ratelimit_reset = headers['X-RateLimit-Reset']
        to_sleep = int(ratelimit_reset) - int(time.time())
        app.logger.debug('Rate limit exceeded, will sleep for %i seconds',
                         to_sleep)
        time.sleep(to_sleep)


def fill_db(items, fields):
    """Fill Repository table based on given input"""
    for item in items:
        repo = Repository()
        for field_name in fields:
            setattr(repo, field_name, item[field_name])
        db.session.add(repo)
        db.session.commit()


def get_next_link(header):
    """Parse Link header values instead of constructing your own URLs"""
    # Very basic regex for url
    url_pattern = re.compile(r'<([a-zA-Z0-9_:/.?=+&%]+)>')
    rel_pattern = re.compile(r'rel="([a-z]+)"')

    if header is not None:
        for item in header.split(', '):
            url, rel = item.split('; ')
            m = re.match(rel_pattern, rel)
            if m:
                if 'next' == m.group(1):
                    match = re.match(url_pattern, url)
                    if match:
                        return unquote(match.group(1))

    return None

if __name__ == '__main__':
    try:
        keyword = options.keyword
        lang = options.lang
        fields = options.import_fields.split(',')

        import_data(keyword, lang, fields)
    except Exception as e:
        app.logger.debug(e)
