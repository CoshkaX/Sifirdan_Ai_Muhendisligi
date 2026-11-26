# Faz 3 – Ders 5: Optimizasyon: SGD, momentum ve Adam

> ⏱️ Tahmini süre: 50-65 dk · 📚 Ön koşul: 1.3 Türev ve gradyan, 3.3 Geri yayılım · 💻 Gereksinim: Python 3.11+, ek paket yok

## Bu derste ne öğreneceksin?

- Düz gradyan inişinin dar vadilerde neden yavaşladığını
- Öğrenme hızı biraz fazla seçilince neden her şeyin bozulabildiğini
- **Momentum**'un geçmiş adımları hatırlayarak nasıl hızlandığını
- **Adam**'ın her parametre için adım büyüklüğünü nasıl ayarladığını
- Veriyi **mini-batch**'lere bölerek eğitmenin ne demek olduğunu

## 1. Problem

Şimdiye kadar parametreleri hep aynı kuralla güncelledik:

`yeni ağırlık = eski ağırlık - öğrenme hızı × türev`

Buna **gradyan inişi** veya kütüphanelerdeki adıyla **SGD** denir. Basit ve işe yarar, ama bir zayıflığı var: Bütün parametreler için **tek bir öğrenme hızı** kullanır.

Kaybın bir yönde çok dik, başka bir yönde çok yatık olduğunu düşün; dar ve uzun bir vadi gibi. Dik yönde küçük adım atmak gerekir, yoksa vadinin bir duvarından ötekine zıplarsın. Ama aynı küçük adım yatık yönde çok yavaş ilerler. Gerçek sinir ağlarının kayıp yüzeyleri bu tür vadilerle doludur. Bu derste bu sorunu çözmek için geliştirilmiş iki yöntemi, **momentum**'u ve **Adam**'ı sıfırdan yazacağız.

Deneme alanımız şu kayıp fonksiyonu olacak:

`kayıp(x, y) = x² + 50 × y²`

En küçük değeri `(0, 0)` noktasında. `y` yönü `x` yönünden 50 kat daha dik. Türevler: `x`'e göre `2x`, `y`'ye göre `100y`. Her yöntem `(5, 1)` noktasından başlayacak ve kayıp `0.001`'in altına inene kadar kaç adım attığını sayacağız.

## 2. Kendin yaz

### 2.1 Düz gradyan inişi (SGD)

```python {.python-playground}
def turev(x, y):
    return 2 * x, 100 * y


def sgd(ogrenme_hizi):
    x, y = 5.0, 1.0
    for adim in range(1, 501):
        tx, ty = turev(x, y)
        x -= ogrenme_hizi * tx
        y -= ogrenme_hizi * ty
        if x * x + 50 * y * y < 0.001:
            return f"{adim} adımda ulaştı"
    return f"ulaşamadı (son kayıp {x * x + 50 * y * y:.1f})"


for ogrenme_hizi in [0.005, 0.01, 0.019, 0.02]:
    print(f"öğrenme hızı {ogrenme_hizi}: {sgd(ogrenme_hizi)}")
```
```text {.python-playground-expected}
öğrenme hızı 0.005: ulaşamadı (son kayıp 0.0)
öğrenme hızı 0.01: 251 adımda ulaştı
öğrenme hızı 0.019: 131 adımda ulaştı
öğrenme hızı 0.02: ulaşamadı (son kayıp 50.0)
```
```text {.python-playground-help}
`def turev(x, y):` | Kaybın iki parametreye göre türevlerini döndürür. `y`'nin türevi `100y` olduğu için `y` yönü çok daha diktir.
`x, y = 5.0, 1.0` | Her deneme aynı noktadan başlar; böylece yöntemleri adil karşılaştırırız.
`for adim in range(1, 501):` | En fazla 500 adım atarız.
`x -= ogrenme_hizi * tx` | 1.3 dersindeki gradyan inişi: türevin tersi yönünde, öğrenme hızı kadar ölçeklenmiş adım.
`if x * x + 50 * y * y < 0.001:` | Kayıp yeterince küçüldüyse kaçıncı adımda olduğumuzu döndürürüz.
`return f"ulaşamadı ..."` | 500 adımda hedefe varılamadıysa son kaybı gösteririz.
`f"{... :.1f}"` | Sayıyı virgülden sonra bir basamakla yazar.
```

Sonuçları oku:

