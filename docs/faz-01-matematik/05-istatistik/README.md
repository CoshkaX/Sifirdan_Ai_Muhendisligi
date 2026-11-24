# Faz 1 – Ders 5: İstatistik: ortalama, varyans ve korelasyon

> ⏱️ Tahmini süre: 55-70 dk · 📚 Ön koşul: 0.2 Python hızlı tekrar, 1.4 Olasılık ve dağılımlar · 💻 Gereksinim: Python 3.11+, ek paket yok

## Bu derste ne öğreneceksin?

- Bir veri grubunun ortalamasını hesaplamayı
- Değerlerin ortalamadan ne kadar yayıldığını varyansla ölçmeyi
- İki sayısal değişkenin birlikte nasıl değiştiğini korelasyonla incelemeyi
- İstatistiksel ilişkiyi neden-sonuç ilişkisiyle karıştırmamayı

## 1. Problem

Bir sınıftaki öğrencilerin sınav notlarını düşün. Yalnızca ortalamayı bilmek, notların birbirine yakın mı yoksa çok farklı mı olduğunu söylemez. İki dersin notları birlikte yükselip düşüyor mu diye bakmak da ayrı bir sorudur.

İstatistik, bir veri grubunu düzenleyip özetlememize ve verideki ilişkileri incelememize yardım eder. Bu derste üç temel ölçüyü kullanacağız:

- **Ortalama:** Değerlerin toplamını değer sayısına bölerek bulduğumuz merkez ölçüsü.
- **Varyans:** Değerlerin ortalamadan ne kadar yayıldığını gösteren ölçü.
- **Korelasyon:** İki sayısal değişkenin birlikte değişme yönünü ve bu ilişkinin ne kadar doğrusal olduğunu gösteren ölçü.

Bu ölçüler veriyi özetler; tek başlarına bir neden-sonuç açıklaması vermez.

## 2. Kendin yaz

### 2.1 Ortalama: değerlerin merkezini bul

Dört sınav notumuz olsun: `60`, `70`, `80` ve `90`. Ortalama için önce notları toplar, sonra kaç not olduğunu sayıp toplama böleriz.

```python {.python-playground}
puanlar = [60, 70, 80, 90]
toplam = sum(puanlar)
ogrenci_sayisi = len(puanlar)
ortalama = toplam / ogrenci_sayisi

print("Toplam puan:", toplam)
print("Öğrenci sayısı:", ogrenci_sayisi)
print("Ortalama:", ortalama)
```
```text {.python-playground-expected}
Toplam puan: 300
Öğrenci sayısı: 4
Ortalama: 75.0
```
```text {.python-playground-help}
`puanlar = [60, 70, 80, 90]` | Dört öğrencinin notunu bir listede saklarız. Her sayı bir öğrencinin notudur.
`toplam = sum(puanlar)` | `sum`, listedeki sayıları toplar. Bu notların toplamı `300` olur.
`ogrenci_sayisi = len(puanlar)` | `len`, listedeki değer sayısını bulur. Burada dört not bulunduğu için sonuç `4` olur.
`ortalama = toplam / ogrenci_sayisi` | Toplam puanı öğrenci sayısına böleriz: `300 / 4 = 75`. Sonucu `ortalama` değişkeninde saklarız.
`print("Toplam puan:", toplam)` | Toplam puanı açıklama metniyle birlikte gösteririz.
`print("Öğrenci sayısı:", ogrenci_sayisi)` | Hesapta kaç not kullandığımızı gösteririz.
`print("Ortalama:", ortalama)` | Bulduğumuz ortalamayı yazarız. Python bölme işleminin sonucunu `75.0` biçiminde gösterir.
```

Ortalama, grubu tek bir sayıyla özetler; fakat her öğrencinin notunun `75` olduğu anlamına gelmez. Ayrıca çok uç bir değer ortalamayı kolayca değiştirebilir. Örneğin listedeki `90` yerine yanlışlıkla `900` yazılırsa ortalama da belirgin biçimde yükselir. Bu yüzden ortalamaya bakarken verilerin geri kalanını da kontrol et.

