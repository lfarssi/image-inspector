import numpy as np
from PIL import Image

PGP_MARKERS = [
    "-----BEGIN PGP PUBLIC KEY BLOCK-----",
    "-----BEGIN PGP PRIVATE KEY BLOCK-----",
    "-----BEGIN PGP MESSAGE-----",
    "-----BEGIN PGP ARMORED FILE-----"
]

def search_pgp(text: str) -> str | None:
    for marker in PGP_MARKERS:
        if marker in text:
            start = text.find(marker)
            end_marker = marker.replace("BEGIN", "END")
            end = text.find(end_marker, start)
            return text[start:end + len(end_marker)] if end != -1 else text[start:start + 4096]
    return None

def extract_steganography(image_path: str) -> dict:
    """Extract hidden LSB steganography payload from image."""
    result = {"found": False, "payload": "No hidden data found."}

    try:
        img = Image.open(image_path).convert("RGB")
        lsb = np.array(img) & 1

        candidates = [
            lsb.reshape(-1),
            lsb[:, :, 0].reshape(-1),
            lsb[:, :, 1].reshape(-1),
            lsb[:, :, 2].reshape(-1),
            np.transpose(lsb, (1, 0, 2)).reshape(-1)
        ]

        for bits in candidates:
            n = len(bits) // 8
            if n == 0:
                continue
            for order in ["big", "little"]:
                text = np.packbits(bits[:n * 8], bitorder=order).tobytes().decode("utf-8", errors="ignore")
                payload = search_pgp(text)
                if payload:
                    result["found"] = True
                    result["payload"] = payload
                    return result
    except Exception as e:
        result["payload"] = f"Error opening image: {e}"

    return result



