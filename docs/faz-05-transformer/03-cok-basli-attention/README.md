# Faz 5 – Ders 3: Çok başlı attention

> ⏱️ Tahmini süre: 55-70 dk · 📚 Ön koşul: 5.2 Attention, 1.2 Matris çarpımı · 💻 Gereksinim: Python 3.11+, ek paket yok; NumPy ve PyTorch örnekleri isteğe bağlı

## Bu derste ne öğreneceksin?

- Tek bir attention'ın neden yetmediğini
- Bir vektörü **kafalara** bölmeyi ve her kafanın ayrı bir ilişkiye bakmasını
- **Projeksiyonun** (matrisle yeni bir uzaya taşımanın) ne olduğunu
- Kafa çıktılarını yan yana **birleştirmeyi**
- `nn.MultiheadAttention`'ın içinde ne olduğunu

## 1. Problem

5.2'deki attention, bir token için tek bir ağırlık dağılımı üretir. Ama bir cümlede bir token aynı anda birden çok şeyle ilgili olabilir. "Küçük kedi sütü içti" cümlesinde `içti` hem **kimin** (kedi) hem **neyi** (süt) içtiğine bakmak ister; `küçük` ise `kedi`'ye bağlıdır. Tek bir ağırlık dağılımı bütün bu ilişkileri aynı anda taşımak zorunda kalır.

Çözüm: attention'ı **birden çok kez, paralel** çalıştırmak. Her birine **kafa** (head) denir. Her kafa vektörün farklı bir parçasına, farklı bir "açıdan" bakar ve kendi ağırlıklarını hesaplar. Sonra kafaların çıktıları yan yana birleştirilir. Buna **çok başlı attention** (multi-head attention) denir.

Bu derste dört token'lı bir örnek kullanacağız. Her token'ın vektörünün ilk iki sayısı **tür** (canlı mı, taşıt mı), son iki sayısı **boyut** (küçük mü, büyük mü) bilgisini taşıyor:

| Token | Tür (ilk iki sayı) | Boyut (son iki sayı) |
|---|---|---|
| kedi | canlı | küçük |
| köpek | canlı | büyük |
| bisiklet | taşıt | küçük |
| otobüs | taşıt | büyük |

Bir kafa türe, bir kafa boyuta baksın. İki kafa aynı token için farklı komşuları öne çıkaracak.

## 2. Kendin yaz

### 2.1 İki kafa, iki farklı bakış

Vektörü ikiye bölüp (ilk iki sayı, son iki sayı) her parça üzerinde ayrı attention çalıştıracağız. `baktigi` işlevi, bir token'ın (`i`) bütün token'lara verdiği ağırlıkları hesaplar. Bu, 5.2'deki puan ve softmax adımlarının aynısıdır.

```python {.python-playground}
import math

tokenlar = ["kedi", "köpek", "bisiklet", "otobüs"]
X = [
    [2.0, 0.0, 2.0, 0.0],
    [2.0, 0.0, 0.0, 2.0],
    [0.0, 2.0, 2.0, 0.0],
    [0.0, 2.0, 0.0, 2.0],
]


def softmax(puanlar):
    ustler = [math.exp(p - max(puanlar)) for p in puanlar]
    return [u / sum(ustler) for u in ustler]


def baktigi(vektorler, i):
    d = len(vektorler[0])
    puanlar = [sum(a * b for a, b in zip(vektorler[i], v)) / math.sqrt(d) for v in vektorler]
    return softmax(puanlar)


for kafa, (bas, son) in enumerate([(0, 2), (2, 4)], start=1):
    parca = [x[bas:son] for x in X]
    agirliklar = baktigi(parca, 0)
    print(f"Kafa {kafa}:", {t: round(w, 2) for t, w in zip(tokenlar, agirliklar)})
```
```text {.python-playground-expected}
Kafa 1: {'kedi': 0.47, 'köpek': 0.47, 'bisiklet': 0.03, 'otobüs': 0.03}
Kafa 2: {'kedi': 0.47, 'köpek': 0.03, 'bisiklet': 0.47, 'otobüs': 0.03}
```
```text {.python-playground-help}
`X = [[2.0, 0.0, 2.0, 0.0], ...]` | Dört token, her biri 4 sayılık vektör. İlk iki sayı tür, son iki sayı boyut bilgisidir.
`def baktigi(vektorler, i):` | `i`. token'ın bütün token'lara verdiği attention ağırlıklarını döndürür (puan, `√d` bölmesi, softmax).
`enumerate([(0, 2), (2, 4)], start=1)` | İki kafanın dilim sınırları: ilk kafa `0:2`, ikinci kafa `2:4`. `start=1` kafaları 1'den numaralandırır.
`parca = [x[bas:son] for x in X]` | Her token'ın vektöründen yalnızca o kafanın parçasını alırız.
`baktigi(parca, 0)` | Kedi'nin (`0`. token) bu parçaya göre kimlere baktığı.
`{t: round(w, 2) for t, w in zip(tokenlar, agirliklar)}` | Token adı ve ağırlığı eşleştirip bir sözlük yapar; okunması kolay olur.
```

