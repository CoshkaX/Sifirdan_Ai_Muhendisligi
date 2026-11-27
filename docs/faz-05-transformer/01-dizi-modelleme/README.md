# Faz 5 – Ders 1: Dizi modelleme

> ⏱️ Tahmini süre: 45-60 dk · 📚 Ön koşul: 4.1 Metni sayılara dönüştürmek, 4.4 Gömme · 💻 Gereksinim: Python 3.11+, ek paket yok; NumPy örneği için NumPy kurulmalıdır

## Bu derste ne öğreneceksin?

- Sıranın neden anlam taşıdığını ve sözcük torbasının bu bilgiyi neden kaybettiğini
- Bir metni **(bağlam → sonraki token)** çiftlerine çevirmeyi
- Bağlam penceresi kavramını
- Sayarak çalışan en basit dizi modelini (bigram) yazmayı ve sınırını görmeyi
- Farklı uzunluktaki dizileri **padding** ile aynı uzunluğa getirmeyi

## 1. Problem

"Film güzel değil, sıkıcı" ile "film sıkıcı değil, güzel" aynı sözcüklerden oluşur, ama anlamları tam tersidir. 4.5'te kullandığımız **sözcük torbası** yöntemi yalnızca hangi sözcüğün kaç kez geçtiğine baktığı için bu iki cümleyi ayıramaz.

Metin, ses, müzik, hava durumu ölçümleri, bir kullanıcının tıklama geçmişi gibi pek çok veri **sıralı** veridir: elemanların sırası bilginin bir parçasıdır. Sıralı veriyle çalışan modellere **dizi modelleri** denir. Bu fazda, günümüzün dil modellerinin temelindeki dizi modelini, **transformer**'ı adım adım kuracağız.

Dil modelinin temel işi çok basit görünür: **şimdiye kadar gelen token'lara bakıp sıradaki token'ı tahmin etmek.** "Bugün hava çok ..." cümlesinin devamında `güzel`, `soğuk` gibi sözcükleri olası, `kitap` gibi sözcükleri olasılığı düşük görmek. Bu derste bu işi en basit hâliyle kuracağız; sonraki derslerde modeli güçlendireceğiz.

## 2. Kendin yaz

### 2.1 Sıra bilgisi: sözcük torbası neyi kaybeder?

İki cümleyi sözcük torbası olarak karşılaştıralım, sonra sıralı liste olarak:

```python {.python-playground}
from collections import Counter

cumle1 = "film güzel değil sıkıcı"
cumle2 = "film sıkıcı değil güzel"

print("Sözcük torbaları aynı mı?", Counter(cumle1.split()) == Counter(cumle2.split()))
print("Sıralı listeler aynı mı?", cumle1.split() == cumle2.split())
```
```text {.python-playground-expected}
Sözcük torbaları aynı mı? True
Sıralı listeler aynı mı? False
```
```text {.python-playground-help}
`from collections import Counter` | 4.5'te gördüğümüz sayaç. Bir listedeki öğelerin kaç kez geçtiğini sayar.
`Counter(cumle1.split())` | Cümleyi sözcüklere böler ve her sözcüğün sayısını tutar. Sözcüklerin sırası bu yapıda saklanmaz.
`cumle1.split() == cumle2.split()` | Listeler sırayı da karşılaştırır. Aynı öğeler farklı sıradaysa iki liste eşit olmaz.
```

Sayaçlar eşit, listeler farklı. Dizi modelleri sırayı korumak zorundadır. Kutudaki iki cümleyi başka sözcüklerle değiştirip tekrar çalıştır. Aynı sözcüklerden oluşan, ama anlamı farklı iki cümle bulabilir misin?

### 2.2 Bir metni (bağlam → sonraki) çiftlerine çevirmek

Dil modelini eğitmek için metinden örnekler üretiriz. Her örnekte model, birkaç token'dan oluşan **bağlama** bakar ve hemen sonra gelen token'ı, yani **hedefi** tahmin etmeye çalışır. Bağlamın uzunluğuna **pencere boyutu** denir. Pencereyi metnin üzerinde birer birer kaydırarak örnekleri üretiriz.

