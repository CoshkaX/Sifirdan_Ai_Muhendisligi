import os
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kod"))

from yapay_zeka_durumu import BasitKararSistemi  # noqa: E402


class YapayZekaDurumuTestleri(unittest.TestCase):
    def setUp(self):
        self.sistem = BasitKararSistemi({
            "hava": ("yağmurlu", "Şemsiyeyi düşün."),
        })

    def test_gözlem_belleğe_eklenir(self):
        gözlem = self.sistem.gözlemle({"hava": "yağmurlu"})
        anahtar, açıklama = self.sistem.çıkarım_yap(gözlem)
        self.assertEqual(anahtar, "hava")
        self.assertEqual(açıklama, "Şemsiyeyi düşün.")
        self.assertEqual(len(self.sistem.bellek), 1)

    def test_tanımsız_gözlem_belirsiz_der(self):
        gözlem = self.sistem.gözlemle({"hava": "rüzgarlı"})
        anahtar, açıklama = self.sistem.çıkarım_yap(gözlem)
        self.assertEqual(anahtar, "belirsiz")
        self.assertIn("eşleşmedi", açıklama)

    def test_tam_ornek_dosyasi_calistirilabilir(self):
        dosya = os.path.join(os.path.dirname(__file__), "..", "kod", "yapay_zeka_durumu.py")
        sonuc = subprocess.run(
            [sys.executable, dosya],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self.assertIn(b"Bellek ", sonuc.stdout)


if __name__ == "__main__":
    unittest.main()
