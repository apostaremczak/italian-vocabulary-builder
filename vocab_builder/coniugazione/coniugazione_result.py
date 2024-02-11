from vocab_builder.api_result import ApiResult


class ConiugazioneResult(ApiResult):
    def __init__(self, tenses_html: list[str]):
        self.tenses = tenses_html
        self.first_column = [t for i, t in enumerate(tenses_html) if not i % 2]
        self.second_column = [t for i, t in enumerate(tenses_html) if i % 2]

    def to_html(self) -> str:
        first_column_html = "\r\n".join(self.first_column)
        second_column_html = "\r\n".join(self.second_column)
        return f"""
        <div class="conjugation-column">{first_column_html}</div>
        <div class="conjugation-column">{second_column_html}</div>
        """
