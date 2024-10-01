from .._resource import SyncAPIResource


class Models(SyncAPIResource):
    def get_models(self, family=None, pipeline=None):
        return self._get("models", params=locals())

    def get_model(self, model_id):
        return self._get(f"models/{model_id}")
