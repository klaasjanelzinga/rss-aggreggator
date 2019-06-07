from datetime import datetime
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement


class RSSChannel:

    def __init__(self):
        self.title = 'Events from all venues'
        self.link = 'https://rss-aggregator-236707.appspot.com'
        self.description = 'Aggregation of several venues'
        self.language = 'nl'
        self.copyright = 'None'
        self.managing_editor = 'klaasjanelzinga@gmail.com'
        self.web_master = 'klaasjanelzinga@gmail.com'
        self.generator = 'Python3'
        self.pub_date = datetime.now()
        self.last_build_date = datetime.now()
        self.category = 'Entertainment'
        self.docs = 'https://cyber.harvard.edu/rss/rss.html'

    def generate_pre_amble(self) -> str:
        root = Element('rss', {'version': '2.0'})
        channel = SubElement(root, 'channel')
        SubElement(channel, 'title').text = self.title
        SubElement(channel, 'link').text = self.link
        SubElement(channel, 'description').text = self.description
        SubElement(channel, 'webMaster').text = self.web_master
        SubElement(channel, 'managingEditor').text = self.managing_editor
        SubElement(channel, 'generator').text = self.generator
        SubElement(channel, 'category').text = self.category

        image = SubElement(channel, 'image')
        SubElement(image, 'url').text = f'{self.link}/channel-image.png'
        SubElement(image, 'title').text = self.title
        SubElement(image, 'link').text = self.link
        return ElementTree.tostring(root, encoding='unicode')

    @staticmethod
    def generate_post_amble() -> str:
        return '</channel></rss>'
