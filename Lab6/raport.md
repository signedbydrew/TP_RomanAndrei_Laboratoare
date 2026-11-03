# Raport Laborator 6

### Lucrarea A
* **Mesajul decodat (`mesaj.txt`)**: A ascuns textul `FLAG{straturi_de_encoding}`. A fost codat aplicând Hex, urmat de două straturi de Base64.
* **XOR Bruteforce (`xor.bin`)**: Cheia găsită a fost `128` (`0x80`), iar mesajul clar este: `Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}`.
* **Spargere Hash (`hashuri.txt`)**: Primul hash MD5 s-a potrivit cu parola `password` din dicționar.

### Lucrarea B
* **Magic bytes**: `foto.jpg` a fost identificat corect ca fiind JPEG (`\xff\xd8`).
* **Metadate GPS**: Coordonatele găsite în poză sunt 47°01'00.0"N, 28°51'27.0"E (Chișinău).
* **File Carving**: Am extras o arhivă `.zip` de la coada fișierului `ascuns.png`. În interior se afla `secret.txt` conținând `FLAG{ascuns_prin_carving}`.
* **Steganografie LSB**: Am ascuns și apoi am recuperat cu succes mesajul `FLAG{ascuns_in_pixeli}` modificând ultimul bit din canalele RGB ale pozei.