from datetime import datetime
from typing import List


class Item:

    def __init__(self,
                 url: str,
                 title: str,
                 description: str,
                 tags: List[str],
                 source: str,
                 date_published: datetime,
                 when: datetime,
                 image_url: str):
        self.url = url
        self.title = title
        self.description = description
        self.tags = tags
        self.source = source
        self.date_published = date_published
        self.when = when
        self.image_url = image_url
