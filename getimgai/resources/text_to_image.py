from typing import Optional

from .._resource import SyncAPIResource


class TextToImage(SyncAPIResource):
    def essential_v2(
        self,
        prompt: str,
        *,
        style: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        payload = self.build_payload(locals())
        return self._post("/v1/essential-v2/text-to-image", json=payload)

    def stable_diffusion_xl(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        prompt_2: Optional[str] = None,
        negative_prompt_2: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        steps: Optional[int] = None,
        guidance: Optional[float] = None,
        seed: Optional[int] = None,
        scheduler: Optional[str] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        payload = self.build_payload(locals())
        return self._post("/v1/stable-diffusion-xl/text-to-image", json=payload)

    def stable_diffusion(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        steps: Optional[int] = None,
        guidance: Optional[float] = None,
        seed: Optional[int] = None,
        scheduler: Optional[str] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        payload = self.build_payload(locals())
        return self._post("/v1/stable-diffusion/text-to-image", json=payload)

    def latent_consistency(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        steps: Optional[int] = None,
        seed: Optional[int] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        payload = self.build_payload(locals())
        return self._post("/v1/latent-consistency/text-to-image", json=payload)