- `0.005` çok küçük: 500 adımda bile hedefe varamadı. Kayıp `0.0` gibi görünüyor, ama bu yalnızca bir basamağa yuvarlandığı için; aslında hâlâ `0.001`'in biraz üstünde.
- `0.019` en hızlısı: 131 adım.
- `0.02` biraz daha büyük, ama tamamen başarısız. `y` her adımda `1`'den `-1`'e, sonra tekrar `1`'e zıplıyor ve kayıp hep `50` kalıyor.

`0.019` ile `0.02` arasındaki bu keskin sınır, dik yönden kaynaklanıyor: `y` yönü öğrenme hızına izin verilen üst sınırı belirliyor; `x` yönü ise o küçük adımla yavaş yavaş ilerlemek zorunda kalıyor.

### 2.2 Momentum: yokuştan aşağı yuvarlanan top

Yokuştan aşağı yuvarlanan bir top düşün. Top yalnızca o anki eğime bakmaz; önceki hızını da taşır. Aynı yönde giderken hızlanır, yön sürekli değişiyorsa (vadinin iki duvarı arasında gidip gelirken) zıt itmeler birbirini kısmen siler.

**Momentum** bu fikri kullanır. Her parametre için bir **hız** tutar:

```text
hız = β × hız + türev
ağırlık = ağırlık - öğrenme hızı × hız
```

`β` (beta) genellikle `0.9` seçilir: hızın %90'ı bir sonraki adıma taşınır.

```python {.python-playground}
def turev(x, y):
    return 2 * x, 100 * y


def momentum(ogrenme_hizi, beta=0.9):
    x, y = 5.0, 1.0
    hiz_x, hiz_y = 0.0, 0.0
    for adim in range(1, 501):
        tx, ty = turev(x, y)
        hiz_x = beta * hiz_x + tx
        hiz_y = beta * hiz_y + ty
        x -= ogrenme_hizi * hiz_x
        y -= ogrenme_hizi * hiz_y
        if x * x + 50 * y * y < 0.001:
            return f"{adim} adımda ulaştı"
    return "ulaşamadı"


print("Momentum, öğrenme hızı 0.015:", momentum(0.015))
```
```text {.python-playground-expected}
Momentum, öğrenme hızı 0.015: 84 adımda ulaştı
```
```text {.python-playground-help}
`hiz_x, hiz_y = 0.0, 0.0` | Top durgun başlar; hız sıfırdır.
`hiz_x = beta * hiz_x + tx` | Önceki hızın %90'ını korur, üstüne yeni türevi ekleriz. `x` yönünde türev hep aynı işaretli olduğundan hız birikir ve ilerleme hızlanır.
`hiz_y = beta * hiz_y + ty` | `y` yönünde türev her adımda işaret değiştirir; eski hız ile yeni türev birbirini kısmen siler, zıplama azalır.
`x -= ogrenme_hizi * hiz_x` | Güncellemede türevin kendisi yerine hız kullanılır.
`momentum(0.015)` | Aynı başlangıç noktası, aynı hedef; yalnızca güncelleme kuralı farklı.
```

Momentum 131 yerine 84 adımda vardı. Daha da önemlisi, birikmiş hız sayesinde yatık `x` yönünde hızlandı.

### 2.3 Adam: her parametreye kendi adım büyüklüğü

**Adam** (adaptive moment estimation), bugün en sık kullanılan optimizasyon yöntemidir. Momentum'daki hıza ek olarak her parametrenin türevlerinin **ne kadar büyük olduğunu** da takip eder ve adımı buna böler:

- Türevi hep büyük olan parametre (dik `y` yönü) → bölen büyük → **küçük adım**
- Türevi hep küçük olan parametre (yatık `x` yönü) → bölen küçük → **büyük adım**

Böylece tek bir öğrenme hızı, her yön için ayrı ayrı uygun boyuta gelir.

```text
m = β1 × m + (1 - β1) × türev           # türevlerin ortalaması (yön)
v = β2 × v + (1 - β2) × türev²          # türev karelerinin ortalaması (büyüklük)
m̂ = m / (1 - β1^adım)                   # başlangıçtaki sıfırlardan kaynaklı sapmayı düzelt
v̂ = v / (1 - β2^adım)
ağırlık = ağırlık - öğrenme hızı × m̂ / (√v̂ + ε)
```

