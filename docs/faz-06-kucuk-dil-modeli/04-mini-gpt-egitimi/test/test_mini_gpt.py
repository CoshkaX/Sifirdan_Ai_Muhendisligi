import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kod"))

try:
    import torch
    import mini_gpt as mg
except ImportError:  # PyTorch kurulu değilse testler atlanır
    torch = None


@unittest.skipUnless(torch is not None, "PyTorch kurulu değil")
class MiniGPTTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metin = mg.VERI_YOLU.read_text(encoding="utf-8")
        cls.karakterler, cls.stoi, cls.egitim, cls.dogrulama = mg.veri_hazirla(cls.metin)

    def test_veri_bolme(self):
        self.assertEqual(len(self.egitim) + len(self.dogrulama), len(self.metin))
        self.assertEqual(len(self.egitim), int(len(self.metin) * 0.9))
        geri = "".join(self.karakterler[i] for i in self.egitim[:20].tolist())
        self.assertEqual(geri, self.metin[:20])

    def test_hedef_bir_kayik(self):
        torch.manual_seed(0)
        girdi, hedef = mg.batch_al(self.egitim, 4)
        self.assertEqual(girdi.shape, (4, mg.BLOK))
        self.assertTrue(torch.equal(girdi[:, 1:], hedef[:, :-1]))

    def test_baslangic_kaybi_rastgele_tahmine_yakin(self):
        torch.manual_seed(0)
        model = mg.MiniGPT(len(self.karakterler))
        kayip = mg.kayip_olc(model, self.egitim)
        self.assertAlmostEqual(kayip, math.log(len(self.karakterler)), delta=0.5)

    def test_maske_gelecegi_gizler(self):
        torch.manual_seed(0)
        model = mg.MiniGPT(len(self.karakterler)).eval()
        a, _ = mg.batch_al(self.egitim, 2)
        b = a.clone()
        b[:, -1] = (b[:, -1] + 1) % len(self.karakterler)
        with torch.no_grad():
            self.assertTrue(torch.allclose(model(a)[:, :-1], model(b)[:, :-1], atol=1e-5))

    def test_egitim_dogrulama_kaybini_dusurur(self):
        torch.manual_seed(0)
        model = mg.MiniGPT(len(self.karakterler))
        gecmis = mg.egit(model, self.egitim, self.dogrulama, adim_sayisi=500)
        self.assertLess(gecmis[-1][2], gecmis[0][2] - 1.0)
        metin = mg.uret(model, "ali ", self.stoi, self.karakterler, uzunluk=20)
        self.assertEqual(len(metin), 24)


if __name__ == "__main__":
    unittest.main()
