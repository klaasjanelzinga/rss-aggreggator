from dataclasses import dataclass
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement


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
