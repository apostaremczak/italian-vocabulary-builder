"""
Container class for definitions (and potentially synonyms) from treccani.it
"""

from dataclasses import dataclass
from vocab_builder.api_result import ApiResult
from vocab_builder.treccani.treccani_html_parser_utils import (
    TreccaniVocabularyPage,
    TreccaniDefinition,
)


@dataclass
class TreccaniResult(ApiResult):
    """Data holder for parsed results from Treccani.it"""

    def __init__(self, treccani_pages: list[TreccaniVocabularyPage]):
        self.definitions = [TreccaniDefinition(page) for page in treccani_pages]

    def to_html(self) -> str:
        definitions_html = [
            f"""
            <div class="treccani-definition">{definition.to_html()}</div>
            """
            for definition in self.definitions
        ]
        return " ".join(definitions_html)