```python {.python-playground}
import math


def turev(x, y):
    return 2 * x, 100 * y


def adam(ogrenme_hizi, beta1=0.9, beta2=0.999, epsilon=1e-8):
    params = [5.0, 1.0]
    m = [0.0, 0.0]
    v = [0.0, 0.0]
    for adim in range(1, 501):
        turevler = turev(params[0], params[1])
        for i in range(2):
            m[i] = beta1 * m[i] + (1 - beta1) * turevler[i]
            v[i] = beta2 * v[i] + (1 - beta2) * turevler[i] ** 2
            m_duzeltilmis = m[i] / (1 - beta1 ** adim)
            v_duzeltilmis = v[i] / (1 - beta2 ** adim)
            params[i] -= ogrenme_hizi * m_duzeltilmis / (math.sqrt(v_duzeltilmis) + epsilon)
        x, y = params
        if x * x + 50 * y * y < 0.001:
            return f"{adim} adımda ulaştı"
    return "ulaşamadı"


print("Adam, öğrenme hızı 0.5:", adam(0.5))
```
```text {.python-playground-expected}
Adam, öğrenme hızı 0.5: 67 adımda ulaştı
```
```text {.python-playground-help}
`params = [5.0, 1.0]` | İki parametreyi (`x` ve `y`) bir listede tutarız; böylece aynı kuralı döngüyle ikisine de uygularız.
`m = [0.0, 0.0]` | Her parametre için türevlerin ortalaması; momentum'daki hızın benzeri.
`v = [0.0, 0.0]` | Her parametre için türev karelerinin ortalaması; türevin tipik büyüklüğünü ölçer.
`m[i] = beta1 * m[i] + (1 - beta1) * turevler[i]` | Eski ortalamanın %90'ı ile yeni türevin %10'unu karıştırırız.
`v[i] = beta2 * v[i] + (1 - beta2) * turevler[i] ** 2` | Kare aldığımız için işaret kaybolur; yalnızca büyüklük kalır.
`m[i] / (1 - beta1 ** adim)` | `m` sıfırdan başladığı için ilk adımlarda gerçek ortalamadan küçük kalır; bu bölme o sapmayı düzeltir. Adım sayısı arttıkça etkisi kaybolur.
`math.sqrt(v_duzeltilmis) + epsilon` | Türevin tipik büyüklüğü. `epsilon` sıfıra bölmeyi önleyen çok küçük bir sayıdır.
`params[i] -= ...` | Adım ≈ öğrenme hızı × (yön / büyüklük). Büyüklükle böldüğümüz için her parametre benzer boyda adım atar.
```

Adam 67 adımda vardı. Burada öğrenme hızı `0.5` kadar büyük olmasına rağmen dik `y` yönünde zıplama olmadı; çünkü Adam o yöndeki büyük türevleri bölerek adımı kendisi küçülttü. SGD'de `0.02` bile felakete yol açmıştı.

!!! note "Hangisi en iyisi?"
    Bu yarış tek bir fonksiyonda yapıldı; başka bir problemde sıralama değişebilir. Pratikte **Adam** çoğu problemde ayarla fazla uğraşmadan iyi çalıştığı için varsayılan tercih olarak kullanılır. **SGD + momentum** ise bazı görüntü modelleri gibi alanlarda dikkatli ayarlandığında hâlâ çok iyi sonuç verir.

### 2.4 Mini-batch: veriyi parça parça kullan

Şimdiye kadar her güncellemede **bütün** örneklerin türevini hesapladık. XOR'da 4 örnek vardı; gerçek veri setlerinde milyonlarca örnek olur. Tek bir adım atmak için hepsini dolaşmak çok yavaştır.

Bunun yerine veriyi karıştırıp küçük parçalara, yani **mini-batch**'lere böleriz. Her parçanın türeviyle bir adım atarız. Bütün parçalar bir kez kullanılınca bir **tur** (epoch) tamamlanmış olur.

