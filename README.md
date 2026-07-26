# Image Inspector 🔍

**Image Inspector** is a command-line digital forensics tool written in Python. It allows digital forensics investigators, security researchers, and privacy analysts to explore hidden layers of image files by extracting embedded EXIF metadata (GPS coordinates, camera device info, timestamps) and detecting concealed payloads (such as PGP public keys or text strings) embedded via Least Significant Bit (LSB) steganography techniques.

---

## 📋 Table of Contents
- [Features](#features)
- [Prerequisites & Installation](#prerequisites--installation)
- [Usage & Options](#usage--options)
- [Usage Examples](#usage-examples)
- [Generating Test Suite](#generating-test-suite)
- [Ethical & Legal Considerations](#ethical--legal-considerations)
- [Role-Play Audit Defense Guide (Digital Forensics Expert)](#role-play-audit-defense-guide-digital-forensics-expert)

---

## ✨ Features

- **EXIF Metadata Extraction (`-m`)**:
  - **Geolocation**: Converts EXIF GPS rational values (degrees, minutes, seconds) into standardized decimal Latitude and Longitude format.
  - **Device Information**: Identifies camera manufacturer and model (e.g. `Canon EOS 5D Mark III`).
  - **Timestamps**: Extracts photo creation/capture date and time (`YYYY-MM-DD HH:MM:SS`).
  - **Auxiliary Info**: Captures format, image dimensions, color mode, software used, and ISO/exposure settings.

- **LSB Steganography Detection (`-s`)**:
  - Scans Least Significant Bits across RGB pixel arrays.
  - Detects PGP Public/Private key blocks (`-----BEGIN PGP PUBLIC KEY BLOCK-----`, etc.).
  - Reconstructs concealed ASCII/UTF-8 byte streams across row-major and per-channel bit orderings.

- **Flexible Output Management (`-o`)**:
  - Displays formatted report to stdout.
  - Optionally saves analysis results into a specified output file.

- **Robust Error Handling**:
  - Gracefully handles images without EXIF metadata or hidden payloads without crashing.
  - Validates input file paths and provides clean user error messages.

---

## ⚙️ Prerequisites & Installation

### Requirements
- Python 3.10 or higher
- `Pillow` (PIL) >= 10.0.0
- `numpy` >= 1.20.0

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/lfarssi/image-inspector.git
   cd image-inspector
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Make the Tool Executable**:
   ```bash
   chmod +x image-inspector
   ```

---

## 🚀 Usage & Options

Run the executable directly from the project directory:

```bash
image-inspector [OPTIONS] <IMAGE_FILE>
```

### Help Menu Output

```bash
$> image-inspector --help

Welcome to Image Inspector

OPTIONS:
    -m  Metadata          Extract metadata from the image (e.g., geolocation, device info)
    -s  Steganography     Detect and extract hidden data from the image using steganography techniques
    -o  "FileName"        Specify the file name to save output
    --help                Display this help message
```

---

## 💻 Usage Examples

### 1. Metadata Extraction (`-m`)

Extract GPS location, camera model, and timestamp, saving the result to `metadata.txt`:

```bash
$> ./image-inspector -m -o metadata.txt image-example1.jpeg
Lat/Lon: (13.731) / (-1.1373)
Device: Canon EOS 5D Mark III
Date: 2023-07-20 14:32:10
Data saved in metadata.txt
```

### 2. Steganography Detection (`-s`)

Detect and extract a concealed PGP public key from an image, saving to `hidden_data.txt`:

```bash
$> ./image-inspector -s -o hidden_data.txt image-example1.jpeg
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: 01

mQENBF/x876BHAD8921JkLz0912KksmLqA00912zXmQ541189...
-----END PGP PUBLIC KEY BLOCK-----
Data saved in hidden_data.txt
```

### 3. Combined Analysis (`-m -s`)

Perform both metadata extraction and steganography detection simultaneously:

```bash
$> ./image-inspector -m -s -o results.txt image-example1.jpeg
Lat/Lon: (13.731) / (-1.1373)
Device: Canon EOS 5D Mark III
Date: 2023-07-20 14:32:10

-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: 01

mQENBF/x876BHAD8921JkLz0912KksmLqA00912zXmQ541189...
-----END PGP PUBLIC KEY BLOCK-----
Data saved in results.txt
```

### 4. Handling Clean Images (No Metadata or Hidden Data)

```bash
$> ./image-inspector -m -s image-example4.jpeg
No metadata found.

No hidden data found.
```

---

## 🧪 Generating Test Suite

The project includes a generator script to create 4 test images for verification:

```bash
python3 create_test_images.py
```

This creates:
- `image-example1.jpeg`: Image with EXIF metadata (Canon EOS 5D, Lat 13.731, Lon -1.1373) + embedded PGP key.
- `image-example2.jpeg`: Image with EXIF metadata only (Nikon D850, San Francisco GPS).
- `image-example3.jpeg`: Image with embedded PGP key only (no EXIF metadata).
- `image-example4.jpeg`: Clean image with no EXIF metadata and no steganography payload.

---

## ⚖️ Ethical & Legal Considerations

> [!WARNING]
> **Legal Disclaimer & Responsible Use Notice**

1. **Obtain Explicit Authorization**:
   Always obtain written permission before extracting or inspecting metadata and hidden data from images belonging to individuals, organizations, or third parties. Unauthorized analysis of media can violate privacy rights and local cybercrime statutes.

2. **Respect Data Privacy**:
   EXIF metadata often contains highly sensitive personal information, including exact physical coordinates (GPS), time of capture, and camera serial numbers. Treat extracted metadata as Personally Identifiable Information (PII) and handle, store, or delete it in compliance with applicable privacy regulations (such as GDPR, CCPA).

3. **Chain of Custody & Evidence Handling**:
   In digital forensics investigations, ensure that analysis tools do not alter original target files. `Image Inspector` performs read-only operations on target images to preserve cryptographic hash integrity.

4. **Educational & Defense Purpose**:
   This tool was developed strictly for educational and official digital forensics investigation purposes. The authors and institution assume no liability for unauthorized or illegal use of this software.

---

## 🎭 Role-Play Audit Defense Guide (Digital Forensics Expert)

During audits, you may be asked to act as a **Digital Forensics Expert** explaining this tool to stakeholders. Use the following structured answers for your evaluation:

### Q1: What is metadata in the context of digital images, and why is it important?
> **Answer**: Metadata ("data about data") in digital images refers to EXIF (Exchangeable Image File Format) headers automatically written by digital cameras and smartphones. It stores technical parameters such as GPS coordinates, capture date/time, camera make/model, aperture, and shutter speed. In digital forensics, metadata is crucial for establishing timelines, verifying photo authenticity, proving physical presence at a crime scene, and correlating evidence across multiple devices.

### Q2: How does steganography work, and what are its potential uses and risks?
> **Answer**: Steganography is the technique of concealing secret messages or data within an ordinary file (the cover object) so that an observer cannot tell the message exists. In LSB (Least Significant Bit) steganography, the least significant bit of each pixel color value (0–255) is modified to hold payload bits. Because changing the LSB alters pixel intensity by at most 1 unit, the human eye cannot perceive any visual degradation.
> - **Uses**: Secure communication in privacy-restricting environments, digital watermarking, copyright protection.
> - **Risks**: Exfiltration of stolen corporate data, malware payload concealment (stegware), or covert command-and-control (C2) channel communication by malicious actors.

### Q3: What challenges did you face while developing the Image Inspector tool, and how did you address them?
> **Answer**: Key technical challenges included:
> 1. **GPS Coordinate Parsing**: EXIF stores GPS coordinates as IFD Rational tuples of degrees, minutes, and seconds. I implemented a mathematical conversion function in `utils.py` to translate these tuples into standard signed decimal degrees while correctly evaluating North/South and East/West reference direction tags.
> 2. **LSB Bitstream Extraction**: Reconstructing hidden ASCII/PGP payloads required accounting for bit-ordering differences (MSB first vs. LSB first) and multi-channel traversal. I utilized NumPy arrays to perform vectorized bitwise operations (`arr & 1`) across pixel channels for fast payload recovery.
> 3. **Non-Destructive Parsing**: Ensured the tool operates in strict read-only mode to maintain evidentiary integrity.

### Q4: How can this tool be used in real-life digital forensics or cybersecurity scenarios?
> **Answer**:
> - **Incident Response & Threat Hunting**: Inspecting images attached to phishing emails or posted on compromised websites to detect covert C2 payloads or embedded cryptographic keys.
> - **Law Enforcement & Criminal Investigations**: Extracting geolocation data from photos uploaded by suspects or victims to identify exact incident locations.
> - **OSINT (Open Source Intelligence)**: Validating public images during investigative journalism or intelligence gathering to confirm where and when an image was taken.

### Q5: What ethical considerations should be taken into account when analyzing images for hidden data?
> **Answer**:
> - **Consent & Scope**: Ensuring investigative activities stay within authorized legal warrants or explicit client consent.
> - **Privacy Protection**: Redacting personal GPS data when publishing forensic reports to avoid inadvertent doxxing or privacy breaches.
> - **Chain of Custody**: Documenting tool hash integrity and ensuring analysis does not modify source evidence files.
