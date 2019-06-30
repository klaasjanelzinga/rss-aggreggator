import base64
import re
from typing import List, Tuple, Optional, Any


class DatastoreUtils:

    @staticmethod
    def done_as_bytes_base64() -> bytes:
        return base64.encodebytes(bytes('DONE', 'UTF-8'))

    @staticmethod
    def create_cursor(earlier_curor: Optional[bytes]) -> Optional[bytes]:
        return base64.decodebytes(earlier_curor) if earlier_curor is not None else None

    @staticmethod
    def entities_and_cursor(query_iter: Any) -> Tuple[List, bytes]:
        page = next(query_iter.pages)
        results = list(page)
        next_cursor = query_iter.next_page_token
        next_cursor_encoded = base64.encodebytes(next_cursor) if next_cursor is not None \
            else DatastoreUtils.done_as_bytes_base64()
        return results, next_cursor_encoded

    @staticmethod
    def split_term(term: str) -> List[str]:
        return [re.sub(r'[^\w]+', '', t.lower()) for t in re.split(r'[ \-]', term) if len(t) > 3]
