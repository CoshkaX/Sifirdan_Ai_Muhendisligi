# Faz 5 – Ders 5: Transformer bloğu

> ⏱️ Tahmini süre: 60-75 dk · 📚 Ön koşul: 5.2 Attention, 5.3 Çok başlı attention, 3.4 Çok katmanlı ağ · 💻 Gereksinim: Python 3.11+, ek paket yok; PyTorch örnekleri isteğe bağlı

## Bu derste ne öğreneceksin?

- Bir transformer bloğunun dört parçasını: attention, ileri besleme, normalizasyon, artık bağlantı
- **Katman normalizasyonunun** (layer norm) ne yaptığını ve neden gerektiğini
- **İleri besleme ağının** (feed-forward) her token'ı tek başına işlediğini
- **Artık bağlantının** (residual connection) neden bir vektörü sonuca olduğu gibi taşıdığını
- Bütün parçaları tek bir blokta birleştirip üst üste yığmayı

## 1. Problem

5.2–5.4'te attention'ı kurduk: token'lar birbirine bakıp bilgi karıştırıyor ve konum bilgisi de eklendi. Ama attention tek başına bir model değildir. Çıktısı, değerlerin ağırlıklı **ortalamasıdır**; yani yalnızca doğrusal bir karışım. 3.4'te gördüğümüz gibi doğrusal işlemler tek başına karmaşık örüntüleri öğrenemez. Ayrıca onlarca katmanı üst üste koyarsak sayılar kontrolden çıkar ya da öğrenme durur (3.3'teki kaybolan gradyan).

**Transformer bloğu**, bu sorunları çözen dört parçayı bir araya getirir:

| Parça | Ne yapar? |
|---|---|
| **Attention** | Token'lar arasında bilgi taşır ("kim kime bakıyor?") |
| **İleri besleme ağı** | Her token'ı tek başına, doğrusal olmayan bir ağdan geçirir (3.4'teki gizli katman gibi) |
| **Katman normalizasyonu** | Sayıları dengeli aralıkta tutar; öğrenmeyi kararlı yapar |
| **Artık bağlantı** | Bir parçanın çıktısını girdisine **toplar**; bilgi ve gradyan kestirmeden akar |

Bir transformer modeli, bu bloktan onlarca kez art arda yığılmış hâldir.

## 2. Kendin yaz

### 2.1 Katman normalizasyonu

Bir token'ın vektörünü (örneğin 4 sayı) şöyle normalleştiririz: sayıların **ortalamasını** çıkarır, **standart sapmaya** böleriz. Sonuçta vektörün ortalaması `0`, varyansı `1` olur. Normalleştirme her token'ın kendi sayıları üzerinde yapılır, token'lar arasında değil. Paydaya çok küçük bir sayı (`eps`) ekleriz; bütün sayılar aynıysa varyans `0` olur ve sıfıra bölmeyi önlemek gerekir.

```python {.python-playground}
import math


def layer_norm(x, eps=1e-5):
    ortalama = sum(x) / len(x)
    varyans = sum((v - ortalama) ** 2 for v in x) / len(x)
    return [(v - ortalama) / math.sqrt(varyans + eps) for v in x]


x = [2.0, 4.0, 6.0, 8.0]
y = layer_norm(x)

print("Normalleşmiş:", [round(v, 2) for v in y])
print("Ortalama:", round(sum(y) / len(y), 4))
print("Varyans:", round(sum(v * v for v in y) / len(y), 3))
print("Büyük sayılar:", [round(v, 2) for v in layer_norm([2000.0, 4000.0, 6000.0, 8000.0])])
```
```text {.python-playground-expected}
Normalleşmiş: [-1.34, -0.45, 0.45, 1.34]
Ortalama: 0.0
Varyans: 1.0
Büyük sayılar: [-1.34, -0.45, 0.45, 1.34]
```
```text {.python-playground-help}
`ortalama = sum(x) / len(x)` | Sayıların ortalaması. 1.5'teki ortalama.
`varyans = sum((v - ortalama) ** 2 for v in x) / len(x)` | Her sayının ortalamadan farkının karesinin ortalaması. 1.5'teki varyans.
`(v - ortalama) / math.sqrt(varyans + eps)` | Ortalamayı çıkarır, standart sapmaya (`varyansın karekökü`) böler. `eps`, paydanın sıfır olmasını önler.
`layer_norm([2000.0, ...])` | Aynı sayıların 1000 katı. Normalleşince sonuç değişmez: ölçek ortadan kalkar.
```

