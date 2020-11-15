from datetime import datetime
from typing import List, Dict, AsyncIterable

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag

from core_lib.core.app_config import AppConfig
from core_lib.core.models import Event, Venue
from core_lib.core.parser import Parser, ParsingContext, ParserUtil
from core_lib.core.processing_chain import DatabaseSink, Chain, OnlyEventsWithWhen
from core_lib.core.repositories import EventRepository, VenueRepository
from core_lib.core.source import Source
from core_lib.core.venue_processor import VenueProcessor


class HedonParser(Parser):
    """
    <article class=\"event-block type--headliner ng-trigger ng-trigger-slide-in\" style=\"transform:translateX(0px);\">
        <div class=\"event-block__mask\"></div>
        <figure class=\"event-block__crop ng-trigger ng-trigger-fade-in\" style=\"opacity:0;\">
            <!----><img alt=\"\" class=\"ng-tns-c3-60 ng-star-inserted\"
                src=\"//www.hedon-zwolle.nl/media/uploads/HeaderCMYK.jpg?width=600&amp;height=600&amp;ranchor=middlecenter&amp;rmode=crop\" style=\"\">
        </figure>
        <div class=\"event-block__content\">
            <h1 class=\"event-block__title\">GRANDMASTER FLASH</h1>
            <!---->
            <div class=\"subtitle event-block__subtitle ng-tns-c3-60 ng-star-inserted\" style=\"\">
            <time class=\"date\" datetime=\"2019-11-28\">do 28 nov.</time>
            <time class=\"time\" datetime=\"21:00\">21:00</time> Grote Zaal </div>
            <!---->
            <!---->
            <!---->
            <!---->
            <!---->
        </div>
        <!----><a class=\"block-link ng-tns-c3-60 ng-star-inserted\" href=\"/voorstelling/26978/grandmaster-flash\" style=\"\">
         meer informatie over GRANDMASTER FLASH </a>
    </article>
    """

    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        soup = BeautifulSoup(parsing_context.content, "html.parser")
        program_items = soup.find_all("article")
        unique_items: Dict[str, Tag] = {}
        for program_item in program_items:
            url = program_item.a.get("href")
            if url not in unique_items:
                unique_items[url] = program_item
            else:
                has_figure = program_item.find("figure") is not None
                has_time = program_item.find("time") is not None
                old_has_time = unique_items[url].find("time") is not None
                if has_figure and has_time:
                    unique_items[url] = program_item
                if has_time and not old_has_time:
                    unique_items[url] = program_item
        return [HedonParser._transform(parsing_context.venue, f) for f in unique_items.values()]

    @staticmethod
    def _transform(venue: Venue, article: Tag) -> Event:
        source = venue.source_url
        base_url = venue.url
        url = f"{base_url}{article.a.get('href')}"
        title = article.find("h1").text
        description = title
        figure = None
        when = None
        if article.find("figure") is not None:
            figure = article.find("figure").img.get("src")
            figure = f"https:{figure}" if not figure.startswith("https://") else figure
        if article.find("time"):
            date = article.find("time", {"class": "date"}).text
            time = article.find("time", {"class": "time"}).text
            when = ParserUtil.parse_date_time_to_datetime(date, time, venue.timezone)

        return Event(
            url=url,
            title=title,
            description=description,
            venue=venue,
            image_url=figure,
            source=source,
            date_published=datetime.now(),
            when=when,
        )


class HedonProcessor(VenueProcessor):
    def __init__(self, event_repository: EventRepository, venue_repository: VenueRepository):
        self.venue = HedonProcessor.create_venue()
        super().__init__(event_repository, venue_repository, self.venue)

    def fetch_source(self) -> Source:
        return HedonSource(self.venue)

    def create_processing_chain(self, client_session: ClientSession, database_sink: DatabaseSink) -> Chain:
        if AppConfig.is_production():
            return super().create_processing_chain(client_session, database_sink)
        return Chain([OnlyEventsWithWhen(), database_sink])

    @staticmethod
    def create_venue() -> Venue:
        return Venue(
            venue_id="hedon-zwolle",
            name="Hedon",
            short_name="Hedon NL-ZWO",
            phone="+31 038-452 72 29",
            city="Zwolle",
            country="NL",
            timezone="Europe/Amsterdam",
            email="info@hedon-zwolle.nl",
            url="https://www.hedon-zwolle.nl",
            source_url="https://www.hedon-zwolle.nl/#programma",
        )


class HedonSource(Source):
    def __init__(self, venue: Venue, scrape_url: str = "https://www.hedon-zwolle.nl/#programma"):
        super().__init__(venue, scrape_url, HedonParser())

    async def fetch_events(self, session: ClientSession) -> AsyncIterable[List[Event]]:
        return self.fetch_page_in_one_call(session=session)
