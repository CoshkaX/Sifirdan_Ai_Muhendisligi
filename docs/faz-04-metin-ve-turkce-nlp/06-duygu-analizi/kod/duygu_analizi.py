"""Ders 4.6 – Duygu analizi: Türkçe yorumlar için sözcük torbası + lojistik regresyon.

Ek paket gerektirmez. Çalıştır:  python kod/duygu_analizi.py
Etiketler: 1 = olumlu, 0 = olumsuz. Yorumlar bu ders için yazılmış örneklerdir.
"""

import math
import unicodedata

EGITIM = [
    ("Ürün çok güzel, çok beğendim", 1),
    ("Kargo hızlı geldi, teşekkürler", 1),
    ("Kalitesi harika, herkese tavsiye ederim", 1),
    ("Fiyatına göre gayet iyi", 1),
    ("Film çok güzeldi, bayıldım", 1),
    ("Oyunculuk harika, tekrar izlerim", 1),
    ("Kumaşı yumuşak ve kaliteli, memnun kaldım", 1),
    ("Beklediğimden iyi çıktı, beğendim", 1),
    ("Ürün kötü, hiç beğenmedim", 0),
    ("Kargo çok geç geldi, memnun değilim", 0),
    ("Kalitesi berbat, tavsiye etmem", 0),
    ("Fiyatına göre çok pahalı ve kötü", 0),
    ("Film çok sıkıcıydı, beğenmedim", 0),
    ("Oyunculuk kötü, bir daha izlemem", 0),
    ("Kumaşı ince, iki yıkamada yırtıldı", 0),
    ("Hiç güzel değil, para çöpe gitti", 0),
]

TEST = [
    ("Telefon çok güzel, beğendim", 1),
    ("Hızlı kargo için teşekkürler", 1),
    ("Harika bir film, tavsiye ederim", 1),
    ("Kaliteli ve iyi bir ürün", 1),
    ("Berbat bir ürün, beğenmedim", 0),
    ("Çok sıkıcı bir dizi", 0),
    ("Kargo geç geldi, kötü", 0),
    ("Rengi güzel değil", 0),
]


def normallestir(metin):
    metin = unicodedata.normalize("NFC", metin)
    metin = metin.replace("İ", "i").replace("I", "ı").lower()
    metin = "".join(h if h.isalnum() else " " for h in metin)
    return metin.split()


def ozellikler(metin, olumsuzluk=True):
    """Sözcük kümesi. `olumsuzluk` açıksa 'güzel değil' → 'güzel_değil' olur."""
    sozcukler = normallestir(metin)
    if olumsuzluk:
        birlesik = []
        for sozcuk in sozcukler:
            if sozcuk.startswith("değil") and birlesik:
                birlesik[-1] = birlesik[-1] + "_değil"
            else:
                birlesik.append(sozcuk)
        sozcukler = birlesik
    return set(sozcukler)


def sigmoid(z):
    return 1 / (1 + math.exp(-z))


class DuyguModeli:
    def __init__(self, olumsuzluk=True):
        self.olumsuzluk = olumsuzluk
        self.agirliklar = {}
        self.sabit = 0.0

    def olasilik(self, metin):
        z = self.sabit + sum(self.agirliklar.get(s, 0.0) for s in ozellikler(metin, self.olumsuzluk))
        return sigmoid(z)

    def tahmin(self, metin):
        return int(self.olasilik(metin) >= 0.5)

    def egit(self, veri, tur_sayisi=300, ogrenme_hizi=0.5):
        for _ in range(tur_sayisi):
            gradyanlar = {}
            sabit_gradyani = 0.0
            for metin, etiket in veri:
                hata = self.olasilik(metin) - etiket  # çapraz entropi + sigmoid türevi (2.3)
                for s in ozellikler(metin, self.olumsuzluk):
                    gradyanlar[s] = gradyanlar.get(s, 0.0) + hata
                sabit_gradyani += hata
            for s, g in gradyanlar.items():
                self.agirliklar[s] = self.agirliklar.get(s, 0.0) - ogrenme_hizi * g / len(veri)
            self.sabit -= ogrenme_hizi * sabit_gradyani / len(veri)


def dogruluk(model, veri):
    return sum(model.tahmin(m) == e for m, e in veri) / len(veri)


def main() -> None:
    for olumsuzluk in [False, True]:
        model = DuyguModeli(olumsuzluk=olumsuzluk)
        model.egit(EGITIM)
        print(f"Olumsuzluk birleştirme {'açık' if olumsuzluk else 'kapalı'}: "
              f"test doğruluğu {dogruluk(model, TEST):.2f}")
        for metin, etiket in TEST:
            print(f"  {model.olasilik(metin):.2f}  hedef={etiket}  {metin}")
    # Eşit ağırlıklarda alfabetik sıraya bakarız; böylece çıktı her çalıştırmada aynı olur.
    sirali = sorted(model.agirliklar.items(), key=lambda x: (round(x[1], 6), x[0]))
    print("En olumlu sözcükler:", [s for s, _ in reversed(sirali[-5:])])
    print("En olumsuz sözcükler:", [s for s, _ in sirali[:5]])


if __name__ == "__main__":
    main()
