import base64


def save_image(image_b64, file_path="image.png"):
    image_bytes = base64.decodebytes(image_b64.encode())
    with open(file_path, "wb") as f:
        f.write(image_bytes)


def load_image(file_path):
    with open(file_path, "rb") as f:
        image_bytes = f.read()
    image_b64 = base64.encodebytes(image_bytes)
    return image_b64
