from typing import Union, Literal

import httpx


class APIStatusError(Exception):
    response: httpx.Response
    status_code: int

    def __init__(
        message: str,
        *,
        response: HttpxResponse,
        body: Union[object, None] = None
    ):
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code


class APIBadRequest(APIStatusError):
    """Invalid request parameter."""

    status_code: Literal[400] = 400


class APIUnauthorized(APIStatusError):
    """Invalid API Key provided."""

    status_code: Literal[401] = 401


class APIPaymentRequired(APIStatusError):
    """Quota exceeded"""

    status_code: Literal[402] = 402


class APITooManyRequests(APIStatusError):
    """Too many requests hit the API too quickly."""

    status_code: Literal[429] = 429


class APINotFound(APIStatusError):
    """The resource doesn't exist."""

    status_code: Literal[404] = 404


class APIServerError(APIStatusError):
    """Something went wrong on our end."""

    status_code: Literal[500] = 500


class TempMailError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MailNotFound(TempMailError):
    """No verification message."""


__all__ = [
    "APIBadRequest",
    "APIUnauthorized",
    "APIPaymentRequired",
    "APITooManyRequests",
    "APINotFound",
    "APIServerError",
]

