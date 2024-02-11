"""
Utils for parsing the source code of Treccani websites
"""

import re
from dataclasses import dataclass
from typing import Optional

from bs4 import BeautifulSoup
from bs4.element import Tag


def _remove_repeated_spaces(input_string: str) -> str:
    # Regex to replace consecutive spaces with a single space
    cleaned_string = re.sub(r"\s{2,}", " ", input_string)
    return cleaned_string.strip()


def _find_strong_or_em(element: Tag) -> bool:
    """
    Style classes 'strong' and 'em' are used by treccani for special formatting
    of the definitions
    """
    return element.name in ["strong", "em"]


def _definition_paragraph_filter(class_name) -> bool:
    return class_name and class_name.startswith(
        "MuiTypography-root MuiTypography-bodyL"
    )


def _simplify(element: Tag) -> str:
    """
    Remove custom 'strong' and 'em' classes and replace them with bold text and
    italics respectively.
    """
    text = str(element.text)
    if element.name == "strong":
        is_another_meaning = len(re.findall(r"^[0-9a-z]\.", text)) > 0
        if is_another_meaning:
            return f"<br><br><b>{text}</b> "
        return f" <b>{text}</b> "
    return f" <i>{text}</i>"


def _extract_definition_text(html_text: str) -> str:
    """
    :param html_text: Source code of a section from 'Vocabolario on line',
    e.g. https://www.treccani.it/vocabolario/ancora/
    :return: Extracted text of the word's definition
    """
    if not html_text:
        return "No definition found"

    soup = BeautifulSoup(html_text, "html.parser")
    # Find the paragraph containing word definition
    definition_par = soup.find_all("p", class_=_definition_paragraph_filter)[1]
    # Select objects that define additional formatting
    highlights = definition_par.find_all(_find_strong_or_em)

    # Select the starting text of the paragraph, before the first highlight
    raw_definition_text = definition_par.text
    first_element_text = highlights[0].text
    first_text_index = raw_definition_text.find(first_element_text)
    result_text = raw_definition_text[:first_text_index]

    # Extract the text content between the selected elements
    for element in highlights:
        result_text += _simplify(element)
        text_between = element.nextSibling.text.strip()
        # Break lines when new paragraph is detected for more readability
        text_between = text_between.replace("◆", "<br>◆").replace("–", "<br>–")
        result_text += text_between
    return _remove_repeated_spaces(result_text)


@dataclass
class TreccaniVocabularyPage:
    """
    Container for input Treccani details
    """

    title: str
    url: str
    html_source_code: Optional[str] = None

    def set_html_source_code(self, html_source_code):
        """Update the source HTML code storage"""
        self.html_source_code = html_source_code


@dataclass
class TreccaniDefinition:
    """
    Container for parsed definitions,
    e.g. when searching up the word "ancora" two TreccaniDefinition instances
    would be created:
        - TreccaniDefinition(ancóra, definition of 'still')
        - TreccaniDefinition(àncora, definition of 'anchor')
    """

    title: str
    original_url: str
    definition: str

    def __init__(self, page: TreccaniVocabularyPage):
        self.title = page.title
        self.original_url = page.url
        self.definition = _extract_definition_text(page.html_source_code)

    def to_html(self) -> str:
        """Parsed HTML representation for displaying results"""
        return f"""
        <h3>
        <a href="{self.original_url}" target="_blank">{self.title}</a>
        </h3>
        <br>
        {self.definition}
        """
