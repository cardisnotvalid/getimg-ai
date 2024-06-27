from typing import Optional

from .._pipeline import SyncAPIPipeline


class Enhancement(SyncAPIPipeline):
    def upscale(
        self,
        image: str,
        *,
        model: Optional[str] = None,
        scale: Optional[float] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        return self._post(
            "/enhancements/upscale",
            json=self._prepare_options(locals())
        )

    def fix_faces(
        self,
        image: str,
        *,
        model: Optional[str] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        return self._post(
            "enhancements/face-fix",
            json=self._prepare_options(locals())
        )
