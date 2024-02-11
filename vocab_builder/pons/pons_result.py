"""
Container for translations returned by pons.com
To fully understand different entities, see an example like this:
https://en.pons.com/translate/italian-english/chiedere
"""

import logging
from dataclasses import dataclass
from typing import Optional

from vocab_builder.api_result import ApiResult, EmptyApiResult


@dataclass
class PonsTranslation:
    """
    Example: source = 'chiedere qc a qu', target = 'to ask sb for sth'
    """

    source: str
    target: Optional[str] = None

    def to_html(self) -> str:
        """Convert a single line to HTML to be displayed in the results page"""

        # If only one word is provided (e.g. it's an additional context, like
        # 'chiedere (per sapere)', span it over two columns and make it bold
        if self.target is None:
            return f'<tr><th colspan="2"><b>{self.target}</b></th></tr>'

        # Otherwise display the source phrase in one column and the translation
        # in another column
        return f"<tr><td>{self.source}</td><td>{self.target}</td></tr>"


@dataclass
class PonsMeaning:
    """
    Example:
        headword = 'chiedere <chiedo, chiesi, chiesto> [ˈkiɛ:·de·re] VB trans'
        translations = [
            source = 'chiedere (per sapere)', target = None,
            source = 'chiedere', target = 'to ask',
            source = 'chiedere qc a qu', target = 'to ask sb for sth',
        ]
    """

    # additional information, such as phonetics, gender, etc.
    headword: str
    # translations
    translations: list[PonsTranslation]

    def to_html(self) -> str:
        """Convert to HTML to be displayed in the results page"""
        table_header = f'<tr><th colspan="2">{self.headword}</th></tr>'
        rows = "\n".join([tr.to_html() for tr in self.translations])
        # TODO: Add CSS class pons-meaning
        return f"""
        <div class="pons-meaning">
        <table>{table_header}\n{rows}</table>
        </div>
        """


@dataclass
class PonsApiResult(ApiResult):
    """
    Data container for (possibly multiple) translations from PONS.com

    For example: https://en.pons.com/translate/italian-english/ancora
    Would return two PonsMeaning:
        - one for 'still, again'
        - one for 'anchor'
    """

    def __init__(self, entries: list[dict]):
        self.meanings: list[PonsMeaning] = [
            _parse_single_result(entry) for entry in entries
        ]

    def to_html(self) -> str:
        meanings_html = "\n".join(
            [meaning.to_html() for meaning in self.meanings]
        )
        return meanings_html


def _parse_single_result(result: dict) -> PonsMeaning:
    """
    Example of a single result, from
    https://en.pons.com/translate/italian-english/chiedere

    headword:
    chiedere <chiedo, chiesi, chiesto> [ˈkiɛ:·de·re] VB trans

    meaning 1:
    1. chiedere (per sapere):
        chiedere                            to ask
        chiedere qc a qu                    to ask sb for sth
        chiedere il prezzo di qc            to ask the price of sth
        chiedere notizie di qu              to ask after sb

    meaning 2:
    2. chiedere (per avere):
        chiedere                            to ask for
        chiedere a qu di fare qc            to ask sb to do sth
        chiedere un favore a qu             to ask sb a favor
        chiedere la mano di una ragazza     to ask for a girl's hand
    """
    roms = result["roms"]
    if len(roms) > 1:
        logging.warning("PONS returned multiple roms in %s", roms)
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
    return PonsMeaning(headword=headword, translations=translations)


def _parse_api_response(json_response) -> ApiResult:
    try:
        hits = json_response[0]["hits"]
        entries = [r for r in hits if r["type"] == "entry"]
        pons_api_result = PonsApiResult(entries)
    except (IndexError, KeyError):
        logging.warning(
            "JSON returned by PONS was different than expected\n %s",
            json_response,
        )
        return EmptyApiResult()
    return pons_api_result
