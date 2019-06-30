import logging
import re

import requests

from app.core.app_config import AppConfig
from app.core.data_fixer import fix


# pylint: disable=too-many-return-statements
# pylint: disable=too-many-branches
def fetch(url: str) -> str:
    if AppConfig.is_running_in_gae():
        result = requests.get(url)
        if result.status_code > 299:
            raise Exception(f'unable to fetch data from {url} - {result.status_code}')
        return str(result.content)
    logging.getLogger(__name__).warning('Retrieving stubbed data locally for %s', url)
    if re.match('.*spotgroningen.*', url):
        with open('tests/samples/spot/Programma - Spot Groningen.html') as sample_file:
            return ''.join([fix(line) for line in sample_file.readlines()])
    elif re.match('.*vera-groningen.*page=1.*', url):
        with open('tests/samples/vera-groningen/raw-fetch-0.html') as sample_file:
            return ''.join([fix(line) for line in sample_file.readlines()])
    elif re.match('.*vera-groningen.*page=2.*', url):
        with open('tests/samples/vera-groningen/raw-fetch-1.html') as sample_file:
            return ''.join([fix(line) for line in sample_file.readlines()])
    elif re.match('.*simplon.nl.*', url):
        with open('tests/samples/simplon-groningen/Simplon.html') as sample_file:
            return ''.join([fix(line) for line in sample_file.readlines()])
    elif re.match('.*komoost.nl.*', url):
        with open('tests/samples/oost-groningen/komoost.html') as sample_file:
            return ''.join([fix(line) for line in sample_file.readlines()])
    elif re.match('.*tivolivredenburg.nl.*page=1.*', url):
        with open('tests/samples/tivoli-utrecht/ajax-1.js') as sample_file:
            return ''.join([fix(line) for line in sample_file.readlines()])
    elif re.match('.*tivolivredenburg.nl.*page=2.*', url):
        with open('tests/samples/tivoli-utrecht/ajax-2.js') as sample_file:
            return ''.join([fix(line) for line in sample_file.readlines()])
    elif re.match('.*paradiso.nl.*page=1.*', url):
        with open('tests/samples/paradiso-amsterdam/ajax-1.js') as sample_file:
            return ''.join([fix(line) for line in sample_file.readlines()])
    elif re.match('.*paradiso.nl.*page=2.*', url):
        with open('tests/samples/paradiso-amsterdam/ajax-2.js') as sample_file:
            return ''.join([fix(line) for line in sample_file.readlines()])
    elif re.match('https://www.melkweg.nl/large-json', url):
        with open('tests/samples/melkweg-amsterdam/-1.json') as sample_file:
            return ''.join([fix(line) for line in sample_file.readlines()])
    elif re.match('https://www.melkweg.nl/.*', url):
        with open('tests/samples/melkweg-amsterdam/small-sample.json') as sample_file:
            return ''.join([fix(line) for line in sample_file.readlines()])
    raise Exception(f'No support for stubbed url {url}')
