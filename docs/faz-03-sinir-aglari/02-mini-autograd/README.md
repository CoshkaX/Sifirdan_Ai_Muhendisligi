# Faz 3 – Ders 2: Mini autograd

> ⏱️ Tahmini süre: 60-75 dk · 📚 Ön koşul: 0.2 Python hızlı tekrar (sınıflar), 1.3 Türev ve gradyan, 3.1 Tek nöron · 💻 Gereksinim: Python 3.11+, ek paket yok; PyTorch örneği isteğe bağlı

## Bu derste ne öğreneceksin?

- Zincir kuralıyla iç içe bir hesabın türevini adım adım bulmayı
- Bir hesabı küçük işlemlerden oluşan bir **hesaplama grafiği** olarak düşünmeyi
- Türevleri otomatik hesaplayan küçük bir `Deger` sınıfı yazmayı
- Aynı değişken birden fazla kez kullanıldığında türevlerin neden toplandığını
- PyTorch'un `backward()` işleminin arkasındaki fikri

## 1. Problem

1.3 dersinde `kayıp = (ağırlık - 4)²` gibi tek bir formülün türevini elle bulduk. Gerçek bir sinir ağında ise kayıp, binlerce ağırlığın çarpılıp toplanmasından ve aktivasyonlardan geçmesinden oluşur. Her ağırlık için türevi elle yazmak imkânsızdır.

Çözüm şu gözleme dayanır: Ne kadar büyük olursa olsun, her hesap küçük adımlardan oluşur (toplama, çarpma, sigmoid...). Her küçük adımın türevini biliyoruz. **Zincir kuralı**, bu küçük türevleri çarparak bütün hesabın türevini bulmamızı sağlar. Bunu bilgisayara yaptıran sisteme **otomatik türev alma** (automatic differentiation, kısaca **autograd**) denir.

Bu derste, birkaç düzine satırlık kendi autograd motorumuzu yazacağız. Sonraki derslerde sinir ağlarını bu fikirle eğiteceğiz.

## 2. Kendin yaz

### 2.1 Zincir kuralı: türevi adım adım geri taşı

Şu hesabı düşün: `sonuc = (a × b + c) × f`. Değerler `a = 3`, `b = -2`, `c = 4`, `f = -3` olsun. Hesabı ara adımlara bölelim:

```text
e = a × b        →  3 × (-2) = -6
d = e + c        →  -6 + 4   = -2
sonuc = d × f    →  -2 × (-3) = 6
```

Şimdi her değişkenin `sonuc`'u ne kadar etkilediğini, yani `sonuc`'un ona göre türevini bulalım. Sondan başlarız:

