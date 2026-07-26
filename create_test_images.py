import numpy as np
from PIL import Image
from PIL.TiffImagePlugin import IFDRational

def create_pgp_key_bits(pgp_key_text: str) -> list[int]:
    key_bytes = pgp_key_text.encode('utf-8')
    bits = []
    for b in key_bytes:
        for i in range(7, -1, -1):
            bits.append((b >> i) & 1)
    return bits

def embed_lsb(image_array: np.ndarray, bits: list[int]) -> np.ndarray:
    arr = image_array.copy()
    flat_arr = arr.reshape(-1)
    for i, bit in enumerate(bits):
        flat_arr[i] = np.uint8((int(flat_arr[i]) & 0xFE) | bit)
    return flat_arr.reshape(arr.shape)

def generate_test_images():
    pgp_key_1 = """-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: 01

mQENBF/x876BHAD8921JkLz0912KksmLqA00912zXmQ541189...
-----END PGP PUBLIC KEY BLOCK-----"""

    pgp_key_3 = """-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: 02

mQENBF/y987CAD9032KlMz1023LltnMrB11023yYnR652290...
-----END PGP PUBLIC KEY BLOCK-----"""

    # Image 1: Metadata + Steganography (matches usage example in prompt)
    exif1 = Image.Exif()
    exif1[0x010F] = "Canon"
    exif1[0x0110] = "Canon EOS 5D Mark III"
    exif1[0x9003] = "2023:07:20 14:32:10"
    gps1 = exif1.get_ifd(0x8825)
    gps1[1] = 'N'
    gps1[2] = (IFDRational(13, 1), IFDRational(43, 1), IFDRational(516, 10)) # 13.731 N
    gps1[3] = 'W'
    gps1[4] = (IFDRational(1, 1), IFDRational(8, 1), IFDRational(1428, 100)) # 1.1373 W

    base_img1 = Image.new('RGB', (250, 250), color=(120, 140, 180))
    arr1 = np.array(base_img1, dtype=np.uint8)
    steg_arr1 = embed_lsb(arr1, create_pgp_key_bits(pgp_key_1))
    img1 = Image.fromarray(steg_arr1)
    img1.save('image-example1.jpeg', format='PNG', exif=exif1)
    print("Created image-example1.jpeg (Metadata + Steganography)")

    # Image 2: Metadata only
    exif2 = Image.Exif()
    exif2[0x010F] = "Nikon"
    exif2[0x0110] = "Nikon D850"
    exif2[0x9003] = "2024:01:15 09:15:00"
    gps2 = exif2.get_ifd(0x8825)
    gps2[1] = 'N'
    gps2[2] = (IFDRational(37, 1), IFDRational(46, 1), IFDRational(2964, 100)) # 37.7749 N
    gps2[3] = 'W'
    gps2[4] = (IFDRational(122, 1), IFDRational(25, 1), IFDRational(984, 100)) # 122.4194 W

    img2 = Image.new('RGB', (250, 250), color=(180, 120, 140))
    img2.save('image-example2.jpeg', format='PNG', exif=exif2)
    print("Created image-example2.jpeg (Metadata only)")

    # Image 3: Steganography only (no EXIF metadata)
    base_img3 = Image.new('RGB', (250, 250), color=(140, 180, 120))
    arr3 = np.array(base_img3, dtype=np.uint8)
    steg_arr3 = embed_lsb(arr3, create_pgp_key_bits(pgp_key_3))
    img3 = Image.fromarray(steg_arr3)
    img3.save('image-example3.jpeg', format='PNG')
    print("Created image-example3.jpeg (Steganography only)")

    # Image 4: Clean image (no metadata, no steganography)
    img4 = Image.new('RGB', (250, 250), color=(200, 200, 200))
    img4.save('image-example4.jpeg', format='PNG')
    print("Created image-example4.jpeg (Clean image - no metadata/steg)")

if __name__ == "__main__":
    generate_test_images()
