# Faz 3 – Ders 1: Tek nöron

> ⏱️ Tahmini süre: 45-60 dk · 📚 Ön koşul: 1.2 Matris çarpımı, 2.3 Lojistik regresyon · 💻 Gereksinim: Python 3.11+; temel örnekler ek paketsiz, NumPy örneği için NumPy kurulmalıdır

## Bu derste ne öğreneceksin?

- Bir yapay nöronun girdileri ağırlıklarla nasıl birleştirdiğini
- Aktivasyon fonksiyonunun ne işe yaradığını ve üç yaygın örneğini
- Ağırlıkları elle seçerek basit bir mantık kapısı kurmayı
- Perceptron kuralıyla nöronun ağırlıklarını örneklerden öğrenmesini
- Tek bir nöronun neyi yapamadığını

## 1. Problem

Sinir ağları adını beyindeki sinir hücrelerinden alır, ama bilgisayardaki **yapay nöron** çok daha basittir. Birkaç sayı alır, her birini kendi **ağırlığıyla** çarpar, sonuçları toplar, bir **sabit terim** ekler ve toplamı bir **aktivasyon fonksiyonundan** geçirir.

```text
girdiler → (ağırlıklarla çarp ve topla) + sabit → aktivasyon → çıktı
```

Bu yapıyı aslında 2.3 dersinde gördün: lojistik regresyon, sigmoid aktivasyonu kullanan tek bir nörondur. Bu derste aynı parçayı "sinir ağının yapı taşı" gözüyle inceleyeceğiz. Sonraki derslerde bu nöronlardan katmanlar ve ağlar kuracağız.

## 2. Kendin yaz

### 2.1 Ağırlıklı toplam

Nöronun ilk işi, girdileri ağırlıklarla çarpıp toplamaktır. Bu, 1.2 dersindeki noktasal çarpımın aynısıdır. Sonuca sabit terimi ekleriz. Bu ara değere genellikle `z` denir.

```python {.python-playground}
girdiler = [1.0, 0.5]
agirliklar = [0.8, -0.4]
sabit = 0.1

z = 0
for i in range(len(girdiler)):
    z += girdiler[i] * agirliklar[i]
z += sabit

print("Ağırlıklı toplam z:", round(z, 2))
```
```text {.python-playground-expected}
Ağırlıklı toplam z: 0.7
```
```text {.python-playground-help}
`girdiler = [1.0, 0.5]` | Nörona gelen iki sayıyı listede tutarız. Gerçek bir uygulamada bunlar bir örneğin özellikleri olabilir.
`agirliklar = [0.8, -0.4]` | Her girdinin ne kadar önemli olduğunu belirleyen ağırlıklardır. Negatif ağırlık, o girdi büyüdükçe toplamı küçültür.
`sabit = 0.1` | Girdilerden bağımsız olarak toplama eklenen sayıdır. Nöronun ne kadar kolay "ateşleneceğini" kaydırır.
`z = 0` | Toplamı biriktirmek için sıfırdan başlarız.
`z += girdiler[i] * agirliklar[i]` | Aynı konumdaki girdi ile ağırlığı çarpıp toplama ekleriz: `1.0 × 0.8 + 0.5 × (-0.4) = 0.6`.
`z += sabit` | Sabit terimi ekleriz: `0.6 + 0.1 = 0.7`.
`round(z, 2)` | Ondalıklı sayılardaki küçük yuvarlama farklarını gizlemek için sonucu iki basamağa yuvarlarız.
```

Bir ağırlığı büyütürsen o girdinin sonuca etkisi artar. `agirliklar` listesindeki ikinci sayıyı `0.4` yapıp sonucun nasıl değiştiğine bak.

### 2.2 Aktivasyon fonksiyonu

Ağırlıklı toplam herhangi bir sayı olabilir. **Aktivasyon fonksiyonu** bu sayıyı nöronun çıktısına çevirir. Üç yaygın örnek:

