from typing import TypeVar, Generic, Optional, Dict, Any

import httpx
from httpx import URL, Timeout, Response, Request

from ._constants import DEFAULT_TIMEOUT


HttpxClientT = TypeVar("HttpxClientT", bound=[httpx.Client, httpx.AsyncClient])


class BaseClient(Generic[HttpxClientT]):
    _client: HttpxClientT
    timeout: Timeout

    def __init__(self, *, timeout: Optional[float] = None) -> None:
        self.base_url = URL("https://api.getimg.ai")
        self.timeout = Timeout(timeout) or DEFAULT_TIMEOUT

    def _prepare_options(
        self,
        options: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        if options:
            post_params = {}
            for key, value in options.items():
                if key != "self" and value is not None:
                    post_params[key] = value
            return post_params
        return None

    def _build_request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Request:
        return self._client.build_request(
            method=method,
            url=url,
            headers=self.default_headers,
            params=self._prepare_options(params),
            json=self._prepare_options(payload),
            timeout=self.timeout,
        )

    @property
    def auth_headers(self) -> Dict[str, str]:
        return {}

    @property
    def default_headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            **self.auth_headers,
        }


class SyncAPIClient(BaseClient[httpx.Client]):
    _client: httpx.Client

    def __init__(self, *, timeout: Optional[float] = None) -> None:
        super().__init__(timeout=timeout)

        self._client = httpx.Client(base_url=self.base_url)

    def __enter__(self) -> "SyncAPIClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def close(self) -> None:
        if hasattr(self, "_client"):
            self._client.close()

    def get(
        self,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Response:
        return self._request("GET", url, params=params, payload=payload)

    def post(
        self,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Response:
        return self._request("POST", url, params=params, payload=payload)

    def _request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Response:
        request = self._build_request(method, url, params=params, payload=payload)
        return self._client.send(request)
