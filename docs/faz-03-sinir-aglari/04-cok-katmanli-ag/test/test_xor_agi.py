import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kod"))

from xor_agi import XOR_VERISI, IkiKatmanliAg  # noqa: E402


class XorAgiTesti(unittest.TestCase):
    def test_xor_ogrenilir(self):
        ag = IkiKatmanliAg(W1=[[0.5, -0.4], [-0.3, 0.8], [0.9, 0.2]], W2=[0.3, -0.5, 0.4])
        ag.egit(XOR_VERISI)
        for x, y in XOR_VERISI:
            self.assertEqual(int(ag.ileri(x)[1] >= 0.5), y)

    def test_rastgele_baslangicla_da_ogrenilir(self):
        for tohum in range(3):
            ag = IkiKatmanliAg(tohum=tohum)
            ag.egit(XOR_VERISI, tur_sayisi=4000)
            self.assertLess(ag.kayip(XOR_VERISI), 0.05, f"tohum={tohum}")

    def test_egitim_kaybi_azaltir(self):
        ag = IkiKatmanliAg(tohum=1)
        once = ag.kayip(XOR_VERISI)
        ag.egit(XOR_VERISI, tur_sayisi=200)
        self.assertLess(ag.kayip(XOR_VERISI), once)

    def test_gradyan_kontrolu(self):
        """Geri yayılımın türevleri sonlu farkla aynı olmalı."""
        ag = IkiKatmanliAg(tohum=5)
        g_W1, _, g_W2, g_b2 = ag.gradyanlar(XOR_VERISI)
        h = 1e-6

        def sayisal(liste, i, j=None):
            def ayarla(fark):
                if j is None:
                    liste[i] += fark
                else:
                    liste[i][j] += fark
            ayarla(h)
            artti = ag.kayip(XOR_VERISI)
            ayarla(-2 * h)
            azaldi = ag.kayip(XOR_VERISI)
            ayarla(h)
            return (artti - azaldi) / (2 * h)

        self.assertAlmostEqual(g_W1[1][0], sayisal(ag.W1, 1, 0), places=6)
        self.assertAlmostEqual(g_W2[2], sayisal(ag.W2, 2), places=6)
        ag.b2 += h
        artti = ag.kayip(XOR_VERISI)
        ag.b2 -= 2 * h
        azaldi = ag.kayip(XOR_VERISI)
        self.assertAlmostEqual(g_b2, (artti - azaldi) / (2 * h), places=6)

    def test_simetrik_baslangic_noronlari_ayni_tutar(self):
        ag = IkiKatmanliAg(W1=[[0.5, 0.5] for _ in range(3)], W2=[0.5, 0.5, 0.5])
        ag.egit(XOR_VERISI, tur_sayisi=300)
        self.assertAlmostEqual(ag.W1[0][0], ag.W1[1][0])
        self.assertAlmostEqual(ag.W1[1][0], ag.W1[2][0])


if __name__ == "__main__":
    unittest.main()
