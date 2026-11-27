# Faz 5 – Ders 4: Konum bilgisi

> ⏱️ Tahmini süre: 50-65 dk · 📚 Ön koşul: 5.2 Attention, 5.3 Çok başlı attention · 💻 Gereksinim: Python 3.11+, ek paket yok; NumPy ve PyTorch örnekleri isteğe bağlı

## Bu derste ne öğreneceksin?

- Attention'ın neden token'ların **sırasını** hiç bilmediğini
- Konum bilgisini vektöre **eklemek** fikrini
- Sinüs ve kosinüsle **konum kodlamasını** hesaplamayı
- Aynı sözcüğün farklı konumlarda neden farklı davrandığını görmeyi
- Öğrenilen konum tablolarını (`nn.Embedding`) ve sınırlarını

## 1. Problem

5.1'in başında sıranın anlam taşıdığını görmüştük: "film güzel değil, sıkıcı" ile "film sıkıcı değil, güzel" aynı sözcüklerdir, ama anlamları farklıdır. Peki 5.2 ve 5.3'te kurduğumuz attention bu farkı görebilir mi?

**Hayır.** Attention her token'ı, bütün token'larla karşılaştırır. Karşılaştırma yalnızca vektörlerin içeriğine bakar; hangi token'ın kaçıncı sırada olduğunu hiçbir yerde kullanmaz. Token'ların sırasını karıştırırsan her token aynı bağlamı görür, aynı çıktıyı üretir; yalnızca çıktılar da karışık sırada gelir.

Bu, bir dil modeli için ciddi bir eksiktir. Çözüm basit: Her token'ın vektörüne, **kaçıncı sırada olduğunu** anlatan bir bilgi ekleriz. Bu bilgiye **konum kodlaması** (positional encoding) denir.

## 2. Kendin yaz

### 2.1 Attention sıradan habersizdir

5.2'deki self-attention'ı bir işlev olarak yazıp, aynı token'ları iki farklı sırada verelim:

```python {.python-playground}
import math


def softmax(puanlar):
    ustler = [math.exp(p - max(puanlar)) for p in puanlar]
    return [u / sum(ustler) for u in ustler]


def self_attention(X):
    d = len(X[0])
    sonuc = []
    for sorgu in X:
        puanlar = [sum(a * b for a, b in zip(sorgu, anahtar)) / math.sqrt(d) for anahtar in X]
        w = softmax(puanlar)
        sonuc.append([round(sum(wi * v[j] for wi, v in zip(w, X)), 4) for j in range(d)])
    return sonuc


kedi, icti, sut = [2.0, 0.0], [0.5, 2.0], [1.5, 1.5]

duz = self_attention([kedi, icti, sut])
ters = self_attention([sut, icti, kedi])

print("Düz sıra   :", duz)
print("Ters sıra  :", ters)
print("Ters sıranın çıktıları, düzün ters çevrilmişi mi?", ters == duz[::-1])
```
```text {.python-playground-expected}
Düz sıra   : [[1.7357, 0.6072], [0.9731, 1.6938], [1.2853, 1.3836]]
Ters sıra  : [[1.2853, 1.3836], [0.9731, 1.6938], [1.7357, 0.6072]]
Ters sıranın çıktıları, düzün ters çevrilmişi mi? True
```
```text {.python-playground-help}
`def self_attention(X):` | 5.2'deki self-attention: her token sorgu olur, bütün token'lara bakar, değerleri ağırlıklarıyla karıştırır.
`round(..., 4)` | Ondalık yuvarlama farkları yüzünden eşitlik kontrolü bozulmasın diye sonucu 4 basamağa yuvarlarız.
`duz[::-1]` | Bir listeyi ters çevirir: son öğe başa gelir.
`ters == duz[::-1]` | Ters sıradan gelen çıktılar, düz sıradakilerin sadece ters çevrilmiş hâli mi?
```

Çıktı **True**: Her token aynı çıktıyı üretti, yalnızca sırayla birlikte yer değiştirdi. Attention için "kedi süt içti" ile "süt içti kedi" arasında token'ların kendi çıktıları açısından fark yok. Modelin sırayı kullanabilmesi için sıra bilgisini **girdiye** koymalıyız.

### 2.2 Konum kodlaması: sinüs ve kosinüs

