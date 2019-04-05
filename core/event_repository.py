import logging
from typing import List

from core.event import Event


class EventRepository:

    def sync_items(self, items: List[Event]):
        logging.info('syncing items')
        pass

    def fetch_items(self) -> List[Event]:
        pass