```python {.python-playground}
cumle = "bugün hava çok güzel ve deniz sakin"
tokenlar = cumle.split()
pencere = 3

for i in range(len(tokenlar) - pencere):
    baglam = tokenlar[i:i + pencere]
    hedef = tokenlar[i + pencere]
    print(baglam, "→", hedef)
```
```text {.python-playground-expected}
['bugün', 'hava', 'çok'] → güzel
['hava', 'çok', 'güzel'] → ve
['çok', 'güzel', 've'] → deniz
['güzel', 've', 'deniz'] → sakin
```
```text {.python-playground-help}
`tokenlar = cumle.split()` | Cümleyi sözcüklere ayırırız. Gerçek bir dil modelinde burada 4.1'deki gibi bir tokenizer olurdu; sözcük bölme bizim için yeterli.
`pencere = 3` | Model her seferinde 3 token'a bakacak.
`range(len(tokenlar) - pencere)` | Pencerenin hemen ardından bir hedef token kalması gerekir. Bu yüzden son `pencere` konuma pencere başlatmayız.
`tokenlar[i:i + pencere]` | `i` konumundan başlayan `pencere` kadar token; bağlam.
`tokenlar[i + pencere]` | Bağlamın hemen sonrasındaki token; hedef.
```

7 token ve 3'lük pencereyle 4 örnek çıktı. Pencereyi `2` ve `5` yapıp çıktının nasıl değiştiğine bak. Pencere büyüdükçe örnek sayısı azalır, ama her örnek daha çok bağlam taşır.

### 2.3 En basit dizi modeli: bigram

**Bigram** modeli yalnızca **bir** önceki token'a bakar. Eğitim metninde her token'dan sonra hangi token'ın kaç kez geldiğini sayar. Tahmin ederken o sayıları olasılığa çevirir.

```python {.python-playground}
metin = "kedi süt içti köpek su içti kedi mama yedi köpek mama yedi"
tokenlar = metin.split()

sayac = {}
for onceki, sonraki in zip(tokenlar, tokenlar[1:]):
    sayac.setdefault(onceki, {})
    sayac[onceki][sonraki] = sayac[onceki].get(sonraki, 0) + 1


def olasiliklar(onceki):
    secenekler = sayac[onceki]
    toplam = sum(secenekler.values())
    return {t: s / toplam for t, s in secenekler.items()}


print("mama →", olasiliklar("mama"))
print("içti →", olasiliklar("içti"))
```
```text {.python-playground-expected}
mama → {'yedi': 1.0}
içti → {'köpek': 0.5, 'kedi': 0.5}
```
```text {.python-playground-help}
`zip(tokenlar, tokenlar[1:])` | Listeyi bir kaydırılmış hâliyle eşleştirir: her token, kendinden hemen sonra gelenle çift olur.
`sayac.setdefault(onceki, {})` | `onceki` anahtarı yoksa onun için boş bir sözlük açar. Varsa dokunmaz.
`sayac[onceki].get(sonraki, 0) + 1` | O çiftin şimdiye kadarki sayısını alır (yoksa `0`) ve bir artırır.
`toplam = sum(secenekler.values())` | Bir token'dan sonra gelen bütün seçeneklerin toplam sayısı.
`s / toplam` | Sayıyı olasılığa çevirir: oran `0` ile `1` arasındadır ve bir token'ın seçeneklerinin toplamı `1` eder.
```

`mama` her zaman `yedi`'den önce geldiği için model emin: `yedi` olasılığı `1.0`. `içti` ise bir kez `köpek`, bir kez `kedi` ile devam etmiş; model ikisi arasında kararsız (`0.5` ve `0.5`).

Neden? Bigram modeli yalnızca bir önceki token'a baktığı için "süt içti" ile "su içti" arasındaki farkı göremez. Oysa bağlamı genişletirsek (`süt içti` → `köpek`, `su içti` → `kedi`) karar verilebilir. Bu, dil modellerinin temel sorunudur: **ne kadar bağlam, hangi token'lara dikkat?** Sonraki dersler tam olarak bunu çözecek.

### 2.4 Farklı uzunluktaki dizileri aynı boya getirmek

Modeller aynı anda birden fazla örnekle (**batch**) çalışır ve bunları tek bir tablo olarak ister. Cümlelerin uzunluğu farklıysa kısa olanın sonuna özel bir **padding** (`[PAD]`) token'ı ekleriz.

```python {.python-playground}
sozluk = {"[PAD]": 0, "bugün": 1, "hava": 2, "çok": 3, "güzel": 4}
cumleler = [
    ["bugün", "hava", "çok", "güzel"],
    ["hava", "güzel"],
    ["çok", "güzel", "bugün"],
]

en_uzun = max(len(c) for c in cumleler)

for cumle in cumleler:
    idler = [sozluk[t] for t in cumle]
    idler = idler + [sozluk["[PAD]"]] * (en_uzun - len(idler))
    print(idler)
```
```text {.python-playground-expected}
[1, 2, 3, 4]
[2, 4, 0, 0]
[3, 4, 1, 0]
```
```text {.python-playground-help}
`sozluk = {...}` | Her token'a bir numara. `0` numarasını padding için ayırdık.
`max(len(c) for c in cumleler)` | En uzun cümlenin uzunluğu. Bütün cümleleri bu boya getireceğiz.
`[sozluk[t] for t in cumle]` | Cümledeki her token'ı numarasına çevirir.
`[sozluk["[PAD]"]] * (en_uzun - len(idler))` | Eksik kalan konum sayısı kadar `0` ekler. Bir listeyi `n` ile çarpmak onu `n` kez tekrarlar.
```

