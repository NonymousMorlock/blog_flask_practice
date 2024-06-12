from typing import Any


class Response:
    def __init__(
            self,
            data: Any = None,
            redirect_url: str | None = None,
            error_message: str | None = None,
            error_category: str | None = None
    ):
        self.data = data
        self.redirect_url = redirect_url
        self.error_message = error_message
        self.error_category = error_category
