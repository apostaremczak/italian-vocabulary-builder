"""
Configuration for the service.
If you want to change the target translation language, this is where you can
do it.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TranslationConfig:
    """
    Translation configuration: which language should Italian be translated to?
    """

    # Default language for translations
    main_target_language: str
    # If you speak more than one language, you can add another language as
    # a fallback to look up when translation to your target language
    # couldn't be found
    fallback_language: Optional[str]


# TODO: Change this according to your target language
def get_translation_config() -> TranslationConfig:
    """Parser for TranslationConfig"""
    # TODO: Create a configuration file instead
    return TranslationConfig(main_target_language="pl", fallback_language="en")
