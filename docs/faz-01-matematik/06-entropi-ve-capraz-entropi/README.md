# Faz 1 – Ders 6: Entropi ve çapraz entropi

> ⏱️ Tahmini süre: 45-60 dk · 📚 Ön koşul: 0.2 Python hızlı tekrar, 1.4 Olasılık ve dağılımlar, 1.5 İstatistik · 💻 Gereksinim: Python 3.11+; temel örnekler ek paketsiz, isteğe bağlı PyTorch örneği için PyTorch kurulmalıdır

## Bu derste ne öğreneceksin?

- Bir olasılık dağılımındaki belirsizliği entropiyle ölçmeyi
- Modelin tahminlerini gerçek sonuçlarla çapraz entropi kullanarak karşılaştırmayı
- Çapraz entropinin sınıflandırma modellerinde neden kayıp olarak kullanıldığını
- Entropi ve çapraz entropinin neyi söylemediğini

## 1. Problem

Bir madeni paranın yazı mı tura mı geleceğini tahmin ettiğini düşün. Para adilse iki sonuç da eşit olasılıklıdır; hangisinin geleceğini önceden kestirmek zordur. Para her atışta yazı geliyorsa sonuç belirsiz değildir. **Entropi**, bir olasılık dağılımındaki bu belirsizliği sayıyla anlatır.

Şimdi bir sınıflandırma modeli düşün: bir fotoğrafın kedi mi köpek mi olduğunu tahmin ediyor. Model yalnızca bir sınıfı seçmekle kalmaz; çoğu zaman her sınıf için olasılık da üretir. Doğru cevap köpek olduğu hâlde modele köpek olasılığını düşük veriyorsa tahmini kötüdür. **Çapraz entropi**, modelin olasılık tahminlerini gerçek cevapla karşılaştırıp bu yanlışı bir kayıp sayısına dönüştürür.

Kısaca: entropi bir dağılımdaki belirsizliği ölçer; çapraz entropi modelin tahmin dağılımının gerçek cevapla ne kadar uyuşmadığını ölçer.

## 2. Kendin yaz

### 2.1 Entropi: sonuç ne kadar belirsiz?

Adil para için yazı ve tura olasılıkları `0.5` ve `0.5` olsun. Dağılımın olasılıkları toplamı `1` olmalıdır. Entropi hesabında her olasılığı kendi ikili logaritmasıyla çarpar, bu sonuçları toplar ve toplamın işaretini değiştiririz:

`H = -Σ p × log₂(p)` — `Σ`, listedeki bütün sonuçlar için yapılan toplamı gösterir.

Burada `p`, bir sonucun olasılığıdır. `log₂`, ikinin hangi kuvvetinin verilen sayıyı oluşturduğunu sorar. Entropi kodunda olasılığı `0` olan sonuçları atlarız; çünkü `log₂(0)` hesaplanamaz ve bu sonucun entropiye katkısı sıfır kabul edilir.

```python {.python-playground}
import math

olasiliklar = [0.5, 0.5]
entropi = 0.0

for olasilik in olasiliklar:
    if olasilik > 0:
        entropi -= olasilik * math.log2(olasilik)

print("Yazı-tura entropisi:", round(entropi, 2), "bit")
```
```text {.python-playground-expected}
Yazı-tura entropisi: 1.0 bit
```
```text {.python-playground-help}
`import math` | Python'ın standart matematik araçlarını kullanıma açarız; yeni bir paket kurmamız gerekmez.
`olasiliklar = [0.5, 0.5]` | Yazı ve tura olasılıklarını aynı sırayla listeye koyarız. İki olasılığın toplamı `1` eder.
`entropi = 0.0` | Entropi hesabında bulacağımız parçaları eklemek için toplamı sıfırdan başlatırız.
`for olasilik in olasiliklar:` | Listedeki olasılıkları birer birer `olasilik` değişkenine alırız; girintili satırlar her olasılık için çalışır.
`if olasilik > 0:` | Olasılık sıfırdan büyükse altındaki hesabı yaparız. Sıfırın logaritması hesaplanamadığı için sıfır olasılıklı sonuçları atlarız.
`entropi -= olasilik * math.log2(olasilik)` | Olasılığı kendi ikili logaritmasıyla çarpıp toplamdan çıkarırız. `-=` mevcut toplamdan bu parçayı çıkarır; logaritma negatif olduğu için entropiye pozitif katkı eklenir.
`print("Yazı-tura entropisi:", round(entropi, 2), "bit")` | Sonucu iki basamağa yuvarlayıp gösteririz. `log2` kullandığımız için ölçü birimi bittir.
```

