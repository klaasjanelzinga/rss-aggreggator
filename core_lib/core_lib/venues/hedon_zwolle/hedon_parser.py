from datetime import datetime
from typing import Dict, List

from bs4 import BeautifulSoup
from bs4.element import Tag

from core_lib.core.event.event import Event
from core_lib.core.parser import Parser
from core_lib.core.parser_util import ParserUtil
from core_lib.core.parsing_context import ParsingContext
from core_lib.core.venue.venue import Venue


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
            when=when if when is not None else datetime.min,
        )