Her konum için, token vektörüyle aynı uzunlukta bir **konum vektörü** üretiriz. Orijinal transformer makalesindeki yöntem, bu vektörü sinüs ve kosinüs dalgalarıyla kurar:

- Çift numaralı boyut `2i` için: `sin(konum / 10000^(2i / d))`
- Tek numaralı boyut `2i+1` için: `cos(konum / 10000^(2i / d))`

Burada `d` vektörün boyutu. Her boyut çifti (`sin`, `cos`) farklı bir hızda salınır: ilk boyutlar konum arttıkça çabuk, son boyutlar yavaş değişir. Tıpkı bir saatin saniye, dakika ve saat ibreleri gibi: birlikte, her konumu benzersiz biçimde tanımlarlar.

```python {.python-playground}
import math


def konum_kodlamasi(konum, d):
    satir = []
    for i in range(d):
        aci = konum / 10000 ** ((i // 2 * 2) / d)
        satir.append(math.sin(aci) if i % 2 == 0 else math.cos(aci))
    return satir


for konum in range(4):
    print(konum, [round(v, 2) for v in konum_kodlamasi(konum, 4)])
```
```text {.python-playground-expected}
0 [0.0, 1.0, 0.0, 1.0]
1 [0.84, 0.54, 0.01, 1.0]
2 [0.91, -0.42, 0.02, 1.0]
3 [0.14, -0.99, 0.03, 1.0]
```
```text {.python-playground-help}
`def konum_kodlamasi(konum, d):` | Bir konum numarası için `d` sayılık bir konum vektörü üretir.
`i // 2 * 2` | `i`'yi çift sayıya yuvarlar: `0, 1 → 0` ve `2, 3 → 2`. Böylece her `sin`-`cos` çifti aynı hızı paylaşır.
`10000 ** ((i // 2 * 2) / d)` | Boyuta göre değişen bölen. İlk çiftte `1`, ikinci çiftte `100` olur (`d = 4` için). Bu yüzden ilk boyutlar hızlı, sonraki yavaş değişir.
`math.sin(aci) if i % 2 == 0 else math.cos(aci)` | Çift boyutlarda sinüs, tek boyutlarda kosinüs. Tek satırlık koşul: `değer1 if koşul else değer2`.
```

Çıktıya bak: Konum `0` için vektör `[0, 1, 0, 1]`. İlk iki sayı (hızlı çift) konum arttıkça belirgin değişiyor; son iki sayı (yavaş çift) çok yavaş kayıyor. Her konumun vektörü farklı. Bu, bir token'a "ben 2. sıradayım" bilgisini sayıyla yapıştırmak için yeterlidir.

Neden 10000? Orijinal makalede seçilen bir sabittir; bölenlerin geniş bir aralıkta (`1`'den `10000`'e) dağılmasını sağlar. Böylece modelin hem yakın, hem uzak konum farklarını ayırt edecek hızları olur.

### 2.3 Konumu vektöre eklemek

Konum vektörü, token'ın (gömme) vektörüne **toplanır**. Yeni vektör hem token'ın ne olduğunu hem nerede durduğunu taşır. `kedi içti kedi` cümlesinde `kedi` iki kez geçer. Konum kodlaması olmadan iki `kedi` birbirinin tıpatıp aynısıdır. Kodlamayla farklılaşır:

```python {.python-playground}
import math


def softmax(puanlar):
    ustler = [math.exp(p - max(puanlar)) for p in puanlar]
    return [u / sum(ustler) for u in ustler]


def baktigi(X, i):
    d = len(X[0])
    return softmax([sum(a * b for a, b in zip(X[i], k)) / math.sqrt(d) for k in X])


def konum_ekle(X):
    return [[v + math.sin(k) if j == 0 else v + math.cos(k) for j, v in enumerate(x)]
            for k, x in enumerate(X)]


X = [[2.0, 0.0], [0.5, 2.0], [2.0, 0.0]]
XP = konum_ekle(X)

