# Faz 6 – Ders 1: Sonraki token tahmini

> ⏱️ Tahmini süre: 50-65 dk · 📚 Ön koşul: 1.4 Olasılık, 1.6 Entropi ve çapraz entropi, 5.1 Dizi modelleme · 💻 Gereksinim: Python 3.11+, ek paket yok; PyTorch örneği isteğe bağlı

## Bu derste ne öğreneceksin?

- Bir dil modelinin aslında bir **olasılık dağılımı** olduğunu
- Bir cümlenin olasılığını **zincir kuralıyla** hesaplamayı
- Neden olasılıkları çarpmak yerine **logaritmalarını topladığımızı**
- Kayıp ile **perplexity** arasındaki bağı ve perplexity'yi yorumlamayı
- Olasılıklardan **örnekleyerek** metin üretmeyi

## 1. Problem

ChatGPT gibi büyük dil modellerinin yaptığı iş, ne kadar karmaşık görünürse görünsün, tek bir sorudan ibarettir: **"Şimdiye kadarki metne bakınca sıradaki token ne olabilir?"** Model bu soruya kesin bir cevap vermez; sözlükteki her token için bir **olasılık** verir. "Bugün hava çok" metninden sonra `güzel` için `0.3`, `soğuk` için `0.2`, `kitap` için `0.0001` gibi.

Bu fazda, Faz 5'te kurduğumuz transformer'ı gerçek metinle eğitip küçük bir Türkçe dil modeli yapacağız. Ama önce dil modelinin ne ölçtüğünü, nasıl değerlendirildiğini ve metni nasıl ürettiğini sayılarla anlamamız gerekiyor. Bu derste her şeyi en basit modelle, **karakter düzeyinde bigram** ile yapacağız (5.1'deki bigram'ın harfli hâli). Fikirler, büyük modellerde de birebir aynıdır.

## 2. Kendin yaz

### 2.1 Sonraki karakterin olasılıkları

Bir metinde her karakterden sonra hangi karakterin geldiğini sayıp olasılığa çevirelim:

```python {.python-playground}
metin = "kedi süt içti. kedi uyudu. köpek su içti. köpek koştu."

sayac = {}
for onceki, sonraki in zip(metin, metin[1:]):
    sayac.setdefault(onceki, {})
    sayac[onceki][sonraki] = sayac[onceki].get(sonraki, 0) + 1


def olasiliklar(harf):
    secenekler = sayac[harf]
    toplam = sum(secenekler.values())
    sirali = sorted(secenekler.items(), key=lambda cift: -cift[1])
    return {t: round(s / toplam, 2) for t, s in sirali}


print("'k' sonrası:", olasiliklar("k"))
print("'t' sonrası:", olasiliklar("t"))
```
```text {.python-playground-expected}
'k' sonrası: {'e': 0.29, 'ö': 0.29, ' ': 0.29, 'o': 0.14}
't' sonrası: {'i': 0.5, ' ': 0.25, 'u': 0.25}
```
```text {.python-playground-help}
`zip(metin, metin[1:])` | Her karakteri kendinden sonra gelenle eşleştirir. Boşluk ve nokta da birer karakterdir.
`sayac[onceki][sonraki] = ... + 1` | 5.1'deki bigram sayımı, bu kez harflerle.
`sorted(..., key=lambda cift: -cift[1])` | Seçenekleri sayısına göre büyükten küçüğe sıralar; eksi işareti ters sıralama içindir.
`round(s / toplam, 2)` | Sayıyı olasılığa çevirir: bir harfin seçeneklerinin olasılıkları toplamı `1` eder.
```

Model `k`'den sonra `e`, `ö` ya da boşluk bekliyor (`kedi`, `köpek` ve `köpek` sözcüğünün sonu); `o` daha az olası (`koştu`). Bu sözlük, modelin bildiği her şeydir: her bağlam için bir olasılık dağılımı. Büyük bir dil modelinin farkı, bu dağılımı tek bir harfe değil binlerce token'lık bağlama bakarak hesaplamasıdır.