Çalışma penceresindeki beklenen çıktı, başlangıçta verilen dört not içindir. Verileri değiştirince doğru sonuç da değişir; sonuç işaretinin başlangıçtaki çıktıyla eşleşmemesi tek başına hata yaptığın anlamına gelmez.

### 2.2 Varyans: değerler birbirinden ne kadar farklı?

İki grubun ortalaması aynı olsa bile değerleri farklı yayılmış olabilir. Örneğin `[7, 8, 9]` ve `[2, 8, 14]` listelerinin ikisinin de ortalaması `8`'dir; ikinci listedeki değerler ortalamadan daha uzaktadır.

Varyansı hesaplarken her değerin ortalamadan farkını buluruz. Bu farka **sapma** denir. Sapmaları kendileriyle çarparız; böylece negatif ve pozitif farklar birbirini silmez, büyük farklar da daha fazla etkili olur. Sonra kareli sapmaları toplayıp değer sayısına böleriz.

```python {.python-playground}
notlar = [6, 8, 10]
ortalama = sum(notlar) / len(notlar)
kareli_sapmalar = []

for notu in notlar:
    sapma = notu - ortalama
    kareli_sapmalar.append(sapma ** 2)

varyans = sum(kareli_sapmalar) / len(notlar)
print("Ortalama:", ortalama)
print("Kareli sapmalar:", kareli_sapmalar)
print("Varyans:", round(varyans, 2))
```
```text {.python-playground-expected}
Ortalama: 8.0
Kareli sapmalar: [4.0, 0.0, 4.0]
Varyans: 2.67
```
```text {.python-playground-help}
`notlar = [6, 8, 10]` | Üç değeri inceleyeceğimiz listeye koyarız. Bu örnekte listedeki üç değerin tamamını ölçmek istediğimiz grup kabul ediyoruz.
`ortalama = sum(notlar) / len(notlar)` | Değerleri toplar ve sayısına böleriz. Bu listenin ortalaması `8.0` olur.
`kareli_sapmalar = []` | Her notun ortalamadan farkının karesini biriktirmek için boş liste oluştururuz.
`for notu in notlar:` | Notları sırayla ele alırız; girintili satırlar her not için bir kez çalışır.
`sapma = notu - ortalama` | O not ile ortalama arasındaki farkı buluruz. İlk not için `6 - 8 = -2` olur.
`kareli_sapmalar.append(sapma ** 2)` | Sapmayı kendisiyle çarpıp listeye ekleriz. İlk notun karesi `(-2) × (-2) = 4` olur; Python'da `** 2` kare alma işlemidir.
`varyans = sum(kareli_sapmalar) / len(notlar)` | Kareli sapmaları toplar ve değer sayısına böleriz: `(4 + 0 + 4) / 3`, yaklaşık `2.67` eder.
`print("Ortalama:", ortalama)` | İncelediğimiz değerlerin ortalamasını gösterir.
`print("Kareli sapmalar:", kareli_sapmalar)` | Her notun ortalamadan farkının karesini gösterir. Ortalamaya eşit olan `8` için fark ve karesi `0` olur.
`print("Varyans:", round(varyans, 2))` | Varyansı virgülden sonra iki basamağa yuvarlayıp gösteririz.
```

Bu hesap, listedeki değerlerin tamamını ilgilendiğimiz grup kabul ettiğimiz **anakitle varyansı**dır; bu nedenle değeri sayısına böldük. Daha büyük bir grubun içinden seçilmiş bir **örneklemi** incelerken, örneklem varyansı için payda genellikle değer sayısının bir eksiği olur. Bu iki hesabı birbirine karıştırmamak gerekir.

Varyans büyüdükçe değerler ortalamadan daha geniş alana yayılmış demektir. Varyans, farkların karesini kullandığı için ölçü birimi de karelenir; bu yüzden sayı doğrudan yorumlanması kolay bir değer olmayabilir. Bu derste yalnızca yayılımın karşılaştırılmasına odaklanıyoruz.

Bu çalışma penceresinin beklenen sonucu `[6, 8, 10]` değerlerine göredir. Alıştırmada başka değerler kullandığında çıktı değişir; yeni sonucu formülle kontrol et.

### 2.3 Korelasyon: iki değişken birlikte değişiyor mu?