**Kafa 1** (tür) kedi için `kedi` ve `köpek`'e yüksek, taşıtlara düşük ağırlık veriyor: ikisi de canlı. **Kafa 2** (boyut) ise `kedi` ve `bisiklet`'e yüksek ağırlık veriyor: ikisi de küçük. Aynı token, aynı anda iki farklı ilişkiyi iki ayrı ağırlık dağılımında taşıyor. Tek bir attention bu ikisini tek bir dağılıma sıkıştırmak zorunda kalırdı.

Kutudaki `baktigi(parca, 0)` içinde `0`'ı `3` yap (otobüs). Hangi komşuları öne çıkarıyorlar?

### 2.2 Projeksiyon: vektörü yeni bir uzaya taşımak

Yukarıda vektörü **dilimleyerek** kafalara böldük: kafa 1 ilk iki sayıyı, kafa 2 son iki sayıyı aldı. Gerçek modellerde bu o kadar katı değildir. Her kafa, vektörü kendi **ağırlık matrisiyle** çarpıp yeni, daha küçük bir vektöre çevirir. Buna **projeksiyon** denir. Matrisin sayıları eğitim sırasında öğrenilir; yani model, her kafanın neye bakacağını kendisi seçer.

Bir vektörü matrisle çarpmak 1.2'deki satır-sütun noktasal çarpımlarının tekrarıdır:

```python {.python-playground}
def matvec(x, W):
    return [sum(x[i] * W[i][j] for i in range(len(x))) for j in range(len(W[0]))]


kedi = [2.0, 0.0, 2.0, 0.0]

W_tur = [[1, 0], [0, 1], [0, 0], [0, 0]]
W_boyut = [[0, 0], [0, 0], [1, 0], [0, 1]]
W_karisik = [[0.5, 0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5]]

print("Tür matrisi    :", matvec(kedi, W_tur))
print("Boyut matrisi  :", matvec(kedi, W_boyut))
print("Karışık matris :", matvec(kedi, W_karisik))
```
```text {.python-playground-expected}
Tür matrisi    : [2.0, 0.0]
Boyut matrisi  : [2.0, 0.0]
Karışık matris : [2.0, 2.0]
```
```text {.python-playground-help}
`def matvec(x, W):` | `x` vektörünü `W` matrisiyle çarpar. Sonuç, matrisin sütun sayısı kadar uzunlukta yeni bir vektördür.
`W[i][j]` | Matrisin `i`. satır, `j`. sütunundaki sayı.
`for j in range(len(W[0]))` | Her çıktı boyutu (matrisin her sütunu) için bir sayı hesaplarız.
`sum(x[i] * W[i][j] for i in range(len(x)))` | `x` ile matrisin `j`. sütununun noktasal çarpımı.
`W_tur`, `W_boyut` | Dilimlemenin aynısını yapan matrisler: yalnızca belirli sütunlardaki sayıları bırakıp öbürlerini sıfırlar.
`W_karisik` | Sayıları herhangi bir şey olabilir; eğitilen bir modelde bu sayılar öğrenilir.
```

