import logging
from dataclasses import dataclass
from typing import Optional

from vocab_builder.api_result import ApiResult, EmptyApiResult


@dataclass
class PonsTranslation:
    source: str
    target: Optional[str] = None

    def to_html(self) -> str:
        if self.target is None:
            return f'<tr><th colspan="2">{self.target}</th></tr>'
        return f"<tr><td>{self.source}</td><td>{self.target}</td></tr>"


@dataclass
class PonsMeaning:
    # additional information, such as phonetics, gender, etc.
    headword: str
    # translations
    translations: list[PonsTranslation]

    def to_html(self) -> str:
        table_header = f'<tr><th colspan="2">{self.headword}</th></tr>'
        rows = "\n".join([tr.to_html() for tr in self.translations])
        return f"""
        <div class="pons-meaning">
        <table>{table_header}\n{rows}</table>
        </div>
        """


class PonsApiResult(ApiResult):
    def __init__(self, entries: list[dict]):
        self.meanings: list[PonsMeaning] = [
            _parse_single_result(entry) for entry in entries
        ]

    def to_html(self) -> str:
        meanings_html = "\n".join([meaning.to_html() for meaning in self.meanings])
        return meanings_html


def _parse_single_result(result: dict) -> PonsMeaning:
    roms = result["roms"]
    if len(roms) > 1:
        logging.warning(f"PONS returned multiple roms in {roms}")
    rom = roms[0]
    headword = rom["headword_full"]
    translations = []
    for arab in rom["arabs"]:
        header = arab["header"]
        if header:
            translations.append(PonsTranslation(source=header))
        for translation in arab["translations"]:
            translations.append(
                PonsTranslation(
                    source=translation["source"], target=translation["target"]
                )
            )
    logging.debug(translations)
    return PonsMeaning(headword=headword, translations=translations)


def _parse_api_response(json_response) -> ApiResult:
    try:
        hits = json_response[0]["hits"]
        entries = [r for r in hits if r["type"] == "entry"]
        logging.debug(entries)
        pons_api_result = PonsApiResult(entries)
    except (IndexError, KeyError):
        logging.warning(
            f"JSON returned by PONS was different " f"than expected\n {json_response}"
        )
        return EmptyApiResult()
    return pons_api_result
