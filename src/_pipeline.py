from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Getimg


class SyncAPIPipeline:
    _client: Getimg

    def __init__(self, client: Getimg):
        self._client = client
        self._get = client.get
        self._post = client.post

    def _prepare_options(self, options):
        return {key: value
                for key, value in options.items()
                if key != "self" and value is not None}