print("Konumsuz  :", [round(w, 2) for w in baktigi(X, 0)], [round(w, 2) for w in baktigi(X, 2)])
print("Konumlu   :", [round(w, 2) for w in baktigi(XP, 0)], [round(w, 2) for w in baktigi(XP, 2)])
print("Birinci ve üçüncü 'kedi' aynı mı (konumsuz)?", baktigi(X, 0) == baktigi(X, 2))
print("Birinci ve üçüncü 'kedi' aynı mı (konumlu)? ", baktigi(XP, 0) == baktigi(XP, 2))
```
```text {.python-playground-expected}
Konumsuz  : [0.47, 0.06, 0.47] [0.47, 0.06, 0.47]
Konumlu   : [0.29, 0.33, 0.38] [0.09, 0.01, 0.89]
Birinci ve üçüncü 'kedi' aynı mı (konumsuz)? True
Birinci ve üçüncü 'kedi' aynı mı (konumlu)?  False
```
```text {.python-playground-help}
`X = [[2.0, 0.0], [0.5, 2.0], [2.0, 0.0]]` | Üç token: `kedi`, `içti`, `kedi`. İlk ve üçüncü satır birebir aynı.
`konum_ekle(X)` | Her token'a konumuna göre bir sayı çifti ekler: ilk boyuta `sin(konum)`, ikinciye `cos(konum)`. Konum, token'ın listedeki sırasıdır (`enumerate` ile).
`baktigi(X, 0)` | İlk token'ın bütün token'lara verdiği ağırlıklar.
`baktigi(X, 0) == baktigi(X, 2)` | İlk ve üçüncü `kedi`'nin ağırlıkları eşit mi?
```

Konumsuz hâlde iki `kedi`'nin ağırlıkları birebir aynı: model onları ayırt edemez. Konum eklenince ağırlıklar farklılaşıyor: Birinci `kedi` ile üçüncü `kedi` artık farklı bağlamlara sahip. Dikkat: Bu örnekte konum kodlamasını basit tuttuk (iki boyutlu `sin`, `cos`); gerçek modellerde 2.2'deki gibi çok sayıda boyut kullanılır.

### Öğrenilen konum vektörleri

Konum vektörlerini formülle üretmek zorunda değiliz. Bir **tablo** da öğrenebiliriz: her konum için bir satır, 5.1'deki gömme tablosu gibi. Satırların sayıları eğitimde öğrenilir. GPT-2 gibi modeller böyle yapar. Tablonun bir sınırı vardır: yalnızca eğitimde görülen maksimum uzunluğa kadar konum bilir. Formül yöntemi ise teoride herhangi bir konum için çalışır.

Modern modeller (örneğin Llama) **döndürmeli konum gömmesi** (RoPE) gibi, konumu vektöre eklemek yerine sorgu ve anahtarı konuma göre döndüren yöntemler kullanır. Bu derste kapsam dışı, ama temel fikir aynı: attention'a sıra bilgisini bir şekilde vermek.

### Şimdi sen yaz: konum vektörünü hesapla

**Görev:** Bir konum numarası (`2`) ve vektör boyutu (`4`) kodda hazır. Her boyut için açıyı hesaplayıp çift boyutlarda sinüs, tek boyutlarda kosinüs alacaksın. Ekranda `2`. konumun 4 sayılık konum vektörü görünmeli.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
import math

d = 4
konum = 2

kodlama = []
for i in range(d):
    # TODO: Açı = konum / 10000 üzeri (çift sıra numarası / d). Çift sıra numarası: i // 2 * 2.
    aci = konum / 10000 ** (___ / d)
    # TODO: Çift i için sinüs, tek i için kosinüs ekle (math.sin, math.cos).
    if i % 2 == 0:
        kodlama.append(___)
    else:
        kodlama.append(___)

print([round(v, 3) for v in kodlama])
```
```text {.python-playground-expected}
[0.909, -0.416, 0.02, 1.0]
```
```text {.python-playground-help}
`10000 ** (___ / d)` | Bölen boyuta göre değişir. Aynı sinüs-kosinüs çifti aynı böleni paylaşsın diye `i`'yi çift sayıya yuvarla: `i // 2 * 2`.
`kodlama.append(___)` (ilki) | Çift boyutta sinüs alınır: `math.sin(aci)`.
`kodlama.append(___)` (ikincisi) | Tek boyutta kosinüs alınır: `math.cos(aci)`.
```
```python {.python-playground-solution}
import math

d = 4
konum = 2

