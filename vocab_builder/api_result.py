from abc import ABC, abstractmethod


class ApiResult(ABC):
    @abstractmethod
    def to_html(self) -> str:
        pass


class EmptyApiResult(ApiResult):
    def to_html(self) -> str:
        return ""
