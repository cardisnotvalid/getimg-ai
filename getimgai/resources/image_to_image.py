from typing import Optional

from .._resource import SyncAPIResource


class ImageToImage(SyncAPIResource):
    def stable_diffusion_xl(
        self,
        prompt: str,
        image: str,
        *,
        model: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        prompt_2: Optional[str] = None,
        negative_prompt_2: Optional[str] = None,
        strength: Optional[float] = None,
        steps: Optional[int] = None,
        guidance: Optional[float] = None,
        seed: Optional[int] = None,
        scheduler: Optional[str] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        return self._post("/v1/stable-diffusion-xl/image-to-image", json=locals())

    def stable_diffusion(
        self,
        prompt: str,
        *,
        image: str,
        model: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        strength: Optional[float] = None,
        steps: Optional[int] = None,
        guidance: Optional[float] = None,
        seed: Optional[int] = None,
        scheduler: Optional[str] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        return self._post("/v1/stable-diffusion/image-to-image", json=locals())

    def latent_consistency(
        self,
        prompt: str,
        image: str,
        *,
        model: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        strength: Optional[float] = None,
        steps: Optional[int] = None,
        seed: Optional[int] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        return self._post("/v1/latent-consistency/image-to-image", json=locals())
