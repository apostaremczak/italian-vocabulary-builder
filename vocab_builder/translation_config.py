from dataclasses import dataclass
from typing import Optional


@dataclass
class TranslationConfig:
    main_target_language: str
    # If you speak more than one language, you can add another language as
    # a fallback to look up when translation to your target language
    # couldn't be found
    fallback_language: Optional[str]


# TODO: Change this accordingly to your target language
def get_translation_config() -> TranslationConfig:
    return TranslationConfig(main_target_language="pl", fallback_language="en")