```python {.python-playground}
import random

veri = list(range(1, 11))   # 10 örneği temsil eden sayılar
batch_boyutu = 4

rastgele = random.Random(0)
karisik = veri.copy()
rastgele.shuffle(karisik)

for i in range(0, len(karisik), batch_boyutu):
    batch = karisik[i:i + batch_boyutu]
    print("Bu adımda kullanılan örnekler:", batch)
```
```text {.python-playground-expected}
Bu adımda kullanılan örnekler: [8, 9, 2, 6]
Bu adımda kullanılan örnekler: [4, 5, 3, 1]
Bu adımda kullanılan örnekler: [10, 7]
```
```text {.python-playground-help}
`veri = list(range(1, 11))` | Örnekleri temsil etmek için 1'den 10'a kadar sayılar kullanırız.
`batch_boyutu = 4` | Her güncellemede kaç örnek kullanılacağı.
`rastgele = random.Random(0)` | Sabit başlangıç sayısıyla karıştırırız; böylece her çalıştırmada aynı sonucu görürsün (2.4 dersindeki gibi).
`rastgele.shuffle(karisik)` | Örneklerin sırasını karıştırırız. Her turda yeniden karıştırmak, modelin hep aynı sırayı görmesini önler.
`range(0, len(karisik), batch_boyutu)` | `0, 4, 8` başlangıç konumlarını üretir; üçüncü argüman adım büyüklüğüdür.
`karisik[i:i + batch_boyutu]` | Dilimleme ile o parçanın örneklerini alırız. Son parça daha kısa olabilir.
```

10 örnek ve 4'lük parçalarla bir tur üç güncellemeden oluşur. Her parça bütün verinin yalnızca bir bölümü olduğu için türevi biraz "gürültülüdür"; ama adımlar çok daha ucuzdur ve bu gürültü çoğu zaman öğrenmeye zarar vermez, hatta yardımcı olabilir. "SGD" adındaki "S" (stochastic, yani rastlantısal) buradan gelir.

### Şimdi sen yaz: momentum adımı

`x²` kaybını küçültmek için üç momentum adımı at. `# TODO` yazan yerlerdeki `___` boşluklarını tamamla, sonra çalıştır.

```python {.python-playground-task}
def turev(x):
    return 2 * x          # kayıp: x²


x = 4.0
hiz = 0.0
ogrenme_hizi = 0.1
beta = 0.9

for adim in range(1, 4):
    # TODO: hız = beta × eski hız + yeni türev.
    hiz = ___
    # TODO: x'i hızın ters yönünde güncelle.
    x = x - ___ * hiz
    print(f"Adım {adim}: x = {x:.3f}")
```
```text {.python-playground-expected}
Adım 1: x = 3.200
Adım 2: x = 1.840
Adım 3: x = 0.248
```
```text {.python-playground-help}
`hiz = ___` | Önceki hızın `beta` kadarı korunur, üstüne yeni türev eklenir: `beta * hiz + turev(x)`.
`x = x - ___ * hiz` | Güncellemede türev yerine hız kullanılır; adım büyüklüğü öğrenme hızıdır.
```
```python {.python-playground-solution}
def turev(x):
    return 2 * x          # kayıp: x²


x = 4.0
hiz = 0.0
ogrenme_hizi = 0.1
beta = 0.9

for adim in range(1, 4):
    # hız = beta × eski hız + yeni türev.
    hiz = beta * hiz + turev(x)
    # x'i hızın ters yönünde güncelle.
    x = x - ogrenme_hizi * hiz
    print(f"Adım {adim}: x = {x:.3f}")
```

## 3. Kütüphaneyle yap

PyTorch'ta bu yöntemlerin hepsi hazırdır ve aynı biçimde kullanılır. Yalnızca optimizer satırı değişir:

```python
import torch

parametreler = [torch.nn.Parameter(torch.tensor([5.0, 1.0]))]

optimizer = torch.optim.SGD(parametreler, lr=0.019)
# optimizer = torch.optim.SGD(parametreler, lr=0.015, momentum=0.9)
# optimizer = torch.optim.Adam(parametreler, lr=0.5)

for adim in range(1, 501):
    x, y = parametreler[0]
    kayip = x ** 2 + 50 * y ** 2
    if kayip.item() < 0.001:
        print(adim - 1, "adımda ulaştı")
        break
    optimizer.zero_grad()
    kayip.backward()
    optimizer.step()
```

Her adımda üç satır tekrar eder: `zero_grad()` eski türevleri sıfırlar (3.2 dersindeki `+=` birikmesini hatırla), `backward()` türevleri hesaplar, `step()` seçtiğin kurala göre parametreleri günceller. Yorum satırlarındaki optimizer'ları sırayla deneyip adım sayılarını bu dersin sonuçlarıyla karşılaştır. PyTorch'un momentum ve Adam formülleri bizimkilerle aynıdır. PyTorch varsayılan olarak daha az basamaklı sayılarla (float32) hesap yaptığı için adım sayısı bazen bir adım farklı çıkabilir.

## 4. Sık yapılan hatalar

