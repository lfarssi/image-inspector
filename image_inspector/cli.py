import sys
import os
import argparse
from .metadata import extract_metadata, format_metadata_report
from .steganography import extract_steganography
from .utils import save_output

HELP_TEXT = """Welcome to Image Inspector

OPTIONS:
    -m  Metadata          Extract metadata from the image (e.g., geolocation, device info)
    -s  Steganography     Detect and extract hidden data from the image using steganography techniques
    -o  "FileName"        Specify the file name to save output
    --help                Display this help message"""

def print_help():
    print(HELP_TEXT)

def main():
    if len(sys.argv) == 1 or "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        sys.exit(0)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-m", "--metadata", action="store_true")
    parser.add_argument("-s", "--steganography", action="store_true")
    parser.add_argument("-o", "--output", type=str)
    parser.add_argument("image", nargs="?", type=str)

    try:
        args, unknown = parser.parse_known_args()
    except Exception:
        print_help()
        sys.exit(1)

    if not args.image and unknown:
        for item in unknown:
            if not item.startswith("-"):
                args.image = item
                break

    if not args.image:
        print_help()
        sys.exit(1)

    if not os.path.exists(args.image):
        print(f"Error: Image file '{args.image}' not found.")
        sys.exit(1)

    run_meta = args.metadata
    run_steg = args.steganography
    if not run_meta and not run_steg:
        run_meta = True
        run_steg = True

    sections = []
    if run_meta:
        sections.append(format_metadata_report(extract_metadata(args.image)))
    if run_steg:
        sections.append(extract_steganography(args.image)["payload"])

    final_output = "\n\n".join(sections).strip()
    print(final_output)

    if args.output:
        save_output(final_output, args.output)

if __name__ == "__main__":
    main()