Bir öğrencinin çalışma süresi ile aldığı puanı eşleştirilmiş listelerde tutalım. Aynı sıradaki iki değer aynı öğrenciyi anlatmalıdır: ilk süre ilk puanla, ikinci süre ikinci puanla eşleşir.

**Korelasyon katsayısı** `-1` ile `1` arasında olur:

- `1`'e yakın pozitif değer, iki değişkenin birlikte artma eğiliminde olduğunu gösterir.
- `-1`'e yakın negatif değer, biri artarken diğerinin azalma eğiliminde olduğunu gösterir.
- `0`'a yakın değer, belirgin bir doğrusal ilişkinin görülmediğini gösterir. Bu, değişkenler arasında hiçbir ilişki yok demek değildir; ilişki düz bir çizgi biçiminde olmayabilir.

Aşağıdaki küçük örnekte her çalışma saati değeriyle aynı sıradaki puanı eşleştirip korelasyonu kendimiz hesaplıyoruz. Ayrıntılı formülü parçalara ayırdık: önce her listede ortalamadan farkları buluyor, sonra bu farkları birbiriyle karşılaştırıyoruz.

```python {.python-playground}
import math

calisma_saatleri = [1, 2, 3]
puanlar = [2, 4, 6]
saat_ortalama = sum(calisma_saatleri) / len(calisma_saatleri)
puan_ortalama = sum(puanlar) / len(puanlar)

carpim_toplami = 0
saat_kareleri_toplami = 0
puan_kareleri_toplami = 0

for i in range(len(calisma_saatleri)):
    saat_farki = calisma_saatleri[i] - saat_ortalama
    puan_farki = puanlar[i] - puan_ortalama
    carpim_toplami += saat_farki * puan_farki
    saat_kareleri_toplami += saat_farki ** 2
    puan_kareleri_toplami += puan_farki ** 2

payda = math.sqrt(saat_kareleri_toplami * puan_kareleri_toplami)
korelasyon = carpim_toplami / payda
print("Korelasyon:", round(korelasyon, 2))
```
```text {.python-playground-expected}
Korelasyon: 1.0
```
```text {.python-playground-help}
`import math` | Python'la birlikte gelen matematik araçlarını kullanıma açarız; yeni bir paket kurmamız gerekmez.
`calisma_saatleri = [1, 2, 3]` | Üç gözlemin çalışma sürelerini listede tutarız.
`puanlar = [2, 4, 6]` | Aynı üç gözlemin puanlarını aynı sırada tutarız. Her iki listenin uzunluğu ve sırası eşleşmelidir.
`saat_ortalama = sum(calisma_saatleri) / len(calisma_saatleri)` | Çalışma sürelerinin ortalamasını buluruz; bu, sürelerin hangi merkez çevresinde toplandığını gösterir.
`puan_ortalama = sum(puanlar) / len(puanlar)` | Puanların ortalamasını da aynı yöntemle buluruz.
`carpim_toplami = 0` | Her gözlem için iki ortalamadan uzaklıkları çarpacağız; çarpımları bu değişkende toplayacağız.
`saat_kareleri_toplami = 0` | Çalışma sürelerinin ortalamadan farklarının karelerini burada toplarız.
`puan_kareleri_toplami = 0` | Puanların ortalamadan farklarının karelerini burada toplarız.
`for i in range(len(calisma_saatleri)):` | `i`, önce `0`, sonra `1`, sonra `2` olur. Aynı sıradaki süre ve puanı bu konum numarasıyla eşleştiririz.
`saat_farki = calisma_saatleri[i] - saat_ortalama` | O gözlemin çalışma süresinin kendi ortalamasından farkını buluruz.
`puan_farki = puanlar[i] - puan_ortalama` | Aynı gözlemin puanının kendi ortalamasından farkını buluruz.
`carpim_toplami += saat_farki * puan_farki` | İki farkı çarpar ve önceki çarpımların üzerine ekleriz. İki fark aynı işaretliyse bu çarpım pozitiftir.
`saat_kareleri_toplami += saat_farki ** 2` | Süre farkını kendisiyle çarpıp toplama ekleriz; kare alma negatif farkların birbirini silmesini önler.
`puan_kareleri_toplami += puan_farki ** 2` | Puan farkları için de aynı kare alma işlemini yaparız.
`payda = math.sqrt(saat_kareleri_toplami * puan_kareleri_toplami)` | Kareli farkların toplamlarını çarpıp karekökünü alırız. `sqrt` karekök demektir; bu adım sonucu `-1` ile `1` arasındaki ölçekte tutmaya yardım eder.
`korelasyon = carpim_toplami / payda` | Toplanan çarpımları paydada bulduğumuz ölçek değerine böleriz. Sonuç, iki listenin doğrusal ilişki katsayısıdır.
`print("Korelasyon:", round(korelasyon, 2))` | Katsayıyı iki ondalık basamakla gösteririz. Bu örnekte sonuç `1.0`, tam pozitif doğrusal ilişki demektir.
```