- **Öğrenme hızını "biraz büyük olsa da olur" sanmak.** 2.1'de `0.019` iyi çalışırken `0.02` tamamen başarısız oldu. Kayıp düşmek yerine zıplıyor veya artıyorsa önce öğrenme hızını küçült.
- **Momentum'da hızı sıfırlamak.** Hız değişkeni turlar boyunca korunmalıdır; her adımda sıfırlarsan düz SGD'ye dönersin.
- **Adam'da düzeltme adımını unutmak.** `m` ve `v` sıfırdan başladığı için ilk adımlarda çok küçük kalırlar; `1 - β^adım` ile bölmezsen ilk adımlar yanlış boyda olur.
- **Farklı optimizer'lar için aynı öğrenme hızını kullanmak.** Adam için uygun bir öğrenme hızı SGD'yi patlatabilir. Her yöntemin kendi uygun aralığı vardır.
- **`zero_grad()` çağırmayı unutmak.** PyTorch türevleri biriktirir; sıfırlamazsan her adım öncekilerin toplamıyla güncellenir.
- **Mini-batch'leri karıştırmamak.** Veri sıralıysa (örneğin önce bütün `0` etiketliler) her parça tek bir sınıftan oluşur ve model ileri geri savrulur.

## 5. Pekiştir

**Quiz**

1. Tek bir öğrenme hızı dar bir vadide neden sorun çıkarır?
2. Momentum'daki `β = 0.9` ne anlama gelir?
3. Adam, türevi büyük olan bir parametre için neden daha küçük adım atar?
4. Adam'daki `1 - β^adım` bölmesi neden gerekli?
5. Mini-batch ve tur (epoch) arasındaki fark nedir?

**Alıştırmalar**

1. 2.1'de öğrenme hızını `0.021` yap ve `return` satırından önce `print(round(y, 2))` ekleyerek `y`'nin her adımda nasıl değiştiğini izle. Ne oluyor?
2. 2.2'de `beta` değerini `0` yap. Sonuç neden 2.1'deki SGD ile aynı türden davranır? Sonra `0.99` dene.
3. 2.3'te öğrenme hızını `0.1` ve `1.0` yap. Adam her ikisinde de hedefe ulaşıyor mu?
4. Kayıp fonksiyonunu `x² + y²` yap (türevler `2x` ve `2y`). Üç yöntemin adım sayıları nasıl değişti? Vadi dar değilken momentum ve Adam'ın avantajı sürüyor mu?
5. (İsteğe bağlı) 2.4'te `batch_boyutu` değerini `1`, `3` ve `10` yap. Bir turda kaç güncelleme yapılıyor?

??? success "Quiz cevapları"
    1. Dik yön küçük öğrenme hızı ister, yoksa zıplar; yatık yön bu küçük adımla çok yavaş ilerler. Tek sayı iki yöne birden uyamaz.
    2. Her adımda önceki hızın %90'ının korunması; top geçmiş hareketini büyük ölçüde hatırlar.
    3. Adımı, türevin tipik büyüklüğüne (`√v̂`) böler. Büyük türevler büyük bölen demektir.
    4. `m` ve `v` sıfırdan başladığı için ilk adımlarda gerçek değerlerinden küçük kalırlar; bu bölme o sapmayı düzeltir.
    5. Mini-batch, tek bir güncellemede kullanılan küçük örnek grubudur. Tur, bütün verinin bir kez kullanılmasıdır; bir tur birçok mini-batch güncellemesinden oluşur.

## Özet

Düz gradyan inişi (SGD) bütün parametreler için tek bir öğrenme hızı kullanır; dar vadilerde dik yön öğrenme hızını sınırlar, yatık yön yavaş ilerler. Momentum geçmiş adımlardan bir hız biriktirerek tutarlı yönlerde hızlanır ve zıplamaları azaltır. Adam ise her parametrenin türev büyüklüğünü takip ederek adımları ayrı ayrı ölçekler ve pratikte varsayılan tercih olarak kullanılır. Büyük veri setlerinde güncellemeler, karıştırılmış mini-batch'ler üzerinden yapılır.

## Kaynaklar

- Diederik P. Kingma ve Jimmy Ba (2015), *Adam: A Method for Stochastic Optimization*, ICLR
- Sebastian Ruder (2016), *An overview of gradient descent optimization algorithms*: [ruder.io/optimizing-gradient-descent](https://www.ruder.io/optimizing-gradient-descent/)
- [Distill: Why Momentum Really Works](https://distill.pub/2017/momentum/)
- [PyTorch resmî belgesi: `torch.optim`](https://pytorch.org/docs/stable/optim.html)
