from datetime import datetime
from typing import List
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

from rss.rss_item import RSSItem


class RSSChannel:

    def __init__(self, items: List[RSSItem]):
        self.title = 'Events aggregator'
        self.link = 'http://unknown'
        self.description = 'Aggregation of several venues'
        self.language = 'nl'
        self.copyright = 'None'
        self.managing_editor = 'the Interwebs'
        self.web_master = 'klaasjanelzinga@gmail.com'
        self.pub_date = datetime.now()
        self.last_build_date = datetime.now()
        self.category = 'Entertainment'
        self.docs = 'https://cyber.harvard.edu/rss/rss.html'
        self.items = items

    def as_xml(self) -> str:
        root = Element('rss', {'version': '2.0'})
        channel = SubElement(root, 'channel')
        SubElement(channel, 'title').text = self.title
        SubElement(channel, 'link').text = self.link
        SubElement(channel, 'description').text = self.description

        [item.as_xml(channel) for item in self.items]
        return ElementTree.tostring(root)
