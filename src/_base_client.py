from typing import TypeVar, Generic, Mapping

import httpx
from httpx import URL, Timeout, Response

from ._constants import DEFAULT_TIMEOUT

HttpxClientT = TypeVar("HttpxClientT", bound=[httpx.Client, httpx.AsyncClient])


class BaseClient(Generic[HttpxClientT]):
    _client: HttpxClientT
    _base_url: URL
    timeout: float | Timeout | None
    _custom_headers: Mapping[str, str]

    def __init__(
        self, 
        *,
        base_url: str | URL,
        timeout: float | Timeout | None = None,
        custom_headers: Mapping[str, str] | None = None,
    ) -> None:
        self._base_url = URL(base_url)
        self.timeout = timeout or DEFAULT_TIMEOUT
        self._custom_headers = custom_headers or {}

    def _build_request(
        self,
        method: str,
        path: str,
        **kwargs,
    ) -> httpx.Request:
        headers = self.default_headers
        return self._client.build_request(
            method=method,
            url=path,
            headers=headers,
            **kwargs,
        )

    def _make_payload(
        self,
        options: Mapping[str, object]
    ) -> Mapping[str, object]:
        return {
            key: value
            for key, value in options.items()
            if key != "self" and value is not None
        }


    @property
    def auth_headers(self) -> dict[str, str]:
        return {}

    @property
    def default_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            **self.auth_headers,
            **self._custom_headers
        }


class SyncAPIClient(BaseClient[httpx.Client]):
    _client: httpx.Client

    def __init__(
        self, 
        *,
        base_url: str | URL,
        timeout: float | Timeout | None = None,
        custom_headers: Mapping[str, str] | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            timeout=timeout,
            custom_headers=custom_headers
        )

        self._client = http_client or httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers=custom_headers
        )

    def close(self) -> None:
        if hasattr(self, "_client"):
            self._client.close()

    def __enter__(self) -> "SyncAPIClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def get(self, path: str | URL, **kwargs) -> Response:
        return self._client.send(self._build_request("GET", path, **kwargs))

    def post(self, path: str | URL, **kwargs) -> Response:
        return self._client.send(self._build_request("POST", path, **kwargs))

