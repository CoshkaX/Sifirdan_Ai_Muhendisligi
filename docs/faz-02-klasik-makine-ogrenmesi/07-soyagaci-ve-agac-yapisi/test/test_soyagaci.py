import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kod"))

from soyagaci import akrabalik_katsayisi, dogrula_soyagaci  # noqa: E402


class SoyagaciTestleri(unittest.TestCase):
    def setUp(self):
        self.soya = {
            "Ayse": None,
            "Bora": None,
            "Cem": ("Ayse", "Bora"),
            "Derya": None,
            "Emre": ("Cem", "Derya"),
        }

    def test_aynı_ebeveynlere_sahip_kardeşler(self):
        soya = dict(self.soya)
        soya["Fidan"] = ("Ayse", "Bora")
        self.assertAlmostEqual(akrabalik_katsayisi(soya, "Cem", "Fidan"), 0.25)

    def test_babanın_tamamen_farklı_olduğunu_dolaylı_olur(self):
        self.assertAlmostEqual(akrabalik_katsayisi(self.soya, "Ayse", "Derya"), 0.0)

    def test_birey_kendisiyle(self):
        self.assertAlmostEqual(akrabalik_katsayisi(self.soya, "Ayse", "Ayse"), 0.5)

    def test_donguyu_yakalar(self):
        soya = {"A": ("B", "C"), "B": ("A", "C"), "C": None}
        with self.assertRaises(ValueError):
            dogrula_soyagaci(soya)


if __name__ == "__main__":
    unittest.main()
