import base64


def bytes_to_base64(img: bytes) -> str:
    return base64.b64encode(img).decode()