- `sonuc = d × f` olduğundan: `d`'ye göre türev `f = -3`, `f`'ye göre türev `d = -2`.
- `d = e + c` olduğundan: toplama, gelen türevi olduğu gibi iletir. `e` ve `c`'nin türevi de `-3` olur.
- `e = a × b` olduğundan: `a`'nın türevi `b × (e'nin türevi) = -2 × -3 = 6`; `b`'nin türevi `a × (e'nin türevi) = 3 × -3 = -9`.

Bu "gelen türevi yerel türevle çarp ve geriye aktar" kuralına **zincir kuralı** denir.

```python {.python-playground}
a, b, c, f = 3, -2, 4, -3

# İleri hesap
e = a * b
d = e + c
sonuc = d * f

# Geri hesap: sondan başa doğru
d_sonuc = 1
d_d = f * d_sonuc
d_f = d * d_sonuc
d_e = 1 * d_d
d_c = 1 * d_d
d_a = b * d_e
d_b = a * d_e

print("sonuc =", sonuc)
print("Türevler: a =", d_a, "b =", d_b, "c =", d_c, "f =", d_f)
```
```text {.python-playground-expected}
sonuc = 6
Türevler: a = 6 b = -9 c = -3 f = -2
```
```text {.python-playground-help}
`a, b, c, f = 3, -2, 4, -3` | Dört değişkene tek satırda değer veririz; sırayla eşleşirler.
`e = a * b` | İleri hesabın ilk adımı. Ara sonuçları ayrı değişkenlerde tutarız, çünkü geri hesapta onlara ihtiyacımız olacak.
`d_sonuc = 1` | `sonuc`'un kendisine göre türevi her zaman `1`'dir. Geri hesap buradan başlar.
`d_d = f * d_sonuc` | `sonuc = d × f` olduğundan `d`'ye göre yerel türev `f`'dir; gelen türevle çarparız.
`d_f = d * d_sonuc` | Aynı çarpmada `f`'ye göre yerel türev `d`'dir.
`d_e = 1 * d_d` | `d = e + c` toplamasında yerel türev `1`'dir; gelen türev olduğu gibi geçer.
`d_a = b * d_e` | `e = a × b` çarpmasında `a`'ya göre yerel türev `b`'dir. Zincir kuralı: yerel türev × gelen türev.
`print(...)` | Bulduğumuz türevleri gösteririz. Örneğin `a = 6`, "a'yı biraz artırırsan sonuç bunun 6 katı kadar artar" demektir.
```

Kontrol etmek için `a`'yı `3`'ten `3.001`'e çıkar ve `sonuc`'u yeniden hesapla. Sonuç yaklaşık `6 × 0.001 = 0.006` kadar artmalıdır. Bu, 1.3 dersindeki sonlu fark yöntemidir.

### 2.2 `Deger` sınıfı: türevi kendisi hesaplayan sayılar

Elle yazdığımız geri hesabı her ifade için yeniden yazmak istemeyiz. Bunun yerine her sayıyı bir **`Deger`** nesnesine sararız. Her işlem iki şey yapar:

1. Sonucu hesaplar (ileri hesap).
2. Sonucun hangi değerlerden geldiğini ve türevin onlara nasıl dağıtılacağını hatırlar.

Bu bağlantılar bir **hesaplama grafiği** oluşturur. `geri_yay()` çağırınca grafik sondan başa dolaşılır ve her düğüm kendi türev kuralını uygular.

```python {.python-playground}
class Deger:
    def __init__(self, veri, girdiler=()):
        self.veri = veri
        self.grad = 0.0
        self._girdiler = girdiler
        self._geri = lambda: None

    def __add__(self, diger):
        sonuc = Deger(self.veri + diger.veri, (self, diger))
        def _geri():
            self.grad += sonuc.grad
            diger.grad += sonuc.grad
        sonuc._geri = _geri
        return sonuc

    def __mul__(self, diger):
        sonuc = Deger(self.veri * diger.veri, (self, diger))
        def _geri():
            self.grad += diger.veri * sonuc.grad
            diger.grad += self.veri * sonuc.grad
        sonuc._geri = _geri
        return sonuc

    def geri_yay(self):
        sira = []
        ziyaret_edilen = set()
        def dolas(deger):
            if deger not in ziyaret_edilen:
                ziyaret_edilen.add(deger)
                for girdi in deger._girdiler:
                    dolas(girdi)
                sira.append(deger)
        dolas(self)
        self.grad = 1.0
        for deger in reversed(sira):
            deger._geri()


a, b, c, f = Deger(3), Deger(-2), Deger(4), Deger(-3)
sonuc = (a * b + c) * f
sonuc.geri_yay()

print("sonuc =", sonuc.veri)
print("Türevler: a =", a.grad, "b =", b.grad, "c =", c.grad, "f =", f.grad)
```
```text {.python-playground-expected}
sonuc = 6
Türevler: a = 6.0 b = -9.0 c = -3.0 f = -2.0
```
```text {.python-playground-help}
`self.veri = veri` | Nesnenin taşıdığı sayıdır.
`self.grad = 0.0` | Sonucun bu sayıya göre türevi. Geri yayılımdan önce sıfırdır.
`self._girdiler = girdiler` | Bu değer hangi değerlerden hesaplandı? `a * b` sonucu için `(a, b)` olur. Başlangıç değerlerinin girdisi yoktur.
`self._geri = lambda: None` | Türevi girdilere dağıtacak fonksiyon. Başlangıç değerleri için hiçbir şey yapmaz.
`def __add__(self, diger):` | Python `a + b` yazınca bu metodu çağırır. Böylece `+` işaretini kendi sınıfımız için tanımlarız.
`self.grad += sonuc.grad` | Toplamanın yerel türevi `1`'dir; sonucun türevini olduğu gibi ekleriz.
`def __mul__(self, diger):` | `a * b` yazınca çağrılır.
`self.grad += diger.veri * sonuc.grad` | Çarpmada `a`'nın yerel türevi `b`'nin değeridir. Zincir kuralı: yerel türev × gelen türev.
`sonuc._geri = _geri` | Türev kuralını sonuç nesnesine iliştiririz; geri yayılımda çağrılacak.
`def dolas(deger):` | Grafiği dolaşıp her değeri, kendi girdilerinden **sonra** listeye ekler. Böylece listeyi ters çevirince sondan başa doğru doğru sırayı elde ederiz.
`self.grad = 1.0` | Sonucun kendisine göre türevi `1`'dir; geri yayılım buradan başlar.
`for deger in reversed(sira): deger._geri()` | Sondan başa her düğüm, türevini girdilerine dağıtır.
`sonuc = (a * b + c) * f` | Artık normal Python yazımıyla hesap yaparız; grafik arka planda kendiliğinden kurulur.
```

Sonuçlar 2.1'deki elle hesapla aynı. Fark şu: Artık istediğin ifadeyi yazabilirsin; geri hesabı sınıf kendisi yapar. `sonuc` ifadesini `(a + b) * (c + f)` gibi başka bir şeyle değiştirip türevleri kâğıtta kontrol et.

### 2.3 Neden `=` değil de `+=`?

Bir değişken hesapta birden fazla yerde kullanılabilir. `y = x × x + x` ifadesinde `x` üç kez geçer. `x`'i biraz değiştirmek `y`'yi üç yoldan birden etkiler; toplam etki bu yolların toplamıdır. Bu yüzden `_geri` fonksiyonları türevi **üzerine ekler** (`+=`). `y = x² + x` için türev `2x + 1`'dir; `x = 3` iken `7` olmalı.

```python {.python-playground}
class Deger:
    def __init__(self, veri, girdiler=()):
        self.veri = veri
        self.grad = 0.0
        self._girdiler = girdiler
        self._geri = lambda: None

    def __add__(self, diger):
        sonuc = Deger(self.veri + diger.veri, (self, diger))
        def _geri():
            self.grad += sonuc.grad
            diger.grad += sonuc.grad
        sonuc._geri = _geri
        return sonuc

    def __mul__(self, diger):
        sonuc = Deger(self.veri * diger.veri, (self, diger))
        def _geri():
            self.grad += diger.veri * sonuc.grad
            diger.grad += self.veri * sonuc.grad
        sonuc._geri = _geri
        return sonuc

    def geri_yay(self):
        sira = []
        ziyaret_edilen = set()
        def dolas(deger):
            if deger not in ziyaret_edilen:
                ziyaret_edilen.add(deger)
                for girdi in deger._girdiler:
                    dolas(girdi)
                sira.append(deger)
        dolas(self)
        self.grad = 1.0
        for deger in reversed(sira):
            deger._geri()


x = Deger(3)
y = x * x + x
y.geri_yay()
print("y =", y.veri)
print("dy/dx =", x.grad)
```
```text {.python-playground-expected}
y = 12
dy/dx = 7.0
```
```text {.python-playground-help}
`class Deger:` | Önceki penceredeki sınıfın aynısı. Her pencere bağımsız çalıştığı için yeniden yazdık.
`x = Deger(3)` | Türevini merak ettiğimiz tek değişken.
`y = x * x + x` | `x` üç yerde kullanılır: çarpmanın iki tarafında ve toplamada.
`y.geri_yay()` | Her kullanım `x.grad` değerine kendi katkısını ekler: çarpmadan `3 + 3`, toplamadan `1`.
`print("dy/dx =", x.grad)` | Katkıların toplamı `7`'dir; bu, `2x + 1` formülünün `x = 3` için değeridir.
```

Sınıftaki `+=` işaretlerini `=` yapıp yeniden çalıştır. Sonuç `7` yerine yanlış bir sayı çıkar; çünkü her yol bir öncekinin katkısının üzerine yazar.

### 2.4 Ders kodu

Kodun tam hâli [`kod/mini_autograd.py`](kod/mini_autograd.py) dosyasında. Orada toplama ve çarpmaya ek olarak çıkarma, üs alma, sayılarla işlem (`2 * x` gibi) ve `sigmoid` ile `relu` aktivasyonları da var. Proje klasöründeyken çalıştır:

```bash
cd docs/faz-03-sinir-aglari/02-mini-autograd
python kod/mini_autograd.py
python -m unittest discover -s test -v
```

Testler, motorun bulduğu türevleri 1.3 dersindeki sonlu fark yöntemiyle karşılaştırır. Bu karşılaştırmaya **gradyan kontrolü** denir ve 3.3 dersinde ayrıntılı göreceğiz.

### Şimdi sen yaz: zincir kuralı

`sonuc = a × b + c` hesabının türevlerini zincir kuralıyla bul. Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur, sonra çalıştır.

```python {.python-playground-task}
a, b, c = 2, 3, 4

# İleri hesap
e = a * b
sonuc = e + c

# Geri hesap: sondan başa doğru
d_sonuc = 1
# TODO: Toplamada gelen türev olduğu gibi geçer.
d_e = ___
d_c = ___
# TODO: Çarpmada a'nın türevi b × d_e, b'nin türevi a × d_e'dir.
d_a = ___
d_b = ___

print("sonuc =", sonuc)
print("Türevler:", d_a, d_b, d_c)
```
```text {.python-playground-expected}
sonuc = 10
Türevler: 3 2 1
```
```text {.python-playground-help}
`d_e = ___` ve `d_c = ___` | Toplamanın yerel türevi `1`'dir. Gelen türev `d_sonuc` ile çarpılır.
`d_a = ___` | Çarpmada `a`'ya göre yerel türev `b`'dir: `b * d_e`.
`d_b = ___` | `b`'ye göre yerel türev `a`'dır: `a * d_e`.
```
```python {.python-playground-solution}
a, b, c = 2, 3, 4

# İleri hesap
e = a * b
sonuc = e + c

# Geri hesap: sondan başa doğru
d_sonuc = 1
# Toplamada gelen türev olduğu gibi geçer.
d_e = 1 * d_sonuc
d_c = 1 * d_sonuc
# Çarpmada a'nın türevi b × d_e, b'nin türevi a × d_e'dir.
d_a = b * d_e
d_b = a * d_e

print("sonuc =", sonuc)
print("Türevler:", d_a, d_b, d_c)
```

## 3. Kütüphaneyle yap

PyTorch'un autograd sistemi aynı fikirle çalışır: `requires_grad=True` olan tensörlerle yapılan her işlem grafiğe kaydedilir, `backward()` zincir kuralını uygular, türevler `.grad` içinde birikir.

```python
import torch

a = torch.tensor(3.0, requires_grad=True)
b = torch.tensor(-2.0, requires_grad=True)
c = torch.tensor(4.0, requires_grad=True)
f = torch.tensor(-3.0, requires_grad=True)

sonuc = (a * b + c) * f
sonuc.backward()

print(sonuc.item(), a.grad.item(), b.grad.item(), c.grad.item(), f.grad.item())
```

Beklenen çıktı:

```text
6.0 6.0 -9.0 -3.0 -2.0
```

Bu kod tarayıcıdaki pencerede çalışmaz. PyTorch'u 1.3 dersinde anlatıldığı gibi resmî kurulum sayfasından kur, kodu `autograd_torch.py` adıyla kaydedip `python autograd_torch.py` ile çalıştır.

Bizim `Deger` sınıfımız tek tek sayılarla çalışır; PyTorch ise aynı işi milyonlarca sayılık tensörlerle ve ekran kartında yapar. Fikir aynıdır.

## 4. Sık yapılan hatalar

- **Türevleri `=` ile yazmak.** Bir değer birden çok yerde kullanılınca katkılar toplanmalıdır; `=` önceki katkıyı siler.
- **Geri yayılımı yanlış sırada yapmak.** Bir düğüm türevini girdilerine dağıtmadan önce kendi türevinin tamamlanmış olması gerekir. Bu yüzden grafik, girdiler önce gelecek biçimde sıralanıp ters çevrilir.
- **`grad` değerlerini sıfırlamayı unutmak.** `geri_yay()` iki kez çağrılırsa türevler üst üste eklenir. Eğitimde her adımdan önce türevler sıfırlanır; PyTorch'taki `optimizer.zero_grad()` bunu yapar.
- **Yerel türevi gelen türevle çarpmayı unutmak.** Zincir kuralı her adımda "yerel türev × sonuçtan gelen türev" demektir.
- **Autograd'ı sihir sanmak.** Motor yalnızca her küçük işlemin türev kuralını bilir ve onları zincirler. Kuralını yazmadığın bir işlemin türevini bulamaz.

## 5. Pekiştir

**Quiz**

1. Zincir kuralı neyi söyler?
2. Toplama işlemi gelen türevi girdilerine nasıl iletir? Çarpma nasıl iletir?
3. `geri_yay()` neden sonucun türevini `1` yaparak başlar?
4. `y = x × x` için `x = 5` iken `x.grad` kaç olur?
5. Türevleri neden `+=` ile biriktiririz?

**Alıştırmalar**

1. 2.1'deki elle hesapta `c`'yi `10` yap. Hangi türevler değişir, hangileri değişmez? Neden?
2. `Deger` penceresinde `sonuc = (a + b) * (c + f)` hesapla. Türevleri önce kâğıtta bul, sonra kodla karşılaştır.
3. `+=` işaretlerini `=` yaparak 2.3'teki örneği bozup sonucun neden değiştiğini açıkla.
4. (İsteğe bağlı) `Deger` sınıfına `__sub__` metodu ekle (`a - b`). İpucu: `a`'ya göre türev `1`, `b`'ye göre türev `-1`'dir.
5. (Zor) `kod/mini_autograd.py` dosyasına `tanh` aktivasyonu ekle. `tanh(x)`'in türevi `1 - tanh(x)²`'dir. Sonucu sonlu farkla kontrol eden bir test yaz.

??? success "Quiz cevapları"
    1. İç içe bir hesapta, bir değişkenin sonuca etkisi, yol üzerindeki yerel türevlerin çarpımıdır.
    2. Toplama gelen türevi değiştirmeden iki girdiye de iletir. Çarpma, her girdiye diğer girdinin değeriyle çarpılmış türevi iletir.
    3. Sonucun kendisine göre türevi `1`'dir; zincir buradan başlar.
    4. `10`; çünkü `x × x` iki yoldan katkı verir: `5 + 5`. Bu, `x²`'nin türevi olan `2x` ile aynıdır.
    5. Aynı değer birden fazla yerde kullanılabilir; her kullanımın sonuca etkisi toplanmalıdır.

## Özet

Her büyük hesap, türevini bildiğimiz küçük işlemlerden oluşur. Zincir kuralı, bu yerel türevleri sondan başa çarparak her değişkenin sonuca etkisini bulur. `Deger` sınıfı her işlemde sonucu hesaplarken türev kuralını da kaydeder ve bir hesaplama grafiği kurar; `geri_yay()` grafiği ters sırada dolaşıp türevleri doldurur. PyTorch'un `backward()` işlemi aynı fikrin büyük ölçekli hâlidir.

## Kaynaklar

- [PyTorch: Otomatik türev alma (autograd) öğreticisi](https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)
- Baydin ve ark. (2018), *Automatic Differentiation in Machine Learning: a Survey*, Journal of Machine Learning Research
- [Python resmî belgesi: özel metotlar (`__add__`, `__mul__`)](https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types)
