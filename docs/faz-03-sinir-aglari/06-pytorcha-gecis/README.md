# Faz 3 – Ders 6: PyTorch'a geçiş

> ⏱️ Tahmini süre: 60-75 dk · 📚 Ön koşul: 3.2 Mini autograd, 3.4 Çok katmanlı ağ, 3.5 Optimizasyon · 💻 Gereksinim: Python 3.11+; ilk bölüm ek paketsiz, PyTorch bölümü için PyTorch kurulmalıdır

## Bu derste ne öğreneceksin?

- PyTorch'un temel parçalarının (tensör, `nn.Linear`, kayıp, optimizer) bizim yazdıklarımızdaki karşılıklarını
- Her eğitim döngüsünün aynı beş adımdan oluştuğunu
- Kendi küçük "katman" ve "optimizer" sınıflarımızı yazarak PyTorch'un içini anlamayı
- 3.4 dersindeki XOR ağını PyTorch ile birkaç satırda yeniden kurmayı
- Optimizer'ı ve aktivasyonu tek satırla değiştirmeyi

## 1. Problem

3.4 dersinde XOR ağını yazarken türevleri tek tek elle hesapladık: `g_W1`, `g_W2`, `d_z1`... Katman sayısı arttıkça bu kod hızla uzar ve hata yapmak kolaylaşır. 3.2 dersinde türevleri otomatik bulan bir motor yazdık, ama o motor tek tek sayılarla çalışıyor ve büyük ağlar için çok yavaş.

**PyTorch**, bu dersler boyunca kendi elimizle yazdığımız parçaların hızlı, güvenilir ve büyük ölçekli hâllerini sunan bir kütüphanedir:

| Biz yazdık | PyTorch'taki karşılığı |
|---|---|
| Sayı listeleri, matris çarpımı (1.1, 1.2) | `torch.tensor`, `@` |
| `Deger` sınıfı ve `geri_yay()` (3.2) | `requires_grad=True` ve `.backward()` |
| Ağırlıklı toplam + sabit (3.1) | `nn.Linear` |
| Sigmoid, ReLU (3.1) | `nn.Sigmoid`, `nn.ReLU` |
| Ortalama kare hata (2.2) | `nn.MSELoss` |
| Gradyan inişi, momentum, Adam (3.5) | `torch.optim.SGD`, `torch.optim.Adam` |

Bu derste önce bu parçaların içinde ne olduğunu kendi küçük sürümlerimizle göreceğiz, sonra aynı ağı PyTorch ile kuracağız.

## 2. Kendin yaz

### 2.1 Her eğitim döngüsünün beş adımı

Doğrusal regresyondan büyük dil modellerine kadar hemen her sinir ağı aynı döngüyle eğitilir:

```text
1. Tahmin et        (ileri geçiş)
2. Kaybı hesapla
3. Eski türevleri sıfırla
4. Yeni türevleri hesapla   (geri geçiş)
5. Parametreleri güncelle   (optimizer adımı)
```

Aşağıda bu döngüyü 3.2 dersindeki `Deger` sınıfıyla, PyTorch'a çok benzeyen bir yapıda yazıyoruz. `Dogrusal` sınıfı PyTorch'taki `nn.Linear`'ın, `SGD` sınıfı da `torch.optim.SGD`'nin küçük bir taklidi. Problem olarak 2.2 dersindeki kilogram-fiyat verisini kullanıyoruz; doğru cevap `fiyat = 2 × kilogram`.

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

    def __sub__(self, diger):
        sonuc = Deger(self.veri - diger.veri, (self, diger))
        def _geri():
            self.grad += sonuc.grad
            diger.grad -= sonuc.grad
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
        sira, ziyaret_edilen = [], set()
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


class Dogrusal:                      # nn.Linear(1, 1) taklidi
    def __init__(self):
        self.agirlik = Deger(0.0)
        self.sabit = Deger(0.0)

    def __call__(self, x):
        return self.agirlik * x + self.sabit

    def parametreler(self):
        return [self.agirlik, self.sabit]


class SGD:                           # torch.optim.SGD taklidi
    def __init__(self, parametreler, ogrenme_hizi):
        self.parametreler = parametreler
        self.ogrenme_hizi = ogrenme_hizi

    def sifirla(self):               # optimizer.zero_grad()
        for p in self.parametreler:
            p.grad = 0.0

    def adim(self):                  # optimizer.step()
        for p in self.parametreler:
            p.veri -= self.ogrenme_hizi * p.grad


