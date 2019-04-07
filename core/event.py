import base64
from datetime import datetime, tzinfo
from typing import Dict

from pytz import timezone

from core.app_config import AppConfig


class Event:

    def __init__(self,
                 url: str,
                 title: str,
                 description: str,
                 venue_id: str,
                 source: str,
                 date_published: datetime,
                 when: datetime,
                 image_url: str):
        self.url = url
        self.title = title
        self.description = description
        self.venue_id = venue_id
        self.source = source
        self.date_published = date_published
        self.when = when
        self.image_url = image_url
        self.id = str(base64.encodebytes(bytes(self.url, 'utf-8')), 'utf-8')

    @staticmethod
    def from_map(entity_map):
        return Event(
            url=entity_map['url'],
            title=entity_map['title'],
            description=entity_map['description'],
            venue_id=entity_map['venue_id'],
            source=entity_map['source'],
            date_published=AppConfig.datetime_utc_to_amsterdam(entity_map['date_published']),
            when=AppConfig.datetime_utc_to_amsterdam(entity_map['when']),
            image_url=entity_map['image_url'])

    def to_map(self) -> Dict:
        return {
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'venue_id': self.venue_id,
            'source': self.source,
            'date_published': self.date_published,
            'when': self.when,
            'image_url': self.image_url
        }
