from typing import List

from rss.channel import RSSChannel
from rss.item import RSSItem


class ChannelFactory:

    @staticmethod
    def create_default_channel(items: List[RSSItem]) -> RSSChannel:
        return RSSChannel(items)
