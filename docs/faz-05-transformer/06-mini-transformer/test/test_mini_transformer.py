import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kod"))

try:
    import torch
    import mini_transformer as mt
except ImportError:  # PyTorch kurulu değilse testler atlanır
    torch = None


@unittest.skipUnless(torch is not None, "PyTorch kurulu değil")
class MiniTransformerTesti(unittest.TestCase):
    def test_veri_periyodik(self):
        torch.manual_seed(0)
        dizi = mt.veri_uret(5)
        self.assertEqual(dizi.shape, (5, mt.UZUNLUK))
        self.assertTrue(torch.equal(dizi[:, 2:], dizi[:, :-2]))

    def test_cikis_sekli_ve_parametre_sayisi(self):
        torch.manual_seed(0)
        model = mt.MiniTransformer()
        cikti = model(mt.veri_uret(3)[:, :-1])
        self.assertEqual(cikti.shape, (3, mt.UZUNLUK - 1, mt.SOZLUK))
        self.assertEqual(sum(p.numel() for p in model.parameters()), 26216)

    def test_maske_gelecegi_gizler(self):
        torch.manual_seed(0)
        model = mt.MiniTransformer().eval()
        a = mt.veri_uret(2)[:, :-1]
        b = a.clone()
        b[:, -1] = (b[:, -1] + 1) % mt.SOZLUK  # yalnızca son token değişir
        with torch.no_grad():
            self.assertTrue(torch.allclose(model(a)[:, :-1], model(b)[:, :-1], atol=1e-5))

    def test_egitim_ogrenir(self):
        torch.manual_seed(0)
        model = mt.MiniTransformer()
        kayitlar = mt.egit(model)
        self.assertLess(kayitlar[800], 0.4)
        self.assertGreater(kayitlar[1], 1.5)
        torch.manual_seed(123)
        self.assertGreater(mt.dogruluk(model), 0.95)

    def test_uretim_dizisi(self):
        torch.manual_seed(0)
        model = mt.MiniTransformer()
        mt.egit(model)
        self.assertEqual(mt.uret(model, [2, 5]), [2, 5, 2, 5, 2, 5, 2, 5])

    def test_maskesiz_model_kopya_ceker(self):
        torch.manual_seed(0)
        model = mt.MiniTransformer(maskeli=False)
        kayitlar = mt.egit(model)
        taban = 0.297
        self.assertLess(kayitlar[800], taban / 3)  # kaçınılmaz kaybın çok altı: gelecek görüldü


if __name__ == "__main__":
    unittest.main()
