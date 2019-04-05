from typing import List

from core.event import Event


class Venue:

    def __init__(self, venue_id: str, name: str, url: str, events: List[Event]):
        self.name = name
        self.url = url
        self.venue_id = venue_id
        self.events = events
