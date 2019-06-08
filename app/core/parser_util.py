import re

from bs4.element import Tag


class ParserUtil:

    @staticmethod
    def not_empty(text: str) -> bool:
        return text is not None and text != '' and text.strip() != ''

    @staticmethod
    def is_empty(text: str) -> bool:
        return not ParserUtil.not_empty(text)

    @staticmethod
    def has_non_empty_text(tag: Tag):
        return tag is not None and ParserUtil.not_empty(tag.text)

    @staticmethod
    def stripped_text_or_default_if_empty(tag: Tag, default: str) -> str:
        if tag is None or ParserUtil.is_empty(tag.text):
            return default
        return tag.text.strip()

    @staticmethod
    def sanitize_text(text: str) -> str:
        return re.sub(r'[\ \ ]{2,}', '', text).replace('\n', '')

    @staticmethod
    def remove_children_text_from(parent_tag: Tag, text: str) -> str:
        for tag in parent_tag.children:
            if isinstance(tag, Tag):
                child_text = tag.text
                text = text.replace(child_text, '')
        return text
