import argparse
import json
import re
import base64
import hashlib
from urllib.parse import unquote

def ghici_strat(s):
    if "%" in s and re.search(r'%[0-9a-fA-F]{2}', s): return "url"
    if re.fullmatch(r'[0-9a-fA-F]+', s) and len(s) % 2 == 0: return "hex"
    if re.fullmatch(r'[A-Za-z0-9+/]+={0,2}', s): return "base64"
    return "necunoscut"

def desfa(s):
    strat = ghici_strat(s)
    try:
        if strat == "base64": return strat, base64.b64decode(s)
        if strat == "hex": return strat, bytes.fromhex(s)
        if strat == "url": return strat, unquote(s).encode()
    except Exception:
        pass
    return strat, s.encode()

def citibil(b):
    return all(32 <= c < 127 for c in b)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    # Partea 1: Decodare straturi
    val = open(a.intrare, "r").read().strip() if a.fisier else a.intrare
    rezultat_final = val
    strat_final = "text clar"
    
    for _ in range(8):
        strat, b = desfa(val)
        if citibil(b):
            rezultat_final = b.decode()
            strat_final = strat
            break
        val = b.decode('utf-8', errors='ignore')
    
    print(f"Mesaj decodat: {rezultat_final}")
    
    with open("arsenal/forensics/fisa.json", "w") as f:
        json.dump({"strat": strat_final, "rezultat": rezultat_final}, f)

    # Partea 2: XOR bruteforce
    try:
        date_xor = open("probe/xor.bin", "rb").read()
        for k in range(256):
            clar = bytes(b ^ k for b in date_xor)
            if citibil(clar):
                print(f"Cheie XOR găsită: {k} -> {clar.decode()}")
                break
    except FileNotFoundError: pass

    # Partea 3: Spargere Hash
    try:
        tinta = open("probe/hashuri.txt").readline().strip()
        for cuv in open("probe/wordlist.txt", encoding="latin1"):
            cuv = cuv.strip()
            if hashlib.md5(cuv.encode()).hexdigest() == tinta:
                print(f"Parolă găsită pentru hash: {cuv}")
                break
    except FileNotFoundError: pass