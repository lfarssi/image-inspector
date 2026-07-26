def convert_to_degrees(value):
    """Convert EXIF GPS tuple (degrees, minutes, seconds) to decimal degrees."""
    try:
        def val(x):
            return float(x[0]) / float(x[1]) if isinstance(x, (tuple, list)) else float(x)
        return val(value[0]) + val(value[1]) / 60.0 + val(value[2]) / 3600.0
    except Exception:
        return None

def save_output(content: str, filename: str):
    """Save content to output file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Data saved in {filename}")
    except Exception as e:
        print(f"Error saving file {filename}: {e}")


