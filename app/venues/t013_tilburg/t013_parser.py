from datetime import datetime
import json
from typing import Dict, List

from bs4 import BeautifulSoup
import dateparser

from app.core.event.event import Event
from app.core.parser import Parser
from app.core.parsing_context import ParsingContext
from app.core.venue.venue import Venue


class T013Parser(Parser):
    dateformat: str = "%Y-%m-%dT:%H%M:%S%z"

    def parse(self, parsing_context: ParsingContext) -> List[Event]:
        soup = BeautifulSoup(parsing_context.content, "html.parser")
        program_items = soup.find("body").find_all("script")
        data_script = [p for p in program_items if "src" not in p][0].text
        start_index = data_script.find("event_index:") + 12
        end_index = data_script.find("""]},""") + 2
        json_script = data_script[start_index:end_index]
        json_script = json_script.replace("\\n", "").replace("""\\""", "")
        json_data_events = json.loads(json_script)
        return [T013Parser._transform(parsing_context.venue, json_data) for json_data in json_data_events["events"]]

    @staticmethod
    def _transform(venue: Venue, json_event: Dict) -> Event:
        title = json_event["title"]
        description = json_event["subtitle"]
        if not description:
            description = title
        if "supportAct" in json_event and not json_event["supportAct"] is None:
            title = f"{title} {json_event['supportAct']}"
        source = venue.source_url
        url = f"{venue.url}{json_event['url']}"
        starts_at = json_event["dates"]["startsAt"]
        date = dateparser.parse(starts_at, settings={"TIMEZONE": venue.timezone, "RETURN_AS_TIMEZONE_AWARE": True})
        image_url = f"{venue.url}{json_event['images']['regular']['mobile']}"
        return Event(
            url=url,
            title=title,
            venue=venue,
            image_url=image_url,
            source=source,
            description=description,
            date_published=datetime.now(),
            when=date,
        )