Ortalama `0`, varyans `1`. Sayıları `1000` ile çarpsak bile normalleşmiş çıktı aynı. Bu, yüzlerce katmandan geçen sayıların büyüyüp küçülmesini engeller. Gerçek katman normalizasyonu bir de her sayıya öğrenilen bir çarpan ve ekleme uygular; bu derste sade tuttuk.

### 2.2 İleri besleme ağı: her token tek başına

Attention token'ları birbirine karıştırır. **İleri besleme ağı** ise her token'ı **ayrı ayrı**, aynı ağdan geçirir. İki doğrusal katman ve aralarında ReLU'dur (3.1): vektör önce daha geniş bir boyuta açılır, ReLU ile doğrusal olmayan bir dönüşüm yapılır, sonra eski boyuta döner. Gerçek modellerde ara boyut genellikle girdinin 4 katıdır.

```python {.python-playground}
def relu(v):
    return [max(0.0, a) for a in v]


def linear(x, W, b):
    return [sum(x[i] * W[i][j] for i in range(len(x))) + b[j] for j in range(len(b))]


W1 = [[1.0, -1.0, 0.5, 0.0], [0.0, 1.0, -0.5, 1.0]]
b1 = [0.0, 0.0, 0.0, -0.5]
W2 = [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5], [1.0, -1.0]]
b2 = [0.0, 0.0]


def ffn(x):
    return linear(relu(linear(x, W1, b1)), W2, b2)


for token, x in [("kedi", [2.0, 0.0]), ("süt", [0.5, 2.0]), ("içti", [1.5, 1.5])]:
    print(f"{token:5} {x} → {[round(v, 2) for v in ffn(x)]}")
```
```text {.python-playground-expected}
kedi  [2.0, 0.0] → [2.5, 0.5]
süt   [0.5, 2.0] → [2.0, 0.0]
içti  [1.5, 1.5] → [2.5, -1.0]
```
```text {.python-playground-help}
`def relu(v):` | Listedeki negatif sayıları `0` yapar, pozitifleri olduğu gibi bırakır (3.1).
`def linear(x, W, b):` | Bir doğrusal katman: vektörü `W` matrisiyle çarpar ve `b`'yi ekler (5.3'teki `matvec` + sabit).
`W1` | 2 boyutlu girdiyi 4 boyuta açar: iki satır, dört sütun.
`W2` | 4 boyutu yeniden 2 boyuta indirir.
`ffn(x)` | Doğrusal → ReLU → doğrusal. Aynı ağırlıklar her token için kullanılır.
`for token, x in [...]` | Her token ayrı ayrı işlenir; hiçbiri öbürünün çıktısını görmez.
```

Dikkat: Üç token aynı `W1` ve `W2` ile ama **birbirinden bağımsız** işlendi. Token'ların arasındaki iletişim yalnızca attention'da gerçekleşir; ileri besleme ağı her token'ın kendi vektörünü zenginleştirir. Basit bir iş bölümü: attention "kime bakıyorum?", ileri besleme "bulduklarımdan ne çıkarıyorum?"

### 2.3 Artık bağlantı ve blok

**Artık bağlantı**, bir parçanın çıktısını girdiye toplar: `çıktı = x + parça(x)`. Parça işe yaramasa bile (çıktısı `0` olsa) `x` olduğu gibi kalır. Bu iki işe yarar: bilgi kestirmeden ilerler ve geri yayılımda gradyan toplamadan geçip kaybolmadan öncekilere ulaşır (3.3).

Bloğun akışı şöyledir (modern modellerin çoğunda kullanılan **ön normalizasyonlu** biçim):

```text
x → [normalleştir → attention] → + x   (artık bağlantı 1)
  → [normalleştir → ileri besleme] → + önceki   (artık bağlantı 2)
```

