from typing import Optional

from .._pipeline import SyncAPIPipeline


class Instruct(SyncAPIPipeline):
    def stable_diffusion(
        self,
        prompt: str,
        image: str,
        *,
        model: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        image_guidance: str | None = None,
        steps: int | None = None,
        guidance: float | None = None,
        seed: Optional[int] = None,
        scheduler: Optional[str] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        return self._post(
            "/stable-diffusion/instruct",
            json=self._prepare_options(locals())
        )
