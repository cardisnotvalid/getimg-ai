from typing import Union, List

from .._resource import SyncAPIResource
from ..models.models import Model


class Models(SyncAPIResource):
    def get_models(self, *, family: Union[str, None] = None, pipeline: Union[str, None] = None):
        return self._get("/v1/models", params=locals()).json()

    def get_model(self, model_id: str):
        return self._get(f"/v1/models/{model_id}").json()


