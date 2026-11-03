import re
from PIL import Image
from PIL.ExifTags import TAGS

# B1: Magic bytes
def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"): return "pdf"
    if cap.startswith(b"\x89PNG"): return "png"
    if cap.startswith(b"\xff\xd8"): return "jpeg"
    if cap.startswith(b"PK\x03\x04"): return "zip/docx"
    return cap.hex()
print(f"[B1] Tip real foto.jpg: {tip_real('probe/foto.jpg')}")

# B2: Strings
date_ascuns = open("probe/ascuns.png", "rb").read()
print("\n[B2] Strings găsite în ascuns.png:")
for m in re.findall(rb"[ -~]{4,}", date_ascuns):
    if b"FLAG" in m or b".txt" in m:
        print(m.decode())

# B3: EXIF și GPS
print("\n[B3] GPS Metadate:")
exif = Image.open("probe/foto.jpg")._getexif() or {}
gps_info = exif.get(34853)
if gps_info:
    print(f"Latitudine/Longitudine brută: {gps_info}")

# B4: File carving
i = date_ascuns.find(b"PK\x03\x04")
if i != -1:
    open("gasit.zip", "wb").write(date_ascuns[i:])
    print(f"\n[B4] Arhivă ZIP extrasă de la octetul {i}")

# B5 & B6: LSB Steganography
def ascunde_mesaj(mesaj, poza_in, poza_out):
    img = Image.open(poza_in).convert("RGB")
    px = list(img.getdata())
    mesaj += b"\x00"  # adăugăm un null byte ca să știm unde se termină
    biti = "".join(f"{x:08b}" for x in mesaj)
    
    px_nou = []
    bit_idx = 0
    for r, g, b in px:
        if bit_idx < len(biti):
            r = (r & ~1) | int(biti[bit_idx]); bit_idx += 1
        if bit_idx < len(biti):
            g = (g & ~1) | int(biti[bit_idx]); bit_idx += 1
        if bit_idx < len(biti):
            b = (b & ~1) | int(biti[bit_idx]); bit_idx += 1
        px_nou.append((r, g, b))
        
    img.putdata(px_nou)
    img.save(poza_out)
    print(f"\n[B5] Mesaj ascuns în {poza_out}")

def extrage_mesaj(poza):
    px = list(Image.open(poza).convert("RGB").getdata())
    biti = ""
    for r, g, b in px:
        biti += str(r & 1) + str(g & 1) + str(b & 1)
    
    octeti = [int(biti[i:i+8], 2) for i in range(0, len(biti), 8)]
    mesaj = bytearray()
    for o in octeti:
        if o == 0: break
        mesaj.append(o)
    print(f"[B6] Mesaj extras: {mesaj.decode(errors='ignore')}")

ascunde_mesaj(b"FLAG{ascuns_in_pixeli}", "probe/foto.jpg", "stego.png")
extrage_mesaj("stego.png")