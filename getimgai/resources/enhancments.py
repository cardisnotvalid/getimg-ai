from typing import Optional

from .._resource import SyncAPIResource


class Enhancement(SyncAPIResource):
    def upscale(
        self,
        image: str,
        *,
        model: Optional[str] = None,
        scale: Optional[float] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        return self._post("enhancements/upscale", json_data=locals())

    def fix_faces(
        self,
        image: str,
        *,
        model: Optional[str] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        return self._post("enhancements/face-fix", json_data=locals())
