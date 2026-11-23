"""Ders 4.1 – Metni sayılara çevirmek: tokenizer demosu.

Ek paket gerektirmez, yalnızca Python standart kütüphanesi kullanır.
Çalıştır:  python kod/tokenizer_demo.py
"""

import unicodedata


def karakter_tokenizer(metin: str) -> list[str]:
    """Metni karakterlerine böler."""
    return list(metin)


def kelime_tokenizer(metin: str) -> list[str]:
    """Metni boşluklardan böler."""
    return metin.split()


def utf8_bayt_sayisi(metin: str) -> int:
    """Metnin UTF-8 olarak kaç bayt tuttuğunu döndürür."""
    return len(metin.encode("utf-8"))


def turkce_kucuk_harf(metin: str) -> str:
    """Türkçe kurallarına uygun küçük harfe çevirir (İ→i, I→ı).

    Python'un str.lower() metodu 'I' harfini 'i' yapar, 'İ' harfini ise
    iki karakterli bir diziye çevirir. İkisi de Türkçe için yanlıştır.
    O yüzden bu iki harfi önce kendimiz çeviriyoruz.
    """
    return metin.replace("İ", "i").replace("I", "ı").lower()


def unicode_normallestir(metin: str) -> str:
    """Metni NFC biçimine getirir.

    'ü' harfi bilgisayarda iki farklı şekilde saklanabilir: tek bir karakter
    olarak ("ü") ya da 'u' + birleşen iki nokta olarak ("u\\u0308"). Ekranda
    aynı görünürler ama == ile karşılaştırınca eşit çıkmazlar. NFC, ikinci
    biçimi birinciye çevirir.
    """
    return unicodedata.normalize("NFC", metin)


def acgozlu_altkelime(kelime: str, sozluk: set[str],
                      bilinmeyen: str = "[BİLİNMEYEN]") -> list[str]:
    """Açgözlü (en uzun eşleşme) alt-kelime tokenizer'ı.

    Her adımda, kelimenin kalan kısmının sözlükte bulunan EN UZUN önekini
    seçer. Hiçbir önek bulunamazsa o tek karakter için `bilinmeyen` yazar.
    """
    parcalar: list[str] = []
    i = 0
    while i < len(kelime):
        for son in range(len(kelime), i, -1):
            aday = kelime[i:son]
            if aday in sozluk:
                parcalar.append(aday)
                i = son
                break
        else:  # hiçbir aday eşleşmedi
            parcalar.append(bilinmeyen)
            i += 1
    return parcalar


# Elle hazırladığımız küçük bir örnek sözlük. Gerçek tokenizer'lar bunu
# veriden otomatik öğrenir (Ders 6.2'de BPE ile yapacağız).
ORNEK_SOZLUK = {
    "ev", "ler", "imiz", "den",
    "kitap", "lar", "ımız", "dan",
    "göz", "lük", "çü",
}


def main() -> None:
    kelimeler = ["evlerimizden", "kitaplarımızdan", "gözlükçü", "okuldan"]

    print("== 1) UTF-8: Türkçe harfler daha fazla bayt tutar ==")
    for metin in ["sac", "saç", "Türkçe", "Turkce"]:
        print(f"{metin!r:10} -> {len(metin)} karakter, {utf8_bayt_sayisi(metin)} bayt")

    print("\n== 2) Küçük harf tuzağı ==")
    for metin in ["ISPARTA", "İSTANBUL"]:
        print(f"{metin:10} str.lower() -> {metin.lower()!r:14} "
              f"turkce_kucuk_harf() -> {turkce_kucuk_harf(metin)!r}")

    print("\n== 3) Aynı görünen iki farklı 'ü' ==")
    tek, iki_parca = "ü", "u\u0308"
    print(f"tek karakter : {tek!r}, uzunluk={len(tek)}, bayt={utf8_bayt_sayisi(tek)}")
    print(f"iki parça    : {iki_parca!r}, uzunluk={len(iki_parca)}, bayt={utf8_bayt_sayisi(iki_parca)}")
    print(f"== ile eşit mi?            {tek == iki_parca}")
    print(f"NFC'den sonra eşit mi?     {tek == unicode_normallestir(iki_parca)}")

    print("\n== 4) Karakter ve alt-kelime bölmesi ==")
    for kelime in kelimeler:
        print(f"\n{kelime}")
        print("  karakter  :", karakter_tokenizer(kelime))
        print("  alt-kelime:", acgozlu_altkelime(kelime, ORNEK_SOZLUK))


if __name__ == "__main__":
    main()