kilogramlar = [Deger(1.0), Deger(2.0), Deger(3.0)]
fiyatlar = [Deger(2.0), Deger(4.0), Deger(6.0)]

model = Dogrusal()
optimizer = SGD(model.parametreler(), ogrenme_hizi=0.05)

for tur in range(200):
    kayip = Deger(0.0)
    for x, y in zip(kilogramlar, fiyatlar):
        tahmin = model(x)                          # 1. tahmin et
        fark = tahmin - y
        kayip = kayip + fark * fark                # 2. kaybı hesapla
    kayip = kayip * Deger(1 / len(kilogramlar))
    optimizer.sifirla()                            # 3. türevleri sıfırla
    kayip.geri_yay()                               # 4. türevleri hesapla
    optimizer.adim()                               # 5. güncelle

print("Ağırlık:", round(model.agirlik.veri, 2), " Sabit:", round(model.sabit.veri, 2))
print("Son kayıp:", round(kayip.veri, 5))
```
```text {.python-playground-expected}
Ağırlık: 1.97  Sabit: 0.07
Son kayıp: 0.00063
```
```text {.python-playground-help}
`class Deger:` | 3.2 dersindeki sınıf; MSE için bir de çıkarma (`__sub__`) ekledik. Çıkarmada ikinci girdinin yerel türevi `-1` olduğu için `diger.grad -=` yazdık.
`class Dogrusal:` | Bir katman, parametrelerini (ağırlık ve sabit) kendi içinde tutar.
`def __call__(self, x):` | Nesneyi fonksiyon gibi çağırabilmemizi sağlar: `model(x)` yazınca bu metot çalışır. PyTorch'ta da katmanlar böyle çağrılır.
`def parametreler(self):` | Optimizer'ın hangi değerleri güncelleyeceğini bilmesi için parametre listesini döndürür (`model.parameters()`).
`class SGD:` | Optimizer, parametrelerin listesini ve öğrenme hızını tutar.
`p.grad = 0.0` | 3.2 dersinde türevlerin `+=` ile biriktiğini görmüştük; her adımdan önce sıfırlamazsak eski türevler yenilere eklenir.
`p.veri -= self.ogrenme_hizi * p.grad` | Gradyan inişi. Yalnızca sayıyı değiştiririz, grafiğe yeni düğüm eklemeyiz.
`kayip = kayip * Deger(1 / len(kilogramlar))` | Toplam kare hatayı örnek sayısına böleriz; sonuç ortalama kare hatadır (MSE).
`optimizer.sifirla()` ... `optimizer.adim()` | Döngünün kalbi: sıfırla, geri yay, güncelle. PyTorch'ta da tam olarak bu üç satır vardır.
```

Model ağırlığı `2`'ye, sabiti `0`'a yaklaşıyor. 2.2 dersindeki sonuçla aynı yöne gidiyoruz, ama bu kez türevleri elle hiç yazmadık: katman, kayıp ve optimizer birbirinden ayrı parçalar. Turu `200` yerine `1000` yaparsan sonuç `2.0` ve `0.0`'a iyice yaklaşır.

### 2.2 Neden kendi motorumuzla devam etmiyoruz?

`Deger` sınıfı her sayı için ayrı bir Python nesnesi oluşturur. XOR ağında bu birkaç düzine nesne demek; ama milyonlarca parametreli bir dil modelinde milyarlarca nesne olurdu. PyTorch ise:

- Sayıları tek tek değil, **tensör** denen büyük bloklar hâlinde tutar ve işlemleri hızlı C++ kodunda yapar.
- Aynı kodu **ekran kartında (GPU)** çalıştırabilir.
- Yüzlerce hazır katman, kayıp fonksiyonu ve optimizer sunar; bunlar binlerce kişi tarafından test edilmiştir.

Fikir aynı; yalnızca ölçek ve hız farklı.

## 3. Kütüphaneyle yap

### 3.1 Kurulum

PyTorch'u [resmî kurulum sayfasından](https://pytorch.org/get-started/locally/) işletim sistemine uygun komutla kur. Ekran kartın yoksa "CPU" seçeneğini seç; bu dersteki örnekler için yeterlidir. Kurulumdan sonra kontrol et:

```bash
python -c "import torch; print(torch.__version__)"
```

Bilgisayarına kurmak istemezsen kodu [Google Colab](https://colab.research.google.com/)'da çalıştırabilirsin; orada PyTorch hazır kurulu gelir (0.4 dersi).

### 3.2 XOR ağı PyTorch ile

3.4 dersindeki ağın aynısı: 2 girdi → 3 gizli nöron (sigmoid) → 1 çıktı (sigmoid), ortalama kare hata, öğrenme hızı `2.0`, 2000 tur. Sonuçları karşılaştırabilmek için ağırlıkları da 3.4'teki sayılarla başlatıyoruz. Kodu `xor_torch.py` adıyla kaydet ve `python xor_torch.py` ile çalıştır:

```python
import torch
from torch import nn

X = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
Y = torch.tensor([[0.0], [1.0], [1.0], [0.0]])

model = nn.Sequential(
    nn.Linear(2, 3),
    nn.Sigmoid(),
    nn.Linear(3, 1),
    nn.Sigmoid(),
)

# 3.4 dersindeki başlangıç ağırlıkları
with torch.no_grad():
    model[0].weight.copy_(torch.tensor([[0.5, -0.4], [-0.3, 0.8], [0.9, 0.2]]))
    model[0].bias.zero_()
    model[2].weight.copy_(torch.tensor([[0.3, -0.5, 0.4]]))
    model[2].bias.zero_()

kayip_fonksiyonu = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=2.0)

for tur in range(2001):
    tahmin = model(X)                       # 1. tahmin et
    kayip = kayip_fonksiyonu(tahmin, Y)     # 2. kaybı hesapla
    if tur % 500 == 0:
        print(f"Tur {tur}: kayıp {kayip.item():.4f}")
    if tur == 2000:
        break
    optimizer.zero_grad()                   # 3. türevleri sıfırla
    kayip.backward()                        # 4. türevleri hesapla
    optimizer.step()                        # 5. güncelle

with torch.no_grad():
    for x, y, p in zip(X.tolist(), Y.tolist(), model(X).tolist()):
        print(f"{x[0]:.0f} XOR {x[1]:.0f}: hedef {y[0]:.0f}, tahmin {p[0]:.2f}")
```

Beklenen çıktı (3.4 dersindeki sonuçla aynı; PyTorch daha az basamakla hesap yaptığı için son basamaklarda çok küçük farklar görülebilir):

```text
Tur 0: kayıp 0.2511
Tur 500: kayıp 0.0215
Tur 1000: kayıp 0.0036
Tur 1500: kayıp 0.0018
Tur 2000: kayıp 0.0012
0 XOR 0: hedef 0, tahmin 0.01
0 XOR 1: hedef 1, tahmin 0.96
1 XOR 0: hedef 1, tahmin 0.96
1 XOR 1: hedef 0, tahmin 0.05
```

Satır satır karşılıkları:

- `X` ve `Y`: Dört örnek, dört satırlık birer **tensör**. Döngüyle tek tek dolaşmak yerine ağa hepsini birden veririz.
- `nn.Linear(2, 3)`: 2 girdiden 3 nörona giden katman. İçinde `3 × 2` boyutlu bir ağırlık matrisi (3.4'teki `W1`) ve 3 sabit (`b1`) bulunur. Ağırlıklı toplamı `X @ W1ᵀ + b1` matris işlemiyle, bütün örnekler için tek seferde hesaplar.
- `nn.Sequential(...)`: Katmanları sırayla birbirine bağlar; birinin çıktısı sonrakinin girdisi olur.
- `torch.no_grad()`: İçindeki işlemler hesaplama grafiğine kaydedilmez. Ağırlıkları elle ayarlarken ve yalnızca tahmin yaparken kullanırız.
- `nn.MSELoss()`: Ortalama kare hata. 3.4'teki `(p - y)² / 4` toplamının aynısı.
- `model.parameters()`: Ağdaki bütün ağırlık ve sabitler; optimizer bunları günceller.
- Son döngü: `tolist()` tensörleri Python listelerine çevirir; `zip` her girdiyi kendi hedefi ve tahminiyle eşler.

3.4'te yaklaşık 40 satır tutan türev hesabının yerini `kayip.backward()` aldı. Katman eklemek de artık tek satır.

### 3.3 Tek satırla deney yapmak

PyTorch'ta parçalar birbirinden bağımsız olduğu için deney yapmak çok kolaydır:

```python
# Gizli katmanda ReLU kullan
model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 1), nn.Sigmoid())