Bu örnekte sayılar birlikte aynı yönde değiştiği için korelasyon `1.0` çıkar. `puanlar` listesini `[6, 4, 2]` yaparsan katsayı `-1.0` olur; beklenen çıktı başlangıçtaki listeye göre ayarlandığından işaret değişebilir, fakat bu kodun çalışmadığı anlamına gelmez.

**Korelasyon neden-sonuç kanıtı değildir.** Örneğin çalışma süresi ile puanın birlikte artması, çalışma süresinin puandaki artışın tek nedeni olduğunu kanıtlamaz. Ön bilgi, uyku veya sınavın zorluğu gibi başka etkenler de sonucu etkileyebilir.

Bu hesapta iki listede de değişen değer bulunmalıdır. Listelerden biri sabitse payda `0` olur ve korelasyon hesaplanamaz. Gerçek veride ayrıca iki listenin eşit uzunlukta olduğundan ve her sıranın aynı kişiye ya da olaya ait olduğundan emin ol.

## 3. Kütüphaneyle yap

Python'ın standart `statistics` modülü, ortalama ve varyans gibi yaygın ölçüleri hazır olarak sunar. Bu modül Python ile birlikte gelir; ayrıca kurulum yapman gerekmez. Korelasyon için de eşleştirilmiş iki liste veriyoruz.

```python {.python-playground}
import statistics

puanlar = [6, 8, 10]
saatler = [1, 2, 3]
sonuclar = [2, 4, 6]

print("Ortalama:", float(statistics.mean(puanlar)))
print("Anakitle varyansı:", round(statistics.pvariance(puanlar), 2))
print("Korelasyon:", statistics.correlation(saatler, sonuclar))
```
```text {.python-playground-expected}
Ortalama: 8.0
Anakitle varyansı: 2.67
Korelasyon: 1.0
```
```text {.python-playground-help}
`import statistics` | Python'ın temel istatistik hesaplarını sağlayan standart modülünü kullanıma açarız.
`puanlar = [6, 8, 10]` | Ortalama ve varyansını bulacağımız üç puanı belirleriz.
`saatler = [1, 2, 3]` | Korelasyon için ilk değişkenin, yani çalışma saatlerinin değerlerini yazarız.
`sonuclar = [2, 4, 6]` | İkinci değişkeni aynı sırada yazarız; her puan aynı konumdaki saat değeriyle eşleşir.
`statistics.mean(puanlar)` | `mean`, listedeki sayıların ortalamasını hazır olarak hesaplar. `float` sonucu ondalıklı biçimde gösterir.
`statistics.pvariance(puanlar)` | `pvariance`, listedeki değerlerin tamamını grup kabul ederek anakitle varyansını hesaplar.
`statistics.correlation(saatler, sonuclar)` | İki eşit uzunluktaki listenin Pearson korelasyon katsayısını hesaplar. Sonuç, sıfırdan farklı yayılıma sahip veriler için `-1` ile `1` arasındadır.
```

Hazır modül, elle yazdığımız hesapları kısaltır. Ancak hangi ölçünün ne anlattığını bilmek, doğru aracı seçebilmek ve sonucunu yorumlayabilmek için önemlidir.

## 4. Sık yapılan hatalar

