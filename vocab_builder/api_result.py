"""
Abstract data container for results from different providers
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ApiResult(ABC):
    """Abstract data container for results from different providers"""

    @abstractmethod
    def to_html(self) -> str:
        """Convert to HTML to be displayed in the results page"""


@dataclass
class EmptyApiResult(ApiResult):
    """Empty object for missing data, e.g. conjugations of a noun"""

    def to_html(self) -> str:
        """Convert to HTML to be displayed in the results page"""
        return ""