| Ad | Kural | Çıktı aralığı |
|---|---|---|
| **Basamak** | `z ≥ 0` ise `1`, değilse `0` | yalnızca `0` veya `1` |
| **Sigmoid** | `1 / (1 + e^(-z))` | `0` ile `1` arası |
| **ReLU** | `z` pozitifse `z`, değilse `0` | `0` ve üstü |

```python {.python-playground}
import math


def basamak(z):
    return 1 if z >= 0 else 0


def sigmoid(z):
    return 1 / (1 + math.exp(-z))


def relu(z):
    return max(0, z)


for z in [-2, 0, 2]:
    print(f"z={z}: basamak={basamak(z)}, sigmoid={round(sigmoid(z), 2)}, relu={relu(z)}")
```
```text {.python-playground-expected}
z=-2: basamak=0, sigmoid=0.12, relu=0
z=0: basamak=1, sigmoid=0.5, relu=0
z=2: basamak=1, sigmoid=0.88, relu=2
```
```text {.python-playground-help}
`def basamak(z):` | Basamak fonksiyonu yalnızca iki çıktı verir; nöron ya "açık" ya "kapalı"dır.
`return 1 if z >= 0 else 0` | Tek satırlık koşul: `z` sıfır veya daha büyükse `1`, değilse `0` döndürür.
`def sigmoid(z):` | 2.3 dersindeki sigmoid; çıktıyı yumuşak biçimde `0` ile `1` arasına sıkıştırır.
`def relu(z):` | ReLU, negatif sayıları sıfıra çevirir, pozitifleri olduğu gibi bırakır.
`return max(0, z)` | `max` iki sayıdan büyüğünü verir; `z` negatifse `0` daha büyüktür.
`for z in [-2, 0, 2]:` | Üç fonksiyonu aynı üç sayı üzerinde karşılaştırırız.
`print(f"...")` | Her `z` için üç aktivasyonun sonucunu tek satırda gösteririz.
```

Aktivasyon neden gerekli? Aktivasyon olmadan nöronlar yalnızca çarpıp toplar. Bu tür işlemleri art arda yapmak yine çarpıp toplamaya denk gelir; yani ne kadar katman eklersen ekle, ağ düz bir çizgiden fazlasını öğrenemez. Sigmoid ve ReLU gibi **doğrusal olmayan** fonksiyonlar, ağa eğri sınırlar çizme gücü verir. Bunu 3.4 dersinde göreceğiz.

### 2.3 Ağırlıkları elle seçerek bir VE kapısı kur

**VE** (AND) kapısı iki girdiyi alır; yalnızca ikisi de `1` ise `1` verir. Ağırlıkları `1` ve `1`, sabiti `-1.5` seçersek toplam yalnızca iki girdi de `1` olduğunda sıfırı geçer.

```python {.python-playground}
def noron(girdiler, agirliklar, sabit):
    z = 0
    for i in range(len(girdiler)):
        z += girdiler[i] * agirliklar[i]
    z += sabit
    return 1 if z >= 0 else 0


agirliklar = [1, 1]
sabit = -1.5

for a in [0, 1]:
    for b in [0, 1]:
        print(f"{a} VE {b} = {noron([a, b], agirliklar, sabit)}")
```
```text {.python-playground-expected}
0 VE 0 = 0
0 VE 1 = 0
1 VE 0 = 0
1 VE 1 = 1
```
```text {.python-playground-help}
`def noron(girdiler, agirliklar, sabit):` | Önceki iki adımı tek fonksiyonda birleştiririz: ağırlıklı toplam ve basamak aktivasyonu.
`return 1 if z >= 0 else 0` | Toplam sıfır veya daha büyükse nöron `1` verir.
`agirliklar = [1, 1]` | İki girdi de eşit önemdedir.
`sabit = -1.5` | Toplamı aşağı çeker. `1 + 1 - 1.5 = 0.5` sıfırdan büyük olur; ama `1 + 0 - 1.5 = -0.5` sıfırdan küçük kalır.
`for a in [0, 1]:` ve `for b in [0, 1]:` | İç içe iki döngü, dört olası girdi çiftini sırayla dener.
`noron([a, b], agirliklar, sabit)` | Girdi çiftini nörona verip sonucunu yazdırırız.
```

