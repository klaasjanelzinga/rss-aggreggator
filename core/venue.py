from typing import List

from core.item import Item


class Venue:

    def __init__(self, venue_id: str, name: str, url: str, items: List[Item]):
        self.name = name
        self.url = url
        self.venue_id = venue_id
        self.items = items