```python {.python-playground}
import math


def softmax(p):
    u = [math.exp(a - max(p)) for a in p]
    return [a / sum(u) for a in u]


def layer_norm(x, eps=1e-5):
    o = sum(x) / len(x)
    v = sum((a - o) ** 2 for a in x) / len(x)
    return [(a - o) / math.sqrt(v + eps) for a in x]


def self_attention(X):
    d = len(X[0])
    sonuc = []
    for q in X:
        w = softmax([sum(a * b for a, b in zip(q, k)) / math.sqrt(d) for k in X])
        sonuc.append([sum(wi * v[j] for wi, v in zip(w, X)) for j in range(d)])
    return sonuc


def relu(v):
    return [max(0.0, a) for a in v]


def linear(x, W, b):
    return [sum(x[i] * W[i][j] for i in range(len(x))) + b[j] for j in range(len(b))]


W1 = [[1.0, -1.0, 0.5, 0.0], [0.0, 1.0, -0.5, 1.0]]
b1 = [0.0, 0.0, 0.0, -0.5]
W2 = [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5], [1.0, -1.0]]
b2 = [0.0, 0.0]


def ffn(x):
    return linear(relu(linear(x, W1, b1)), W2, b2)


def topla(a, b):
    return [[x + y for x, y in zip(s1, s2)] for s1, s2 in zip(a, b)]


def blok(X):
    h = topla(X, self_attention([layer_norm(x) for x in X]))
    return topla(h, [ffn(layer_norm(x)) for x in h])


X = [[2.0, 0.0], [0.5, 2.0], [1.5, 1.5]]
Y = blok(X)
Z = blok(Y)

print("Girdi :", [[round(v, 2) for v in s] for s in X])
print("Blok 1:", [[round(v, 2) for v in s] for s in Y])
print("Blok 2:", [[round(v, 2) for v in s] for s in Z])
print("Boyut korunuyor mu?", len(X) == len(Z) and len(X[0]) == len(Z[0]))
```
```text {.python-playground-expected}
Girdi : [[2.0, 0.0], [0.5, 2.0], [1.5, 1.5]]
Blok 1: [[4.22, -0.22], [0.28, 4.22], [1.5, 1.5]]
Blok 2: [[6.45, -0.45], [0.05, 6.45], [3.08, 1.92]]
Boyut korunuyor mu? True
```
```text {.python-playground-help}
`def topla(a, b):` | İki "token listesini" aynı konumlardaki sayıları toplayarak birleştirir. Artık bağlantı bu toplamadır.
`self_attention([layer_norm(x) for x in X])` | Önce her token normalleştirilir, sonra attention çalışır (ön normalizasyon).
`h = topla(X, ...)` | Artık bağlantı 1: attention'ın çıktısı, girdiye eklenir.
`[ffn(layer_norm(x)) for x in h]` | Her token yine normalleştirilir ve ileri besleme ağına verilir.
`topla(h, ...)` | Artık bağlantı 2: ileri besleme çıktısı `h`'ye eklenir.
`Z = blok(Y)` | Bloğu art arda uygularız. Çıktı girdiyle aynı biçimde olduğu için bu mümkün.
```

Bu pencere eksiksiz bir (tek kafalı, öğrenilmiş ağırlıksız) transformer bloğudur. Girdi ile çıktının biçimi aynı (3 token × 2 sayı), bu yüzden bloklar art arda yığılabilir. Gerçek bir model aynı bloğu onlarca kez yığar; her blok farklı ağırlıklara sahiptir ve ağırlıklar eğitimde öğrenilir.

### Şimdi sen yaz: katman normalizasyonu

**Görev:** 4 sayılık bir vektör kodda hazır. Katman normalizasyonunu adım adım yazacaksın: ortalama, varyans, sonra her sayıyı normalleştirmek. Ekranda normalleşmiş vektör, ortalaması (`0`) ve varyansı (`1`) görünmeli.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
import math

x = [2.0, 4.0, 6.0, 8.0]
eps = 1e-5

# TODO: Ortalama: sayıların toplamı bölü sayı adedi.
ortalama = ___

# TODO: Varyans: her sayının ortalamadan farkının karesinin ortalaması.
varyans = ___

sonuc = []
for v in x:
    # TODO: (sayı - ortalama) / karekök(varyans + eps).
    sonuc.append(___)

print("Normalleşmiş:", [round(v, 2) for v in sonuc])
print("Ortalama:", round(sum(sonuc) / len(sonuc), 4))
print("Varyans:", round(sum(v * v for v in sonuc) / len(sonuc), 3))
```
```text {.python-playground-expected}
Normalleşmiş: [-1.34, -0.45, 0.45, 1.34]
Ortalama: 0.0
Varyans: 1.0
```
```text {.python-playground-help}
`ortalama = ___` | Toplamı `sum(x)`, sayı adedini `len(x)` verir. Toplamı adede böl.
`varyans = ___` | Her `v` için `(v - ortalama) ** 2` hesapla, hepsini `sum` ile topla ve sayı adedine böl.
`sonuc.append(___)` | Ortalamayı çıkar, standart sapmaya böl. Standart sapma, `varyans + eps`'in karekökü: `math.sqrt(...)`.
```
```python {.python-playground-solution}
import math