`sabit` değerini `-0.5` yaparsan nöron **VEYA** (OR) kapısı gibi davranır: girdilerden biri `1` olunca bile toplam sıfırı geçer. Dene ve tabloyu kontrol et.

### 2.4 Perceptron: ağırlıkları örneklerden öğren

Ağırlıkları elle bulmak küçük örneklerde kolaydır, ama asıl istediğimiz nöronun bunları **veriden öğrenmesidir**. 1958'de Frank Rosenblatt'ın tanıttığı **perceptron kuralı** çok basittir:

- Nöron doğru tahmin ettiyse hiçbir şeyi değiştirme.
- Yanlış tahmin ettiyse her ağırlığı `öğrenme hızı × (hedef - tahmin) × girdi` kadar düzelt; sabiti de `öğrenme hızı × (hedef - tahmin)` kadar.

`hedef - tahmin` farkı `+1` ise nöron fazla çekingen davranmıştır ve ağırlıklar artar; `-1` ise fazla hevesli davranmıştır ve ağırlıklar azalır. Aşağıda nöron VEYA kapısını sıfırdan öğreniyor:

```python {.python-playground}
veri = [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 1)]
agirliklar = [0.0, 0.0]
sabit = 0.0
ogrenme_hizi = 0.1

for tur in range(1, 21):
    hata_sayisi = 0
    for girdiler, hedef in veri:
        z = agirliklar[0] * girdiler[0] + agirliklar[1] * girdiler[1] + sabit
        tahmin = 1 if z >= 0 else 0
        fark = hedef - tahmin
        if fark != 0:
            hata_sayisi += 1
            agirliklar[0] += ogrenme_hizi * fark * girdiler[0]
            agirliklar[1] += ogrenme_hizi * fark * girdiler[1]
            sabit += ogrenme_hizi * fark
    print(f"Tur {tur}: {hata_sayisi} hata")
    if hata_sayisi == 0:
        break

print("Ağırlıklar:", [round(a, 2) for a in agirliklar], "Sabit:", round(sabit, 2))
```
```text {.python-playground-expected}
Tur 1: 2 hata
Tur 2: 2 hata
Tur 3: 1 hata
Tur 4: 0 hata
Ağırlıklar: [0.1, 0.1] Sabit: -0.1
```
```text {.python-playground-help}
`veri = [([0, 0], 0), ...]` | Her öğe bir `(girdiler, hedef)` çiftidir. Hedefler VEYA kapısının doğru cevaplarıdır.
`agirliklar = [0.0, 0.0]` ve `sabit = 0.0` | Nöron hiçbir şey bilmeden, sıfır ağırlıklarla başlar.
`for tur in range(1, 21):` | Veriyi en fazla 20 kez baştan sona dolaşırız. Her dolaşmaya bir **tur** (epoch) denir.
`hata_sayisi = 0` | Bu turda kaç yanlış tahmin yapıldığını sayarız.
`for girdiler, hedef in veri:` | Örnekleri sırayla alırız ve çifti iki değişkene açarız.
`tahmin = 1 if z >= 0 else 0` | Nöronun o anki ağırlıklarla verdiği cevaptır.
`fark = hedef - tahmin` | Doğruysa `0`; nöron `0` deyip `1` gerekiyorsa `+1`; tersiyse `-1` olur.
`agirliklar[0] += ogrenme_hizi * fark * girdiler[0]` | Perceptron kuralı. Girdi `0` ise bu ağırlık değişmez, çünkü o girdi hataya katkı vermemiştir.
`sabit += ogrenme_hizi * fark` | Sabit, her zaman `1` olan hayali bir girdinin ağırlığı gibi güncellenir.
`if hata_sayisi == 0: break` | Bütün örnekler doğru bilindiyse öğrenme tamamlanmıştır; döngüden çıkarız.
```

Öğrenilen ağırlıklar elle seçtiğimiz sayılardan farklı ama aynı işi yapıyor: `0.1 + 0.1 - 0.1` sıfırdan büyük, `0 + 0 - 0.1` sıfırdan küçük. Bir problemin genellikle birden çok doğru ağırlık takımı vardır.

