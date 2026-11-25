import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kod"))

from mini_autograd import Deger  # noqa: E402


def sayisal_turev(fonksiyon, x, h=1e-6):
    """Sonlu farkla (1.3 dersi) yaklaşık türev."""
    return (fonksiyon(x + h) - fonksiyon(x - h)) / (2 * h)


class MiniAutogradTesti(unittest.TestCase):
    def test_ders_ornegi(self):
        a, b, c, f = Deger(3), Deger(-2), Deger(4), Deger(-3)
        sonuc = (a * b + c) * f
        sonuc.geri_yay()
        self.assertEqual(sonuc.veri, 6)
        self.assertEqual(a.grad, 6)
        self.assertEqual(b.grad, -9)
        self.assertEqual(c.grad, -3)
        self.assertEqual(f.grad, -2)

    def test_ayni_degisken_iki_kez(self):
        x = Deger(3)
        y = x * x + x
        y.geri_yay()
        self.assertEqual(x.grad, 7)

    def test_sayi_ile_islem(self):
        x = Deger(2)
        y = 3 * x + 1 - x ** 2
        y.geri_yay()
        self.assertEqual(y.veri, 3)
        self.assertEqual(x.grad, 3 - 2 * 2)

    def test_sigmoid_sayisal_turevle_ayni(self):
        x0 = 0.7
        x = Deger(x0)
        x.sigmoid().geri_yay()
        beklenen = sayisal_turev(lambda t: 1 / (1 + math.exp(-t)), x0)
        self.assertAlmostEqual(x.grad, beklenen, places=6)

    def test_relu(self):
        pozitif, negatif = Deger(2), Deger(-1)
        (pozitif.relu() + negatif.relu()).geri_yay()
        self.assertEqual(pozitif.grad, 1)
        self.assertEqual(negatif.grad, 0)

    def test_karisik_ifade_sayisal_turevle_ayni(self):
        def ifade(t):
            return (t * t - 2 * t + 5) ** 2

        x0 = 1.3
        x = Deger(x0)
        ifade(x).geri_yay()
        self.assertAlmostEqual(x.grad, sayisal_turev(ifade, x0), places=4)


if __name__ == "__main__":
    unittest.main()
