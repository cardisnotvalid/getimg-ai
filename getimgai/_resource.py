class SyncAPIResource:
    def __init__(self, client):
        self._client = client
        self._get = client.get
        self._post = client.post
