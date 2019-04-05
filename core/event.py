from datetime import datetime


class Event:

    def __init__(self,
                 url: str,
                 title: str,
                 description: str,
                 source: str,
                 date_published: datetime,
                 when: datetime,
                 image_url: str):
        self.url = url
        self.title = title
        self.description = description
        self.source = source
        self.date_published = date_published
        self.when = when
        self.image_url = image_url
