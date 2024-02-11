"""
Client class for retrieving word definitions from Treccani dictionary
"""

import logging
from dataclasses import dataclass

import aiohttp

from vocab_builder.api_client import ApiClient
from vocab_builder.treccani.treccani_result import TreccaniResult


@dataclass
class TreccaniClient(ApiClient):
    """Client class for retrieving word definitions from treccani.it"""

    VOCABULARY_URL = "https://www.treccani.it/vocabolario"

    def __init__(self):
        self.vocab_url = TreccaniClient.VOCABULARY_URL

    # TODO: Handle multiple meanings
    #  Example: https://www.treccani.it/vocabolario/ricerca/sete/
    async def fetch_data(self, word: str) -> TreccaniResult:
        async with aiohttp.ClientSession() as session:
            word_url = f"{self.vocab_url}/{word}"
            async with session.get(word_url) as response:
                if not response.ok:
                    logging.warning(
                        "Invalid response from Treccani with code %s",
                        response.status,
                    )
                    return TreccaniResult("")
                source_html = await response.text()
        return TreccaniResult(source_html)