### 2.2 Bir cümlenin olasılığı: zincir kuralı

Model her adımda sıradaki token'ın olasılığını verir. Bir dizinin olasılığı, bu adım olasılıklarının **çarpımıdır**:

`P(k, e, d, i) = P(e | k) × P(d | e) × P(i | d)` (ilk harfi verilmiş sayıyoruz)

Uzun metinlerde bu çarpım çok küçük sayılara iner. Bilgisayarlar belli bir sınırın altındaki sayıları `0` olarak görür. Bu yüzden olasılıkları çarpmak yerine **logaritmalarını toplarız**: `log(a × b) = log(a) + log(b)`.

```python {.python-playground}
import math

adim_olasiliklari = [0.5, 0.67, 1.0]
carpim = 1.0
log_toplam = 0.0
for p in adim_olasiliklari:
    carpim *= p
    log_toplam += math.log(p)

print("Çarpım:", round(carpim, 3))
print("Log toplamı:", round(log_toplam, 3), "→ e üzeri:", round(math.exp(log_toplam), 3))

uzun_carpim = 1.0
for _ in range(2000):
    uzun_carpim *= 0.1
print("2000 adımlık çarpım:", uzun_carpim)
print("2000 adımlık log toplamı:", round(2000 * math.log(0.1), 1))
```
```text {.python-playground-expected}
Çarpım: 0.335
Log toplamı: -1.094 → e üzeri: 0.335
2000 adımlık çarpım: 0.0
2000 adımlık log toplamı: -4605.2
```
```text {.python-playground-help}
`adim_olasiliklari = [0.5, 0.67, 1.0]` | Her adımda doğru karakterin olasılığı (örneğin `kedi` için `k→e`, `e→d`, `d→i`).
`carpim *= p` | Zincir kuralı: adım olasılıklarını çarparız.
`log_toplam += math.log(p)` | Aynı bilgiyi logaritmaların toplamı olarak tutarız. Olasılıklar `1`'den küçük olduğu için logaritmaları negatiftir.
`math.exp(log_toplam)` | Log toplamının `e` üstü, çarpımın kendisini geri verir.
`uzun_carpim *= 0.1` | `0.1`'i 2000 kez çarpmak `10⁻²⁰⁰⁰` eder; bilgisayar bunu tutamaz ve `0.0` yazar.
```

Kısa dizide çarpım ile log toplamı aynı bilgiyi taşır. Uzun dizide çarpım `0.0` oldu (sayı bilgisayarın tutabileceği en küçük değerin altına indi), log toplamı ise `-4605.2` gibi rahatça tutulabilen bir sayı. Dil modelleri bu yüzden hep **log olasılıklarla** çalışır.

### 2.3 Kayıp ve perplexity

Eğitimde kullandığımız **kayıp**, doğru token'ların log olasılıklarının ortalamasının eksisidir. Bu, 1.6'daki **çapraz entropidir**. Bir model doğru token'lara yüksek olasılık veriyorsa kayıp düşüktür.

Kayıp sayısını yorumlamak zordur. Daha sezgisel bir ölçü **perplexity**'dir (şaşkınlık): `e üzeri kayıp`. Anlamı: "Model her adımda ortalama kaç seçenek arasında kararsız kalıyor?" Her adımda 4 seçeneğe eşit olasılık veren bir modelin perplexity'si `4`'tür.