# Optimizer'ı Adam yap (3.5 dersi)
optimizer = torch.optim.Adam(model.parameters(), lr=0.05)
```

Bu iki satırı yukarıdaki koda koyarsan (ve ağırlıkları elle ayarlayan `with torch.no_grad():` bloğunu silersen) ağırlıklar PyTorch'un kendi rastgele yöntemiyle başlar. Her çalıştırmada aynı sonucu almak için en başa `torch.manual_seed(0)` ekle.

## 4. Sık yapılan hatalar

- **`optimizer.zero_grad()` çağırmayı unutmak.** PyTorch türevleri biriktirir; sıfırlanmazsa her adım önceki adımların türevlerini de içerir. Kayıp tuhaf biçimde zıplıyorsa ilk bakılacak yer burasıdır.
- **`backward()` ile `step()` sırasını karıştırmak.** Önce türevler hesaplanır (`backward`), sonra güncelleme yapılır (`step`).
- **Tahmin yaparken `torch.no_grad()` kullanmamak.** Gereksiz yere grafik kurulur, bellek ve zaman harcanır.
- **Tensör boyutlarını karıştırmak.** `nn.Linear(2, 3)` girdinin son boyutunun `2` olmasını bekler. `Y`'nin boyutunun `(4, 1)` olması da önemlidir; `(4,)` olursa `MSELoss` uyarı verir ve yanlış hesaplayabilir.
- **Python sayısı ile tensörü karıştırmak.** Kayıp bir tensördür; ekrana yazdırırken veya karşılaştırırken `.item()` ile normal sayıya çevir.
- **PyTorch'u sihir sanmak.** İçinde bu fazda yazdığın parçaların aynısı var: ağırlıklı toplam, aktivasyon, zincir kuralı, gradyan inişi. Bir şey ters gidince bu bilgiyle neye bakacağını bilirsin.

## 5. Pekiştir

**Quiz**

1. Bir eğitim döngüsünün beş adımı nelerdir?
2. `nn.Linear(2, 3)` içinde kaç ağırlık ve kaç sabit vardır?
3. `optimizer.zero_grad()` neden her adımda çağrılır?
4. `torch.no_grad()` ne zaman kullanılır?
5. 2.1'deki `Dogrusal` ve `SGD` sınıfları PyTorch'taki hangi parçaların karşılığıdır?

**Alıştırmalar**

1. 2.1'deki pencerede `optimizer.sifirla()` satırını sil. Sonuç neden bozuluyor?
2. 2.1'de fiyatları `[3.0, 5.0, 7.0]` yap ve 1000 tur eğit. Ağırlık ve sabit kaç çıkıyor?
3. XOR kodunda öğrenme hızını `0.5` yap. 3.4 dersindeki alıştırma 2'nin sonucuyla karşılaştır.
4. 3.3'teki ReLU + Adam değişikliğini yap ve `torch.manual_seed(0)` ekle. Ağ kaç turda iyi tahmin yapmaya başlıyor?
5. (İsteğe bağlı) XOR ağına ikinci bir gizli katman ekle: `nn.Linear(3, 3), nn.Sigmoid()`. Elle türev yazmak zorunda olsaydın ne kadar kod eklemen gerekirdi?

??? success "Quiz cevapları"
    1. Tahmin et, kaybı hesapla, eski türevleri sıfırla, yeni türevleri hesapla, parametreleri güncelle.
    2. `3 × 2 = 6` ağırlık ve `3` sabit; toplam 9 parametre.
    3. Türevler `+=` ile birikir. Sıfırlanmazsa güncelleme yalnızca bu adımın değil, önceki bütün adımların türevleriyle yapılır.
    4. Türev gerekmeyen işlemlerde: tahmin yaparken ve ağırlıkları elle değiştirirken.
    5. `Dogrusal` → `nn.Linear`, `SGD` → `torch.optim.SGD`; `sifirla` → `zero_grad`, `adim` → `step`.

## Özet

PyTorch, bu fazda sıfırdan yazdığımız parçaların hızlı ve hazır hâllerini sunar: tensörler, otomatik türev (`backward`), katmanlar (`nn.Linear`), aktivasyonlar, kayıp fonksiyonları ve optimizer'lar. Her eğitim döngüsü aynı beş adımdan oluşur: tahmin et, kaybı hesapla, türevleri sıfırla, geri yay, güncelle. 3.4'teki XOR ağını PyTorch ile kurduğumuzda aynı sonucu çok daha az kodla aldık. Artık daha büyük ağlar ve gerçek veriyle çalışmaya hazırsın.

## Kaynaklar

- [PyTorch resmî öğreticisi: Learn the Basics](https://pytorch.org/tutorials/beginner/basics/intro.html)
- [PyTorch resmî belgesi: `torch.nn`](https://pytorch.org/docs/stable/nn.html)
- [PyTorch resmî belgesi: `torch.optim`](https://pytorch.org/docs/stable/optim.html)
