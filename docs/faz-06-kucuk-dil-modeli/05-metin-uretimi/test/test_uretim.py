import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kod"))

try:
    import torch
    import uretim as u
except ImportError:  # PyTorch kurulu değilse testler atlanır
    torch = None


@unittest.skipUnless(torch is not None, "PyTorch kurulu değil")
class UretimTesti(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(0)
        # olasılıklar yaklaşık 0.5, 0.3, 0.15, 0.05
        self.logitler = torch.log(torch.tensor([0.5, 0.3, 0.15, 0.05]))

    def secimler(self, n=500, **ayarlar):
        return {u.sonraki_token(self.logitler, **ayarlar) for _ in range(n)}

    def test_acgozlu_en_yuksegi_secer(self):
        self.assertEqual(self.secimler(20, sicaklik=0), {0})

    def test_top_k(self):
        self.assertEqual(self.secimler(top_k=1), {0})
        self.assertEqual(self.secimler(top_k=2), {0, 1})

    def test_top_p(self):
        self.assertEqual(self.secimler(top_p=0.4), {0})
        self.assertEqual(self.secimler(top_p=0.8), {0, 1})
        self.assertEqual(self.secimler(top_p=0.9), {0, 1, 2})

    def test_dusuk_sicaklik_keskinlestirir(self):
        self.assertEqual(self.secimler(sicaklik=0.05), {0})
        self.assertEqual(self.secimler(sicaklik=1.0), {0, 1, 2, 3})


if __name__ == "__main__":
    unittest.main()
