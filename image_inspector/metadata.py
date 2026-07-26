from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from .utils import convert_to_degrees

def extract_metadata(image_path: str) -> dict:
    """Extract key EXIF metadata from an image."""
    result = {"lat_lon_str": None, "device": None, "date": None, "has_metadata": False}

    try:
        img = Image.open(image_path)
        exif = img._getexif()
    except Exception:
        return result

    if not exif:
        return result

    parsed_exif = {}
    gps_info = {}
    for tag_id, value in exif.items():
        tag_name = TAGS.get(tag_id, tag_id)
        if tag_name == "GPSInfo":
            for g_id in value:
                gps_info[GPSTAGS.get(g_id, g_id)] = value[g_id]
        else:
            parsed_exif[tag_name] = value

    # Geolocation
    if "GPSLatitude" in gps_info and "GPSLatitudeRef" in gps_info:
        lat = convert_to_degrees(gps_info["GPSLatitude"])
        lon = convert_to_degrees(gps_info.get("GPSLongitude", (0, 0, 0)))
        if lat is not None and lon is not None:
            if str(gps_info["GPSLatitudeRef"]).strip().upper() == "S":
                lat = -lat
            if str(gps_info.get("GPSLongitudeRef", "")).strip().upper() == "W":
                lon = -lon
            lat_str = f"{lat:.4f}".rstrip('0').rstrip('.')
            lon_str = f"{lon:.4f}".rstrip('0').rstrip('.')
            result["lat_lon_str"] = f"Lat/Lon: ({lat_str}) / ({lon_str})"
            result["has_metadata"] = True

    # Device
    make = str(parsed_exif.get("Make", "")).strip()
    model = str(parsed_exif.get("Model", "")).strip()
    if make and model:
        device = model if model.lower().startswith(make.lower()) else f"{make} {model}"
    else:
        device = make or model

    if device:
        result["device"] = f"Device: {device}"
        result["has_metadata"] = True

    # Date
    date_val = parsed_exif.get("DateTimeOriginal") or parsed_exif.get("DateTimeDigitized") or parsed_exif.get("DateTime")
    if date_val and isinstance(date_val, str):
        parts = date_val.strip().split(" ")
        date_str = f"{parts[0].replace(':', '-')} {parts[1]}" if len(parts) == 2 else date_val
        result["date"] = f"Date: {date_str}"
        result["has_metadata"] = True

    return result

def format_metadata_report(meta_dict: dict) -> str:
    """Format metadata dictionary into report string."""
    lines = [meta_dict[k] for k in ("lat_lon_str", "device", "date") if meta_dict.get(k)]
    return "\n".join(lines) if lines else "No metadata found."

