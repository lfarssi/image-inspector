def convert_to_degrees(value):
    """Convert EXIF GPS (degrees, minutes, seconds) to decimal degrees."""
    try:
        def to_float(x):
            if hasattr(x, 'numerator') and hasattr(x, 'denominator'):
                return float(x.numerator) / float(x.denominator) if x.denominator != 0 else float(x)
            if isinstance(x, (tuple, list)) and len(x) == 2:
                return float(x[0]) / float(x[1]) if x[1] != 0 else float(x[0])
            return float(x)

        d, m, s = to_float(value[0]), to_float(value[1]), to_float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    except Exception:
        return None

def save_output(content: str, filename: str):
    """Save text content to file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Data saved in {filename}")
    except Exception as e:
        print(f"Error saving file {filename}: {e}")

