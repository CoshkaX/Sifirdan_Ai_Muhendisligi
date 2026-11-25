import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kod"))

from duygu_analizi import EGITIM, TEST, DuyguModeli, dogruluk, ozellikler  # noqa: E402


class DuyguAnaliziTesti(unittest.TestCase):
    def test_olumsuzluk_birlestirme(self):
        self.assertEqual(ozellikler("Hiç güzel değil"), {"hiç", "güzel_değil"})
        self.assertEqual(ozellikler("memnun değilim"), {"memnun_değil"})
        self.assertEqual(ozellikler("güzel değil", olumsuzluk=False), {"güzel", "değil"})

    def test_cumle_basindaki_degil_kaybolmaz(self):
        self.assertEqual(ozellikler("Değil mi?"), {"değil", "mi"})

    def test_egitim_verisini_ogrenir(self):
        model = DuyguModeli()
        model.egit(EGITIM)
        self.assertEqual(dogruluk(model, EGITIM), 1.0)

    def test_olumsuzluk_test_basarisini_artirir(self):
        kapali, acik = DuyguModeli(olumsuzluk=False), DuyguModeli(olumsuzluk=True)
        kapali.egit(EGITIM)
        acik.egit(EGITIM)
        self.assertGreater(dogruluk(acik, TEST), dogruluk(kapali, TEST))
        self.assertEqual(acik.tahmin("Rengi güzel değil"), 0)

    def test_agirlik_yonleri(self):
        model = DuyguModeli()
        model.egit(EGITIM)
        self.assertGreater(model.agirliklar["harika"], 0)
        self.assertLess(model.agirliklar["kötü"], 0)


if __name__ == "__main__":
    unittest.main()
