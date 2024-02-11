"""
TODO: Container for results from https://context.reverso.net/translation
"""

from dataclasses import dataclass

from vocab_builder.api_result import ApiResult


@dataclass
class ReversoResult(ApiResult):
    """Container for translation results from reverso.net"""

    def to_html(self) -> str:
        # TODO: Convert results to HTML
        pass
