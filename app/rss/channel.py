from dataclasses import dataclass
from datetime import datetime
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement


@dataclass
class RSSChannel:
    title: str = "Events from all venues"
    link: str = "https://venues.n-kj.nl"
    description: str = "Aggregation of several venues"
    language: str = "nl"
    copyright: str = "None"
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