!!! warning "Tek nöronun sınırı"
    Tek bir nöron girdileri **düz bir çizgiyle** ikiye ayırabilir. VE ve VEYA kapıları böyle ayrılabilir; ama **XOR** (girdiler farklıysa `1`) ayrılamaz. Alıştırma 4'te bunu kendin göreceksin. 1969'da Minsky ve Papert'in bu sınırı göstermesi, sinir ağlarına ilgiyi yıllarca azalttı. Çözüm birden fazla katmandır; 3.4 dersinde XOR'u çok katmanlı bir ağla öğreteceğiz.

### Şimdi sen yaz: VEYA kapısı

Nöron fonksiyonunu tamamla ve VEYA kapısı için sabit terimi seç. Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur, sonra çalıştır.

```python {.python-playground-task}
def noron(girdiler, agirliklar, sabit):
    z = 0
    for i in range(len(girdiler)):
        # TODO: Girdiyi kendi ağırlığıyla çarpıp z'ye ekle.
        z += ___
    z += sabit
    return 1 if z >= 0 else 0


# TODO: VEYA kapısı için uygun sabiti seç. Ağırlıklar [1, 1].
# (0, 0) için çıktı 0, diğer üç girdi için 1 olmalı.
for a in [0, 1]:
    for b in [0, 1]:
        print(f"{a} VEYA {b} = {noron([a, b], [1, 1], ___)}")
```
```text {.python-playground-expected}
0 VEYA 0 = 0
0 VEYA 1 = 1
1 VEYA 0 = 1
1 VEYA 1 = 1
```
```text {.python-playground-help}
`z += ___` | Ağırlıklı toplamda her girdi kendi ağırlığıyla çarpılır: `girdiler[i] * agirliklar[i]`.
`noron([a, b], [1, 1], ___)` | `(0, 0)` iken toplam sadece sabittir ve çıktı `0` olmalı: sabit negatif. `(0, 1)` iken `1 + sabit` sıfırdan küçük olmamalı. `-0.5` ikisini de sağlar.
```
```python {.python-playground-solution}
def noron(girdiler, agirliklar, sabit):
    z = 0
    for i in range(len(girdiler)):
        # Girdiyi kendi ağırlığıyla çarpıp z'ye ekle.
        z += girdiler[i] * agirliklar[i]
    z += sabit
    return 1 if z >= 0 else 0


# VEYA kapısı için uygun sabiti seç. Ağırlıklar [1, 1].
# (0, 0) için çıktı 0, diğer üç girdi için 1 olmalı.
for a in [0, 1]:
    for b in [0, 1]:
        print(f"{a} VEYA {b} = {noron([a, b], [1, 1], -0.5)}")
```

## 3. Kütüphaneyle yap

Gerçek ağlarda tek tek döngü yazmak yerine bütün örnekleri bir matris olarak tutar, ağırlıklı toplamı tek bir matris çarpımıyla hesaplarız. NumPy'yi 2.1 dersindeki gibi kur, aşağıdaki kodu `noron_numpy.py` adıyla kaydedip `python noron_numpy.py` ile çalıştır:

```python
import numpy as np

girdiler = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
agirliklar = np.array([1, 1])
sabit = -1.5

z = girdiler @ agirliklar + sabit
ciktilar = (z >= 0).astype(int)

print("z:", z)
print("VE çıktıları:", ciktilar)
```

Beklenen çıktı:

```text
z: [-1.5 -0.5 -0.5  0.5]
VE çıktıları: [0 0 0 1]
```

`girdiler @ agirliklar` her satırı ağırlıklarla çarpıp toplar, yani dört örneğin `z` değerini tek seferde bulur. `+ sabit` yayınlama (broadcasting) ile her sonuca eklenir. `(z >= 0)` her eleman için `True`/`False` üretir; `.astype(int)` bunları `1`/`0` yapar. Bu kod tarayıcıdaki pencerede çalışmaz, çünkü orada NumPy kurulu değildir.

## 4. Sık yapılan hatalar

