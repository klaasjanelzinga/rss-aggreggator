from dataclasses import dataclass

from app.core.venue.venue import Venue


@dataclass
class ParsingContext:
    venue: Venue
    content: str
