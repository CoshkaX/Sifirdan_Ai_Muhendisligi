import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kod"))

try:
    import torch
    import deney
except ImportError:  # PyTorch kurulu değilse testler atlanır
    torch = None


@unittest.skipUnless(torch is not None, "PyTorch kurulu değil")
class DeneyTesti(unittest.TestCase):
    def setUp(self):
        mg = deney.mg
        self.eski = (mg.D, mg.DROPOUT)
        self.karakterler, _, self.egitim, self.dogrulama = mg.veri_hazirla(mg.VERI_YOLU.read_text(encoding="utf-8"))

    def tearDown(self):
        deney.mg.D, deney.mg.DROPOUT = self.eski

    def test_parametre_sayilari(self):
        self.assertEqual(sum(p.numel() for p in deney.model_kur(31, 32, 0.2).parameters()), 28511)
        self.assertEqual(sum(p.numel() for p in deney.model_kur(31, 64, 0.0).parameters()), 106143)

    def test_erken_durdurma_en_iyiyi_saklar(self):
        gecmis, (en_iyi_kayip, en_iyi_adim, durum), _ = deney.deney_yap(
            self.egitim, self.dogrulama, len(self.karakterler), 32, 0.2, 1.0, adim_sayisi=300, aralik=100)
        self.assertEqual(len(gecmis), 4)
        self.assertEqual(en_iyi_kayip, min(v for _, _, v in gecmis))
        self.assertIn(en_iyi_adim, [a for a, _, _ in gecmis])
        model = deney.model_kur(len(self.karakterler), 32, 0.2)
        model.load_state_dict(durum)  # saklanan model yeniden yüklenebilmeli


if __name__ == "__main__":
    unittest.main()