- **Ortalama ile bütün değerleri aynı sanmak.** Ortalama grubun özeti olan tek sayıdır; listedeki her değer farklı olabilir.
- **Uç bir değerin etkisini görmezden gelmek.** Yanlış veya çok büyük bir değer ortalamayı ve varyansı güçlü biçimde değiştirebilir; önce veriyi kontrol et.
- **Varyansın neyi ölçtüğünü karıştırmak.** Varyans, değerlerin ortalamadan yayılımını ölçer; yüksek varyans daha geniş yayılım demektir.
- **Anakitle ve örneklem varyansını karıştırmak.** Bu dersteki elle hesap tüm grubu kabul edip `n`'ye böler; örneklem varyansında payda genellikle `n - 1` olur.
- **Korelasyonu neden-sonuç sanmak.** İki değişkenin birlikte değişmesi, birinin diğerine sebep olduğunu tek başına göstermez.
- **Korelasyon sıfıra yakınsa hiçbir ilişki yok sanmak.** Bu katsayı doğrusal ilişkiyi ölçer; değişkenler eğri biçiminde ilişkili olabilir.
- **Eşleşmiş verilerin sırasını karıştırmak.** Süre listesinin `i` konumundaki değeri, puan listesinin aynı `i` konumundaki değerle aynı gözleme ait olmalıdır.
- **Değerleri değişmeyen listeyle korelasyon hesaplamak.** Bir listedeki bütün sayılar aynıysa yayılım yoktur ve korelasyonun paydası sıfır olur; bu durumda katsayı tanımsızdır.

## 5. Pekiştir

**Quiz**

1. Dört notun toplamı `300` ise ortalama nasıl hesaplanır?
2. Varyansın büyük çıkması, değerlerin dağılımı hakkında ne söyler?
3. Korelasyon katsayısının alabileceği aralık nedir?
4. İki değişken arasında yüksek korelasyon bulunması, birinin diğerine neden olduğunu kanıtlar mı?
5. Bu dersteki varyans hesabında neden değer sayısına bölüyoruz?

**Alıştırmalar**

1. Ortalama penceresindeki son notu `900` yap. Ortalama nasıl değişti? Bu değerin doğru olup olmadığını neden kontrol etmeliyiz?
2. Varyans penceresinde önce `[7, 8, 9]`, sonra `[2, 8, 14]` değerlerini kullan. Ortalamalar aynı olsa da varyansların neden farklı olduğunu açıkla.
3. Korelasyon penceresinde `puanlar` listesini `[6, 4, 2]` yap. İşaretin neden negatife döndüğünü anlat.
4. (İsteğe bağlı) Korelasyon penceresinde saatleri `[1, 2, 3, 4]`, puanları `[2, 4, 4, 2]` yap. Katsayı `0` çıkarken verilerde nasıl bir örüntü bulunuyor?

??? success "Quiz cevapları"
    1. Toplamı değer sayısına böleriz: `300 / 4 = 75`.
    2. Değerler ortalamadan daha geniş bir alana yayılmıştır.
    3. `-1` ile `1` arasındadır. Pozitif değer aynı yönde, negatif değer ters yönde doğrusal ilişkiyi gösterir.
    4. Hayır. Korelasyon birlikte değişimi gösterir; sebep-sonuç ilişkisini tek başına kanıtlamaz.
    5. Listeyi ilgilendiğimiz grubun tamamı kabul ettiğimiz için anakitle varyansı hesaplıyoruz. Daha büyük bir grubun örnekleminde payda genellikle `n - 1` olur.

## Özet

Ortalama bir veri grubunun merkezini, varyans ise değerlerin bu merkez çevresinde ne kadar yayıldığını özetler. Korelasyon, eşleşmiş iki sayısal değişkenin doğrusal olarak birlikte değişme yönünü ve gücünü gösterir. Korelasyon neden-sonuç kanıtı değildir; uç değerler ve yanlış eşleştirilmiş veriler ölçüleri yanıltabilir. İstatistiksel ölçüleri yorumlamadan önce hangi verilerin ve hangi grubun ölçüldüğünü kontrol etmeliyiz.

## Kaynaklar

- [Python resmî belgesi: `statistics`](https://docs.python.org/3/library/statistics.html)
- [OpenStax: Introductory Statistics](https://openstax.org/details/books/introductory-statistics)
