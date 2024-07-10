from typing import TypeVar, Generic, Optional, Union, Dict, Any

import httpx
from httpx import URL, Timeout, Response, Request

from ._constants import DEFAULT_TIMEOUT


HttpxClientT = TypeVar("HttpxClientT", bound=[httpx.Client, httpx.AsyncClient])


class BaseClient(Generic[HttpxClientT]):
    _client: HttpxClientT
    _base_url: URL
    _timeout: Optional[Union[float, Timeout]]
    _custom_headers: Dict[str, str]

    def __init__(
        self, 
        *,
        base_url: Union[str, URL],
        timeout: Optional[Union[float, Timeout]] = None,
        custom_headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._base_url = URL(base_url) if isinstance(base_url, str) else base_url
        self._timeout = timeout or DEFAULT_TIMEOUT
        self._custom_headers = custom_headers or {}

    def _build_request(self, method: str, url: str, **kwargs) -> Request:
        return self._client.build_request(
            method=method,
            url=url,
            headers=self.default_headers,
            **kwargs,
        )

    def _build_payload(
        self,
        options: Dict[str, Any],
        *,
        custom_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        payload = {}

        if custom_options:
            payload.update(custom_options)

        for key, value in options.items():
            if key != "self" and value is not None:
                payload[key] = value

        return payload

    @property
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    def base_url(self, url: Union[str, URL]) -> None:
        self._base_url = URL(url) if isinstance(url ,str) else url

    @property
    def auth_headers(self) -> Dict[str, str]:
        return {}

    @property
    def default_headers(self) -> Dict[str, str]:
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
        base_url: Union[str, URL],
        timeout: Optional[Union[float, Timeout]] = None,
        custom_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
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

    def __enter__(self) -> "SyncAPIClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def close(self) -> None:
        if hasattr(self, "_client"):
            self._client.close()

    def get(self, path: Union[str, URL], **kwargs) -> Response:
        request = self._build_request("GET", path, **kwargs)
        return self._client.send(request)

    def post(self, path: Union[str, URL], **kwargs) -> Response:
        request = self._build_request("POST", path, **kwargs)
        return self._client.send(request)

