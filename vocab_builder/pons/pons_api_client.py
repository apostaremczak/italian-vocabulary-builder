import aiohttp
import logging

from vocab_builder.api_client import ApiClient
from vocab_builder.api_result import EmptyApiResult
from vocab_builder.pons.pons_result import PonsApiResult, _parse_api_response
from vocab_builder.translation_config import TranslationConfig


class PonsApiClient(ApiClient):
    PONS_API_URL = "https://api.pons.com/v1/dictionary"
    INPUT_LANGUAGE = "it"

    def __init__(self, secret: str, translation_config: TranslationConfig):
        self.url = PonsApiClient.PONS_API_URL
        self.secret = secret
        self.input_language = PonsApiClient.INPUT_LANGUAGE
        self.target_language = translation_config.main_target_language
        self.fallback_target_language = translation_config.fallback_language
        self.dictionary_code = "".join(sorted(["it", self.target_language]))
        self.fallback_dictionary_code = "".join(
            sorted(["it", self.fallback_target_language])
        )

    async def fetch_data(self, word: str) -> PonsApiResult:
        params = {
            'l': self.dictionary_code,
            'q': word,
            'in': self.input_language
        }
        headers = {
            'X-Secret': self.secret
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=self.url,
                    params=params,
                    headers=headers
            ) as response:
                if response.status != 200:
                    # TODO: Translate to the fallback language
                    logging.warning(f"PONS response code {response.status}")
                    return EmptyApiResult()
                response_json = await response.json()
        return _parse_api_response(response_json)
