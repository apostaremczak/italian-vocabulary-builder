"""
Container for conjugation data returned by coniugazione.it
"""

from dataclasses import dataclass

from vocab_builder.api_result import ApiResult


@dataclass
class TenseConjugation:
    """Helper class for easier display of tense conjugation tables"""

    tense_name: str
    conjugation: str

    def to_html(self) -> str:
        """Convert to HTML to be displayed in the results page"""
        return f"""
        <h3>{self.tense_name}</h3>
        {self.conjugation}
        """


@dataclass
class ConiugazioneResult(ApiResult):
    """Container for conjugation data returned by coniugazione.it"""

    TENSE_NAMES = [
        "Indicativo presente",
        "Passato prossimo",
        "Imperfetto",
        "Trapassato prossimo",
        "Passato remoto",
        "Trapassato remoto",
        "Futuro semplice",
        "Futuro anteriore",
        "Condizionale presente",
        "Condizionale passato",
        "Congiuntivo presente",
        "Congiuntivo passato",
        "Congiuntivo imperfetto",
        "Congiuntivo trapassato",
        "Imperativo",
        "Infinito presente",
        "Infinito passato",
        "Participio presente",
        "Participio passato",
        "Gerundio presente",
        "Gerundio passato",
    ]

    def __init__(self, tenses_html: list[str]):
        self.tenses = tenses_html
        self.first_column: list[TenseConjugation] = [
            TenseConjugation(ConiugazioneResult.TENSE_NAMES[i], t)
            for i, t in enumerate(tenses_html)
            if not i % 2
        ]
        self.second_column = [
            TenseConjugation(ConiugazioneResult.TENSE_NAMES[i], t)
            for i, t in enumerate(tenses_html)
            if i % 2
        ]

    def to_html(self) -> str:
        """Convert to HTML to be displayed in the results page"""
        first_column_html = "\r\n".join([t.to_html() for t in self.first_column])
        second_column_html = "\r\n".join([t.to_html() for t in self.second_column])
        return f"""
        <div class="conjugation-column">{first_column_html}</div>
        <div class="conjugation-column">{second_column_html}</div>
        """