```python {.python-playground}
import math


def perplexity(dogru_olasiliklar):
    kayip = -sum(math.log(p) for p in dogru_olasiliklar) / len(dogru_olasiliklar)
    return kayip, math.exp(kayip)


modeller = {
    "4 seçenek arasında eşit": [0.25, 0.25, 0.25, 0.25],
    "iyi model": [0.9, 0.8, 0.95, 0.7],
    "kötü model": [0.1, 0.05, 0.2, 0.1],
}
for ad, olasiliklar in modeller.items():
    kayip, ppl = perplexity(olasiliklar)
    print(f"{ad:24} kayıp {kayip:.2f}  perplexity {ppl:.1f}")
```
```text {.python-playground-expected}
4 seçenek arasında eşit  kayıp 1.39  perplexity 4.0
iyi model                kayıp 0.18  perplexity 1.2
kötü model               kayıp 2.30  perplexity 10.0
```
```text {.python-playground-help}
`-sum(math.log(p) for p in ...) / len(...)` | Doğru token'ların log olasılıklarının ortalamasının eksisi: çapraz entropi kaybı.
`math.exp(kayip)` | Perplexity, kaybın `e` üstüdür.
`"4 seçenek arasında eşit": [0.25, ...]` | Her adımda doğru token'a `1/4` olasılık veren model; perplexity'si tam `4` çıkar.
`f"{ad:24}"` | Adı 24 karakter genişliğinde yazar; sütunlar hizalı görünür.
```

İyi model doğru token'lara yüksek olasılık verdiği için perplexity'si `1`'e yakın: neredeyse hiç kararsız değil. Kötü model her adımda yaklaşık 10 seçenek arasında kalmış gibi davranıyor. Rastgele tahmin yapan bir modelin perplexity'si sözlük boyutuna eşittir. Eğitimin amacı perplexity'yi bu üst sınırdan aşağı çekmektir.

### 2.4 Olasılıklardan metin üretmek

Model sıradaki token için bir dağılım verdiğinde, ondan **örnekleyerek** bir token seçeriz: olasılığı yüksek olanlar daha sık seçilir, ama düşük olanlar da arada bir seçilir. Seçilen token'ı metne ekleyip tekrar sorarız. Bu, bütün dil modellerinin metin üretme biçimidir (6.5'te ayrıntısıyla göreceğiz).

```python {.python-playground}
import random

metin = "kedi süt içti. kedi uyudu. köpek su içti. köpek koştu."
sayac = {}
for onceki, sonraki in zip(metin, metin[1:]):
    sayac.setdefault(onceki, {})
    sayac[onceki][sonraki] = sayac[onceki].get(sonraki, 0) + 1

r = random.Random(3)
uretilen = "k"
for _ in range(40):
    secenekler = sayac[uretilen[-1]]
    sonraki = r.choices(list(secenekler), weights=list(secenekler.values()))[0]
    uretilen += sonraki

print(uretilen)
```
```text {.python-playground-expected}
keköpedi. i. köpekoşti k i köpekoşti. süt
```
```text {.python-playground-help}
`r = random.Random(3)` | Sabit tohumlu üreteç; her çalıştırmada aynı metin çıkar. Tohumu değiştirince farklı metin görürsün.
`uretilen[-1]` | Şimdiye kadar üretilen metnin son karakteri; bigram yalnızca ona bakar.
`r.choices(liste, weights=...)` | Listeden ağırlıklarına göre bir öğe seçer. Sayısı yüksek karakter daha sık seçilir.
`[0]` | `choices` bir liste döndürür; ilk (ve tek) öğesini alırız.
`uretilen += sonraki` | Seçilen karakteri metne ekleyip bir sonraki adıma geçeriz.
```

