import base64
import re
from dataclasses import dataclass
from typing import List, Optional

from google.cloud.datastore.query import Iterator


@dataclass
class QueryResult:
    items: Iterator
    token: bytes


class DatastoreUtils:

    @staticmethod
    def create_cursor(earlier_curor: Optional[bytes]) -> Optional[bytes]:
        return base64.decodebytes(earlier_curor) if earlier_curor is not None else None

    @staticmethod
    def construct_query_result_from_query(query_iter: Iterator) -> QueryResult:
        page = next(query_iter.pages)
        next_cursor = query_iter.next_page_token
        next_cursor_encoded = base64.encodebytes(next_cursor) if next_cursor is not None \
            else base64.encodebytes(bytes('DONE', 'UTF-8'))
        return QueryResult(items=page, token=next_cursor_encoded)

    @staticmethod
    def split_term(term: str) -> List[str]:
        return [re.sub(r'[^\w]+', '', t.lower()) for t in re.split(' |-', term) if len(t) > 3]
