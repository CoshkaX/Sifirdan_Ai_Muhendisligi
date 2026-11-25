"""Ders 3.2 – Mini autograd: türevleri otomatik hesaplayan küçük bir motor.

Ek paket gerektirmez. Çalıştır:  python kod/mini_autograd.py

Her `Deger` nesnesi bir sayıyı (`veri`) ve sonuçta oluşan çıktının bu sayıya
göre türevini (`grad`) tutar. Toplama, çarpma gibi işlemler yeni bir `Deger`
üretirken "türev geri nasıl dağıtılır?" bilgisini de yanına kaydeder.
`geri_yay()` çağrılınca zincir kuralı sondan başa doğru uygulanır.
"""

import math


class Deger:
    def __init__(self, veri, girdiler=(), islem=""):
        self.veri = float(veri)
        self.grad = 0.0
        self._girdiler = girdiler
        self._islem = islem  # hata ayıklarken hangi işlemden geldiğini görmek için
        self._geri = lambda: None

    def __repr__(self):
        return f"Deger(veri={self.veri:.4g}, grad={self.grad:.4g})"

    # --- temel işlemler -------------------------------------------------
    def __add__(self, diger):
        diger = diger if isinstance(diger, Deger) else Deger(diger)
        sonuc = Deger(self.veri + diger.veri, (self, diger), "+")

        def _geri():
            # Toplamada yerel türev 1'dir: gelen türev olduğu gibi aktarılır.
            self.grad += sonuc.grad
            diger.grad += sonuc.grad

        sonuc._geri = _geri
        return sonuc

    def __mul__(self, diger):
        diger = diger if isinstance(diger, Deger) else Deger(diger)
        sonuc = Deger(self.veri * diger.veri, (self, diger), "*")

        def _geri():
            # a * b işleminde a'ya göre türev b, b'ye göre türev a'dır.
            self.grad += diger.veri * sonuc.grad
            diger.grad += self.veri * sonuc.grad

        sonuc._geri = _geri
        return sonuc

    def __pow__(self, us):
        if not isinstance(us, (int, float)):
            raise TypeError("Üs yalnızca sabit bir sayı olabilir.")
        sonuc = Deger(self.veri ** us, (self,), f"**{us}")

        def _geri():
            self.grad += us * self.veri ** (us - 1) * sonuc.grad

        sonuc._geri = _geri
        return sonuc

    def __neg__(self):
        return self * -1

    def __sub__(self, diger):
        return self + (-diger)

    # 2 + x veya 3 * x gibi, sayının solda olduğu durumlar için
    def __radd__(self, diger):
        return self + diger

    def __rmul__(self, diger):
        return self * diger

    def __rsub__(self, diger):
        return Deger(diger) - self

    # --- aktivasyonlar --------------------------------------------------
    def sigmoid(self):
        s = 1 / (1 + math.exp(-self.veri))
        sonuc = Deger(s, (self,), "sigmoid")

        def _geri():
            self.grad += s * (1 - s) * sonuc.grad

        sonuc._geri = _geri
        return sonuc

    def relu(self):
        sonuc = Deger(max(0.0, self.veri), (self,), "relu")

        def _geri():
            self.grad += (1.0 if self.veri > 0 else 0.0) * sonuc.grad

        sonuc._geri = _geri
        return sonuc

    # --- geri yayılım ---------------------------------------------------
    def geri_yay(self):
        """Bu değerden başlayıp bütün girdilere zincir kuralını uygular."""
        sira = []
        ziyaret_edilen = set()

        def dolas(deger):
            if deger in ziyaret_edilen:
                return
            ziyaret_edilen.add(deger)
            for girdi in deger._girdiler:
                dolas(girdi)
            sira.append(deger)  # girdileri her zaman kendisinden önce eklenir

        dolas(self)
        self.grad = 1.0
        for deger in reversed(sira):
            deger._geri()


def main() -> None:
    a = Deger(3)
    b = Deger(-2)
    c = Deger(4)
    f = Deger(-3)

    e = a * b          # -6
    d = e + c          # -2
    sonuc = d * f      #  6

    sonuc.geri_yay()
    print("sonuc =", sonuc.veri)
    for ad, deger in [("a", a), ("b", b), ("c", c), ("f", f)]:
        print(f"d(sonuc)/d{ad} = {deger.grad}")

    print("\nAynı değişken iki kez kullanılırsa:")
    x = Deger(3)
    y = x * x + x      # türevi 2x + 1 = 7
    y.geri_yay()
    print("y =", y.veri, " dy/dx =", x.grad)


if __name__ == "__main__":
    main()
