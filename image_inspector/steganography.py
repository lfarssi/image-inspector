import numpy as np
from PIL import Image

PGP_MARKERS = [
    "-----BEGIN PGP PUBLIC KEY BLOCK-----",
    "-----BEGIN PGP PRIVATE KEY BLOCK-----",
    "-----BEGIN PGP MESSAGE-----",
    "-----BEGIN PGP ARMORED FILE-----"
]

def bits_to_bytes(bits: np.ndarray) -> bytes:
    """Convert 1D array of 0s and 1s into bytes (MSB first)."""
    n_bytes = len(bits) // 8
    if n_bytes == 0:
        return b""
    truncated = bits[:n_bytes * 8].reshape((n_bytes, 8))
    weights = np.array([128, 64, 32, 16, 8, 4, 2, 1], dtype=np.uint8)
    return np.dot(truncated, weights).astype(np.uint8).tobytes()

def search_pgp(decoded_bytes: bytes) -> str | None:
    """Search decoded bytes for PGP blocks."""
    try:
        text = decoded_bytes.decode("utf-8", errors="ignore")
    except Exception:
        text = decoded_bytes.decode("latin-1", errors="ignore")

    for marker in PGP_MARKERS:
        if marker in text:
            start_idx = text.find(marker)
            end_marker = marker.replace("BEGIN", "END")
            end_idx = text.find(end_marker, start_idx)
            if end_idx != -1:
                return text[start_idx:end_idx + len(end_marker)]
            return text[start_idx:start_idx + 4096]
    return None

def extract_steganography(image_path: str) -> dict:
    """Extract hidden LSB steganography data from image."""
    result = {"found": False, "payload": "No hidden data found."}

    try:
        img = Image.open(image_path).convert("RGB")
    except Exception as e:
        result["payload"] = f"Error opening image: {e}"
        return result

    lsb_arr = np.array(img) & 1

    # Check primary sequential RGB bits
    payload = search_pgp(bits_to_bytes(lsb_arr.reshape(-1)))
    if payload:
        result["found"] = True
        result["payload"] = payload
        return result

    # Check individual channels
    for c in range(3):
        payload = search_pgp(bits_to_bytes(lsb_arr[:, :, c].reshape(-1)))
        if payload:
            result["found"] = True
            result["payload"] = payload
            return result

    return result

