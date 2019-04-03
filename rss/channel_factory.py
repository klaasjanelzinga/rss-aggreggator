from rss.channel import RSSChannel


class ChannelFactory:

    @staticmethod
    def create_default_channel() -> RSSChannel:
        return RSSChannel()
