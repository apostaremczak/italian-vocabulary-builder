"""
Client class for retrieving word definitions from Treccani dictionary
"""

import json
import logging
from dataclasses import dataclass

import aiohttp
from bs4 import BeautifulSoup

from vocab_builder.api_client import ApiClient
from vocab_builder.treccani.treccani_html_parser_utils import (
    TreccaniVocabularyPage,
)
from vocab_builder.treccani.treccani_result import TreccaniResult


@dataclass
class TreccaniClient(ApiClient):
    """Client class for retrieving word definitions from treccani.it"""

    BASE_URL = "https://www.treccani.it"
    VOCABULARY_URL = "https://www.treccani.it/vocabolario"
    SEARCH_URL = "https://www.treccani.it/vocabolario/ricerca"

    def __init__(self):
        self.base_url = TreccaniClient.BASE_URL
        self.vocab_url = TreccaniClient.VOCABULARY_URL
        self.search_url = TreccaniClient.SEARCH_URL

    def _find_all_entries_url(
        self, word: str, results_page_html: str
    ) -> list[TreccaniVocabularyPage]:
        """
        Sometimes a word with the same spelling can have multiple meaning
        with e.g. different accents, such as:
        ancora -> ancóra, àncora

        :param word: Searched word, e.g. "ancora"
        :param results_page_html: Source HTML as returned by
            https://www.treccani.it/vocabolario/ricerca/
        :return: List of URLs for single result pages, e.g. [
            (link to ancóra)
            https://www.treccani.it/vocabolario/ancora_res-d49bd28d-000d-11de-9d89-0016357eee51/,
            (link to àncora)
            https://www.treccani.it/vocabolario/ancora/
        ]
        """
        results_soup = BeautifulSoup(results_page_html, "html.parser")
        result_json_str = results_soup.find("script", type="application/json")
        if result_json_str is None:
            logging.warning(
                """
                Something went wrong when scanning search results from Treccani
                """
            )
            return []
        # Replace line breaks in search results as they mess up JSONs
        result_json = json.loads(result_json_str.text.replace("\n", ""))
        query_matches = result_json["props"]["pageProps"]["data"]["matches"]
        word_def_urls = [
            TreccaniVocabularyPage(
                title=match["title"], url=f"{self.base_url}{match['url']}"
            )
            for match in query_matches
            if word in match["query"]
            and match["section"] == "vocabolario"
            and match["description"] == "Vocabolario on line"
        ]
        return word_def_urls

    async def fetch_data(self, word: str) -> TreccaniResult:
        async with aiohttp.ClientSession() as session:
            # First, search for all entries related to the query
            word_search_url = f"{self.search_url}/{word}"
            async with session.get(word_search_url) as response:
                if not response.ok:
                    logging.warning(
                        "Invalid response from Treccani with code %s",
                        response.status,
                    )
                    return TreccaniResult([])
                results_page_html = await response.text()
            word_urls = self._find_all_entries_url(word, results_page_html)

            # For each meaning/entry, parse the results
            pages: list[TreccaniVocabularyPage] = []
            for word_page in word_urls:
                async with session.get(word_page.url) as response:
                    if not response.ok:
                        logging.warning(
                            "Invalid response from Treccani with code %s",
                            response.status,
                        )
                    word_definition_html = await response.text()
                word_page.set_html_source_code(word_definition_html)
                pages.append(word_page)

        return TreccaniResult(pages)
