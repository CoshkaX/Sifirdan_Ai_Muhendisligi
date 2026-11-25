"""Ders 3.4 – Çok katmanlı ağ: XOR problemini öğrenen küçük bir sinir ağı.

Ek paket gerektirmez. Çalıştır:  python kod/xor_agi.py

Yapı: 2 girdi → gizli katman (sigmoid) → 1 çıktı (sigmoid), kayıp: ortalama kare hata.
Her turda dört örneğin türevleri toplanır, ortalaması alınır ve ağırlıklar güncellenir.
"""

import math
import random

XOR_VERISI = [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]


def sigmoid(z):
    return 1 / (1 + math.exp(-z))


class IkiKatmanliAg:
    def __init__(self, gizli_noron_sayisi=3, tohum=0, W1=None, W2=None):
        rastgele = random.Random(tohum)
        self.gizli = gizli_noron_sayisi
        # W1[j] = j. gizli nöronun iki girdiye ait ağırlıkları
        self.W1 = W1 or [[rastgele.uniform(-1, 1) for _ in range(2)] for _ in range(self.gizli)]
        self.b1 = [0.0] * self.gizli
        # W2[j] = j. gizli nörondan çıktıya giden ağırlık
        self.W2 = W2 or [rastgele.uniform(-1, 1) for _ in range(self.gizli)]
        self.b2 = 0.0

    def ileri(self, x):
        """Gizli katman çıktıları ve ağın tahminini döndürür."""
        h = [sigmoid(self.W1[j][0] * x[0] + self.W1[j][1] * x[1] + self.b1[j])
             for j in range(self.gizli)]
        p = sigmoid(sum(self.W2[j] * h[j] for j in range(self.gizli)) + self.b2)
        return h, p

    def kayip(self, veri):
        return sum((self.ileri(x)[1] - y) ** 2 for x, y in veri) / len(veri)

    def gradyanlar(self, veri):
        """Ortalama kare hatanın bütün parametrelere göre türevleri (geri yayılım)."""
        g_W1 = [[0.0, 0.0] for _ in range(self.gizli)]
        g_b1 = [0.0] * self.gizli
        g_W2 = [0.0] * self.gizli
        g_b2 = 0.0
        n = len(veri)
        for x, y in veri:
            h, p = self.ileri(x)
            d_z2 = 2 * (p - y) * p * (1 - p) / n
            g_b2 += d_z2
            for j in range(self.gizli):
                g_W2[j] += d_z2 * h[j]
                d_z1 = d_z2 * self.W2[j] * h[j] * (1 - h[j])
                g_W1[j][0] += d_z1 * x[0]
                g_W1[j][1] += d_z1 * x[1]
                g_b1[j] += d_z1
        return g_W1, g_b1, g_W2, g_b2

    def adim(self, veri, ogrenme_hizi):
        g_W1, g_b1, g_W2, g_b2 = self.gradyanlar(veri)
        for j in range(self.gizli):
            self.W1[j][0] -= ogrenme_hizi * g_W1[j][0]
            self.W1[j][1] -= ogrenme_hizi * g_W1[j][1]
            self.b1[j] -= ogrenme_hizi * g_b1[j]
            self.W2[j] -= ogrenme_hizi * g_W2[j]
        self.b2 -= ogrenme_hizi * g_b2

    def egit(self, veri, tur_sayisi=2000, ogrenme_hizi=2.0, yazdir=False):
        for tur in range(tur_sayisi + 1):
            if yazdir and tur % 500 == 0:
                print(f"Tur {tur}: kayıp {self.kayip(veri):.4f}")
            if tur < tur_sayisi:
                self.adim(veri, ogrenme_hizi)


def main() -> None:
    ag = IkiKatmanliAg(
        W1=[[0.5, -0.4], [-0.3, 0.8], [0.9, 0.2]],
        W2=[0.3, -0.5, 0.4],
    )
    ag.egit(XOR_VERISI, yazdir=True)
    for x, y in XOR_VERISI:
        print(f"{x[0]} XOR {x[1]}: hedef {y}, tahmin {ag.ileri(x)[1]:.2f}")


if __name__ == "__main__":
    main()
