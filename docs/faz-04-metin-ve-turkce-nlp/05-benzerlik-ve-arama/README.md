# Faz 4 – Ders 5: Benzerlik ve arama

> ⏱️ Tahmini süre: 55-70 dk · 📚 Ön koşul: 4.3 Metin temizleme, 4.4 Gömme · 💻 Gereksinim: Python 3.11+, ek paket yok; scikit-learn örneği için scikit-learn kurulmalıdır

## Bu derste ne öğreneceksin?

- Kosinüs benzerliğinin noktasal çarpımdan neden daha adil olduğunu
- Bir metni **sözcük torbası** vektörüne çevirmeyi
- Sorguya en benzer belgeleri sıralayan küçük bir arama motoru yazmayı
- Türkçe eklerin aramayı neden bozduğunu ve basit bir kök yaklaşımıyla düzeltmeyi
- Her yerde geçen sözcüklerin etkisini **TF-IDF** ile azaltmayı

## 1. Problem

Elinde birkaç yüz belge olduğunu ve kullanıcının "yağmurda sahil" diye arama yaptığını düşün. Hangi belgeleri, hangi sırayla göstermelisin?

Bir arama motoru üç iş yapar:

1. Her belgeyi bir **vektöre** çevirir.
2. Sorguyu da aynı yöntemle bir vektöre çevirir.
3. Sorgu vektörüne en **benzer** belge vektörlerini bulup sıralar.

4.4 dersinde sözcükleri vektörle temsil ettik ve benzerliklerini ölçtük. Şimdi aynı fikri bütün cümlelere ve belgelere uygulayacağız. Türkçede bunun özel bir zorluğu var: "yağmur", "yağmurda", "yağmurlu" bilgisayar için üç ayrı sözcüktür. Bu derste bunu da çözeceğiz.

## 2. Kendin yaz

### 2.1 Kosinüs benzerliği: yöne bak, uzunluğa değil

4.4 dersinde kosinüs benzerliğini tanımlamıştık:

`kosinüs benzerliği = (a · b) / (|a| × |b|)`

Neden noktasal çarpım yetmiyor? Aynı konuyu anlatan kısa ve uzun iki belge düşün. Uzun belgede her sözcük daha çok geçer, vektörünün sayıları daha büyüktür ve noktasal çarpım da büyür. Ama uzun olması, sorguya daha uygun olduğu anlamına gelmez. Kosinüs, vektörleri uzunluklarına bölerek yalnızca **yönlerini** karşılaştırır.

```python {.python-playground}
import math


def nokta_carpim(a, b):
    return sum(x * y for x, y in zip(a, b))


def kosinus(a, b):
    uzunluk_a = math.sqrt(nokta_carpim(a, a))
    uzunluk_b = math.sqrt(nokta_carpim(b, b))
    return nokta_carpim(a, b) / (uzunluk_a * uzunluk_b)


sorgu = [1, 1, 0]
kisa_belge = [1, 1, 0]
uzun_belge = [3, 3, 0]
ilgisiz_belge = [0, 0, 5]

for ad, belge in [("kısa", kisa_belge), ("uzun", uzun_belge), ("ilgisiz", ilgisiz_belge)]:
    print(f"{ad}: nokta={nokta_carpim(sorgu, belge)}, kosinüs={kosinus(sorgu, belge):.2f}")
```
```text {.python-playground-expected}
kısa: nokta=2, kosinüs=1.00
uzun: nokta=6, kosinüs=1.00
ilgisiz: nokta=0, kosinüs=0.00
```
```text {.python-playground-help}
`def kosinus(a, b):` | Noktasal çarpımı, iki vektörün uzunluklarının çarpımına böleriz.
`math.sqrt(nokta_carpim(a, a))` | Bir vektörün kendisiyle noktasal çarpımı, sayılarının karelerinin toplamıdır; karekökü vektörün uzunluğunu verir.
`sorgu = [1, 1, 0]` | Örneğin "yağmur" ve "sahil" sözcükleri birer kez geçiyor, üçüncü sözcük geçmiyor.
`uzun_belge = [3, 3, 0]` | Aynı iki sözcük üçer kez geçiyor; konu aynı, yalnızca belge daha uzun.
`ilgisiz_belge = [0, 0, 5]` | Sorgudaki sözcüklerin hiçbiri yok.
`f"...kosinüs={kosinus(sorgu, belge):.2f}"` | Noktasal çarpım uzun belgeyi üç kat ödüllendirirken kosinüs ikisine de `1.00` verir.
```

