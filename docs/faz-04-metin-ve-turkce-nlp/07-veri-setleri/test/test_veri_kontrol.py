import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kod"))

from veri_kontrol import kalite_raporu, kisisel_veriyi_maskele, normallestir, sizinti  # noqa: E402


class VeriKontrolTesti(unittest.TestCase):
    def test_normallestir(self):
        self.assertEqual(normallestir("  İYİ, çok   İYİ! "), "iyi çok iyi")

    def test_kalite_raporu(self):
        veri = [("A b", 1), ("a B!", 1), ("  ", 0), ("c", 3)]
        rapor = kalite_raporu(veri)
        self.assertEqual(rapor["boş metin"], [2])
        self.assertEqual(rapor["geçersiz etiket"], [3])
        self.assertEqual(rapor["tekrar eden çiftler"], [(0, 1)])
        self.assertEqual(rapor["sınıf dağılımı"], {1: 2, 0: 1, 3: 1})

    def test_sizinti(self):
        self.assertEqual(sizinti([("Güzel film", 1)], [("güzel FİLM.", 1), ("x", 0)]), ["güzel film"])
        self.assertEqual(sizinti([("a", 1)], [("b", 1)]), [])

    def test_eposta(self):
        self.assertEqual(kisisel_veriyi_maskele("yaz: ayse.k+not@ornek.com.tr"), "yaz: [EPOSTA]")

    def test_telefon_bicimleri(self):
        for numara in ["05321234567", "0532 123 45 67", "+90 532 123 45 67", "532-123-45-67"]:
            self.assertEqual(kisisel_veriyi_maskele(f"ara {numara} lütfen"), "ara [TELEFON] lütfen", numara)

    def test_kimlik_numarasi(self):
        self.assertEqual(kisisel_veriyi_maskele("TC: 12345678901"), "TC: [TCKN]")

    def test_siradan_sayilar_kalir(self):
        metin = "2024 yılında 3 ürün aldım, fiyatı 150 TL."
        self.assertEqual(kisisel_veriyi_maskele(metin), metin)


if __name__ == "__main__":
    unittest.main()
