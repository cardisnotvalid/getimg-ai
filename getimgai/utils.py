from typing import Optional

import base64

from ._paths import PATH_API_KEY


def _save_api_key(api_key: str) -> None:
    PATH_API_KEY.write_text(api_key)


def _load_api_key() -> Optional[str]:
    if PATH_API_KEY.is_file():
        return PATH_API_KEY.read_text().strip()
    return None


def save_image(image_b64: str, file_path: str = "image.png") -> None:
    image_bytes = base64.decodebytes(image_b64.encode())

    with open(file_path, "wb") as f:
        f.write(image_bytes)


def load_image(file_path: str) -> str:
    with open(file_path, "rb") as f:
        image_bytes = f.read()

    image_b64 = base64.encodebytes(image_bytes)
    return image_b64
