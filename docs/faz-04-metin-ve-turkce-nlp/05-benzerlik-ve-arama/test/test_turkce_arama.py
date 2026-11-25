import os
import sys
import unittest
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kod"))

from turkce_arama import BELGELER, ara, kosinus, normallestir, vektorlestir  # noqa: E402


class TurkceAramaTesti(unittest.TestCase):
    def test_normallestir(self):
        self.assertEqual(normallestir("İSTANBUL'da, IĞDIR!"), ["istanbul", "da", "ığdır"])

    def test_kosinus_ayni_yon(self):
        self.assertAlmostEqual(kosinus(Counter(a=1, b=1), Counter(a=3, b=3)), 1.0)

    def test_kosinus_ortak_terim_yok(self):
        self.assertEqual(kosinus(Counter(a=1), Counter(b=1)), 0.0)

    def test_bos_vektor(self):
        self.assertEqual(kosinus(Counter(), Counter(a=1)), 0.0)

    def test_kok_yaklasimi_ekli_bicimleri_eslestirir(self):
        self.assertEqual(vektorlestir("kitapları"), vektorlestir("kitap"))

    def test_arama_en_ilgili_belgeyi_bulur(self):
        sonuc = ara("yağmurda sahil", BELGELER)
        self.assertEqual(sonuc[0][1], "Yağmurlu havada sahilde yürümek güzel.")

    def test_koksuz_arama_ekleri_kacirir(self):
        self.assertEqual(ara("yağmurda sahil", BELGELER, kok_uzunlugu=None), [])

    def test_ilgisiz_sorgu_bos_doner(self):
        self.assertEqual(ara("bilgisayar", BELGELER), [])


if __name__ == "__main__":
    unittest.main()
