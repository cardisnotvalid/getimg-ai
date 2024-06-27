from typing import Optional

from .._pipeline import SyncAPIPipeline


class Models(SyncAPIPipeline):
    def get_all(
        self, 
        *,
        family: Optional[str] = None,
        pipeline: Optional[str] = None
    ):
        return self._get(
            "/models", 
            params=self._prepare_options(locals()))

    def get(self, model_id: str):
        return self._get(f"/models/{model_id}")