Adil parada iki sonuç da eşit olasılıklı olduğu için entropi `1` bittir. `olasiliklar` listesini `[1.0, 0.0]` yaparsan sonuç her zaman ilk seçenektir ve entropi `0` olur: artık belirsizlik yoktur. Bu pencerenin beklenen çıktısı başlangıçtaki `[0.5, 0.5]` değerlerine göredir; olasılıkları değiştirince doğru sonuç da değişir.

### 2.2 Çapraz entropi: model doğru cevaba ne kadar güveniyor?

Modelin iki sınıftan birini tahmin ettiğini varsayalım: `0` birinci sınıf, `1` ikinci sınıf olsun. Gerçek cevap ikinci sınıf, yani `1`'dir. Bunu `[0, 1]` listesiyle gösteriyoruz: doğru sınıfın yerinde `1`, diğer sınıfın yerinde `0` vardır. Bu gösterime **one-hot kodlama** denir.

Model iki sınıf için `[0.2, 0.8]` olasılıklarını tahmin etsin. Doğru sınıfın olasılığı `0.8` olduğundan tahmin makuldür. Gerçek etiket `y`, modelin tahmini `p` ise çapraz entropi şöyle hesaplanır:

`H(y, p) = -Σ yᵢ × log₂(pᵢ)`

Buradaki `i`, iki listedeki aynı sıradaki sınıfı gösterir; `Σ` bu sınıfların katkılarını toplar. Gerçek etiket listesinde yanlış sınıfların değeri `0` olduğundan, bu örnekte yalnızca doğru sınıfın tahmini hesaba katkı verir.

```python {.python-playground}
import math

gercek_etiket = [0, 1]
tahmin_olasiliklari = [0.2, 0.8]
capraz_entropi = 0.0

for i in range(len(gercek_etiket)):
    gercek = gercek_etiket[i]
    tahmin = tahmin_olasiliklari[i]
    if gercek > 0:
        capraz_entropi -= gercek * math.log2(tahmin)

print("Doğru sınıfın tahmini:", tahmin_olasiliklari[1])
print("Çapraz entropi:", round(capraz_entropi, 2), "bit")
```
```text {.python-playground-expected}
Doğru sınıfın tahmini: 0.8
Çapraz entropi: 0.32 bit
```
```text {.python-playground-help}
`gercek_etiket = [0, 1]` | Gerçek cevabın ikinci sınıf olduğunu belirtiriz. `1` doğru sınıfı, `0` diğer sınıfı gösterir; buna one-hot gösterim denir.
`tahmin_olasiliklari = [0.2, 0.8]` | Modelin iki sınıfa verdiği olasılıkları yazarız. Toplamları `1` olmalıdır; model ikinci sınıfa daha yüksek olasılık vermiştir.
`capraz_entropi = 0.0` | Yanlış tahmini ölçecek kayıp toplamını sıfırdan başlatırız.
`for i in range(len(gercek_etiket)):` | `i`, önce `0`, sonra `1` olur; böylece iki listenin aynı sıradaki değerlerini karşılaştırırız.
`gercek = gercek_etiket[i]` | Gerçek etikette o sıradaki sınıfın doğru olup olmadığını alırız. İkinci sınıf için bu değer `1`'dir.
`tahmin = tahmin_olasiliklari[i]` | Modelin aynı sınıfa verdiği olasılığı alırız. İkinci sınıf için bu değer `0.8` olur.
`if gercek > 0:` | Yalnızca gerçek cevaba karşılık gelen sınıfın hesabını yaparız; yanlış sınıfların etiketi `0` olduğu için katkıları yoktur.
`capraz_entropi -= gercek * math.log2(tahmin)` | Gerçek sınıfa verilen olasılığın logaritmasını alıp işaretini değiştiririz. Doğru sınıfa yüksek olasılık verilirse kayıp küçülür.
`print("Doğru sınıfın tahmini:", tahmin_olasiliklari[1])` | İkinci sınıfın, yani gerçek sınıfın tahmin olasılığını gösteririz.
`print("Çapraz entropi:", round(capraz_entropi, 2), "bit")` | Kayıp değerini iki basamağa yuvarlayıp bit cinsinden yazarız. `0.8` olasılığı için sonuç yaklaşık `0.32` bittir.
```

Doğru sınıfın olasılığını `0.2`'ye düşürmek için `tahmin_olasiliklari` listesini `[0.8, 0.2]` yap. Çapraz entropi yaklaşık `2.32` bit olur; model doğru cevaba düşük olasılık verdiği için kayıp büyür. Beklenen çıktı başlangıçtaki olasılıklara göredir, bu nedenle değiştirdiğin değerlerle aynı görünmesi gerekmez.

