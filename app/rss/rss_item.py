from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement


class RSSItem:

    def __init__(self, title: str, link: str, description: str, author: str, guid: str, source: str):
        self.title = title
        self.link = link
        self.description = description
        self.author = author
        self.guid = guid
        self.source = source

    def as_node(self) -> str:
        item_element = Element('item')
        SubElement(item_element, 'title').text = self.title
        SubElement(item_element, 'link').text = self.link
        SubElement(item_element, 'description').text = self.description
        SubElement(item_element, 'guid').text = self.guid
        SubElement(item_element, 'source').text = self.source
        SubElement(item_element, 'author').text = self.author
        return ElementTree.tostring(item_element)
