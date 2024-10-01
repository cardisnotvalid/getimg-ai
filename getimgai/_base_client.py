from typing import TypeVar, Generic

import httpx


HttpxClientT = TypeVar("HttpxClientT", bound=[httpx.Client, httpx.AsyncClient])


class BaseClient(Generic[HttpxClientT]):
    def __init__(self, *, timeout=None):
        self._api_version = 1
        self._base_url = "https://api.getimg.ai/"
        self._timeout = httpx.Timeout(timeout if timeout is not None else 60)

    def _prepare_url(self, url):
        merge_url = httpx.URL(url)
        if merge_url.is_relative_url:
            merge_path = self.base_url.raw_path + merge_url.raw_path.lstrip(b"/")
            return self.base_url.copy_with(raw_path=merge_path)

        return merge_url

    def _prepare_options(self, options):
        pre_options = {}

        for key, value in options.items():
            if key != "self" and value is not None:
                pre_options[key] = value

        return pre_options

    def _build_request(self, method, path, *, params=None, json_data=None):
        url = self._prepare_url(path)

        if params is not None:
            params = self._prepare_options(params)
        if json_data is not None:
            json_data = self._prepare_options(json_data)

        prepped = self._client.build_request(
            method=method,
            url=url,
            headers=self.default_headers,
            params=params,
            json=json_data,
            timeout=self._timeout
        )
        return prepped

    @property
    def api_version(self):
        return f"v{self._api_version}/"

    @property
    def base_url(self):
        return httpx.URL(self._base_url + self.api_version)

    @property
    def auth_headers(self):
        return {}

    @property
    def default_headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            **self.auth_headers
        }


class SyncAPIClient(BaseClient[httpx.Client]):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        self._client = httpx.Client(base_url=self.base_url)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        if hasattr(self, "_client"):
            self._client.close()

    def request(self, method, path, *, params=None, json_data=None):
        prepped = self._build_request(
            method,
            path,
            params=params,
            json_data=json_data
        )
        response_data = self._client.send(prepped).json()
        if error := response_data.get("error"):
            err_type = error["type"]
            err_code = error["code"]
            err_msg = error["message"]
            raise NotImplementedError(f"{err_type} ({err_code}): {err_msg}")
        return response_data

    def get(self, path, *, params=None):
        return self.request("GET", path, params=params)

    def post(self, path, *, params=None, json_data=None):
        return self.request("POST", path, params=params, json_data=json_data)
