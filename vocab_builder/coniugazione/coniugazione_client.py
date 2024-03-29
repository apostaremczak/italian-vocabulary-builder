"""
Client class for retrieving results from https://www.coniugazione.it/
"""

import aiohttp
from bs4 import BeautifulSoup

from vocab_builder.api_client import ApiClient
from vocab_builder.coniugazione.coniugazione_result import ConiugazioneResult


class ConiugazioneClient(ApiClient):
    """
    Client class for retrieving results from https://www.coniugazione.it/
    """

    CONIUGAZIONE_URL = "https://www.coniugazione.it/verbo"

    def __init__(self):
        self.base_url = ConiugazioneClient.CONIUGAZIONE_URL

    @staticmethod
    def parse_html(source_html: str) -> ConiugazioneResult:
        """
        :param source_html: Raw HTML returned by coniugazione.it
        :return: ConiugazioneResult with parsed conjugation results
        """
        soup = BeautifulSoup(source_html, "html.parser")
        tenses = soup.find_all("div", class_="tempscorps")
        tenses = [str(t) for t in tenses]
        return ConiugazioneResult(tenses)

    async def fetch_data(self, word: str) -> ConiugazioneResult:
        async with aiohttp.ClientSession() as session:
            word_url = f"{self.base_url}/{word}.php"
            async with session.get(word_url) as response:
                if not response.ok:
                    return ConiugazioneResult([])
                source_html = await response.text()
        return self.parse_html(source_html)
