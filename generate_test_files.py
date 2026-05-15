"""
Run this once to generate sample test images and audio for manual testing.
Output goes to the test_files/ folder.

Usage:
    python generate_test_files.py
"""

import os
import struct
import wave

from PIL import Image, ImageDraw, ImageFont

OUT = "test_files"
os.makedirs(OUT, exist_ok=True)


def _font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()


# ---------------------------------------------------------------------------
# 1. Medicine label
# ---------------------------------------------------------------------------
def make_medicine_label():
    w, h = 600, 400
    img = Image.new("RGB", (w, h), color=(240, 248, 255))
    d = ImageDraw.Draw(img)

    d.rectangle([10, 10, w - 10, h - 10], outline=(0, 80, 160), width=3)
    d.rectangle([10, 10, w - 10, 70], fill=(0, 80, 160))

    d.text((20, 20), "PARACETAMOL 500 mg Tablets", fill="white", font=_font(22))
    d.text((20, 55), "Film-coated tablets", fill=(200, 220, 255), font=_font(13))

    lines = [
        ("Active Ingredient:", "Paracetamol 500 mg per tablet"),
        ("Indication:", "Relief of mild to moderate pain and fever"),
        ("Dosage:", "Adults and children over 12 years:"),
        ("", "1-2 tablets every 4-6 hours as needed"),
        ("Max dose:", "8 tablets in 24 hours"),
        ("Route:", "Oral"),
        ("Storage:", "Store below 25 C, keep away from moisture"),
        ("Manufacturer:", "PharmaCo Ltd, Helsinki, Finland"),
        ("Batch No:", "BC20240915   Exp: 09/2027"),
    ]

    y = 90
    for label, value in lines:
        if label:
            d.text((20, y), label, fill=(0, 80, 160), font=_font(14))
            d.text((180, y), value, fill=(30, 30, 30), font=_font(14))
        else:
            d.text((180, y), value, fill=(30, 30, 30), font=_font(14))
        y += 28

    d.rectangle([10, h - 60, w - 10, h - 10], fill=(255, 240, 240))
    d.text((20, h - 55), "WARNING: Do not exceed stated dose.", fill=(180, 0, 0), font=_font(13))
    d.text((20, h - 35), "Keep out of reach of children.", fill=(180, 0, 0), font=_font(13))

    path = os.path.join(OUT, "test_medicine_label.png")
    img.save(path)
    print(f"Created: {path}")


# ---------------------------------------------------------------------------
# 2. Prescription
# ---------------------------------------------------------------------------
def make_prescription():
    w, h = 620, 500
    img = Image.new("RGB", (w, h), color=(255, 255, 255))
    d = ImageDraw.Draw(img)

    d.rectangle([10, 10, w - 10, h - 10], outline=(100, 100, 100), width=2)
    d.line([10, 100, w - 10, 100], fill=(100, 100, 100), width=1)
    d.line([10, h - 120, w - 10, h - 120], fill=(100, 100, 100), width=1)

    d.text((20, 20), "Dr. Sarah Johnson, MD", fill=(0, 60, 120), font=_font(20))
    d.text((20, 50), "General Practitioner", fill=(60, 60, 60), font=_font(13))
    d.text((20, 68), "Helsinki Medical Centre  |  Tel: +358 9 1234 5678", fill=(60, 60, 60), font=_font(12))

    d.text((20, 115), "Patient Name:  John Doe", fill=(20, 20, 20), font=_font(15))
    d.text((20, 140), "Date of Birth: 14/03/1985", fill=(20, 20, 20), font=_font(15))
    d.text((360, 115), "Date: 15/05/2026", fill=(20, 20, 20), font=_font(15))

    d.text((20, 185), "Rx", fill=(0, 80, 160), font=_font(26))

    rx_lines = [
        "Amoxicillin 500 mg Capsules",
        "Sig: Take ONE capsule THREE times daily",
        "    (morning, afternoon, evening) with food",
        "Duration: 7 days",
        "Quantity: 21 capsules",
        "",
        "Ibuprofen 400 mg Tablets",
        "Sig: Take ONE tablet TWICE daily as needed for pain",
        "Duration: 5 days",
        "Quantity: 10 tablets",
    ]

    y = 220
    for line in rx_lines:
        d.text((40, y), line, fill=(20, 20, 20), font=_font(14))
        y += 24

    d.text((20, h - 110), "Refills: 0", fill=(20, 20, 20), font=_font(14))
    d.text((20, h - 85), "Notes: Complete full antibiotic course.", fill=(20, 20, 20), font=_font(13))
    d.text((20, h - 60), "Dispense as written.", fill=(20, 20, 20), font=_font(13))
    d.text((360, h - 60), "Signature: _______________", fill=(20, 20, 20), font=_font(14))

    path = os.path.join(OUT, "test_prescription.png")
    img.save(path)
    print(f"Created: {path}")


# ---------------------------------------------------------------------------
# 3. Symptom image (redness / rash on arm)
# ---------------------------------------------------------------------------
def make_symptom_image():
    w, h = 500, 400
    img = Image.new("RGB", (w, h), color=(245, 222, 200))
    d = ImageDraw.Draw(img)

    # Simulate skin background with gradient-ish rectangles
    for i in range(0, h, 4):
        shade = 200 + int(40 * i / h)
        d.rectangle([0, i, w, i + 4], fill=(shade, int(shade * 0.85), int(shade * 0.75)))

    # Reddened patch
    for cx, cy, rx, ry, alpha in [
        (200, 200, 90, 60, 180),
        (240, 210, 55, 40, 160),
        (175, 220, 40, 30, 140),
    ]:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(210, 60, 60))

    # Smaller spots suggesting rash
    spots = [(220, 170, 12), (260, 185, 9), (195, 195, 8),
             (230, 235, 11), (265, 225, 7), (180, 215, 6)]
    for sx, sy, sr in spots:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(190, 40, 40))

    d.text((20, 20), "Symptom: Red rash on forearm", fill=(80, 0, 0), font=_font(16))
    d.text((20, 45), "Duration: 2 days  |  Itchy, mild burning", fill=(80, 0, 0), font=_font(13))

    path = os.path.join(OUT, "test_symptom_image.png")
    img.save(path)
    print(f"Created: {path}")


# ---------------------------------------------------------------------------
# 4. Minimal WAV audio (silence placeholder — replace with real speech for AWS)
# ---------------------------------------------------------------------------
def make_audio():
    path = os.path.join(OUT, "test_audio.wav")
    sample_rate = 16000
    duration_s = 3
    num_samples = sample_rate * duration_s

    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        # Simple 440 Hz tone so the file is non-empty and clearly audio
        import math
        frames = bytearray()
        for i in range(num_samples):
            sample = int(8000 * math.sin(2 * math.pi * 440 * i / sample_rate))
            frames += struct.pack("<h", sample)
        wf.writeframes(bytes(frames))

    print(f"Created: {path}")
    print("  NOTE: Replace test_audio.wav with a real speech recording to test")
    print("        Amazon Transcribe Medical. The generated file contains a tone,")
    print("        not speech, so AWS will transcribe it as empty/silence.")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    make_medicine_label()
    make_prescription()
    make_symptom_image()
    make_audio()
    print("\nAll test files are in the test_files/ folder.")
    print("Run:  streamlit run app.py")
