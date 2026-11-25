"""Ders 4.5 – Benzerlik ve arama: kosinüs benzerliğiyle küçük bir Türkçe arama motoru.

Ek paket gerektirmez. Çalıştır:  python kod/turkce_arama.py
"""

import math
import unicodedata
from collections import Counter

BELGELER = [
    "Kitap okumak insanı geliştirir.",
    "Kitapları okudukça kelime dağarcığım genişledi.",
    "Bu hafta sonu sahilde kitap okuyacağım.",
    "Futbol maçı yağmur yüzünden ertelendi.",
    "Yağmurlu havada sahilde yürümek güzel.",
    "Akşam yemeğinde balık ve salata yedik.",
]


def normallestir(metin: str) -> list[str]:
    """4.3 dersindeki adımlar + noktalama temizliği; sözcük listesi döndürür."""
    metin = unicodedata.normalize("NFC", metin)
    metin = metin.replace("İ", "i").replace("I", "ı").lower()
    metin = "".join(h if h.isalnum() else " " for h in metin)
    return metin.split()


def kok_yaklasimi(sozcuk: str, uzunluk: int = 5) -> str:
    """Sözcüğün ilk `uzunluk` harfini alır. Kaba ama Türkçe aramada etkili bir yöntem."""
    return sozcuk[:uzunluk]


def vektorlestir(metin: str, kok_uzunlugu: int | None = 5) -> Counter:
    """Metni 'sözcük torbası' vektörüne çevirir: {terim: kaç kez geçtiği}."""
    sozcukler = normallestir(metin)
    if kok_uzunlugu:
        sozcukler = [kok_yaklasimi(s, kok_uzunlugu) for s in sozcukler]
    return Counter(sozcukler)


def kosinus(a: Counter, b: Counter) -> float:
    nokta = sum(a[t] * b[t] for t in a if t in b)
    uzunluk_a = math.sqrt(sum(v * v for v in a.values()))
    uzunluk_b = math.sqrt(sum(v * v for v in b.values()))
    if uzunluk_a == 0 or uzunluk_b == 0:
        return 0.0
    return nokta / (uzunluk_a * uzunluk_b)


def ara(sorgu: str, belgeler: list[str], k: int = 3, kok_uzunlugu: int | None = 5):
    """Sorguya en benzer `k` belgeyi (skor, belge) çiftleri olarak döndürür."""
    sorgu_vektoru = vektorlestir(sorgu, kok_uzunlugu)
    skorlar = [(kosinus(sorgu_vektoru, vektorlestir(b, kok_uzunlugu)), b) for b in belgeler]
    skorlar.sort(key=lambda cift: cift[0], reverse=True)
    return [(skor, belge) for skor, belge in skorlar[:k] if skor > 0]


def main() -> None:
    for sorgu in ["kitaplar okumak", "yağmurda sahil"]:
        print(f"Sorgu: {sorgu!r}")
        for skor, belge in ara(sorgu, BELGELER):
            print(f"  {skor:.2f}  {belge}")
        print()


if __name__ == "__main__":
    main()
