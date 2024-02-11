"""
Abstract class for fetching data from different providers
"""

from abc import ABC, abstractmethod

from vocab_builder.api_result import ApiResult


class ApiClient(ABC):  # pylint: disable=too-few-public-methods
    """Abstract class for fetching data from different providers"""

    @abstractmethod
    async def fetch_data(self, word: str) -> ApiResult:
        """
        Async method for fetching data
        :param word: Word to be searched, as typed into the search bar
        :return: Data container inhering from ApiResult with the results
        """
