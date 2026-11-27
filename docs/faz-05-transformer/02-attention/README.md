# Faz 5 – Ders 2: Attention

> ⏱️ Tahmini süre: 60-75 dk · 📚 Ön koşul: 1.2 Matris çarpımı, 4.5 Benzerlik ve arama, 5.1 Dizi modelleme · 💻 Gereksinim: Python 3.11+, ek paket yok; NumPy ve PyTorch örnekleri isteğe bağlı

## Bu derste ne öğreneceksin?

- Bir token'ın, bağlamdaki hangi token'lara ne kadar bakacağını sayıyla nasıl ifade ettiğini
- **Softmax** ile puanları ağırlıklara çevirmeyi
- **Sorgu, anahtar ve değer** (query, key, value) fikrini
- Ölçekli noktasal çarpım **attention**'ını sıfırdan yazmayı
- **Maskeleme** ile bir token'ın geleceğe ya da padding'e bakmasını engellemeyi

## 1. Problem

5.1'de bigram modeli yalnızca bir önceki token'a bakıyordu ve "su içti" ile "süt içti" arasındaki farkı göremiyordu. Daha çok token'a bakmak istiyoruz; ama hepsine eşit bakmak da çözüm değil. "Kedi süt içti" cümlesinde `içti`'yi anlamak için `kedi` ve `süt` önemlidir; aradaki bağlaçlar ya da başka sözcükler o kadar önemli olmayabilir.

**Attention** (dikkat mekanizması) şunu yapar: Bir token, bağlamdaki her token için bir **önem puanı** hesaplar. Puanları ağırlıklara çevirir (toplamları `1` olur) ve token'ların bilgisini bu ağırlıklarla karıştırır. Yani her token, "kime ne kadar bakmalıyım?" sorusunu **kendisi** cevaplar.

Bu fikir üç parçayla anlatılır. Bir kütüphane aramasına benzetebilirsin:

- **Sorgu (query):** "Ben ne arıyorum?" Bakan token'ın merak ettiği şey.
- **Anahtar (key):** "Ben neyim?" Her token'ın kendini tanıttığı etiket. Sorgu ile anahtar ne kadar uyuşuyorsa puan o kadar yüksek.
- **Değer (value):** "Sana vereceğim bilgi bu." Puanı yüksek olan token'ların değerleri çıktıya daha çok karışır.

## 2. Kendin yaz

### 2.1 Softmax: puanları ağırlıklara çevirmek

Attention'ın ilk ihtiyacı, herhangi bir sayı listesini, toplamı `1` olan pozitif ağırlıklara çeviren bir işlevdir. Bu işlev **softmax**'tır. 2.3 dersindeki sigmoid'in birden çok sonuç için hâlidir. Her puanın `e` üstünü alır, hepsinin toplamına böler.

```python {.python-playground}
import math


def softmax(puanlar):
    en_buyuk = max(puanlar)
    ustler = [math.exp(p - en_buyuk) for p in puanlar]
    toplam = sum(ustler)
    return [u / toplam for u in ustler]


print([round(a, 3) for a in softmax([2.0, 1.0, 0.1])])
print("Toplam:", round(sum(softmax([2.0, 1.0, 0.1])), 3))
print([round(a, 3) for a in softmax([20.0, 10.0, 1.0])])
```
```text {.python-playground-expected}
[0.659, 0.242, 0.099]
Toplam: 1.0
[1.0, 0.0, 0.0]
```
```text {.python-playground-help}
`def softmax(puanlar):` | Puanlar listesini alıp aynı uzunlukta bir ağırlık listesi döndürür.
`en_buyuk = max(puanlar)` | En büyük puanı buluruz. Her puandan bunu çıkaracağız; sonucu değiştirmez, ama çok büyük sayılarda `math.exp`'in taşmasını önler.
`math.exp(p - en_buyuk)` | Her puanın `e` üstünü alır. Üs alma, negatif puanları da pozitif yapar.
`u / toplam` | Hepsini toplama bölünce ağırlıkların toplamı `1` olur.
`softmax([20.0, 10.0, 1.0])` | Aynı sıralama, ama puanlar birbirinden daha uzak. En büyük puan neredeyse bütün ağırlığı alır.
```

