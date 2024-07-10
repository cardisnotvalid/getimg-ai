from typing import Optional

from .._resource import SyncAPIResource


class Models(SyncAPIResource):
    def get_models(self, *, family: Optional[str] = None, pipeline: Optional[str] = None):
        payload = self.build_payload(locals())
        return self._get("/v1/models", params=payload)

    def get_model(self, model_id: str):
        return self._get(f"/v1/models/{model_id}")


