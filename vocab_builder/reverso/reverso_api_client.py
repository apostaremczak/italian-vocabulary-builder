from reverso_context_api import Client

from vocab_builder.api_client import ApiClient
from vocab_builder.reverso.reverso_result import ReversoResult

client = Client("it", "pl")
print(list(client.get_translations("socchiudere")))
print(list(client.get_translation_samples("socchiudere")))


class ReversoClient(ApiClient):
    def __init__(self):
        pass

    async def fetch_data(self, word: str):
        pass
