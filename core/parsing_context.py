from dataclasses import dataclass

from core.venue import Venue


@dataclass
class ParsingContext:
    venue: Venue
    content: str
