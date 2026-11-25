"""Ders 4.7 – Veri setleri: bir metin veri setini kullanmadan önce kontrol etmek.

Ek paket gerektirmez. Çalıştır:  python kod/veri_kontrol.py
"""

import re
import unicodedata
from collections import Counter


def normallestir(metin: str) -> str:
    """Karşılaştırma için: NFC, Türkçe küçük harf, noktalama yok, tek boşluk."""
    metin = unicodedata.normalize("NFC", metin)
    metin = metin.replace("İ", "i").replace("I", "ı").lower()
    metin = "".join(h if h.isalnum() else " " for h in metin)
    return " ".join(metin.split())


def kalite_raporu(veri, gecerli_etiketler=(0, 1)):
    """(metin, etiket) listesindeki yaygın sorunları sayar."""
    bos = [i for i, (metin, _) in enumerate(veri) if not normallestir(metin)]
    gecersiz = [i for i, (_, etiket) in enumerate(veri) if etiket not in gecerli_etiketler]

    gorulen = {}
    tekrarlar = []
    for i, (metin, _) in enumerate(veri):
        anahtar = normallestir(metin)
        if not anahtar:
            continue
        if anahtar in gorulen:
            tekrarlar.append((gorulen[anahtar], i))
        else:
            gorulen[anahtar] = i

    return {
        "örnek sayısı": len(veri),
        "boş metin": bos,
        "geçersiz etiket": gecersiz,
        "tekrar eden çiftler": tekrarlar,
        "sınıf dağılımı": dict(Counter(etiket for _, etiket in veri)),
    }


def sizinti(egitim, test):
    """Hem eğitimde hem testte bulunan (normalleştirilmiş) metinler."""
    egitim_metinleri = {normallestir(m) for m, _ in egitim}
    return sorted({normallestir(m) for m, _ in test} & egitim_metinleri)


EPOSTA = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
TELEFON = re.compile(r"(?<!\d)(?:\+90\s?|0)?5\d{2}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}(?!\d)")
TC_KIMLIK = re.compile(r"(?<!\d)[1-9]\d{10}(?!\d)")


def kisisel_veriyi_maskele(metin: str) -> str:
    """E-posta, cep telefonu ve 11 haneli kimlik numarası benzeri dizileri gizler."""
    metin = EPOSTA.sub("[EPOSTA]", metin)
    metin = TELEFON.sub("[TELEFON]", metin)
    metin = TC_KIMLIK.sub("[TCKN]", metin)
    return metin


def main() -> None:
    veri = [
        ("Ürün çok güzel", 1),
        ("ürün çok güzel!", 1),
        ("", 0),
        ("Kargo geç geldi", 0),
        ("Fiyatı uygun", 2),
        ("Harika bir film", 1),
    ]
    for anahtar, deger in kalite_raporu(veri).items():
        print(f"{anahtar}: {deger}")

    print("\nSızıntı:", sizinti([("Harika bir film", 1)], [("harika bir film.", 1), ("Kötü", 0)]))
    print(kisisel_veriyi_maskele("Bana ali.veli@ornek.com ya da 0532 123 45 67 üzerinden ulaşın."))


if __name__ == "__main__":
    main()