Kısa ve uzun belge aynı yönü gösterdiği için kosinüs benzerlikleri aynı: `1.00`. Ortak sözcük yoksa benzerlik `0`. Bu ders boyunca sayılar negatif olmayacağı için kosinüs `0` ile `1` arasında kalacak.

### 2.2 Sözcük torbası ile ilk arama motoru

Bir metni vektöre çevirmenin en basit yolu **sözcük torbası** (bag of words) yöntemidir: Sözcüklerin sırasını unutur, yalnızca hangi sözcüğün kaç kez geçtiğini sayarız. Python'ın `Counter` sınıfı bu sayımı yapar ve bir sözlük gibi davranır: `{"kitap": 1, "okumak": 1}`.

```python {.python-playground}
import math
from collections import Counter

belgeler = [
    "Kitap okumak insanı geliştirir.",
    "Kitapları okudukça kelime dağarcığım genişledi.",
    "Bu hafta sonu sahilde kitap okuyacağım.",
    "Futbol maçı yağmur yüzünden ertelendi.",
    "Yağmurlu havada sahilde yürümek güzel.",
    "Akşam yemeğinde balık ve salata yedik.",
]


def vektorlestir(metin):
    return Counter(metin.lower().replace(".", "").split())


def kosinus(a, b):
    nokta = sum(a[t] * b[t] for t in a if t in b)
    uzunluk_a = math.sqrt(sum(v * v for v in a.values()))
    uzunluk_b = math.sqrt(sum(v * v for v in b.values()))
    return nokta / (uzunluk_a * uzunluk_b)


def ara(sorgu):
    sorgu_vektoru = vektorlestir(sorgu)
    skorlar = [(kosinus(sorgu_vektoru, vektorlestir(b)), b) for b in belgeler]
    skorlar.sort(reverse=True)
    return [(round(s, 2), b) for s, b in skorlar if s > 0]


print("kitap okumak   →", ara("kitap okumak"))
print("yağmurda sahil →", ara("yağmurda sahil"))
```
```text {.python-playground-expected}
kitap okumak   → [(0.71, 'Kitap okumak insanı geliştirir.'), (0.29, 'Bu hafta sonu sahilde kitap okuyacağım.')]
yağmurda sahil → []
```
```text {.python-playground-help}
`from collections import Counter` | `Counter`, bir listedeki öğelerin kaç kez geçtiğini sayan hazır bir sözlük türüdür.
`metin.lower().replace(".", "").split()` | Küçük harfe çevirir, noktayı siler ve boşluklardan böler. (Türkçe `I/İ` sorununu 2.3'te düzelteceğiz.)
`Counter(...)` | Sözcük listesini `{sözcük: sayı}` biçimine getirir. Bu, belgenin vektörüdür; geçmeyen sözcükler için sayı `0` kabul edilir.
`sum(a[t] * b[t] for t in a if t in b)` | Noktasal çarpım; yalnızca iki metinde de geçen sözcükler katkı verir.
`skorlar.sort(reverse=True)` | `(skor, belge)` çiftlerini büyükten küçüğe sıralar. Çiftler önce ilk öğelerine, yani skora göre karşılaştırılır.
`if s > 0` | Hiç ortak sözcüğü olmayan belgeleri sonuçlara koymayız.
```

"kitap okumak" araması iyi çalışıyor. Ama "yağmurda sahil" hiçbir şey bulamadı! Oysa "Yağmurlu havada sahilde yürümek güzel." tam aranan şey. Sorun: `yağmurda`, `yağmurlu` ve `yağmur` program için üç ayrı sözcük; `sahil` ile `sahilde` de öyle. Türkçede bir sözcük onlarca ekli biçimde geçebildiği için tam eşleşme çok sık kaçırır.

### 2.3 Türkçe için düzeltme: normalleştir ve kökü yaklaşık al

İki adım ekliyoruz:

1. **Normalleştirme** (4.3 dersi): Türkçe küçük harf, Unicode NFC ve noktalamayı boşluğa çevirme.
2. **Kök yaklaşımı:** Her sözcüğün yalnızca **ilk 5 harfini** almak. `yağmurda → yağmu`, `yağmurlu → yağmu`, `sahilde → sahil`.

İkinci adım kaba görünür, ama Türkçe bilgi erişimi üzerine yapılan araştırmalarda (Can ve ark., 2008) bu basit kesmenin, gerçek bir kök bulucuya yakın sonuç verdiği gösterilmiştir. Türkçede ekler hep sözcüğün sonuna geldiği için baştaki harfler genellikle kökü taşır.

```python {.python-playground}
import math
import unicodedata
from collections import Counter

belgeler = [
    "Kitap okumak insanı geliştirir.",
    "Kitapları okudukça kelime dağarcığım genişledi.",
    "Bu hafta sonu sahilde kitap okuyacağım.",
    "Futbol maçı yağmur yüzünden ertelendi.",
    "Yağmurlu havada sahilde yürümek güzel.",
    "Akşam yemeğinde balık ve salata yedik.",
]


def normallestir(metin):
    metin = unicodedata.normalize("NFC", metin)
    metin = metin.replace("İ", "i").replace("I", "ı").lower()
    metin = "".join(h if h.isalnum() else " " for h in metin)
    return metin.split()


def vektorlestir(metin):
    return Counter(sozcuk[:5] for sozcuk in normallestir(metin))


def kosinus(a, b):
    nokta = sum(a[t] * b[t] for t in a if t in b)
    uzunluk_a = math.sqrt(sum(v * v for v in a.values()))
    uzunluk_b = math.sqrt(sum(v * v for v in b.values()))
    return nokta / (uzunluk_a * uzunluk_b)


def ara(sorgu, k=3):
    sorgu_vektoru = vektorlestir(sorgu)
    skorlar = [(kosinus(sorgu_vektoru, vektorlestir(b)), b) for b in belgeler]
    skorlar.sort(reverse=True)
    return [(round(s, 2), b) for s, b in skorlar[:k] if s > 0]


print("Terimler:", vektorlestir("Yağmurlu havada sahilde yürümek güzel."))
for skor, belge in ara("yağmurda sahil"):
    print(skor, belge)
```
```text {.python-playground-expected}
Terimler: Counter({'yağmu': 1, 'havad': 1, 'sahil': 1, 'yürüm': 1, 'güzel': 1})
0.63 Yağmurlu havada sahilde yürümek güzel.
0.32 Futbol maçı yağmur yüzünden ertelendi.
0.29 Bu hafta sonu sahilde kitap okuyacağım.
```
```text {.python-playground-help}
`def normallestir(metin):` | 4.3 dersindeki adımlar: NFC, Türkçe `İ/I` dönüşümü, küçük harf.
`"".join(h if h.isalnum() else " " for h in metin)` | Harf ve rakam olmayan her karakteri (nokta, virgül, kesme işareti) boşluğa çevirir. `isalnum` Türkçe harfleri de harf sayar.
`Counter(sozcuk[:5] for sozcuk in ...)` | Her sözcüğün ilk 5 harfini alırız. 5 harften kısa sözcükler (`ve`, `bu`) olduğu gibi kalır.
`def ara(sorgu, k=3):` | En iyi `k` sonucu döndürür; `k` verilmezse 3 kabul edilir.
`skorlar[:k]` | Sıralanmış listenin ilk `k` öğesini alır.
`print("Terimler:", ...)` | Bir belgenin vektörünü görmek, aramanın neden eşleştiğini anlamanın en hızlı yoludur.
```

Artık en ilgili belge en üstte. İkinci ve üçüncü sıradakiler de mantıklı: Birinde yağmur, diğerinde sahil geçiyor.

