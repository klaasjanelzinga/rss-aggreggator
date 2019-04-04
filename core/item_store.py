import logging
from typing import List

from core.item import Item


class ItemStore:

    def sync_items(self, items: List[Item]):
        logging.info('syncing items')
        pass

    def fetch_items(self) -> List[Item]:
        pass
