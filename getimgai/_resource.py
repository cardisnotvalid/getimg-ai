from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from .client import GetimgAI


class SyncAPIResource:
    _client: GetimgAI

    def __init__(self, client: GetimgAI) -> None:
        self._client = client
        self._get = client.get
        self._post = client.post

