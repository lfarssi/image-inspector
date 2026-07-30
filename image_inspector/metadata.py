from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from .utils import convert_to_degrees

def extract_metadata(image_path: str) -> dict:
    """Extract EXIF metadata (GPS, camera device, date) from image."""
    result = {"lat_lon_str": None, "device": None, "date": None, "has_metadata": False}
    try:
        exif = Image.open(image_path)._getexif() or {}
    except Exception:
        return result

    data = {TAGS.get(k, k): v for k, v in exif.items()}
    gps = {GPSTAGS.get(k, k): v for k, v in data.get("GPSInfo", {}).items()}

    # Geolocation
    if "GPSLatitude" in gps and "GPSLatitudeRef" in gps:
        lat = convert_to_degrees(gps["GPSLatitude"])
        lon = convert_to_degrees(gps.get("GPSLongitude"))
        if lat is not None and lon is not None:
            if str(gps["GPSLatitudeRef"]).upper() == "S": lat = -lat
            if str(gps.get("GPSLongitudeRef", "")).upper() == "W": lon = -lon
            lat_str = f"{lat:.4f}".rstrip('0').rstrip('.')
            lon_str = f"{lon:.4f}".rstrip('0').rstrip('.')
            result["lat_lon_str"] = f"Lat/Lon: ({lat_str}) / ({lon_str})"

    # Device
    make = str(data.get("Make", "")).strip()
    model = str(data.get("Model", "")).strip()
    if make or model:
        dev = model if model.lower().startswith(make.lower()) else f"{make} {model}".strip()
        result["device"] = f"Device: {dev}"

    # Date
    date_val = data.get("DateTimeOriginal") or data.get("DateTime")
    if date_val and isinstance(date_val, str):
        parts = date_val.strip().split(" ")
        date_str = f"{parts[0].replace(':', '-')} {parts[1]}" if len(parts) == 2 else date_val
        result["date"] = f"Date: {date_str}"

    return result

def format_metadata_report(meta_dict: dict) -> str:
    """Format metadata dictionary into report string, showing 'Not found' for missing fields."""
    lat_lon = meta_dict.get("lat_lon_str") or "Lat/Lon: Not found"
    device = meta_dict.get("device") or "Device: Not found"
    date = meta_dict.get("date") or "Date: Not found"
    return f"{lat_lon}\n{device}\n{date}"


