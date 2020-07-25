from dataclasses import dataclass

from core_lib.core.venue.venue import Venue


@dataclass
class ParsingContext:
    venue: Venue
    content: str