Softmax en büyük puana en büyük ağırlığı verir, ama diğerlerini sıfırlamaz. Puanlar arasındaki fark büyüdükçe dağılım keskinleşir. Son satırdaki sayılara bak: `20` puanlı seçenek ağırlığın neredeyse tamamını aldı.

### 2.2 Tek bir sorgu için attention

Üç token'ımız var: `kedi`, `süt`, `içti`. Her birinin bir anahtarı ve bir değeri var. `içti` token'ı sorgu olarak bunlara bakıyor. Adımlar:

1. **Puan:** Sorgu ile her anahtarın noktasal çarpımını al (1.2). Ne kadar benzerlerse çarpım o kadar büyük olur.
2. **Ölçekle:** Puanı `√d`'ye böl; `d` vektörlerin boyutu. Boyut büyüdükçe noktasal çarpımlar büyür ve softmax keskinleşip öğrenmeyi zorlaştırır. Bölme bunu dengeler.
3. **Softmax:** Puanları ağırlıklara çevir.
4. **Karıştır:** Değer vektörlerini ağırlıklarıyla çarpıp topla. Bu, token'ın yeni temsilidir.

```python {.python-playground}
import math

tokenlar = ["kedi", "süt", "içti"]
anahtarlar = [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]]
degerler = [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]]
sorgu = [1.0, 0.2]
d = len(sorgu)

puanlar = []
for anahtar in anahtarlar:
    nokta = sum(q * k for q, k in zip(sorgu, anahtar))
    puanlar.append(nokta / math.sqrt(d))

ustler = [math.exp(p) for p in puanlar]
agirliklar = [u / sum(ustler) for u in ustler]

cikti = [0.0, 0.0]
for w, deger in zip(agirliklar, degerler):
    cikti[0] += w * deger[0]
    cikti[1] += w * deger[1]

for token, w in zip(tokenlar, agirliklar):
    print(f"{token}: ağırlık {w:.2f}")
print("Çıktı:", [round(c, 2) for c in cikti])
```
```text {.python-playground-expected}
kedi: ağırlık 0.43
süt: ağırlık 0.24
içti: ağırlık 0.32
Çıktı: [0.59, 0.41]
```
```text {.python-playground-help}
`sorgu = [1.0, 0.2]` | Bakan token'ın sorusu. Burada ilk boyutu büyük: ilk boyutu yüksek olan anahtarları arıyor.
`sum(q * k for q, k in zip(sorgu, anahtar))` | Sorgu ile anahtarın noktasal çarpımı; benzerlik puanı.
`nokta / math.sqrt(d)` | Puanı `√d`'ye böleriz. Burada `d = 2`.
`agirliklar = [u / sum(ustler) for u in ustler]` | Softmax: üstleri toplamlarına böleriz.
`cikti[0] += w * deger[0]` | Ağırlıklı toplam: her değer vektörü, ağırlığı kadar çıktıya karışır. İlk boyutu ayrı, ikinci boyutu ayrı toplarız.
```

Sorgunun ilk boyutu büyük olduğu için ilk anahtarı olan `kedi` en yüksek ağırlığı aldı; `süt` en düşüğünü. Çıktı, değerlerin bu ağırlıklarla karışımıdır. Sorguyu `[0.2, 1.0]` yapıp ağırlıkların nasıl el değiştirdiğini gör.

### 2.3 Self-attention: her token herkese bakar