Bu yöntemin sınırları da var. `okumak → okuma`, `okudukça → okudu`, `okuyacağım → okuya` farklı terimler olur; kök `oku-` yalnızca üç harf olduğu için ilk 5 harf ekin bir kısmını da içerir. Tersine, uzun ve farklı iki sözcük ilk 5 harfi ortak olduğu için yanlışlıkla eşleşebilir (`kalem` ve `kalemlik` doğru eşleşir, ama `karpuz` ile `karpuzcu`nun yanında `kardeş` ile `kardelen` de `karde` olarak eşleşir). Daha iyi sonuç için 4.2 dersindeki gibi gerçek bir biçimbilim çözümleyicisi kullanılabilir.

### 2.4 Her yerde geçen sözcükler: TF-IDF

Bazı sözcükler neredeyse her belgede geçer: `ve`, `bir`, `bu`. Sorguda bunlar varsa her belgeye biraz puan kazandırırlar ama ayırt edici değildirler. Buna karşılık `balık` gibi az belgede geçen bir sözcük çok bilgi taşır.

**TF-IDF** bu sezgiyi sayıya döker:

- **TF** (terim sıklığı): Sözcük bu belgede kaç kez geçiyor?
- **IDF** (ters belge sıklığı): `log(toplam belge sayısı / sözcüğü içeren belge sayısı)`. Her belgede geçen sözcüğün IDF'i `log(1) = 0` olur; nadir sözcüğünki büyüktür.

Vektördeki her sayı `TF × IDF` olur.

```python {.python-playground}
import math

belgeler = [
    ["bu", "film", "çok", "güzel"],
    ["bu", "kitap", "çok", "sıkıcı"],
    ["bu", "dizi", "güzel"],
    ["balık", "çok", "taze"],
]

tum_terimler = sorted({t for b in belgeler for t in b})
for terim in tum_terimler:
    iceren = sum(1 for b in belgeler if terim in b)
    idf = math.log(len(belgeler) / iceren)
    print(f"{terim:7} {iceren} belgede, IDF = {idf:.2f}")
```
```text {.python-playground-expected}
balık   1 belgede, IDF = 1.39
bu      3 belgede, IDF = 0.29
dizi    1 belgede, IDF = 1.39
film    1 belgede, IDF = 1.39
güzel   2 belgede, IDF = 0.69
kitap   1 belgede, IDF = 1.39
sıkıcı  1 belgede, IDF = 1.39
taze    1 belgede, IDF = 1.39
çok     3 belgede, IDF = 0.29
```
```text {.python-playground-help}
`belgeler = [[...], ...]` | Normalleştirilmiş ve sözcüklere bölünmüş dört kısa belge.
`sorted({t for b in belgeler for t in b})` | Bütün belgelerdeki farklı terimleri toplayıp sıralarız. (Python, `ç` harfini `z`'den sonra sıralar.)
`sum(1 for b in belgeler if terim in b)` | Terimi içeren belge sayısını sayarız; bir belgede kaç kez geçtiği önemli değildir.
`math.log(len(belgeler) / iceren)` | IDF formülü. `math.log` doğal logaritmadır.
`f"{terim:7}"` | Terimi 7 karakter genişliğinde yazar; sütunlar hizalı görünür.
```

`bu` ve `çok` dört belgenin üçünde geçtiği için düşük ağırlık alıyor; `balık` ve `sıkıcı` gibi tek belgede geçenler yüksek. TF-IDF uzun yıllar arama motorlarının temel yöntemi oldu ve hâlâ güçlü bir başlangıç noktasıdır.

### 2.5 Ders kodu

[`kod/turkce_arama.py`](kod/turkce_arama.py) dosyası 2.3'teki arama motorunun düzenli hâlini içerir; kök uzunluğunu bir parametreyle değiştirebilir veya tamamen kapatabilirsin. Testler, kök yaklaşımının ekli biçimleri eşleştirdiğini ve onsuz aramanın "yağmurda sahil" sorgusunu kaçırdığını denetler.

```bash
cd docs/faz-04-metin-ve-turkce-nlp/05-benzerlik-ve-arama
python kod/turkce_arama.py
python -m unittest discover -s test -v
```

## 3. Kütüphaneyle yap

Scikit-learn'deki `TfidfVectorizer` belgeleri TF-IDF vektörlerine, `cosine_similarity` de benzerlik tablosuna çevirir. Kendi Türkçe adımlarımızı `tokenizer` parametresiyle verebiliriz. scikit-learn'ü 2.4 dersindeki gibi kur, kodu `tfidf_arama.py` adıyla kaydedip `python tfidf_arama.py` ile çalıştır:

