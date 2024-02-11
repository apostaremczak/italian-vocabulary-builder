"""
TODO: Container for retrieving results from
https://context.reverso.net/translation
"""

from dataclasses import dataclass

from reverso_context_api import Client

from vocab_builder.api_client import ApiClient
from vocab_builder.reverso.reverso_result import ReversoResult


@dataclass
class ReversoClient(ApiClient):
    """Wrapper for calling reverso_context_api"""

    def __init__(self):
        pass

    async def fetch_data(self, word: str) -> ReversoResult:
        # TODO: Retrieve results from Reverso
        client = Client("it", "pl")
        print(list(client.get_translations(word)))
        print(list(client.get_translation_samples(word)))