Üç cümle artık aynı uzunlukta, yani tek bir `3 × 4` tablo. Padding konumlarının gerçek bir token olmadığını modele ileride söyleyeceğiz (5.2'deki maskeleme).

### Şimdi sen yaz: pencereyle çift üret

**Görev:** Bir cümlenin token'ları ve pencere boyutu (`2`) kodda hazır. Pencereyi kaydırarak her konumda bir bağlam ve onu izleyen hedef token'ı bulacaksın. Ekranda çift sayısı ve her çiftin `bağlam → hedef` hâli görünmeli.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
tokenlar = ["ben", "yarın", "okula", "gideceğim", "çünkü", "sınav", "var"]
pencere = 2

ciftler = []
# TODO: Hedef için de yer kalmalı; pencere kadar konumu hariç tut.
for i in range(len(tokenlar) - ___):
    # TODO: Bağlam: i. konumdan başlayan, pencere kadar token.
    baglam = tokenlar[i:i + ___]
    # TODO: Hedef: bağlamdan hemen sonra gelen token.
    hedef = tokenlar[___]
    ciftler.append((baglam, hedef))

print("Çift sayısı:", len(ciftler))
for baglam, hedef in ciftler:
    print(baglam, "→", hedef)
```
```text {.python-playground-expected}
Çift sayısı: 5
['ben', 'yarın'] → okula
['yarın', 'okula'] → gideceğim
['okula', 'gideceğim'] → çünkü
['gideceğim', 'çünkü'] → sınav
['çünkü', 'sınav'] → var
```
```text {.python-playground-help}
`range(len(tokenlar) - ___)` | Son token'lara pencere başlatamayız, çünkü ardından hedef gelmesi gerekir. Pencere boyutunu çıkar.
`tokenlar[i:i + ___]` | Bağlam, pencere boyutu kadar token uzunluğundadır; dilimin bitişi `i + pencere` olur.
`hedef = tokenlar[___]` | Bağlam `i + pencere` konumunda biter; hedef tam o konumdaki token'dır.
```
```python {.python-playground-solution}
tokenlar = ["ben", "yarın", "okula", "gideceğim", "çünkü", "sınav", "var"]
pencere = 2

ciftler = []
# Hedef için de yer kalmalı; pencere kadar konumu hariç tut.
for i in range(len(tokenlar) - pencere):
    # Bağlam: i. konumdan başlayan, pencere kadar token.
    baglam = tokenlar[i:i + pencere]
    # Hedef: bağlamdan hemen sonra gelen token.
    hedef = tokenlar[i + pencere]
    ciftler.append((baglam, hedef))

print("Çift sayısı:", len(ciftler))
for baglam, hedef in ciftler:
    print(baglam, "→", hedef)
```

## 3. Kütüphaneyle yap

NumPy'nin `sliding_window_view` işlevi, bir diziyi kaydırarak 2.2'deki pencereleri tek satırda üretir. NumPy'yi 2.1'deki gibi kur, kodu `pencereler.py` adıyla kaydet ve `python pencereler.py` ile çalıştır:

```python
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

idler = np.array([4, 7, 2, 9, 5, 1])
pencereler = sliding_window_view(idler, 3)

baglamlar = pencereler[:, :2]
hedefler = pencereler[:, 2]

print("Bağlamlar:")
print(baglamlar)
print("Hedefler:", hedefler)
```

Beklenen çıktı:

```text
Bağlamlar:
[[4 7]
 [7 2]
 [2 9]
 [9 5]]
Hedefler: [2 9 5 1]
```

- `sliding_window_view(idler, 3)`: Uzunluğu 3 olan bütün ardışık pencereleri satır satır verir. 6 elemanlı dizide 4 pencere çıkar.
- `pencereler[:, :2]`: Her satırın ilk 2 sütunu, yani bağlam.
- `pencereler[:, 2]`: Her satırın 3. sütunu, yani hedef.

Gerçek dil modeli eğitiminde de aynı fikir kullanılır; yalnızca token'lar binlerce, pencereler yüzlerce ya da binlerce uzunluktadır.

## 4. Sık yapılan hatalar

- **Sözcük torbasını dizi sanmak.** Torba yalnızca sayıları tutar; sıra gerekiyorsa liste (dizi) kullan.
- **Pencere sınırında bir eksik ya da fazla yazmak.** `range(len(tokenlar))` yazarsan son pencerelerde hedef konumu listenin dışına taşar ve `IndexError` alırsın. Hedef için `pencere` kadar konum ayır.
- **Hedefi bağlamın içine koymak.** Hedef token'ı girdide de verirsen model cevabı görür ve hiçbir şey öğrenmeden "doğru" tahmin eder. Bağlam hedeften önce biter.
- **Eğitimde görülmeyen token için `KeyError` almak.** Sözlükte olmayan bir token'ı `sayac[onceki]` ile okursan hata verir. Gerçek projelerde bilinmeyen token'lar için özel bir `[BİLİNMEYEN]` kullanılır (4.1).
- **Padding'i gerçek token sanmak.** `[PAD]` anlam taşımaz; modelin ona dikkat etmemesi gerekir. Bunu 5.2'de maskeyle yapacağız.

## 5. Pekiştir

**Quiz**

1. Sözcük torbası neden "film güzel değil sıkıcı" ile "film sıkıcı değil güzel" cümlelerini ayıramaz?
2. 7 token'lık bir cümleden pencere boyutu 3 ile kaç (bağlam, hedef) çifti çıkar?
3. 2.3'teki bigram modeli `içti` token'ından sonra `köpek` mi `kedi` mi geleceğini neden bilemez?
4. Padding neden gerekir?
5. Hedef token bağlamın içine girerse ne olur?

**Alıştırmalar**

1. 2.2'de pencereyi `2` ve `5` yap. Kaç çift çıkıyor? Formülü bul: `n` token ve `p` pencere için çift sayısı kaçtır?
2. 2.3'teki metne `kedi su içti` cümlesini ekle. `içti →` olasılıkları nasıl değişti?
3. (İsteğe bağlı) 2.3'te sayacı bir token yerine **iki** önceki token'a göre tut (anahtar olarak `(onceki1, onceki2)` demetini kullan). `süt içti` sonrası artık tek seçenek kalıyor mu?
4. (İsteğe bağlı) 2.4'e dört token'lık dördüncü bir cümle ekle. Diğer cümlelerin boyutu nasıl değişti?

??? success "Quiz cevapları"
    1. Torba yalnızca hangi sözcüğün kaç kez geçtiğini tutar; iki cümlede de aynı sözcükler aynı sayıda geçer. Sıra bilgisi saklanmaz.
    2. 4 çift. Genel olarak `n - p` çift çıkar.
    3. Yalnızca bir önceki token'a (`içti`) bakar. Eğitim metninde `içti`'den sonra bir kez `köpek`, bir kez `kedi` geldiği için ikisine de aynı olasılığı verir. Daha önceki token'ları (`süt` ya da `su`) görmez.
    4. Model aynı anda birçok örneği tek bir tablo olarak işler; tablonun her satırı aynı uzunlukta olmalıdır. Kısa dizilere padding eklenir.
    5. Model cevabı girdide görür ve hiçbir şey öğrenmeden doğru tahmin eder. Eğitimde başarılı, gerçek kullanımda işe yaramaz bir model çıkar.

## Özet

Sıralı veride elemanların sırası anlam taşır; sözcük torbası bu bilgiyi kaybeder. Dil modeli, bağlamdaki token'lara bakıp sıradaki token'ı tahmin eder. Metni pencereyle kaydırarak (bağlam, hedef) çiftleri üretiriz. Sayarak çalışan bigram modeli yalnızca bir önceki token'a baktığı için kısa bağlamla yetinir ve ayırt edemediği durumlarda kararsız kalır. Farklı uzunluktaki diziler padding ile aynı boya getirilir. Bundan sonraki derslerde modelin bağlamdaki hangi token'lara bakacağına kendisinin karar vermesini sağlayan **attention** mekanizmasını kuracağız.

## Kaynaklar

- Dan Jurafsky ve James H. Martin, *Speech and Language Processing* (3. baskı taslağı), 3. bölüm: N-gram dil modelleri: [web.stanford.edu/~jurafsky/slp3](https://web.stanford.edu/~jurafsky/slp3/)
- [NumPy resmî belgesi: `sliding_window_view`](https://numpy.org/doc/stable/reference/generated/numpy.lib.stride_tricks.sliding_window_view.html)
- [Python resmî belgesi: `collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter)