x = [2.0, 4.0, 6.0, 8.0]
eps = 1e-5

# Ortalama: sayıların toplamı bölü sayı adedi.
ortalama = sum(x) / len(x)

# Varyans: her sayının ortalamadan farkının karesinin ortalaması.
varyans = sum((v - ortalama) ** 2 for v in x) / len(x)

sonuc = []
for v in x:
    # (sayı - ortalama) / karekök(varyans + eps).
    sonuc.append((v - ortalama) / math.sqrt(varyans + eps))

print("Normalleşmiş:", [round(v, 2) for v in sonuc])
print("Ortalama:", round(sum(sonuc) / len(sonuc), 4))
print("Varyans:", round(sum(v * v for v in sonuc) / len(sonuc), 3))
```

## 3. Kütüphaneyle yap

PyTorch'ta katman normalizasyonu `nn.LayerNorm`'dur. 2.1'deki sonucu doğrulayalım. PyTorch'u 3.6'daki gibi kur, kodu `blok_torch.py` adıyla kaydet ve `python blok_torch.py` ile çalıştır:

```python
import torch
from torch import nn

x = torch.tensor([[2.0, 4.0, 6.0, 8.0]])
norm = nn.LayerNorm(4)

with torch.no_grad():
    print(norm(x).round(decimals=2))
```

Beklenen çıktı:

```text
tensor([[-1.3400, -0.4500,  0.4500,  1.3400]])
```

`nn.LayerNorm(4)` 4 sayılık vektörü normalleştirir; sonuç, 2.1'deki sayılarla aynı. `torch.no_grad()` türev takibini kapatır (yalnızca bakıyoruz, eğitmiyoruz); bu yüzden çıktıda `grad_fn` yazmaz.

Şimdi bütün bloğu bir PyTorch modülü olarak yazalım. `nn.MultiheadAttention` 5.3'teki çok başlı attention'dır; `nn.Sequential` ileri besleme ağını kurar. Kodu `transformer_blok.py` adıyla kaydedip çalıştır:

```python
import torch
from torch import nn


class TransformerBlok(nn.Module):
    def __init__(self, d, kafa_sayisi, gizli):
        super().__init__()
        self.norm1 = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, kafa_sayisi, batch_first=True)
        self.norm2 = nn.LayerNorm(d)
        self.ffn = nn.Sequential(nn.Linear(d, gizli), nn.ReLU(), nn.Linear(gizli, d))

    def forward(self, x):
        h = self.norm1(x)
        x = x + self.attn(h, h, h, need_weights=False)[0]
        x = x + self.ffn(self.norm2(x))
        return x


torch.manual_seed(0)
blok = TransformerBlok(d=8, kafa_sayisi=2, gizli=32)
x = torch.randn(2, 5, 8)
y = blok(x)

