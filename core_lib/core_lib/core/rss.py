from dataclasses import dataclass
from datetime import datetime
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

from core_lib.core.models import Event


@dataclass
class RSSChannel:
    title: str = "Events from all venues"
    link: str = "https://venues.n-kj.nl"
    description: str = "Aggregation of several venues"
    language: str = "nl"
    copyright_rss: str = "None"
    managing_editor: str = "klaasjanelzinga@gmail.com"
    web_master: str = "klaasjanelzinga@gmail.com"
    generator: str = "Python3"
    pub_date: datetime = datetime.now()
    last_build_date: datetime = datetime.now()
    category: str = "Entertainment"
    docs: str = "https://cyber.harvard.edu/rss/rss.html"

    def generate_pre_amble(self) -> str:
        root = Element("rss", {"version": "2.0"})
        channel = SubElement(root, "channel")
        SubElement(channel, "title").text = self.title
        SubElement(channel, "link").text = self.link
        SubElement(channel, "description").text = self.description
        SubElement(channel, "webMaster").text = self.web_master
        SubElement(channel, "managingEditor").text = self.managing_editor
        SubElement(channel, "generator").text = self.generator
        SubElement(channel, "category").text = self.category

        image = SubElement(channel, "image")
        SubElement(image, "url").text = f"{self.link}/channel-image.png"
        SubElement(image, "title").text = self.title
        SubElement(image, "link").text = self.link
        return ElementTree.tostring(root, encoding="unicode")

    @staticmethod
    def generate_post_amble() -> str:
        return "</channel></rss>"


@dataclass
class RSSItem:
    title: str
    link: str
    description: str
    author: str
    guid: str
    source: str

    def as_node(self) -> bytes:
        item_element = Element("item")
        SubElement(item_element, "title").text = self.title
        SubElement(item_element, "link").text = self.link
        SubElement(item_element, "description").text = self.description
        SubElement(item_element, "guid").text = self.guid
        SubElement(item_element, "source").text = self.source
        SubElement(item_element, "author").text = self.author
        return ElementTree.tostring(item_element)


class Transformer:
    @staticmethod
    def item_to_rss(item: Event) -> RSSItem:
        venue = item.venue
        when = venue.convert_utc_to_venue_timezone(item.when).strftime("%Y-%m-%d %H:%M")
        title = f"{item.title} [{venue.short_name}]"
        image_url = (
            f'<img src="{item.image_url}" alt="image for event" width=300 height=160/>'
            if item.image_url is not None
            else ""
        )
        description = f"""<html><body>
            <p>{item.description}</p>
            {image_url}
            <p>When: {when} -
               Where: <a href="{venue.url}">{venue.name} ({venue.city}, {venue.country})</a></p>
            </body></html>"""
        return RSSItem(
            title=title, link=item.url, description=description, author=item.source, guid=item.url, source=item.source
        )
