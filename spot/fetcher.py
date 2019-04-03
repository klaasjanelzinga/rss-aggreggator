import logging

import requests

from spot.config import SpotConfig


class SpotFetcher:

    def __init__(self, config: SpotConfig):
        self.url = config.scrape_url

    def fetch(self) -> str:
        logging.info(f'Fetching from url {self.url}')
        result = requests.get(self.url)
        if result.status_code > 299:
            raise Exception(f'unable to fetch data from {self.url} - {result.status_code}')
        return result.content
