from typing import Dict

from app.core.event.event import Event
from app.core.venue.venue_repository import VenueRepository


class EventEntityTransformer:
    def __init__(self, venue_repository: VenueRepository):
        self.venue_repository = venue_repository

    @staticmethod
    def to_entity(event: Event) -> Dict:
        return {
            "url": event.url,
            "title": event.title,
            "description": event.description,
            "venue_id": event.venue.venue_id,
            "source": event.source,
            "date_published": event.date_published,
            "when": event.when,
            "image_url": event.image_url,
            "search_terms": event.generate_search_terms(),
        }

    def to_event(self, entity_map: Dict) -> Event:
        return Event(
            url=entity_map["url"],
            title=entity_map["title"],
            description=entity_map["description"],
            venue=self.venue_repository.get_venue_for(entity_map["venue_id"]),
            source=entity_map["source"],
            date_published=entity_map["date_published"],
            when=entity_map["when"],
            image_url=entity_map["image_url"],
        )