Çıktı Türkçeye benziyor ama anlamsız: bigram yalnızca bir önceki harfe baktığı için heceleri doğru dizer ama sözcükleri ve cümleleri kuramaz. Daha uzun bağlama bakan bir model (Faz 5'teki transformer) çok daha iyi metin üretir. 6.4'te tam olarak bunu yapacağız.

### Şimdi sen yaz: kayıp ve perplexity

**Görev:** Bir modelin dört adımda doğru token'a verdiği olasılıklar kodda hazır. Önce ortalama kaybı (çapraz entropi), sonra perplexity'yi hesaplayacaksın. Ekranda kayıp ve perplexity görünmeli.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
import math

dogru_olasiliklar = [0.5, 0.25, 0.8, 0.1]

toplam = 0.0
for p in dogru_olasiliklar:
    # TODO: Her doğru token'ın kaybı -log(p)'dir (math.log).
    toplam += ___

# TODO: Ortalama kayıp: toplam bölü token sayısı.
kayip = ___

# TODO: Perplexity: e üzeri kayıp (math.exp).
perplexity = ___

print("Kayıp:", round(kayip, 3))
print("Perplexity:", round(perplexity, 2))
```
```text {.python-playground-expected}
Kayıp: 1.151
Perplexity: 3.16
```
```text {.python-playground-help}
`toplam += ___` | Doğru token'ın olasılığı yükseldikçe kayıp küçülmeli. `math.log(p)` negatiftir; başına eksi koy.
`kayip = ___` | Toplamı olasılık sayısına (`len(dogru_olasiliklar)`) böl.
`perplexity = ___` | Perplexity, kaybın `e` üstüdür: `math.exp(kayip)`.
```
```python {.python-playground-solution}
import math

dogru_olasiliklar = [0.5, 0.25, 0.8, 0.1]

toplam = 0.0
for p in dogru_olasiliklar:
    # Her doğru token'ın kaybı -log(p)'dir (math.log).
    toplam += -math.log(p)

# Ortalama kayıp: toplam bölü token sayısı.
kayip = toplam / len(dogru_olasiliklar)

# Perplexity: e üzeri kayıp (math.exp).
perplexity = math.exp(kayip)

print("Kayıp:", round(kayip, 3))
print("Perplexity:", round(perplexity, 2))
```

## 3. Kütüphaneyle yap

PyTorch'ta model, her token için **logit** (ham puan) üretir. `F.cross_entropy` logit'leri softmax ile olasılığa çevirip doğru token'ın log olasılığının eksisini, yani 2.3'teki kaybı hesaplar. Perplexity, bu kaybın `e` üstüdür. PyTorch'u 3.6'daki gibi kur, kodu `kayip_torch.py` adıyla kaydet ve `python kayip_torch.py` ile çalıştır:

```python
import math

import torch
import torch.nn.functional as F

logitler = torch.tensor([[2.0, 1.0, 0.1], [0.5, 2.5, 0.0]])
dogru = torch.tensor([0, 1])

olasiliklar = F.softmax(logitler, dim=-1)
elle = -torch.log(olasiliklar[torch.arange(2), dogru]).mean()
kayip = F.cross_entropy(logitler, dogru)

print("Doğru token olasılıkları:", [round(p, 3) for p in olasiliklar[torch.arange(2), dogru].tolist()])
print("Elle kayıp:", round(elle.item(), 4))
print("cross_entropy:", round(kayip.item(), 4))
print("Perplexity:", round(math.exp(kayip.item()), 3))
```

Beklenen çıktı:

```text
Doğru token olasılıkları: [0.659, 0.821]
Elle kayıp: 0.3069
cross_entropy: 0.3069
Perplexity: 1.359
```

- `logitler`: İki adım, her adımda 3 token için ham puan.
- `dogru`: Her adımdaki doğru token'ın numarası.
- `olasiliklar[torch.arange(2), dogru]`: Her satırdan doğru token'ın olasılığını seçer.
- Elle hesap ile `cross_entropy` aynı sonucu verir; kütüphane bunu sayısal olarak daha güvenli biçimde yapar (1.6).

## 4. Sık yapılan hatalar

- **Olasılıkları çarpmak.** Uzun dizilerde sonuç `0.0`'a iner. Log olasılıkları topla.
- **Kaybı perplexity ile karıştırmak.** Kayıp log ölçeğindedir; perplexity onun `e` üstüdür. "Kayıp 2" ile "perplexity 2" çok farklı şeylerdir (`e² ≈ 7.4`).
- **Doğal logaritma ile `log₂`'yi karıştırmak.** PyTorch doğal logaritma (nat) kullanır; perplexity'yi de `math.exp` ile hesapla. `log₂` kullanıyorsan `2 ** kayıp` almalısın (1.6).
- **Sıfır olasılık vermek.** Doğru token'a `0` olasılık veren bir model için `log(0)` tanımsızdır ve kayıp sonsuz olur. Softmax hiçbir token'a tam `0` vermez; sayarak çalışan modellerde ise görülmemiş durumlara küçük bir olasılık ayrılır (yumuşatma).
- **Farklı tokenizer'lı modellerin perplexity'sini doğrudan karşılaştırmak.** Perplexity token başına ölçülür; token'lar farklıysa (karakter mi, sözcük parçası mı?) sayılar karşılaştırılamaz. Bunu 6.3'te göreceğiz.
- **Örneklemeyi her seferinde en olası token'ı seçmek sanmak.** En olası token'ı seçmek ayrı bir yöntemdir (açgözlü). Örnekleme rastgeledir; bu yüzden aynı modelden farklı metinler çıkar.

## 5. Pekiştir

**Quiz**

1. Bir dil modeli bir bağlam verildiğinde ne üretir?
2. Bir cümlenin olasılığı adım olasılıklarından nasıl bulunur?
3. Olasılıkları çarpmak yerine neden logaritmalarını toplarız?
4. Perplexity'si `4` olan bir model ne anlama gelir?
5. 30 harflik bir sözlükte rastgele tahmin yapan bir modelin perplexity'si yaklaşık kaçtır?

**Alıştırmalar**

1. 2.1'de `olasiliklar("i")` ve `olasiliklar(" ")` (boşluk) sonuçlarına bak. Boşluktan sonra hangi harfler geliyor? Neden?
2. 2.3'teki sözlüğe kendi modelini ekle: `[0.5, 0.5, 0.5, 0.5]`. Perplexity kaç çıktı?
3. 2.4'te `random.Random(3)` tohumunu `5` ve `7` yap. Üretilen metinler nasıl değişti?
4. 2.4'teki metne birkaç cümle daha ekle (`kedi mama yedi.` gibi). Üretim nasıl değişti?
5. (İsteğe bağlı) 2.1'deki modeli iki karakterlik bağlamla (`metin[i:i+2]` → `metin[i+2]`) kur. 2.4'teki üretim daha anlamlı oluyor mu?

??? success "Quiz cevapları"
    1. Sözlükteki her token için sıradaki token olma olasılığını, yani bir olasılık dağılımı.
    2. Her adımda doğru token'ın olasılıkları çarpılır (zincir kuralı).
    3. Uzun dizilerde çarpım bilgisayarın tutabileceğinden küçük bir sayıya iner ve `0` olur; logaritma toplamı ise rahatça tutulur. Ayrıca toplama, çarpmadan sayısal olarak daha kararlıdır.
    4. Model her adımda, ortalamada 4 seçenek arasında eşit kararsız kalıyormuş gibi davranıyor.
    5. Yaklaşık `30`; rastgele tahminin perplexity'si sözlük boyutuna eşittir.

## Özet

Dil modeli, bir bağlama bakıp sözlükteki her token için sıradaki token olma olasılığını verir. Bir dizinin olasılığı adım olasılıklarının çarpımıdır; sayısal güvenlik için log olasılıkları toplarız. Eğitimdeki kayıp, doğru token'ların ortalama negatif log olasılığıdır (çapraz entropi); perplexity onun `e` üstüdür ve modelin her adımda ortalama kaç seçenek arasında kararsız kaldığını anlatır. Metin, modelin dağılımından örnekleyerek ve seçilen token'ı bağlama ekleyerek adım adım üretilir. Sıradaki derste token'ların kendisine, yani metni parçalara bölen **BPE tokenizer'a** geçeceğiz.

## Kaynaklar

- Dan Jurafsky ve James H. Martin, *Speech and Language Processing* (3. baskı taslağı), 3. bölüm: N-gram dil modelleri ve perplexity: [web.stanford.edu/~jurafsky/slp3](https://web.stanford.edu/~jurafsky/slp3/)
- Claude E. Shannon (1948), *A Mathematical Theory of Communication* (harf düzeyinde metin üretme örnekleri)
- [PyTorch resmî belgesi: `F.cross_entropy`](https://pytorch.org/docs/stable/generated/torch.nn.functional.cross_entropy.html)