print("Girdi şekli:", x.shape)
print("Çıktı şekli:", y.shape)
print("Parametre sayısı:", sum(p.numel() for p in blok.parameters()))
print("İki blok art arda:", nn.Sequential(blok, blok)(x).shape)
```

Beklenen çıktı:

```text
Girdi şekli: torch.Size([2, 5, 8])
Çıktı şekli: torch.Size([2, 5, 8])
Parametre sayısı: 872
İki blok art arda: torch.Size([2, 5, 8])
```

- `forward`'daki iki satır, 2.3'teki iki artık bağlantıdır: `x = x + ...`.
- `self.attn(h, h, h, need_weights=False)[0]`: Sorgu, anahtar ve değer olarak aynı `h` verilir (self-attention). İlk çıktı, attention sonucudur.
- Girdi `(2, 5, 8)`: 2 örnek, 5 token, 8 boyut. Çıktı da aynı şekilde olduğu için bloklar yığılabilir.
- **872 parametre:** İki `LayerNorm` (16 + 16), attention (288) ve ileri besleme (552) toplanır.

## 4. Sık yapılan hatalar

- **Artık bağlantıyı unutmak.** `x = attention(x)` yazarsan girdi kaybolur. `x = x + attention(x)` olmalı. Derin modellerde bu fark, öğrenmenin başlayıp başlamamasını belirler.
- **Normalleştirmeyi yanlış eksende yapmak.** Layer norm bir token'ın kendi sayıları üzerinde alınır; token'lar ya da örnekler arasında değil.
- **`eps` koymamak.** Bütün sayılar eşitse varyans `0` olur ve sıfıra bölme hatası alırsın.
- **İleri beslemenin token'ları karıştırdığını sanmak.** Karıştırmaz; yalnızca attention token'lar arası bilgi taşır.
- **Boyutların uyuşmaması.** Artık bağlantı toplama olduğu için attention ve ileri besleme çıktısı, girdiyle aynı uzunlukta olmalıdır.
- **Normalleştirmenin yerini karıştırmak.** Orijinal makalede normalleştirme toplamadan **sonra** yapılıyordu (post-LN); bugün çoğu model ondan **önce** yapar (pre-LN, bu derste kullandığımız). Pre-LN çok katmanlı modellerde eğitimi daha kararlı kılar.

## 5. Pekiştir

**Quiz**

1. Layer norm bir vektöre ne yapar ve çıktının ortalaması ile varyansı kaç olur?
2. Attention ile ileri besleme ağı arasındaki temel fark nedir? Hangisi token'lar arasında bilgi taşır?
3. Artık bağlantı neden yararlıdır?
4. Bir transformer bloğunun girdisi ile çıktısı neden aynı boyutta olmalıdır?
5. İleri besleme ağında ara boyut neden genellikle girdiden büyüktür?

**Alıştırmalar**

1. 2.1'de `x`'i `[5.0, 5.0, 5.0, 5.0]` yap (hepsi aynı). `eps` olmasaydı ne olurdu? Sonuç nedir?
2. 2.2'de `W1`'in son sütununu değiştir. Çıktılar nasıl değişti?
3. 2.3'te `blok(Y)`'yi iki kez daha çağır (`Z`, `U`, `V`). Sayılar büyüyor mu, sabitleniyor mu?
4. 2.3'te `blok` içindeki artık bağlantıyı kaldır (`h = self_attention(...)`, `topla` kullanma). Çıktı nasıl değişti?
5. (İsteğe bağlı) 3. bölümdeki PyTorch kodunda `kafa_sayisi=3` yap. Hangi hatayı alıyorsun?

??? success "Quiz cevapları"
    1. Vektörün ortalamasını çıkarır ve standart sapmaya böler. Çıktının ortalaması `0`, varyansı (yaklaşık) `1` olur.
    2. Attention token'lar arasında bilgi taşır (her token diğerlerine bakar). İleri besleme ağı her token'ı tek başına, aynı ağdan geçirir; token'ları karıştırmaz.
    3. Bilgi ve gradyan, toplama sayesinde kestirmeden akar; parça işe yaramasa bile girdi kaybolmaz ve derin modellerde gradyan kaybolmaz.
    4. Çıktı, girdiye toplanır (artık bağlantı) ve sonraki blok girdi olarak kullanır; ikisi de aynı boyutta olmalıdır.
    5. Geniş bir ara katman, ReLU'dan sonra daha çok özellik hesaplamaya imkân verir; sonra tekrar eski boyuta indirilir.

## Özet

Bir transformer bloğu, attention'ı ileri besleme ağıyla birleştirir. Attention token'lar arasında bilgi taşır, ileri besleme ağı her token'ı doğrusal olmayan bir ağdan geçirir. Layer norm, her token'ın sayılarını ortalaması `0`, varyansı `1` olacak biçimde dengeler. Artık bağlantılar, her parçanın çıktısını girdiye toplayarak bilginin ve gradyanın kestirmeden akmasını sağlar. Blok, girdisiyle aynı biçimde çıktı verdiği için üst üste yığılabilir. Sıradaki ve son derste bu bloklarla gerçek bir **mini transformer** kurup eğiteceğiz.

## Kaynaklar

- Ashish Vaswani ve ark. (2017), *Attention Is All You Need*, NeurIPS (3.1 bölümü: kodlayıcı blokları)
- Jimmy Lei Ba, Jamie Ryan Kiros ve Geoffrey Hinton (2016), *Layer Normalization*
- Ruibin Xiong ve ark. (2020), *On Layer Normalization in the Transformer Architecture* (ön ve son normalizasyon karşılaştırması)
- [PyTorch resmî belgesi: `nn.LayerNorm`](https://pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html)