```python
import unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

belgeler = [
    "Kitap okumak insanı geliştirir.",
    "Kitapları okudukça kelime dağarcığım genişledi.",
    "Bu hafta sonu sahilde kitap okuyacağım.",
    "Futbol maçı yağmur yüzünden ertelendi.",
    "Yağmurlu havada sahilde yürümek güzel.",
    "Akşam yemeğinde balık ve salata yedik.",
]


def turkce_terimler(metin):
    metin = unicodedata.normalize("NFC", metin)
    metin = metin.replace("İ", "i").replace("I", "ı").lower()
    metin = "".join(h if h.isalnum() else " " for h in metin)
    return [sozcuk[:5] for sozcuk in metin.split()]


vektorlestirici = TfidfVectorizer(tokenizer=turkce_terimler, lowercase=False, token_pattern=None)
belge_matrisi = vektorlestirici.fit_transform(belgeler)

sorgu = vektorlestirici.transform(["yağmurda sahil"])
skorlar = cosine_similarity(sorgu, belge_matrisi)[0]

for sira in skorlar.argsort()[::-1][:3]:
    print(f"{skorlar[sira]:.2f}  {belgeler[sira]}")
```

Beklenen çıktı:

```text
0.56  Yağmurlu havada sahilde yürümek güzel.
0.27  Futbol maçı yağmur yüzünden ertelendi.
0.26  Bu hafta sonu sahilde kitap okuyacağım.
```

- `tokenizer=turkce_terimler`: Metni bölme işini bizim fonksiyonumuza bırakır. `lowercase=False` ve `token_pattern=None`, scikit-learn'ün kendi (Türkçeye uygun olmayan) küçük harf ve bölme kurallarını kapatır.
- `fit_transform(belgeler)`: Sözlüğü ve IDF değerlerini belgelerden öğrenir, sonra belgeleri vektöre çevirir.
- `transform([...])`: Sorguyu **aynı** sözlük ve IDF değerleriyle vektöre çevirir. Sorgu için yeniden `fit` yapılmaz.
- `argsort()[::-1][:3]`: Skorları küçükten büyüğe sıralayan konumları verir; ters çevirip ilk üçünü alırız.

Sıralama 2.3'tekiyle aynı; skorlar ise IDF ağırlıkları yüzünden biraz farklı. scikit-learn IDF formülüne küçük bir düzeltme ekler ve vektörleri uzunluğu `1` olacak şekilde ölçekler; fikir aynıdır.

!!! note "Sözcük eşleşmesinden anlam eşleşmesine"
    Bu dersteki yöntemler yalnızca **ortak terimleri** eşleştirir. "otomobil" arayan biri "araba" geçen belgeyi bulamaz. Bunu çözmek için belgeleri 4.4'teki gibi **gömme** vektörleriyle temsil ederiz; o zaman eş anlamlı sözcükler de yakın vektörlere düşer. Buna **anlamsal arama** denir ve Faz 8'de RAG sistemlerinin temelini oluşturacak.

## 4. Sık yapılan hatalar

- **Noktasal çarpımla uzun belgeleri kayırmak.** Uzunluktan bağımsız karşılaştırma için kosinüs kullan.
- **Sorguyu ve belgeleri farklı adımlarla işlemek.** Belgelere kök yaklaşımı uygulayıp sorguya uygulamazsan `yağmurda` ile `yağmu` hiç eşleşmez. İkisi de aynı fonksiyondan geçmelidir.
- **TF-IDF'te sorgu için yeniden `fit` yapmak.** IDF değerleri belge koleksiyonundan öğrenilir; sorguya yalnızca `transform` uygulanır.
- **İngilizce için tasarlanmış varsayılanlara güvenmek.** Kütüphanelerin hazır küçük harf ve bölme kuralları Türkçe `I/İ` ve ekleri bilmez; Türkçe adımları kendin ver.
- **Kök kesme uzunluğunu her duruma uygun sanmak.** 5 harf iyi bir başlangıçtır ama kısa köklü (`oku-`, `ye-`) sözcüklerde yetersiz kalır, bazı farklı sözcükleri de birleştirir. Kendi verinde dene ve ölç.
- **Sıfır skorlu belgeleri sonuç olarak göstermek.** Ortak hiçbir terimi olmayan belge, kullanıcıya "ilgili" diye sunulmamalıdır.

