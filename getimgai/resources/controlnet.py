from typing import Optional

from .._resource import SyncAPIResource


class ControlNet(SyncAPIResource):
    def stable_diffusion(
        self,
        prompt: str,
        image: str,
        controlnet: str,
        *,
        model: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        strength: Optional[float] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        steps: Optional[int] = None,
        guidance: Optional[float] = None,
        seed: Optional[int] = None,
        scheduler: Optional[str] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        return self._post("stable-diffusion/controlnet", json_data=locals())
