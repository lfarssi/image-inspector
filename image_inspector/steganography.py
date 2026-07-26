import numpy as np
from PIL import Image

PGP_MARKERS = [
    "-----BEGIN PGP PUBLIC KEY BLOCK-----",
    "-----BEGIN PGP PRIVATE KEY BLOCK-----",
    "-----BEGIN PGP MESSAGE-----",
    "-----BEGIN PGP ARMORED FILE-----"
]

def extract_steganography(image_path: str) -> dict:
    """Extract hidden LSB steganography payload from image."""
    result = {"found": False, "payload": "No hidden data found."}

    try:
        img = Image.open(image_path).convert("RGB")
        lsb = (np.array(img) & 1).reshape(-1)
        text = np.packbits(lsb).tobytes().decode("utf-8", errors="ignore")

        for marker in PGP_MARKERS:
            if marker in text:
                start = text.find(marker)
                end_marker = marker.replace("BEGIN", "END")
                end = text.find(end_marker, start)
                if end != -1:
                    result["payload"] = text[start:end + len(end_marker)]
                else:
                    result["payload"] = text[start:start + 4096]
                result["found"] = True
                break
    except Exception as e:
        result["payload"] = f"Error opening image: {e}"

    return result


