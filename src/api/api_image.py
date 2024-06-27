from typing import Dict, Optional, Tuple, Union

import requests

from .api_utils import validate_response
from ..paths import PATH_API_KEY

BASE_URL = "https://api.getimg.ai/v1/%s/%s"


class BaseImageGenerator:
    def _get_payload(self) -> Dict[str, Optional[Union[str, float, int]]]:
        return {
            key: value
            for key, value in list(self.__dict__.items())[3:]
            if value is not None
        }

    def _get_headers(self) -> Dict[str, str]:
        api_key = PATH_API_KEY.read_text()
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {api_key}",
        }

    def generate_image(self) -> Tuple[str, str]:
        payload = self._get_payload()
        headers = self._get_headers()

        # print(f"[{self.family} | {self.pipeline}] Processing image")
        if payload.get("image", None):
            temp_payload = payload.copy()
            temp_payload.__delitem__("image")
            print(temp_payload)
        else:
            print(payload)

        response = requests.post(self.url, json=payload, headers=headers)
        data = response.json()
        validate_response(data)
        return data


class TextToImage(BaseImageGenerator):
    def __init__(
        self,
        prompt: str,
        model: str = "dream-shaper-v8",
        family: str = "stable-diffusion",
        pipeline: str = "text-to-image",
        negative_prompt: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        steps: Optional[int] = None,
        guidance: Optional[float] = None,
        seed: Optional[int] = None,
        scheduler: Optional[str] = None,
        output_format: Optional[str] = None,
        response_format: Optional[str] = None,
    ) -> None:
        self.family = family
        self.pipeline = pipeline
        self.url = BASE_URL % (family, pipeline)
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.model = model
        self.width = width
        self.height = height
        self.steps = steps
        self.guidance = guidance
        self.seed = seed
        self.scheduler = scheduler
        self.output_format = output_format
        self.response_format = response_format