`W_tur` ilk iki sayıyı, `W_boyut` son iki sayıyı geçirir: **dilimlemek, belirli bir matrisle çarpmanın özel bir hâlidir.** `W_karisik` ise vektörün bütün sayılarını karıştırarak yepyeni bir "bakış" üretir. Eğitim sırasında her kafa kendi `Wq`, `Wk`, `Wv` matrislerini öğrenir ve sorgu, anahtar, değeri bunlarla üretir. Bu derste hesabı sade tutmak için dilimlemeyi kullanıyoruz.

### 2.3 Kafaları birleştirmek

Her kafa, her token için kendi çıktı vektörünü üretir. Bu vektörleri yan yana yapıştırırız (**birleştirme**, concatenation). İki kafanın çıktıları 2'şer boyutluysa birleşik çıktı 4 boyutlu olur, yani girdiyle aynı boyut. Gerçek modellerde birleşik çıktı bir de son bir matrisle (`Wo`) çarpılıp kafalar arasında bilgi karıştırılır.

```python {.python-playground}
import math

tokenlar = ["kedi", "köpek", "bisiklet", "otobüs"]
X = [
    [2.0, 0.0, 2.0, 0.0],
    [2.0, 0.0, 0.0, 2.0],
    [0.0, 2.0, 2.0, 0.0],
    [0.0, 2.0, 0.0, 2.0],
]


def softmax(puanlar):
    ustler = [math.exp(p - max(puanlar)) for p in puanlar]
    return [u / sum(ustler) for u in ustler]


def baktigi(vektorler, i):
    d = len(vektorler[0])
    puanlar = [sum(a * b for a, b in zip(vektorler[i], v)) / math.sqrt(d) for v in vektorler]
    return softmax(puanlar)


def cok_basli(X, kafa_sayisi):
    d = len(X[0])
    kafa_boyutu = d // kafa_sayisi
    sonuc = [[] for _ in X]
    for kafa in range(kafa_sayisi):
        bas = kafa * kafa_boyutu
        parca = [x[bas:bas + kafa_boyutu] for x in X]
        for i in range(len(X)):
            agirliklar = baktigi(parca, i)
            cikti = [sum(w * v[j] for w, v in zip(agirliklar, parca)) for j in range(kafa_boyutu)]
            sonuc[i] = sonuc[i] + cikti
    return sonuc


for token, satir in zip(tokenlar, cok_basli(X, 2)):
    print(f"{token:9}", [round(c, 2) for c in satir])
```
```text {.python-playground-expected}
kedi      [1.89, 0.11, 1.89, 0.11]
köpek     [1.89, 0.11, 0.11, 1.89]
bisiklet  [0.11, 1.89, 1.89, 0.11]
otobüs    [0.11, 1.89, 0.11, 1.89]
```
```text {.python-playground-help}
`kafa_boyutu = d // kafa_sayisi` | Vektörü kafalara eşit böleriz. `//` tam bölme yapar: `4 // 2 = 2`. Bu yüzden `d`, kafa sayısına tam bölünmelidir.
`bas = kafa * kafa_boyutu` | `kafa`. kafanın parçası bu konumdan başlar: kafa 0 için `0`, kafa 1 için `2`.
`parca = [x[bas:bas + kafa_boyutu] for x in X]` | Bütün token'ların bu kafaya ait parçası.
`for i in range(len(X)):` | Her token için o kafanın attention'ını ayrı hesaplarız.
`cikti = [sum(w * v[j] ...) for j in range(kafa_boyutu)]` | 5.2'deki ağırlıklı toplam: değerleri ağırlıklarıyla karıştırır. Çıktı, kafa boyutu kadar uzunluktadır.
`sonuc[i] = sonuc[i] + cikti` | Kafaların çıktısını token'ın sonucuna yan yana ekler (birleştirme).
```

Her satırın ilk iki sayısı kafa 1'in (tür), son iki sayısı kafa 2'nin (boyut) çıktısı. Girdi 4 boyutluydu, çıktı da 4 boyutlu; çok başlı attention vektörün boyutunu değiştirmez, yalnızca token'ları bağlamla karıştırır.

`cok_basli(X, 2)` içinde `2`'yi `1` yap: tek kafa, yani sıradan attention. Satırlar nasıl değişti? Sonra `4` yap: dört kafa, her biri tek sayıya bakıyor.

### Neden kafaları bölüyoruz, çoğaltmıyoruz?

`d` boyutlu bir vektörü `h` kafaya bölünce her kafa `d / h` boyutlu bir parçayla çalışır. Toplam hesap, tek bir büyük attention'ınkine yakın kalır, ama model aynı anda `h` farklı ilişkiyi izleyebilir. Orijinal transformer makalesinde `d = 512` ve `h = 8`, yani her kafa 64 boyutlu bir parçayla çalışır.

### Şimdi sen yaz: kafalara böl ve birleştir

**Görev:** 6 sayılık bir vektör ve 3 kafa kodda hazır. Vektörü eşit kafalara bölecek, sonra kafaları yeniden yan yana birleştireceksin. Ekranda kafa boyutu, üç kafa ve birleşik vektör görünmeli; birleşik vektör başlangıçtakiyle aynı olmalı.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
kafa_sayisi = 3
d = len(x)

# TODO: Her kafa, d'nin kafa sayısına bölümü kadar sayı alır (tam bölme: //).
kafa_boyutu = ___

kafalar = []
for i in range(kafa_sayisi):
    # TODO: i. kafanın parçası: i * kafa_boyutu ile (i + 1) * kafa_boyutu arasındaki dilim.
    kafalar.append(x[___:___])

birlesik = []
for kafa in kafalar:
    # TODO: Kafaları yan yana yapıştır (listeleri + ile ekle).
    birlesik = birlesik + ___

print("Kafa boyutu:", kafa_boyutu)
print("Kafalar:", kafalar)
print("Birleşik:", birlesik)
```
```text {.python-playground-expected}
Kafa boyutu: 2
Kafalar: [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
Birleşik: [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
```
```text {.python-playground-help}
`kafa_boyutu = ___` | 6 sayıyı 3 kafaya bölüyoruz. Tam bölme için `//` kullan: `d // kafa_sayisi`.
`x[___:___]` | `i`. kafa `i * kafa_boyutu` konumunda başlar ve bir sonraki kafanın başladığı yerde, yani `(i + 1) * kafa_boyutu`'da biter.
`birlesik + ___` | İki listeyi `+` ile eklemek yan yana yapıştırır. Her turda o anki `kafa`'yı ekle.
```
```python {.python-playground-solution}
x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
kafa_sayisi = 3
d = len(x)

