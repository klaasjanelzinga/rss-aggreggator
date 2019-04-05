import logging
import os
import re

import requests


class FetcherUtil:

    @staticmethod
    def fetch(url: str) -> str:
        if 'GAE_ENV' in os.environ:
            logging.info(f'Fetching from url {url}')
            result = requests.get(url)
            if result.status_code > 299:
                raise Exception(f'unable to fetch data from {url} - {result.status_code}')
            return result.content
        else:
            logging.warning(f'Retrieving stubbed data locally for {url}')
            if re.match('.*spotgroningen.*', url):
                with open('test/samples/spot/Programma - Spot Groningen.html') as f:
                    return ''.join(f.readlines())
            raise Exception(f'No support for stubbed url {url}')