Entropi, çapraz entropi ve kayıp aynı şey değildir. Entropi bir dağılımın belirsizliğini; çapraz entropi gerçek dağılımla tahminin uyuşmamasını ölçer. Eğitim sırasında model, doğru cevaplara yüksek olasılık vererek çapraz entropi kaybını azaltmaya çalışır.

Bu örnekte tek bir doğru sınıfı olan tek bir gözlemi inceliyoruz. Eğitimde birden fazla örneğin kayıpları genellikle bir araya getirilip ortalanır. Gerçek cevap tek bir sınıf yerine belirsiz bir dağılım olarak verilirse, tahmin bu dağılımla tamamen aynı olsa bile çapraz entropi sıfır olmak zorunda değildir.

### Şimdi sen yaz: entropi ve kayıp

**Görev:** İki hesap yapacaksın: dört eşit olasılıklı sonucun entropisini ve doğru sınıfa `0.5` olasılık veren bir modelin kaybını. İkisi de bit cinsinden yazılır.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
import math

olasiliklar = [0.25, 0.25, 0.25, 0.25]
entropi = 0.0

for p in olasiliklar:
    # TODO: Entropiye -p × log2(p) ekle (math.log2).
    entropi += ___

# TODO: Doğru sınıfa 0.5 olasılık veren modelin kaybı -log2(0.5) bittir.
kayip = ___

print("Entropi:", entropi, "bit")
print("Kayıp:", kayip, "bit")
```
```text {.python-playground-expected}
Entropi: 2.0 bit
Kayıp: 1.0 bit
```
```text {.python-playground-help}
`entropi += ___` | Entropi formülü `-p × log₂(p)`. Python'da `-p * math.log2(p)`.
`kayip = ___` | Çapraz entropi, doğru sınıfın olasılığının `-log₂`'sidir: `-math.log2(0.5)`.
```
```python {.python-playground-solution}
import math

olasiliklar = [0.25, 0.25, 0.25, 0.25]
entropi = 0.0

for p in olasiliklar:
    # Entropiye -p × log2(p) ekle (math.log2).
    entropi += -p * math.log2(p)

# Doğru sınıfa 0.5 olasılık veren modelin kaybı -log2(0.5) bittir.
kayip = -math.log2(0.5)

print("Entropi:", entropi, "bit")
print("Kayıp:", kayip, "bit")
```

## 3. Kütüphaneyle yap

Önceki pencereler Python'ın standart `math` modülünü kullandı; bunlar tarayıcıda ek paket olmadan çalışır. Gerçek bir sinir ağı eğitirken PyTorch gibi bir çerçeve çapraz entropi hesabını hazır sunar. Aşağıdaki kod, modele ait ham puanları (**logit'leri**) ve doğru sınıfın numarasını verir:

```python
import torch
import torch.nn.functional as F

logitler = torch.tensor([1.0, 2.0])
gercek_sinif = torch.tensor(1)
kayip = F.cross_entropy(logitler, gercek_sinif)