Gerçek bir modelde **her** token aynı anda sorgu olur ve bütün token'lara bakar. Buna **self-attention** denir ("kendine dikkat"): dizi kendi içindeki token'lara bakar. Bu derste basit tutmak için sorgu, anahtar ve değer olarak token'ın kendi vektörünü kullanıyoruz. 5.3'te bunları öğrenilen ağırlıklarla dönüştüreceğiz.

Bütün puanlar bir matris olarak hesaplanır: `puanlar[i][j]`, `i`. token'ın `j`. token'a verdiği puandır.

```python {.python-playground}
import math

tokenlar = ["kedi", "süt", "içti"]
X = [[2.0, 0.0], [0.5, 2.0], [1.5, 1.5]]
d = len(X[0])


def softmax(puanlar):
    ustler = [math.exp(p - max(puanlar)) for p in puanlar]
    return [u / sum(ustler) for u in ustler]


agirlik_matrisi = []
cikti_matrisi = []
for sorgu in X:
    puanlar = [sum(q * k for q, k in zip(sorgu, anahtar)) / math.sqrt(d) for anahtar in X]
    agirliklar = softmax(puanlar)
    agirlik_matrisi.append(agirliklar)
    cikti = [sum(w * deger[j] for w, deger in zip(agirliklar, X)) for j in range(d)]
    cikti_matrisi.append(cikti)

print("Ağırlık matrisi (satır: bakan, sütun: bakılan)")
for token, satir in zip(tokenlar, agirlik_matrisi):
    print(f"{token:5}", [round(w, 2) for w in satir])
print("Çıktılar")
for token, satir in zip(tokenlar, cikti_matrisi):
    print(f"{token:5}", [round(c, 2) for c in satir])
```
```text {.python-playground-expected}
Ağırlık matrisi (satır: bakan, sütun: bakılan)
kedi  [0.62, 0.07, 0.31]
süt   [0.06, 0.55, 0.39]
içti  [0.18, 0.3, 0.52]
Çıktılar
kedi  [1.74, 0.61]
süt   [0.97, 1.69]
içti  [1.29, 1.38]
```
```text {.python-playground-help}
`X = [[2.0, 0.0], ...]` | Üç token'ın vektörleri. Her satır bir token'dır.
`for sorgu in X:` | Sırayla her token sorgu olur.
`for anahtar in X` | Sorgu, bütün token'ların (kendisi dahil) anahtarına bakar.
`softmax(puanlar)` | Bir token'ın puanlarını ağırlıklara çevirir; her satırın toplamı `1` olur.
`sum(w * deger[j] for w, deger in zip(agirliklar, X))` | `j`. boyut için ağırlıklı toplam: her token'ın o boyuttaki değeri, ağırlığı kadar karışır.
`f"{token:5}"` | Token adını 5 karakter genişliğinde yazar; satırlar hizalı görünür.
```

Her satır bir token'ın "kime baktığını" gösterir. `kedi` en çok kendine (`0.62`), `içti` ise en çok kendine ama `süt` ve `kedi`'ye de ciddi ağırlık veriyor. Çıktılar artık bağlamla karışmış vektörlerdir: `içti`'nin yeni vektöründe `kedi` ve `süt`'ten gelen bilgi de var.

### 2.4 Maskeleme: geleceğe bakmak yasak

