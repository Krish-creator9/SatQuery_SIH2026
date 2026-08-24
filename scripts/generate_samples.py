"""
SatQuery AI — Synthetic Sample Satellite Data Generator (Pure Python)

Generates BMP mock satellite images without external dependencies.
"""

import os
import struct
import random

def write_bmp(filepath, width, height, pixels):
    """Write RGB image to 24-bit BMP file using pure Python."""
    row_bytes = width * 3
    padding = (4 - (row_bytes % 4)) % 4
    image_size = (row_bytes + padding) * height
    file_size = 54 + image_size

    # BMP Header
    bmp_header = struct.pack('<2sIHHI', b'BM', file_size, 0, 0, 54)
    # DIB Header
    dib_header = struct.pack('<IIIHHIIIIII', 40, width, height, 1, 24, 0, image_size, 2835, 2835, 0, 0)

    with open(filepath, 'wb') as f:
        f.write(bmp_header)
        f.write(dib_header)
        # BMP rows are stored bottom-to-top
        for y in range(height - 1, -1, -1):
            row_data = bytearray()
            for x in range(width):
                r, g, b = pixels[y][x]
                # BMP stores in BGR order
                row_data.extend([b, g, r])
            row_data.extend(b'\x00' * padding)
            f.write(row_data)

def generate_sample_images():
    samples_dir = os.path.join(os.path.dirname(__file__), "..", "data", "samples")
    os.makedirs(samples_dir, exist_ok=True)
    
    random.seed(42)
    width, height = 512, 512

    # 1. Optical Baseline (2020)
    pixels_a = []
    for y in range(height):
        row = []
        for x in range(width):
            if y >= 250:
                # Water
                r, g, b = 20, 45, 85
            elif 50 <= y <= 180 and 50 <= x <= 200:
                # Green vegetation
                r, g, b = 35, 75, 40
            elif (120 <= y <= 130) or (300 <= x <= 310):
                # Road
                r, g, b = 180, 185, 190
            else:
                # Bare land
                r, g, b = 60, 65, 70
            
            # Subtle noise
            noise = random.randint(-10, 10)
            r = max(0, min(255, r + noise))
            g = max(0, min(255, g + noise))
            b = max(0, min(255, b + noise))
            row.append((r, g, b))
        pixels_a.append(row)

    write_bmp(os.path.join(samples_dir, "optical_2020_baseline.bmp"), width, height, pixels_a)

    # 2. Optical Target (2024) with new structures
    pixels_b = []
    for y in range(height):
        row = []
        for x in range(width):
            base_r, base_g, base_b = pixels_a[y][x]
            if 60 <= y <= 150 and 320 <= x <= 450:
                # New industrial warehouse (bright reflective roofs)
                r, g, b = 220, 220, 230
            elif 250 <= y <= 350 and 280 <= x <= 330:
                # New dock into water
                r, g, b = 170, 175, 180
            else:
                r, g, b = base_r, base_g, base_b
            
            noise = random.randint(-8, 8)
            r = max(0, min(255, r + noise))
            g = max(0, min(255, g + noise))
            b = max(0, min(255, b + noise))
            row.append((r, g, b))
        pixels_b.append(row)

    write_bmp(os.path.join(samples_dir, "optical_2024_target.bmp"), width, height, pixels_b)

    # 3. SAR Backscatter
    pixels_sar = []
    for y in range(height):
        row = []
        for x in range(width):
            if y >= 250:
                val = 25  # Water dark
            elif (60 <= y <= 150 and 320 <= x <= 450) or (250 <= y <= 350 and 280 <= x <= 330):
                val = 240 # Double bounce structure
            else:
                val = 110 # Land
            
            noise = int(random.expovariate(0.08))
            val = max(0, min(255, val + noise))
            row.append((val, val, val))
        pixels_sar.append(row)

    write_bmp(os.path.join(samples_dir, "sar_cband_backscatter.bmp"), width, height, pixels_sar)

    print(f"Generated sample datasets in: {os.path.abspath(samples_dir)}")

if __name__ == "__main__":
    generate_sample_images()
