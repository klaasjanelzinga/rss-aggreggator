from datetime import datetime
from typing import List, AsyncIterable
from xml.etree import ElementTree

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from core_lib.core.fetch_and_parse_details import FetchAndParseDetails
from core_lib.core.models import Event, Venue
from core_lib.core.parser import Parser, ParsingContext, ParserUtil
from core_lib.core.processing_chain import DatabaseSink, Chain, OnlyValidEvents
from core_lib.core.repositories import EventRepository, VenueRepository
from core_lib.core.source import Source
from core_lib.core.venue_processor import VenueProcessor


class NeushoornParser(Parser):
    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        root = ElementTree.fromstring(parsing_context.content)
        events = []
        for item in root.iter("item"):
            maybe_url = item.find("link")
            maybe_description = item.find("description")
            maybe_title = item.find("title")
            if maybe_url is None or maybe_title is None or maybe_description is None:
                break
            url = maybe_url.text
            description = maybe_description.text
            title = maybe_title.text
            events.append(
                Event(
                    url=str(url),
                    title=str(title),
                    description=str(description),
                    venue=parsing_context.venue,
                    source=parsing_context.venue.url,
                    date_published=datetime.now(),
                    when=datetime.min,
                    image_url=None,
                )
            )
        return events

    def update_event_with_details(self, event: Event, additional_details: str) -> Event:
        soup = BeautifulSoup(additional_details, features="html.parser")
        image_url = None
        when_date = None
        if soup.find("meta", {"name": "twitter:image"}) is not None:
            image_url = soup.find("meta", {"name": "twitter:image"})["content"]
        if soup.find("meta", {"property": "og:image"}):
            image_url = soup.find("meta", {"property": "og:image"})["content"]
        summary_div = soup.find("div", {"class": "summary"})
        summary_item_divs = summary_div.find_all("div", {"class": "summary__item"})
        if len(summary_item_divs) == 2:
            date = summary_item_divs[0].text
            time = summary_item_divs[1].text
            date = ParserUtil.sanitize_text(date)
            time = ParserUtil.sanitize_text(time)
            time = time[time.index("Aanvang ") + 8 :]
            when_date = ParserUtil.parse_date_time_to_datetime(date, time, event.venue.timezone)

        if when_date is not None:
            event.when = when_date
        event.image_url = image_url
        return event


class NeushoornProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = NeushoornProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def fetch_source(self) -> Source:
        return NeushoornSource(self.venue)

    # pylint: disable= W0613, R0201
    def create_processing_chain(self, client_session: ClientSession, database_sink: DatabaseSink) -> Chain:
        return Chain(
            [
                FetchAndParseDetails(client_session=client_session, source=self.fetch_source()),
                OnlyValidEvents(),
                database_sink,
            ]
        )

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="neushoorn-leeuwarden",
            short_name="Neus NL-LEE",
            name="Neushoorn Leeuwarden",
            phone="",
            city="Leeuwarden",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@neushoorn.nl",
            url="https://www.neushoorn.nl",
            source_url="https://www.neushoorn.nl",
        )


class NeushoornSource(Source):
    def __init__(self, venue: Venue, scrape_url: str = "https://neushoorn.nl/upcoming_events"):
        super().__init__(venue, scrape_url, NeushoornParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