# Her kafa, d'nin kafa sayısına bölümü kadar sayı alır (tam bölme: //).
kafa_boyutu = d // kafa_sayisi

kafalar = []
for i in range(kafa_sayisi):
    # i. kafanın parçası: i * kafa_boyutu ile (i + 1) * kafa_boyutu arasındaki dilim.
    kafalar.append(x[i * kafa_boyutu:(i + 1) * kafa_boyutu])

birlesik = []
for kafa in kafalar:
    # Kafaları yan yana yapıştır (listeleri + ile ekle).
    birlesik = birlesik + kafa

print("Kafa boyutu:", kafa_boyutu)
print("Kafalar:", kafalar)
print("Birleşik:", birlesik)
```

## 3. Kütüphaneyle yap

NumPy'de bütün kafaları aynı anda `reshape` ile ayırıp matris çarpımlarıyla tek seferde işleyebiliriz. NumPy'yi 2.1'deki gibi kur, kodu `cok_basli_numpy.py` adıyla kaydet ve `python cok_basli_numpy.py` ile çalıştır:

```python
import numpy as np

X = np.array([
    [2.0, 0.0, 2.0, 0.0],
    [2.0, 0.0, 0.0, 2.0],
    [0.0, 2.0, 2.0, 0.0],
    [0.0, 2.0, 0.0, 2.0],
])
kafa_sayisi, kafa_boyutu = 2, 2