Bir dil modeli sıradaki token'ı tahmin ederken henüz **gelmemiş** token'ları göremez; görürse cevabı önceden bilir (5.1'deki hedefi bağlama koymak hatası). Bunun için `i`. token'ın yalnızca kendisine ve öncesine bakmasına izin veririz. Gelecekteki konumların puanını çok küçük bir sayıya (`-1e9`) ayarlarız. Softmax'ta bunların `e` üstü neredeyse `0` olur, yani ağırlıkları `0` olur. Buna **maske** denir.

Aynı yöntem **padding**'i gizlemek için de kullanılır: `[PAD]` konumlarının puanı `-1e9` yapılır ve hiçbir token onlara bakmaz.

```python {.python-playground}
import math

X = [[2.0, 0.0], [0.5, 2.0], [1.5, 1.5]]
d = len(X[0])


def softmax(puanlar):
    ustler = [math.exp(p - max(puanlar)) for p in puanlar]
    return [u / sum(ustler) for u in ustler]


for i, sorgu in enumerate(X):
    puanlar = []
    for j, anahtar in enumerate(X):
        puan = sum(q * k for q, k in zip(sorgu, anahtar)) / math.sqrt(d)
        if j > i:
            puan = -1e9
        puanlar.append(puan)
    print([round(w, 2) for w in softmax(puanlar)])
```
```text {.python-playground-expected}
[1.0, 0.0, 0.0]
[0.09, 0.91, 0.0]
[0.18, 0.3, 0.52]
```
```text {.python-playground-help}
`for i, sorgu in enumerate(X):` | `enumerate` her token'ın konumunu (`i`) de verir. Bakan token `i`. konumdadır.
`for j, anahtar in enumerate(X):` | `j`, bakılan token'ın konumudur.
`if j > i:` | Bakılan konum, bakandan sonra geliyorsa gelecektir.
`puan = -1e9` | Gelecekteki konumun puanını çok küçük yapar; softmax'ta ağırlığı `0` olur.
```

Üst üçgen sıfırlandı: ilk token yalnızca kendine (`1.0`), ikinci token ilk iki token'a, üçüncü hepsine bakıyor. Her satırın toplamı hâlâ `1`. GPT gibi metin üreten modeller bu maskeyi kullanır (Faz 6).

### Şimdi sen yaz: tek sorgulu attention

**Görev:** Üç token'ın anahtarları, değerleri ve bir sorgu kodda hazır. Sorgunun her token'a verdiği puanı hesaplayıp softmax ile ağırlığa çevirecek, sonra değerleri bu ağırlıklarla karıştıracaksın. Ekranda üç ağırlık ve karışım çıktısı görünmeli.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
import math

anahtarlar = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
degerler = [[2.0, 0.0], [0.0, 4.0], [1.0, 1.0]]
sorgu = [1.0, 0.0]
d = 2

puanlar = []
for anahtar in anahtarlar:
    # TODO: Sorgu ile anahtarın noktasal çarpımını al, sonra √d'ye böl (math.sqrt).
    puanlar.append(___)

ustler = [math.exp(p) for p in puanlar]
# TODO: Softmax: her üstü, üstlerin toplamına böl.
agirliklar = [u / ___ for u in ustler]

cikti = [0.0, 0.0]
for w, deger in zip(agirliklar, degerler):
    # TODO: Değerin ilk boyutunu ağırlığıyla çarpıp çıktıya ekle.
    cikti[0] += ___
    cikti[1] += w * deger[1]

print("Ağırlıklar:", [round(w, 2) for w in agirliklar])
print("Çıktı:", [round(c, 2) for c in cikti])
```
```text {.python-playground-expected}
Ağırlıklar: [0.4, 0.2, 0.4]
Çıktı: [1.2, 1.19]
```
```text {.python-playground-help}
`puanlar.append(___)` | Sorgu ile anahtarı boyut boyut çarpıp topla (`zip` ve `sum` ile), sonucu `math.sqrt(d)`'ye böl.
`u / ___` | Softmax'ta her üst, bütün üstlerin toplamına bölünür: `sum(ustler)`.
`cikti[0] += ___` | Altındaki satırın aynısı, ama ilk boyut için: `w * deger[0]`.
```
```python {.python-playground-solution}
import math

anahtarlar = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
degerler = [[2.0, 0.0], [0.0, 4.0], [1.0, 1.0]]
sorgu = [1.0, 0.0]
d = 2

puanlar = []
for anahtar in anahtarlar:
    # Sorgu ile anahtarın noktasal çarpımını al, sonra √d'ye böl (math.sqrt).
    puanlar.append(sum(q * k for q, k in zip(sorgu, anahtar)) / math.sqrt(d))

ustler = [math.exp(p) for p in puanlar]
# Softmax: her üstü, üstlerin toplamına böl.
agirliklar = [u / sum(ustler) for u in ustler]

cikti = [0.0, 0.0]
for w, deger in zip(agirliklar, degerler):
    # Değerin ilk boyutunu ağırlığıyla çarpıp çıktıya ekle.
    cikti[0] += w * deger[0]
    cikti[1] += w * deger[1]

print("Ağırlıklar:", [round(w, 2) for w in agirliklar])
print("Çıktı:", [round(c, 2) for c in cikti])
```

## 3. Kütüphaneyle yap

Bütün hesap, matris çarpımlarıyla tek satırda yazılır: `softmax(Q × Kᵀ / √d) × V`. NumPy'yi 2.1'deki gibi kur, kodu `attention_numpy.py` adıyla kaydet ve `python attention_numpy.py` ile çalıştır:

```python
import numpy as np

X = np.array([[2.0, 0.0], [0.5, 2.0], [1.5, 1.5]])
d = X.shape[1]

puanlar = X @ X.T / np.sqrt(d)
ustler = np.exp(puanlar - puanlar.max(axis=1, keepdims=True))
agirliklar = ustler / ustler.sum(axis=1, keepdims=True)
cikti = agirliklar @ X

print(np.round(agirliklar, 2))
print(np.round(cikti, 2))
```

Beklenen çıktı:

```text
[[0.62 0.07 0.31]
 [0.06 0.55 0.39]
 [0.18 0.3  0.52]]
[[1.74 0.61]
 [0.97 1.69]
 [1.29 1.38]]
```

PyTorch'ta aynı işi yapan hazır bir işlev vardır: `F.scaled_dot_product_attention`. `is_causal=True` verirsen 2.4'teki maskeyi kendisi uygular. PyTorch'u 3.6'daki gibi kur, kodu `attention_torch.py` adıyla kaydet ve `python attention_torch.py` ile çalıştır:

```python
import torch
import torch.nn.functional as F

X = torch.tensor([[[2.0, 0.0], [0.5, 2.0], [1.5, 1.5]]])

cikti = F.scaled_dot_product_attention(X, X, X)
maskeli = F.scaled_dot_product_attention(X, X, X, is_causal=True)

print(cikti.round(decimals=2)[0])
print(maskeli.round(decimals=2)[0])
```

Beklenen çıktı:

```text
tensor([[1.7400, 0.6100],
        [0.9700, 1.6900],
        [1.2900, 1.3800]])
tensor([[2.0000, 0.0000],
        [0.6400, 1.8200],
        [1.2900, 1.3800]])
```

`X`'in ilk boyutu (`[[[...]]]` ile görülen dış köşeli ayraç) **batch** boyutudur; modeller birçok diziyi aynı anda işler. Üç kez `X` vermemizin nedeni sorgu, anahtar ve değerin bu derste aynı olmasıdır.

## 4. Sık yapılan hatalar

- **`√d` bölmesini unutmak.** Boyut büyüdükçe puanlar büyür; softmax tek bir token'a neredeyse tüm ağırlığı verir ve öğrenme zorlaşır.
- **Softmax'ı yanlış eksende almak.** Her token için o token'ın puanları (matrisin bir satırı) üzerinde softmax alınır. Sütun boyunca almak anlamsız sonuç verir.
- **Softmax'ta en büyük puanı çıkarmamak.** `math.exp(1000)` taşar. En büyük puanı çıkarmak sonucu değiştirmez, ama taşmayı önler.
- **Gelecek konumları maskelememek.** Metin üreten bir modelde, maskesiz attention eğitimde cevabı görür ve gerçek kullanımda çalışmaz.
- **Maskeyi 0 ile uygulamak.** Puanı `0` yapmak ağırlığı sıfırlamaz (`e⁰ = 1`). Maske, softmax'tan **önce** çok küçük bir sayı (`-1e9` ya da `-∞`) koyarak uygulanır.
- **Ağırlıkları kesin sayılar sanmak.** Ağırlıklar her zaman pozitiftir ve toplamları `1`'dir; hiçbir token'a tam olarak `0` bakılmaz (maske hariç).

## 5. Pekiştir

**Quiz**

1. Sorgu, anahtar ve değer kavramlarını kendi cümlelerinle anlat.
2. Softmax neden her puanın `e` üstünü alır ve sonra toplama böler?
3. Puanları `√d`'ye neden böleriz?
4. Self-attention'da bir token kimlere bakar?
5. Gelecekteki token'lara bakmayı nasıl engelleriz?

**Alıştırmalar**

1. 2.1'de ilk listeyi `[1.0, 1.0, 1.0]` yap. Ağırlıklar ne oluyor? Neden?
2. 2.2'de sorguyu `[0.2, 1.0]` yap. En yüksek ağırlığı hangi token alıyor?
3. 2.3'te `X`'in ikinci satırını `[0.5, 2.0]`'dan `[2.0, 0.0]`'a çevir. `kedi` ile `süt` aynı vektöre sahip olunca ağırlık matrisi nasıl değişiyor?
4. 2.4'te maskeyi tersine çevir: `j > i` yerine `j < i` koy. Bu hangi tür bir modelde işe yarardı? (İpucu: bir token yalnızca kendisinden *sonrakilere* bakıyor.)
5. (İsteğe bağlı) 2.2'deki puan hesabında `math.sqrt(d)` bölmesini kaldır ve sorguyu `[10.0, 2.0]` yap. Ağırlıklar nasıl değişti?

??? success "Quiz cevapları"
    1. Sorgu: bakan token'ın aradığı şey. Anahtar: her token'ın kendini tanıttığı etiket. Değer: o token'ın çıktıya karıştıracağı bilgi. Sorgu-anahtar uyumu puanı belirler; değerler bu puanlarla karışır.
    2. `e` üstü hem negatif puanları pozitif yapar hem büyük puanı daha da öne çıkarır. Toplama bölmek, ağırlıkların toplamını `1` yapar.
    3. Vektör boyutu büyüdükçe noktasal çarpımların değeri büyür. Büyük puanlar softmax'ı keskinleştirir ve öğrenmeyi zorlaştırır. `√d`'ye bölmek puanları dengelenmiş tutar.
    4. Kendisi dahil, dizideki bütün token'lara (maske yoksa).
    5. Maskeyle: gelecekteki konumların puanını softmax'tan önce çok küçük bir sayı yaparak ağırlıklarını `0` yaparız.

## Özet

Attention, her token'ın bağlamdaki token'lara ne kadar bakacağını sayıyla belirler. Sorgu ile anahtarın noktasal çarpımı puan verir; puan `√d`'ye bölünür, softmax ağırlığa çevirir ve değerler bu ağırlıklarla karıştırılır. Self-attention'da her token aynı anda hem sorgu hem anahtar hem değerdir. Maske, bir token'ın geleceğe ya da padding'e bakmasını engeller. Bütün hesap `softmax(Q Kᵀ / √d) V` biçiminde matrislerle yazılır. Sonraki derste bunu daha güçlü hâle getireceğiz: aynı anda birden fazla ilişkiyi yakalamak için **çok başlı attention**.

## Kaynaklar

- Ashish Vaswani ve ark. (2017), *Attention Is All You Need*, NeurIPS
- Dzmitry Bahdanau, Kyunghyun Cho ve Yoshua Bengio (2015), *Neural Machine Translation by Jointly Learning to Align and Translate*, ICLR (attention fikrinin ilk uygulamalarından)
- [PyTorch resmî belgesi: `scaled_dot_product_attention`](https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)
- Jay Alammar, [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) (görsel anlatım)
