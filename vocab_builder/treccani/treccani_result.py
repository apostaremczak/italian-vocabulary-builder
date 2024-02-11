"""
Container class for definitions (and potentially synonyms) from treccani.it
"""

import re
from dataclasses import dataclass

from bs4 import BeautifulSoup
from bs4.element import Tag
from vocab_builder.api_result import ApiResult


def _remove_repeated_spaces(input_string: str) -> str:
    # Regex to replace consecutive spaces with a single space
    cleaned_string = re.sub(r"\s{2,}", " ", input_string)
    return cleaned_string.strip()


def _find_strong_em(element: Tag) -> bool:
    return element.name in ["strong", "em"]


def _simplify(element: Tag) -> str:
    text = str(element.text)
    if element.name == "strong":
        is_another_meaning = len(re.findall(r"[0-9a-z]\. ", text)) > 0
        # TODO: Add new line/section for easier reading
        if is_another_meaning:
            return f"\n<b>{text}</b> "
        return f" <b>{text}</b> "
    return text


def _extract_treccani_definition(html_text: str):
    if not html_text:
        return "No definition found"

    soup = BeautifulSoup(html_text, "html.parser")
    definition_objects = soup.find_all(_find_strong_em)

    # Extract the text content between the selected elements
    result_text = ""
    for element in definition_objects:
        result_text += _simplify(element)
        text_between = element.nextSibling.text.strip()
        result_text += text_between
    return _remove_repeated_spaces(result_text)


@dataclass
class TreccaniResult(ApiResult):
    """Data holder for results from Treccani.it"""

    def __init__(self, html_text: str):
        self.definition = _extract_treccani_definition(html_text)

    def to_html(self) -> str:
        return self.definition