kafalar = X.reshape(4, kafa_sayisi, kafa_boyutu).transpose(1, 0, 2)
puanlar = kafalar @ kafalar.transpose(0, 2, 1) / np.sqrt(kafa_boyutu)
ustler = np.exp(puanlar - puanlar.max(axis=-1, keepdims=True))
agirliklar = ustler / ustler.sum(axis=-1, keepdims=True)
cikti = agirliklar @ kafalar

print("Kafalar:", kafalar.shape)
print("Kafa 1, kedi:", np.round(agirliklar[0, 0], 2))
print("Kafa 2, kedi:", np.round(agirliklar[1, 0], 2))
print("Birleşik:", cikti.transpose(1, 0, 2).reshape(4, 4).shape)
```

Beklenen çıktı:

```text
Kafalar: (2, 4, 2)
Kafa 1, kedi: [0.47 0.47 0.03 0.03]
Kafa 2, kedi: [0.47 0.03 0.47 0.03]
Birleşik: (4, 4)
```

- `X.reshape(4, 2, 2)`: Her token'ın 4 sayısını 2 kafaya, kafa başına 2 sayıya ayırır.
- `.transpose(1, 0, 2)`: Kafa eksenini öne alır; böylece `kafalar[0]` birinci kafanın bütün token'ları olur.
- `@`: NumPy, ilk eksendeki kafaların her biri için ayrı matris çarpımı yapar.
- `.transpose(1, 0, 2).reshape(4, 4)`: Kafaları tekrar yan yana birleştirir.

PyTorch'ta bütün bu işi `nn.MultiheadAttention` yapar; içinde her kafa için öğrenilen `Wq`, `Wk`, `Wv` matrisleri ve son `Wo` matrisi bulunur. PyTorch'u 3.6'daki gibi kur, kodu `cok_basli_torch.py` adıyla kaydet ve `python cok_basli_torch.py` ile çalıştır:

```python
import torch
from torch import nn

torch.manual_seed(0)
x = torch.randn(1, 4, 4)

mha = nn.MultiheadAttention(embed_dim=4, num_heads=2, batch_first=True)
cikti, agirliklar = mha(x, x, x, average_attn_weights=False)

