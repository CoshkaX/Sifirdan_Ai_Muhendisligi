import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kod"))

from bpe import DERLEM, birlestir, cift_sayilari, coz, egit, kodla, metni_kodla, sozcuk_sayilari  # noqa: E402


class BpeTesti(unittest.TestCase):
    def test_cift_sayilari_siklikla_agirlikli(self):
        sayilar = cift_sayilari({("k", "e", "d", "i"): 3, ("k", "e"): 2})
        self.assertEqual(sayilar[("k", "e")], 5)
        self.assertEqual(sayilar[("d", "i")], 3)

    def test_birlestir(self):
        self.assertEqual(birlestir(("a", "b", "a", "b", "c"), ("a", "b")), ("ab", "ab", "c"))

    def test_kok_ve_ekleri_ogrenir(self):
        b = egit(DERLEM, 30)
        self.assertEqual(kodla("evlerimizden", b), ["evler", "imiz", "de", "n"])
        self.assertEqual(kodla("kitaplarımızda", b), ["kitaplar", "ımız", "da"])

    def test_gorulmemis_sozcuk_harflere_duser(self):
        tokenlar = kodla("bahçe", egit(DERLEM, 30))
        self.assertEqual("".join(tokenlar), "bahçe")

    def test_geri_cevirme_kayipsiz(self):
        b = egit(DERLEM, 30)
        metin = "evlerimizden kitaplarda yeni okullar"
        self.assertEqual(coz(metni_kodla(metin, b)), metin)

    def test_sikistirma(self):
        b = egit(DERLEM, 30)
        token_sayisi = sum(len(t) for t in metni_kodla(DERLEM, b))
        self.assertLess(token_sayisi, len(DERLEM.replace(" ", "")) / 3)

    def test_sozcuk_sayilari(self):
        self.assertEqual(sozcuk_sayilari("ev ev el")[("e", "v")], 2)


if __name__ == "__main__":
    unittest.main()
