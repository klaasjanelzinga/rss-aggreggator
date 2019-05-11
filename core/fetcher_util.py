import logging
import re
import requests

from core.app_config import AppConfig


class FetcherUtil:

    @staticmethod
    def fetch(url: str) -> str:
        if AppConfig.is_running_in_gae():
            result = requests.get(url)
            if result.status_code > 299:
                raise Exception(f'unable to fetch data from {url} - {result.status_code}')
            return result.content
        else:
            logging.warning(f'Retrieving stubbed data locally for {url}')
            if re.match('.*spotgroningen.*', url):
                with open('tests/samples/spot/Programma - Spot Groningen.html') as f:
                    return ''.join(f.readlines())
            elif re.match('.*vera-groningen.*', url):
                with open('tests/samples/vera-groningen/raw-fetch.html') as f:
                    return ''.join(f.readlines())
            elif re.match('.*simplon.nl.*', url):
                with open('tests/samples/simplon-groningen/Simplon.html') as f:
                    return ''.join(f.readlines())
            elif re.match('.*komoost.nl.*', url):
                with open('tests/samples/oost-groningen/komoost.html') as f:
                    return ''.join(f.readlines())
            elif re.match('.*tivolivredenburg.nl.*page=1.*', url):
                with open('tests/samples/tivoli-utrecht/ajax-1.js') as f:
                    return ''.join(f.readlines())
            elif re.match('.*tivolivredenburg.nl.*page=2.*', url):
                with open('tests/samples/tivoli-utrecht/ajax-2.js') as f:
                    return ''.join(f.readlines())
            elif re.match('.*paradiso.nl.*page=1.*', url):
                with open('tests/samples/paradiso-amsterdam/ajax-1.js') as f:
                    return ''.join(f.readlines())
            elif re.match('.*paradiso.nl.*page=2.*', url):
                with open('tests/samples/paradiso-amsterdam/ajax-2.js') as f:
                    return ''.join(f.readlines())
            raise Exception(f'No support for stubbed url {url}')