print("Çıktı:", cikti.shape)
print("Ağırlıklar:", agirliklar.shape)
print("Satır toplamları:", [round(t, 3) for t in agirliklar.sum(dim=-1)[0, 0].tolist()])
```

Beklenen çıktı:

```text
Çıktı: torch.Size([1, 4, 4])
Ağırlıklar: torch.Size([1, 2, 4, 4])
Satır toplamları: [1.0, 1.0, 1.0, 1.0]
```

- `x`'in şekli `(batch, token, boyut) = (1, 4, 4)`.
- `embed_dim=4, num_heads=2`: 4 boyutlu vektör, 2 kafaya bölünür (kafa başına 2).
- `batch_first=True`: Girdinin ilk ekseni batch'tir.
- Ağırlıklar `(1, 2, 4, 4)`: 1 örnek, 2 kafa, her kafada 4 × 4 ağırlık matrisi.
- Her satırın toplamı `1` olduğu için son satır `[1.0, 1.0, 1.0, 1.0]` yazar. `.tolist()` tensörü Python listesine çevirir.

## 4. Sık yapılan hatalar

- **Kafa sayısını boyuta tam bölünmeyen bir sayı seçmek.** `d = 4` ve 3 kafa için kafa boyutu `4 / 3` olurdu. `d`, kafa sayısına tam bölünmelidir; `nn.MultiheadAttention` bunu denetler ve hata verir.
- **Kafaların aynı şeyi öğreneceğini sanmak.** Her kafa kendi matrisleriyle başladığı için farklı ilişkilere bakmayı öğrenebilir. Aynı başlatılırlarsa (3.4'teki simetri sorunu) aynı kalırlar.
- **Kafa çıktılarını toplamak.** Çıktılar toplanmaz, **yan yana birleştirilir**; toplamak kafaların bilgisini birbirine karıştırır.
- **Çok başlı attention'ın vektörün boyutunu büyüttüğünü sanmak.** Birleşik çıktı, girdiyle aynı boyuttadır: `h` kafa × `d / h` boyut = `d`.
- **Her kafayı yorumlanabilir sanmak.** Bu derste kafalar tür ve boyuta bakıyordu çünkü biz öyle kurduk. Eğitilmiş bir modelde kafaların ne yaptığı genellikle bu kadar net değildir; bazı kafalar anlamlı bir ilişki yakalar, bazıları pek bir şey yapmaz.

## 5. Pekiştir

**Quiz**

1. Tek bir attention bir cümledeki bütün ilişkileri neden tek başına taşıyamaz?
2. 8 boyutlu bir vektörü 4 kafaya bölersek her kafa kaç boyutlu bir parçayla çalışır?
3. Dilimlemek ile bir matrisle çarpmak arasında nasıl bir bağlantı vardır?
4. Kafaların çıktıları neden toplanmaz de yan yana birleştirilir?
5. `nn.MultiheadAttention`'da ağırlıkların şekli neden `(1, 2, 4, 4)`?

**Alıştırmalar**

1. 2.1'de `baktigi(parca, 0)` yerine `baktigi(parca, 3)` yaz. Otobüs için hangi komşular öne çıkıyor?
2. 2.2'de `W_karisik`'ı kendi seçtiğin sayılarla değiştir. Bakış nasıl değişti?
3. 2.3'te `cok_basli(X, 2)` yerine `cok_basli(X, 1)` ve `cok_basli(X, 4)` dene. Çıktılar neden farklı?
4. (İsteğe bağlı) 2.3'te token'lara beşinci bir vektör ekle: `[2.0, 0.0, 1.0, 1.0]`. Çıktı boyutu değişti mi?
5. (İsteğe bağlı) 3. bölümdeki PyTorch kodunda `num_heads=3` yap. Hangi hatayı alıyorsun ve neden?

??? success "Quiz cevapları"
    1. Her token için tek bir ağırlık dağılımı üretir; aynı token'ın kime, neye, hangi açıdan baktığı bu tek dağılıma sıkışır.
    2. `8 / 4 = 2` boyutlu bir parçayla.
    3. Dilimlemek, belirli sütunları bırakıp diğerlerini sıfırlayan özel bir matrisle çarpmaya denktir. Genel bir matris ise sayıların hepsini karıştırabilir.
    4. Toplamak, kafaların ayrı ayrı yakaladığı bilgiyi birbirine karıştırır. Yan yana birleştirince her kafanın ürettiği bilgi çıktıda kendi konumunda kalır.
    5. 1 örnek (batch), 2 kafa, her kafada her token'ın 4 token'a verdiği ağırlıklar (4 × 4).

## Özet

Çok başlı attention, vektörü kafalara bölüp her kafada ayrı bir attention çalıştırır; böylece aynı token aynı anda farklı ilişkilere bakabilir. Her kafa, vektörü kendi matrisleriyle (projeksiyon) yeni bir parçaya çevirir; bu matrisler eğitimde öğrenilir. Kafa çıktıları yan yana birleştirilir ve girdiyle aynı boyutta bir sonuç elde edilir. Sıradaki derste attention'ın hâlâ bir eksiğini gidereceğiz: token'ların **sırası** henüz modele hiç verilmedi.

## Kaynaklar

- Ashish Vaswani ve ark. (2017), *Attention Is All You Need*, NeurIPS (3.2.2 bölümü: çok başlı attention)
- [PyTorch resmî belgesi: `nn.MultiheadAttention`](https://pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
- Jay Alammar, [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)