## 5. Pekiştir

**Quiz**

1. Kosinüs benzerliği noktasal çarpımdan neden daha adil bir karşılaştırma yapar?
2. Sözcük torbası yöntemi metnin hangi bilgisini kaybeder?
3. 2.2'deki arama "yağmurda sahil" sorgusunda neden hiçbir şey bulamadı?
4. İlk 5 harfi almak Türkçede neden işe yarar? Hangi durumlarda yetersiz kalır?
5. Her belgede geçen bir sözcüğün IDF değeri neden `0` olur?

**Alıştırmalar**

1. 2.1'de `sorgu` vektörünü `[1, 0, 0]` yap. Üç belgenin kosinüs benzerliği nasıl değişti?
2. 2.3'teki arama penceresinde `sozcuk[:5]` yerine `sozcuk[:4]` ve `sozcuk[:3]` dene. "kitaplar okumak" sorgusunun sonuçları nasıl değişiyor? Hangi uzunluk sana en mantıklı geldi?
3. 2.3'teki belgelere kendi yazdığın üç cümle ekle ve onları bulacak sorgular dene.
4. 2.4'teki belgelere `["bu", "çok", "güzel"]` ekle. `güzel` sözcüğünün IDF değeri nasıl değişti?
5. (İsteğe bağlı) `kod/turkce_arama.py` dosyasına "durak sözcükleri" listesi ekle (`ve`, `bu`, `bir`, `çok` gibi) ve bunları vektörden çıkar. Testleri güncelle.

??? success "Quiz cevapları"
    1. Vektörleri uzunluklarına böldüğü için yalnızca yönlerini karşılaştırır; uzun belgeler sırf uzun oldukları için yüksek puan almaz.
    2. Sözcüklerin sırasını. Örneğin "film güzel değil, sıkıcı" ile "film sıkıcı değil, güzel" aynı sözcüklerden oluştuğu için aynı vektöre sahip olur, ama anlamları tam tersidir.
    3. Sorgudaki `yağmurda` ve `sahil` sözcükleri belgelerde tam olarak bu biçimde geçmiyor; belgelerde `yağmurlu`, `yağmur`, `sahilde` var. Tam eşleşme ekli biçimleri farklı sayar.
    4. Türkçede ekler sözcüğün sonuna geldiği için baştaki harfler genellikle kökü taşır. Kök 5 harften kısaysa (`oku-`) ekin bir kısmı da alınır; farklı sözcükler ilk 5 harfi paylaşıyorsa yanlışlıkla eşleşir.
    5. `log(toplam belge / içeren belge) = log(1) = 0`; her belgede geçen bir sözcük belgeleri birbirinden ayırmaya yardım etmez.

## Özet

Bir arama motoru belgeleri ve sorguyu aynı yöntemle vektöre çevirir ve sorguya en benzer belgeleri sıralar. Kosinüs benzerliği, belge uzunluğundan bağımsız olarak vektörlerin yönünü karşılaştırır. Sözcük torbası yöntemi Türkçede ekler yüzünden pek çok eşleşmeyi kaçırır; normalleştirme ve sözcüklerin ilk birkaç harfini almak gibi basit bir kök yaklaşımı bu sorunu büyük ölçüde azaltır. TF-IDF, her yerde geçen sözcüklerin ağırlığını düşürüp nadir ve ayırt edici sözcükleri öne çıkarır.

## Kaynaklar

- Fazlı Can ve ark. (2008), *Information retrieval on Turkish texts*, Journal of the American Society for Information Science and Technology
- Christopher D. Manning, Prabhakar Raghavan, Hinrich Schütze (2008), *Introduction to Information Retrieval*, 6. bölüm: [nlp.stanford.edu/IR-book](https://nlp.stanford.edu/IR-book/)
- [scikit-learn resmî belgesi: `TfidfVectorizer`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [Python resmî belgesi: `collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter)
