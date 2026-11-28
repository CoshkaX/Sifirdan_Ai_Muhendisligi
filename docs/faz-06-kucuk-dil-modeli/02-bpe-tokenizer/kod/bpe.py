"""Ders 6.2 – BPE tokenizer: alt-kelime sözlüğünü veriden öğrenmek.

Ek paket gerektirmez. Çalıştır:  python kod/bpe.py

Byte Pair Encoding (BPE), metindeki en sık yan yana gelen iki parçayı tekrar tekrar
birleştirerek bir alt-kelime sözlüğü öğrenir. Bu sade sürüm karakterlerle çalışır ve
birleştirmeler sözcük sınırını geçmez.
"""

from collections import Counter

DERLEM = (
    "ev evler evde evden evlerde evlerden evlerimiz evimiz "
    "kitap kitaplar kitapta kitaptan kitaplarda kitaplardan kitaplarımız kitabımız "
    "okul okullar okulda okuldan okullarda okullardan okullarımız okulumuz"
)


def sozcuk_sayilari(metin):
    """Her sözcüğü karakterlerinin demeti olarak sayar: {('e', 'v'): 1, ...}."""
    return Counter(tuple(sozcuk) for sozcuk in metin.split())


def cift_sayilari(sozcukler):
    """Sözcüklerde yan yana gelen parça çiftlerini, sözcük sıklığıyla ağırlıklı sayar."""
    sayilar = Counter()
    for parcalar, sayi in sozcukler.items():
        for i in range(len(parcalar) - 1):
            sayilar[(parcalar[i], parcalar[i + 1])] += sayi
    return sayilar


def birlestir(parcalar, cift):
    """Bir sözcükte `cift`'in geçtiği her yeri tek parçaya çevirir."""
    yeni = []
    i = 0
    while i < len(parcalar):
        if i < len(parcalar) - 1 and (parcalar[i], parcalar[i + 1]) == cift:
            yeni.append(parcalar[i] + parcalar[i + 1])
            i += 2
        else:
            yeni.append(parcalar[i])
            i += 1
    return tuple(yeni)


def egit(metin, birlestirme_sayisi):
    """Sırayla öğrenilen birleştirmelerin listesini döndürür."""
    sozcukler = sozcuk_sayilari(metin)
    birlestirmeler = []
    for _ in range(birlestirme_sayisi):
        sayilar = cift_sayilari(sozcukler)
        if not sayilar:
            break
        en_sik = max(sayilar, key=sayilar.get)   # eşitlikte ilk görülen çift kazanır
        if sayilar[en_sik] < 2:
            break                                 # yalnızca bir kez görülen çiftleri birleştirmeyiz
        birlestirmeler.append(en_sik)
        sozcukler = Counter({birlestir(p, en_sik): s for p, s in sozcukler.items()})
    return birlestirmeler


def kodla(sozcuk, birlestirmeler):
    """Bir sözcüğü, öğrenilen birleştirmeleri sırayla uygulayarak token'lara böler."""
    parcalar = tuple(sozcuk)
    for cift in birlestirmeler:
        parcalar = birlestir(parcalar, cift)
    return list(parcalar)


def metni_kodla(metin, birlestirmeler):
    return [kodla(sozcuk, birlestirmeler) for sozcuk in metin.split()]


def coz(token_listeleri):
    """Token'ları yeniden metne çevirir: sözcük içindekileri yapıştırır, sözcükleri boşlukla ayırır."""
    return " ".join("".join(tokenlar) for tokenlar in token_listeleri)


def main():
    birlestirmeler = egit(DERLEM, 30)
    print("İlk 10 birleştirme:", ["".join(c) for c in birlestirmeler[:10]])
    for sozcuk in ["evlerimizden", "kitaplarımızda", "okulumuzdan", "bahçelerde"]:
        print(f"{sozcuk:15} → {kodla(sozcuk, birlestirmeler)}")


if __name__ == "__main__":
    main()
