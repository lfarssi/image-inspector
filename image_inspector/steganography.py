import numpy as np
from PIL import Image

PGP_MARKERS = [
    "-----BEGIN PGP PUBLIC KEY BLOCK-----",
    "-----BEGIN PGP PRIVATE KEY BLOCK-----",
    "-----BEGIN PGP MESSAGE-----",
    "-----BEGIN PGP ARMORED FILE-----"
]

def _search_pgp(text: str) -> str | None:
    """Search text for a PGP block and return it if found."""
    for marker in PGP_MARKERS:
        if marker in text:
            start = text.find(marker)
            end_marker = marker.replace("BEGIN", "END")
            end = text.find(end_marker, start)
            if end != -1:
                return text[start:end + len(end_marker)]
            return text[start:start + 4096]
    return None

def extract_steganography(image_path: str) -> dict:
    """Extract hidden steganography payload from image."""
    result = {"found": False, "payload": "No hidden data found."}

    # 1. LSB extraction from pixel data
    try:
        img = Image.open(image_path).convert("RGB")
        lsb = (np.array(img) & 1).reshape(-1)
        text = np.packbits(lsb).tobytes().decode("utf-8", errors="ignore")
        payload = _search_pgp(text)
        if payload:
            result["found"] = True
            result["payload"] = payload
            return result
    except Exception:
        pass

    # 2. Data appended after JPEG EOF marker (0xFFD9)
    try:
        with open(image_path, "rb") as f:
            raw = f.read()
        eof = raw.rfind(b"\xff\xd9")
        if eof != -1 and eof + 2 < len(raw):
            tail = raw[eof + 2:]
            text = tail.decode("utf-8", errors="ignore")
            payload = _search_pgp(text)
            if payload:
                result["found"] = True
                result["payload"] = payload
                return result
    except Exception:
        pass

    return result