print("Çapraz entropi:", round(kayip.item(), 2))
```

Beklenen çıktı:

```text
Çapraz entropi: 0.31
```

Logit'ler olasılık değildir; modelin sınıflar için ürettiği ham puanlardır. `F.cross_entropy`, bu puanlardan olasılıkları güvenli biçimde hesaplayıp doğru sınıfa göre kaybı bulur. Burada en yüksek puan ikinci sınıfta ve gerçek sınıfın numarası `1` olduğu için tahmin doğru yöndedir.

Bu örnek PyTorch ayrı kurulmadığı için tarayıcıdaki Python penceresinde çalışmaz. Denemek istersen [PyTorch'un resmî kurulum sayfasından](https://pytorch.org/get-started/locally/) bilgisayarına uygun kurulumu seç; paketi kodu çalıştıracağın aynı Python ortamına kur. Sonra kodu `capraz_entropi.py` adlı dosyaya kaydedip dosyanın bulunduğu klasörde `python capraz_entropi.py` komutuyla çalıştır. Temel entropi ve çapraz entropi örneklerini anlamak için PyTorch kurmak gerekmez.

Elle yazdığımız örnek `log2` kullandığı için sonucu bit cinsinden gösterir. PyTorch gibi araçlar genellikle doğal logaritma kullanır ve sonucu nat cinsinden verir. Ölçü birimi sayısal sonucu değiştirir, hangi tahminin daha iyi olduğunu değil. Örneğin doğru sınıfa `0.8` olasılığı verilirse kayıp yaklaşık `0.32` bit veya `0.22` nat olur.

## 4. Sık yapılan hatalar

- **Entropinin belirsizlik ölçtüğünü unutmak.** Entropi modelin doğru cevap sayısını veya doğruluğunu ölçmez; olasılık dağılımındaki belirsizliği ölçer.
- **Olasılıkların toplamını kontrol etmemek.** Bir dağılımdaki olasılıklar `0` ile `1` arasında olmalı ve toplamları `1` etmelidir.
- **Entropi hesabında `0` olasılığının logaritmasını almaya çalışmak.** `log₂(0)` hesaplanamaz; bu olasılığın entropiye katkısı sıfırdır ve kodda atlanır.
- **Doğru sınıfın olasılığı yerine en yüksek olasılığı kullanmak.** Çapraz entropi, modelin özellikle gerçek cevaba verdiği olasılığa bakar; yanlış sınıfa yüksek olasılık verilmesi kaybı azaltmaz.
- **Doğru sınıfa `0` olasılık vermek.** Matematiksel olarak kayıp sonsuza gider; Python'da `log2(0)` hata verir. Gerçek eğitim çerçeveleri bu hesabı sayısal açıdan güvenli yapar.
- **PyTorch'a olasılık gönderdiğini sanmak.** `F.cross_entropy` ham logit'leri bekler; `[0.2, 0.8]` gibi olasılıkları doğrudan vermek doğru kullanım değildir.
- **Bit ve nat sayılarını aynı ölçekte karşılaştırmak.** `log2` bit, doğal logaritma nat verir. Aynı dağılım farklı sayılar üretebilir; karşılaştırırken kullanılan logaritma tabanını da dikkate al.
- **Düşük çapraz entropinin tek başına her şeyi kanıtladığını düşünmek.** Kayıp, seçilen örneklerde tahmin ile gerçek cevap arasındaki uyumu ölçer; verinin doğru veya temsil edici olduğunu tek başına göstermez.

## 5. Pekiştir

**Quiz**

1. Entropi bir olasılık dağılımı hakkında neyi ölçer?
2. Yazı ve tura olasılıkları `[1.0, 0.0]` ise belirsizlik neden sıfırdır?
3. Çapraz entropi hesabında neden gerçek sınıfa verilen olasılık önemlidir?
4. Gerçek sınıfa `0.8` olasılık veren modelin kaybı, `0.2` veren modelinkinden neden küçüktür?
5. PyTorch `F.cross_entropy` girdisi olarak olasılık mı, logit mi bekler?

**Alıştırmalar**

1. Entropi penceresindeki olasılıkları `[1.0, 0.0]` yap. Çıkan `0` değerini belirsizlik açısından açıkla.
2. Entropi penceresindeki olasılıkları `[0.9, 0.1]` yap. Sonuç yaklaşık `0.47` bit olmalıdır; neden adil paranın `1` bitinden küçüktür?
3. Çapraz entropi penceresindeki tahminleri `[0.8, 0.2]` yap. Doğru sınıfa verilen olasılık ve kayıp nasıl değişti?
4. (İsteğe bağlı) Tahminleri `[0.5, 0.5]` yap. Model hiçbir sınıfı diğerinden daha olası görmediğinde çapraz entropi kaç bit olur?

??? success "Quiz cevapları"
    1. Olası sonuçların ne kadar belirsiz veya öngörülmesi zor olduğunu ölçer.
    2. İlk sonuç kesinlikle gerçekleşir; başka bir olasılık kalmadığı için belirsizlik yoktur.
    3. Kayıp, modelin gerçek cevaba ne kadar olasılık verdiğini ölçer. Gerçek sınıfın etiketi `1`, diğerlerinin `0` olduğu için yanlış sınıflar toplama katkı yapmaz.
    4. Doğru sınıfa yüksek olasılık vermek, `-log(p)` değerini küçültür. `0.2` gibi düşük olasılık daha büyük kayıp üretir.
    5. Ham puanlar olan logit'leri bekler; olasılıkları kendi içinde hesaplar.

## Özet

Entropi, bir olasılık dağılımındaki belirsizliği ölçer: sonuçlar eşit olasılıklı olduğunda belirsizlik en yüksektir, bir sonuç kesin olduğunda sıfırdır. Çapraz entropi, modelin tahmin ettiği olasılıkları gerçek cevapla karşılaştırır ve doğru sınıfa düşük olasılık verilmesini büyük kayıpla cezalandırır. Bu nedenle sınıflandırma modellerini eğitirken sık kullanılan bir kayıp ölçüsüdür. Elle yazdığımız örnekler bit, PyTorch örneği ise nat kullanır; değerler farklı görünse de ölçtükleri uyum aynıdır.

## Kaynaklar

- [Python resmî belgesi: `math.log2`](https://docs.python.org/3/library/math.html#math.log2)
- [PyTorch resmî belgesi: `CrossEntropyLoss`](https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)