- **Sabit terimi unutmak.** Sabit olmadan nöronun karar sınırı her zaman orijinden (bütün girdiler `0` iken) geçmek zorunda kalır. VE kapısı sabitsiz kurulamaz.
- **Ağırlık ile girdiyi karıştırmak.** Girdiler veriden gelir ve değişmez; öğrenme sırasında değişen ağırlıklar ve sabittir.
- **Aktivasyonu atlamak.** Aktivasyonsuz katmanlar üst üste konsa bile ağ doğrusal kalır ve eğri bir sınır öğrenemez.
- **Perceptron kuralını her problemde çalışır sanmak.** Veri düz bir çizgiyle ayrılamıyorsa (XOR gibi) kural hiçbir zaman sıfır hataya ulaşmaz; tur sınırı koymazsan döngü sonsuza kadar sürer.
- **Biyolojik nöronla aynı şey sanmak.** Yapay nöron bir benzetmedir; gerçek sinir hücreleri çok daha karmaşıktır.

## 5. Pekiştir

**Quiz**

1. Bir nöron çıktısını hangi adımlarla hesaplar?
2. ReLU fonksiyonu `-3` ve `5` için ne verir?
3. VE kapısında sabit neden negatif seçildi?
4. Perceptron kuralında tahmin doğruysa ağırlıklar nasıl değişir?
5. Tek bir nöron neden XOR'u öğrenemez?

**Alıştırmalar**

1. İlk penceredeki girdileri `[2.0, 1.0]` yap. `z` değerini önce kâğıtta hesapla, sonra kodla karşılaştır.
2. VE kapısı penceresinde sabiti `-0.5` yaparak VEYA kapısı kur. Sonra ağırlıkları `[-1, -1]`, sabiti `0.5` yap. Bu nöron hangi kapıyı (DEĞİL-VEYA, yani NOR) taklit ediyor?
3. Perceptron penceresindeki hedefleri VE kapısına göre değiştir (`[0, 0, 0, 1]`). Kaç turda öğreniyor?
4. Hedefleri XOR'a göre değiştir (`[0, 1, 1, 0]`). 20 turun sonunda hata sayısı sıfıra iniyor mu? Neden?
5. (İsteğe bağlı) Perceptron'da `ogrenme_hizi` değerini `1.0` yap. Tur sayısı ve öğrenilen ağırlıklar nasıl değişti?

??? success "Quiz cevapları"
    1. Girdileri ağırlıklarla çarpıp toplar, sabiti ekler ve sonucu aktivasyon fonksiyonundan geçirir.
    2. `-3` için `0`, `5` için `5`.
    3. Toplamın yalnızca iki girdi de `1` iken sıfırı geçmesi için. `-1.5`, tek bir `1` girdisinin toplamı sıfırın altında bırakmasını sağlar.
    4. Değişmez; `hedef - tahmin` farkı sıfırdır.
    5. Tek nöron girdileri düz bir çizgiyle ayırır. XOR'da `1` olan noktalar (`(0,1)` ve `(1,0)`) ile `0` olan noktalar (`(0,0)` ve `(1,1)`) çapraz durur; tek bir düz çizgi onları ayıramaz.

## Özet

Yapay nöron, girdileri ağırlıklarla çarpıp toplar, sabit terimi ekler ve sonucu bir aktivasyon fonksiyonundan geçirir. Aktivasyon, ağa doğrusal olmayan davranış kazandırır. Ağırlıkları elle seçerek VE/VEYA kapıları kurabilir ya da perceptron kuralıyla örneklerden öğrenebiliriz. Ama tek bir nöron yalnızca düz bir çizgiyle ayrılabilen problemleri çözebilir; XOR gibi problemler için birden fazla katmana ihtiyaç vardır.

## Kaynaklar

- Frank Rosenblatt (1958), *The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain*, Psychological Review
- Marvin Minsky ve Seymour Papert (1969), *Perceptrons*, MIT Press
- [Google Machine Learning Crash Course: Neural networks](https://developers.google.com/machine-learning/crash-course/neural-networks)