kodlama = []
for i in range(d):
    # Açı = konum / 10000 üzeri (çift sıra numarası / d). Çift sıra numarası: i // 2 * 2.
    aci = konum / 10000 ** (i // 2 * 2 / d)
    # Çift i için sinüs, tek i için kosinüs ekle (math.sin, math.cos).
    if i % 2 == 0:
        kodlama.append(math.sin(aci))
    else:
        kodlama.append(math.cos(aci))

print([round(v, 3) for v in kodlama])
```

## 3. Kütüphaneyle yap

NumPy ile bütün konumları ve bütün boyutları tek seferde üretebiliriz. NumPy'yi 2.1'deki gibi kur, kodu `konum_numpy.py` adıyla kaydet ve `python konum_numpy.py` ile çalıştır:

```python
import numpy as np


def konum_kodlamasi(max_uzunluk, d):
    konum = np.arange(max_uzunluk)[:, None]
    i = np.arange(d)[None, :]
    aci = konum / 10000 ** ((i // 2 * 2) / d)
    return np.where(i % 2 == 0, np.sin(aci), np.cos(aci))


print(np.round(konum_kodlamasi(4, 4), 2))
```

Beklenen çıktı:

```text
[[ 0.    1.    0.    1.  ]
 [ 0.84  0.54  0.01  1.  ]
 [ 0.91 -0.42  0.02  1.  ]
 [ 0.14 -0.99  0.03  1.  ]]
```

- `np.arange(max_uzunluk)[:, None]`: Konumları bir **sütun** olarak dizer (`4 × 1`).
- `np.arange(d)[None, :]`: Boyut numaralarını bir **satır** olarak dizer (`1 × 4`).
- `konum / 10000 ** (...)`: Sütun ile satır yayınlama (broadcasting, 2.1) ile birleşir ve `4 × 4`'lük bir açı tablosu çıkar.
- `np.where(i % 2 == 0, np.sin(aci), np.cos(aci))`: Çift boyutlarda sinüs, tek boyutlarda kosinüs seçer.

Sonuç, 2.2'deki satır satır yazdığımız tabloyla aynıdır. PyTorch'ta **öğrenilen** konum tablosu `nn.Embedding` ile kurulur. PyTorch'u 3.6'daki gibi kur, kodu `konum_torch.py` adıyla kaydet ve `python konum_torch.py` ile çalıştır:

```python
import torch
from torch import nn

sozluk_boyutu, max_uzunluk, d = 100, 16, 8

token_gomme = nn.Embedding(sozluk_boyutu, d)
konum_gomme = nn.Embedding(max_uzunluk, d)

idler = torch.tensor([[5, 12, 5, 40]])
konumlar = torch.arange(idler.shape[1])

x = token_gomme(idler) + konum_gomme(konumlar)

print("Token numaraları:", idler.shape)
print("Konumlar:", konumlar.tolist())
print("Giriş vektörleri:", x.shape)
```

Beklenen çıktı:

```text
Token numaraları: torch.Size([1, 4])
Konumlar: [0, 1, 2, 3]
Giriş vektörleri: torch.Size([1, 4, 8])
```

- `konum_gomme = nn.Embedding(max_uzunluk, d)`: 16 konum için 8 boyutlu birer satır. Satırlar eğitimde öğrenilir.
- `torch.arange(4)`: Konum numaraları `0, 1, 2, 3`.
- `token_gomme(idler) + konum_gomme(konumlar)`: Her token'ın vektörüne kendi konumunun vektörü eklenir. `(1, 4, 8)` ile `(4, 8)` toplanırken PyTorch ikincisini her örneğe yayar.
- Dizinin uzunluğu `max_uzunluk`'u (`16`) aşarsa `konum_gomme` `IndexError` verir; öğrenilen tablonun bir üst sınırı vardır.

## 4. Sık yapılan hatalar

- **Konumu hiç eklememek.** Attention tek başına sıradan habersizdir; konum eklenmezse model sözcüklerin sırasını öğrenemez.
- **Konumu birleştirmek yerine eklemeyi karıştırmak.** Orijinal transformer konum vektörünü token vektörüyle **toplar**; yan yana birleştirme vektörün boyutunu değiştirir.
- **Konum vektörünü token vektörünün boyutundan farklı yapmak.** İkisi toplanacağı için aynı uzunlukta olmalıdır.
- **Öğrenilen tabloda uzunluk sınırını unutmak.** Eğitimde 16 konumlu tablo kurduysan 17. token için hata alırsın. Daha uzun girdilere ihtiyaç varsa tabloyu büyüt ya da formül tabanlı kodlama kullan.
- **Konum 0 ile 1'den başlamayı karıştırmak.** Sayıların başlangıcı sonucu değiştirmez ama tutarlı olmalı: eğitimde nasıl numaralandıysan kullanımda da öyle numaralandır.
- **Konum kodlamasının "doğru sırayı" bildiğini sanmak.** Kodlama yalnızca her konumu ayırt edilebilir yapar; sıranın anlamını (örneğin "değil" sözcüğünün sonrakini olumsuzlaması) modelin kendisi eğitimde öğrenir.

## 5. Pekiştir

**Quiz**

1. Self-attention neden token'ların sırasını bilmez?
2. Konum vektörü neden token vektörüyle **aynı boyutta** olmalıdır?
3. Konum kodlamasında ilk boyutlar neden çabuk, son boyutlar yavaş değişir?
4. Konumsuz bir modelde `kedi içti kedi` cümlesindeki iki `kedi` neden aynı çıktıyı üretir?
5. Öğrenilen konum tablosunun (`nn.Embedding`) formül tabanlı kodlamaya göre bir dezavantajı nedir?

**Alıştırmalar**

1. 2.1'de ters sırayı `[icti, kedi, sut]` gibi başka bir karışıma çevir. Çıktılar yine token'larla birlikte yer değiştiriyor mu?
2. 2.2'de `konum_kodlamasi(konum, 4)` yerine `konum_kodlamasi(konum, 8)` yaz. İlk iki boyut değişti mi? Son boyutlar nasıl?
3. 2.2'de konumu `range(4)` yerine `range(100, 104)` yap. Ardışık konumlar yine birbirinden ayırt edilebiliyor mu?
4. 2.3'e dördüncü bir `kedi` ekle: `X = [[2.0, 0.0], [0.5, 2.0], [2.0, 0.0], [2.0, 0.0]]`. Üç `kedi`'nin ağırlıkları farklı mı?
5. (İsteğe bağlı) 3. bölümdeki PyTorch kodunda `idler`'i 20 token'lık yap (`max_uzunluk = 16`). Hangi hatayı alıyorsun?

??? success "Quiz cevapları"
    1. Her token'ın puanı, yalnızca vektörlerin içeriğine bakan noktasal çarpımla hesaplanır; token'ın listedeki konumu hiçbir yerde kullanılmaz. Sırayı değiştirmek çıktıları yalnızca yer değiştirir.
    2. Konum vektörü token vektörüne toplanır; toplama için iki vektörün aynı uzunlukta olması gerekir.
    3. Her `sin`/`cos` çifti farklı bir böleni kullanır: ilk çiftte bölen `1`, sonraki çiftlerde giderek büyür. Bölen büyüdükçe açı konumla yavaş artar.
    4. İki `kedi`'nin vektörü birebir aynıdır ve attention yalnızca vektörlere baktığı için ikisi de aynı bağlamı görür.
    5. Yalnızca eğitimde kurulan en büyük konuma kadar çalışır; daha uzun dizilerde konum bilgisi yoktur. Formül, herhangi bir konum için üretilebilir.

## Özet

Attention token'ların sırasını bilmez: sırayı değiştirirsen çıktılar yalnızca yer değiştirir. Bu yüzden her token'ın vektörüne, kaçıncı sırada olduğunu anlatan bir **konum vektörü** toplarız. Orijinal transformer, farklı hızlarda salınan sinüs ve kosinüslerle bu vektörü hesaplar; GPT-2 gibi modeller ise konum vektörlerini bir tabloda öğrenir. Konum eklenince aynı sözcüğün farklı konumlardaki kopyaları farklı bağlam görür. Sıradaki derste bütün parçaları (attention, konum, ileri besleme, normalizasyon) bir **transformer bloğunda** birleştireceğiz.

## Kaynaklar

- Ashish Vaswani ve ark. (2017), *Attention Is All You Need*, NeurIPS (3.5 bölümü: konum kodlaması)
- Jianlin Su ve ark. (2021), *RoFormer: Enhanced Transformer with Rotary Position Embedding* (döndürmeli konum gömmesi)
- [PyTorch resmî belgesi: `nn.Embedding`](https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html)
- Amirhossein Kazemnejad, [Transformer Architecture: The Positional Encoding](https://kazemnejad.com/blog/transformer_architecture_positional_encoding/)
