from abc import ABC, abstractmethod

from vocab_builder.api_result import ApiResult


class ApiClient(ABC):
    @abstractmethod
    async def fetch_data(self, word: str) -> ApiResult:
        pass
