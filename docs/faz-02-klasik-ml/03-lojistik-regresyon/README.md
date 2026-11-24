# Faz 2 – Ders 3: Lojistik regresyon

> ⏱️ Tahmini süre: 60-75 dk · 📚 Ön koşul: 0.2 Python hızlı tekrar, 1.3 Türev ve gradyan, 1.6 Entropi ve çapraz entropi, 2.1 NumPy ile veri, 2.2 Doğrusal regresyon · 💻 Gereksinim: Python 3.11+; temel örnekler ek paketsiz, NumPy örneği için NumPy kurulmalıdır

## Bu derste ne öğreneceksin?

- Sayısal bir girdiden iki sınıftan birine ait olma olasılığını hesaplamayı
- Sigmoid işlevinin ham puanı `0` ile `1` arasına nasıl çevirdiğini
- Olasılığı bir eşikle karşılaştırıp sınıf tahmini yapmayı
- Çapraz entropi gradyanıyla lojistik regresyonu basit veriler üzerinde eğitmeyi
- Aynı hesabı NumPy dizileriyle kısa biçimde yazmayı

## 1. Problem

Bir öğrencinin çalışma saatine bakarak sınavı geçip geçemeyeceğini tahmin etmek istediğimizi düşün. Geçme-kalma birer **sınıftır**: `0` başarısız, `1` başarılı anlamına gelsin. Bir sınıf seçmek istiyoruz; bu nedenle doğrusal regresyondan farklı olarak sonuç yalnızca herhangi bir sayı olamaz.

Önceki derste modelin düz bir çizgiyle fiyat gibi sayıları tahmin ettiğini gördün. Lojistik regresyonda da önce çalışma saatiyle ağırlığı çarpıp sabit terimi ekleriz. Bu ham puanı **sigmoid** adlı eğriden geçirerek `0` ile `1` arasında bir olasılık elde ederiz. Sonra bu olasılığı bir eşikle karşılaştırıp sınıf seçeriz.

Bu derste yalnızca iki sınıf ve tek bir girdi kullanacağız. Gerçek uygulamalarda daha fazla girdi olabilir; örneklerimiz yöntemin temel fikrini göstermek için küçük tutulmuştur. Modelin verdiği olasılık bir garantili sonuç değil, eğitim verisinden öğrendiği tahmindir.

## 2. Kendin yaz

### 2.1 Ham puanı olasılığa çevir

Sigmoid, çok küçük veya çok büyük bir ham puanı `0` ile `1` arasındaki değere dönüştürür:

`olasılık = 1 / (1 + e^(-ham puan))`

Buradaki `e`, matematikte kullanılan sabit bir sayıdır. Hesabı elle yapmak yerine Python'ın `math.exp` aracını kullanacağız. Ham puan `0` olduğunda olasılık `0.5` olur; puan yükseldikçe olasılık `1`'e, düştükçe `0`'a yaklaşır.

```python {.python-playground}
import math

for ham_puan in [-2, 0, 2]:
    olasilik = 1 / (1 + math.exp(-ham_puan))
    print(f"Ham puan {ham_puan}: olasılık {round(olasilik, 2)}")
```
```text {.python-playground-expected}
Ham puan -2: olasılık 0.12
Ham puan 0: olasılık 0.5
Ham puan 2: olasılık 0.88
```
```text {.python-playground-help}
`import math` | Python'la birlikte gelen matematik araçlarını kullanıma açar; yeni bir paket kurmamız gerekmez.
`for ham_puan in [-2, 0, 2]:` | Üç farklı puanı sırayla deneriz. Döngünün içindeki satırlar her puan için yeniden çalışır.
`math.exp(-ham_puan)` | `e` sayısının `-ham_puan` kuvvetini hesaplar; sigmoid formülündeki üstel işlem budur.
`olasilik = 1 / (1 + math.exp(-ham_puan))` | Sigmoid formülünü uygularız. Hangi ham puan verilirse verilsin sonuç `0` ile `1` arasında kalır.
`print(f"Ham puan {ham_puan}: olasılık {round(olasilik, 2)}")` | Ham puanı ve iki basamağa yuvarlanmış olasılığı gösteririz.
```

Olasılık `0.88` ise model, bu örneğin `1` sınıfında olma ihtimalini yüksek tahmin etmiştir; bu, sonucun kesin olduğu anlamına gelmez. Olasılık `0.12` ise `1` sınıfı tahmini düşüktür. `0.5`, iki sınıf arasında karar vermek için kullanabileceğimiz eşik değeridir.

### 2.2 Olasılıktan sınıf tahmini yap

Şimdilik ağırlığı `1`, sabit terimi `-3` seçelim. Bu değerler `1` ve `2` saat çalışan öğrenciler için düşük, `4` ve `5` saat çalışanlar için yüksek olasılık üretir. Bu bölümde ağırlık ve sabit terim **elle seçilmiştir**; model henüz veriden öğrenmemiştir.

```python {.python-playground}
import math

agirlik = 1.0
sabit = -3.0
calisma_saatleri = [1, 2, 4, 5]

for saat in calisma_saatleri:
    ham_puan = agirlik * saat + sabit
    olasilik = 1 / (1 + math.exp(-ham_puan))
    if olasilik >= 0.5:
        sinif = "Başarılı"
    else:
        sinif = "Başarısız"
    print(f"{saat} saat: {sinif} (olasılık {round(olasilik, 2)})")
```
```text {.python-playground-expected}
1 saat: Başarısız (olasılık 0.12)
2 saat: Başarısız (olasılık 0.27)
4 saat: Başarılı (olasılık 0.73)
5 saat: Başarılı (olasılık 0.88)
```
```text {.python-playground-help}
`agirlik = 1.0` | Çalışma saati bir artınca ham puanın bir artacağını varsayarız. Bu, şimdilik elle belirlediğimiz başlangıç ağırlığıdır.
`sabit = -3.0` | Ham puanın başlangıç değerini belirleriz; bu örnekte saati sıfır olan kişinin puanı `-3` olur.
`calisma_saatleri = [1, 2, 4, 5]` | Olasılığını hesaplayacağımız dört öğrencinin çalışma saatini listede tutarız.
`for saat in calisma_saatleri:` | Her çalışma saatini sırayla `saat` değişkenine alırız ve alttaki girintili satırları onun için çalıştırırız.
`ham_puan = agirlik * saat + sabit` | Doğrusal modelin önceki derste öğrendiğimiz biçimiyle ham puanı hesaplarız.
`olasilik = 1 / (1 + math.exp(-ham_puan))` | Ham puanı sigmoid formülüne koyup `0` ile `1` arasında bir olasılığa çeviririz.
`if olasilik >= 0.5:` | Olasılığın yarıdan büyük veya yarıya eşit olup olmadığını kontrol ederiz; `>=` “büyük veya eşit” demektir.
`sinif = "Başarılı"` | Eşik koşulu doğruysa tahmini `Başarılı` olarak saklarız.
`else:` | Olasılık eşikten küçükse çalışacak bölümü başlatırız.
`sinif = "Başarısız"` | Eşik koşulu yanlışsa tahmini `Başarısız` olarak saklarız.
`print(f"{saat} saat: {sinif} (olasılık {round(olasilik, 2)})")` | Çalışma saatini, seçilen sınıfı ve olasılığı birlikte gösteririz.
```

`0.5` evrensel ve değiştirilemez bir kural değildir. Yanlış sınıf tahminlerinin maliyetine göre uygulama başka bir eşik seçebilir. Ayrıca eşiği değiştirmek modelin ürettiği olasılıkları değil, olasılıktan sınıf seçme kararını değiştirir.

### 2.3 Modeli örneklerden eğit

Şimdi çalışma saatlerini ve bilinen sonuçları kullanalım. `0`, öğrencinin başarısız olduğunu; `1`, başarılı olduğunu gösterir. Model başlangıçta her örneğe `0.5` olasılık verir. Her turda tahminle gerçek etiketi karşılaştırıp ağırlık ve sabit terimi biraz güncelleriz.

Çapraz entropi, doğru sınıfa düşük olasılık verildiğinde büyük kayıp üretir. Gerçek etiket `1` ise kayıp `-log(olasılık)`, etiket `0` ise `-log(1 - olasılık)` olur. Böylece model doğru cevaba düşük olasılık verdiğinde daha fazla cezalandırılır. Bu fikri [1.6 dersinde](../../faz-01-matematik/06-entropi-ve-capraz-entropi/README.md) gördün.

Sigmoid ile çapraz entropinin bu örnekteki gradyanı şu biçimde sadeleşir:

`ağırlık gradyanı = ortalama((tahmin olasılığı - gerçek etiket) × çalışma saati)`

`sabit gradyanı = ortalama(tahmin olasılığı - gerçek etiket)`

`tahmin olasılığı - gerçek etiket` farkı, hangi yönde düzeltme gerektiğini söyler. Gerçek etiket `1` ama tahmin düşükse fark negatiftir; çalışma saatleri pozitif olduğu için gradyanı çıkarmak ağırlığı artırır ve daha çok çalışanlara daha yüksek olasılık vermeye yöneltir. Gerçek etiket `0` ama tahmin yüksekse güncelleme ters yönde işler. Bu gradyanların nasıl kullanıldığını 1.3 dersindeki gradyan inişiyle birlikte düşün.

```python {.python-playground}
import math


def sigmoid(ham_puan):
    return 1 / (1 + math.exp(-ham_puan))


calisma_saatleri = [1.0, 2.0, 4.0, 5.0]
gercek_etiketler = [0, 0, 1, 1]
agirlik = 0.0
sabit = 0.0
ogrenme_hizi = 0.1

for adim in range(1000):
    agirlik_gradyani = 0.0
    sabit_gradyani = 0.0

    for i in range(len(calisma_saatleri)):
        ham_puan = agirlik * calisma_saatleri[i] + sabit
        olasilik = sigmoid(ham_puan)
        hata = olasilik - gercek_etiketler[i]
        agirlik_gradyani += hata * calisma_saatleri[i]
        sabit_gradyani += hata

    agirlik_gradyani /= len(calisma_saatleri)
    sabit_gradyani /= len(calisma_saatleri)
    agirlik -= ogrenme_hizi * agirlik_gradyani
    sabit -= ogrenme_hizi * sabit_gradyani

olasiliklar = []
tahmin_edilen_siniflar = []
for saat in calisma_saatleri:
    olasilik = sigmoid(agirlik * saat + sabit)
    olasiliklar.append(round(olasilik, 2))
    tahmin_edilen_siniflar.append(int(olasilik >= 0.5))

print("Öğrenilen ağırlık:", round(agirlik, 2))
print("Öğrenilen sabit:", round(sabit, 2))
print("Tahmin olasılıkları:", olasiliklar)
print("Tahmin edilen sınıflar:", tahmin_edilen_siniflar)
```
```text {.python-playground-expected}
Öğrenilen ağırlık: 2.04
Öğrenilen sabit: -5.73
Tahmin olasılıkları: [0.02, 0.16, 0.92, 0.99]
Tahmin edilen sınıflar: [0, 0, 1, 1]
```
```text {.python-playground-help}
`def sigmoid(ham_puan):` | Ham puanı olasılığa çeviren işlevi tanımlarız. Aynı hesabı her örnekte tekrar kullanacağız.
`return 1 / (1 + math.exp(-ham_puan))` | Sigmoid formülünün sonucunu işlevi çağıran yere geri veririz.
`calisma_saatleri = [1.0, 2.0, 4.0, 5.0]` | Modelin öğreneceği dört girdi değerini sırayla yazarız.
`gercek_etiketler = [0, 0, 1, 1]` | Aynı sıradaki gerçek cevapları saklarız: ilk iki öğrenci başarısız, son iki öğrenci başarılıdır.
`agirlik = 0.0` | Ağırlığı başlangıçta sıfır seçeriz; eğitim sırasında değişecektir.
`sabit = 0.0` | Sabit terimi de sıfırdan başlatırız.
`ogrenme_hizi = 0.1` | Her güncellemede gradyanın ne kadarının uygulanacağını belirleriz.
`for adim in range(1000):` | Modeli ve parametrelerini 1000 kez güncelleriz. `adim` tekrar sayısını gösterir.
`agirlik_gradyani = 0.0` | Bu turdaki örneklerden ağırlık gradyanını toplamak için değişkeni sıfırdan başlatırız.
`sabit_gradyani = 0.0` | Sabit terimin gradyanını da her güncelleme turunda yeniden toplarız.
`for i in range(len(calisma_saatleri)):` | Dört eğitim örneğini sırayla inceleriz; `i` aynı konumdaki saat ve etiketi eşleştirir.
`ham_puan = agirlik * calisma_saatleri[i] + sabit` | O anki parametrelerle seçilen öğrencinin ham puanını hesaplarız.
`olasilik = sigmoid(ham_puan)` | Ham puanı sigmoid işlevinden geçirip başarı olasılığını buluruz.
`hata = olasilik - gercek_etiketler[i]` | Tahmin olasılığıyla gerçek `0` veya `1` etiket arasındaki farkı buluruz.
`agirlik_gradyani += hata * calisma_saatleri[i]` | Hatanın ağırlık üzerindeki etkisini, çalışma saatiyle çarpıp gradyan toplamına ekleriz.
`sabit_gradyani += hata` | Aynı hatayı sabit terimin gradyan toplamına ekleriz.
`agirlik_gradyani /= len(calisma_saatleri)` | Toplam gradyanı örnek sayısına bölerek ortalamasını alırız.
`sabit_gradyani /= len(calisma_saatleri)` | Sabit terim gradyanının da örnekler üzerindeki ortalamasını alırız.
`agirlik -= ogrenme_hizi * agirlik_gradyani` | Öğrenme hızıyla ölçeklenmiş gradyanı ağırlıktan çıkarırız; bu güncelleme çapraz entropiyi azaltmaya çalışır.
`sabit -= ogrenme_hizi * sabit_gradyani` | Aynı güncellemeyi sabit terime uygularız.
`olasiliklar = []` | Eğitimden sonra olasılık tahminlerini biriktirmek için boş liste oluştururuz.
`tahmin_edilen_siniflar = []` | Olasılıkları sınıfa çevirdikten sonra sonuçları saklayacağımız listeyi oluştururuz.
`for saat in calisma_saatleri:` | Öğrenilmiş parametrelerle her eğitim girdisi için son tahmini hesaplarız.
`olasilik = sigmoid(agirlik * saat + sabit)` | O girdinin öğrenilmiş modeldeki başarı olasılığını buluruz.
`olasiliklar.append(round(olasilik, 2))` | Olasılığı iki basamağa yuvarlayıp sonuç listesine ekleriz.
`tahmin_edilen_siniflar.append(int(olasilik >= 0.5))` | Olasılık en az `0.5` ise `True`, değilse `False` olur; `int` bunları `1` ve `0` olarak listeye ekler.
`print("Öğrenilen ağırlık:", round(agirlik, 2))` | Eğitim sonunda ayarlanan ağırlığı gösteririz.
`print("Öğrenilen sabit:", round(sabit, 2))` | Eğitim sonunda ayarlanan sabit terimi gösteririz.
`print("Tahmin olasılıkları:", olasiliklar)` | Dört örnek için modelin tahmin ettiği olasılıkları ekrana yazarız.
`print("Tahmin edilen sınıflar:", tahmin_edilen_siniflar)` | Eşik uygulandıktan sonra elde edilen `0` ve `1` sınıflarını gösteririz.
```

Bu küçük veri kümesinde model eğitim örneklerini doğru sınıflara ayırdı. Bu, yeni öğrencilerde de kesinlikle doğru tahmin yapacağını kanıtlamaz; yeni örneklerdeki başarısını ayrıca ölçmeliyiz. Olasılığı değiştirmekle sınıf kararını değiştirmek de aynı şey değildir: eşik değişirse sınıf listesi değişebilir, fakat modelin hesapladığı olasılıklar aynı kalır.

## 3. Kütüphaneyle yap

NumPy, sigmoid ve gradyan işlemlerini tek tek Python listelerinde dolaşmadan bütün örneklere uygular. Aşağıdaki kod aynı modeli ve aynı güncelleme kuralını NumPy dizileriyle eğitir. NumPy kurulumu için 2.1 dersindeki yönergeyi kullan.

```python
import numpy as np


def sigmoid(ham_puan):
    return 1 / (1 + np.exp(-ham_puan))


calisma_saatleri = np.array([1.0, 2.0, 4.0, 5.0])
gercek_etiketler = np.array([0.0, 0.0, 1.0, 1.0])
agirlik = 0.0
sabit = 0.0
ogrenme_hizi = 0.1

for adim in range(1000):
    olasiliklar = sigmoid(agirlik * calisma_saatleri + sabit)
    hatalar = olasiliklar - gercek_etiketler
    agirlik_gradyani = np.mean(hatalar * calisma_saatleri)
    sabit_gradyani = np.mean(hatalar)
    agirlik -= ogrenme_hizi * agirlik_gradyani
    sabit -= ogrenme_hizi * sabit_gradyani

print("Ağırlık:", round(agirlik, 2))
print("Sabit:", round(sabit, 2))
```
```text
Ağırlık: 2.04
Sabit: -5.73
```

NumPy kodu tarayıcıdaki Python penceresinde çalışmaz; bu çalışma alanında NumPy kurulu değildir. Kodu `lojistik_regresyon_numpy.py` adlı dosyaya kaydet ve NumPy'nin kurulu olduğu Python ortamında `python lojistik_regresyon_numpy.py` komutuyla çalıştır.

`agirlik * calisma_saatleri + sabit`, NumPy dizisindeki her çalışma saati için ham puanı hesaplar. `np.exp` sigmoidin üstel kısmını, `np.mean` ise tüm eğitim örneklerinden gelen gradyanların ortalamasını bulur. NumPy kodu daha kısa yazar; modelin matematiği değişmez.

## 4. Sık yapılan hatalar

- **Lojistik regresyonun doğrudan sınıf ürettiğini sanmak.** Önce `0` ile `1` arasında olasılık hesaplar, sonra bu olasılığı eşikle karşılaştırıp sınıf seçeriz.
- **Sigmoid sonucunu kesinlik garantisi saymak.** `0.9`, modelin bu sınıfa yüksek olasılık verdiğini gösterir; gerçek sonucun kesinlikle öyle olacağını kanıtlamaz.
- **`0` ve `1` etiketlerini sayısal büyüklük sanmak.** Bu örnekte `0` başarısız, `1` başarılı sınıfının adıdır; aralarında ölçülebilir bir “bir birim” fark yoktur.
- **Eşiğin olasılığı değiştirdiğini düşünmek.** Eşik yalnızca sınıf kararını değiştirir; modelin olasılık hesabını değiştirmez.
- **`0.5` eşiğini her görev için zorunlu kabul etmek.** Yanlış pozitif ve yanlış negatif hatalarının maliyetine göre başka eşik gerekebilir.
- **MSE'yi sınıflandırmada otomatik olarak doğru kayıp sanmak.** Bu derste sigmoid olasılıklarını gerçek etiketlerle karşılaştırmak için çapraz entropi gradyanı kullanıyoruz; 1.6 dersinde bunun nedenini görmüştün.
- **Eğitim örneklerindeki doğru sınıflandırmayı genel başarı sanmak.** Modelin daha önce görmediği örneklerde de nasıl çalıştığını ayrı veriyle ölçmek gerekir.
- **Çalışma saatinin başarıyı tek başına belirlediğini varsaymak.** Bu yalnızca yöntemi göstermek için kurulmuş basit bir örnektir; gerçek bir sınav sonucu birçok etkene bağlıdır.

## 5. Pekiştir

**Quiz**

1. Lojistik regresyonun bu dersteki amacı nedir?
2. Sigmoid ham puana ne yapar?
3. Olasılık `0.73` ve eşik `0.5` ise model hangi sınıfı seçer?
4. Eşiği değiştirmek modelin olasılık tahminlerini değiştirir mi?
5. Modelin eğitim örneklerini doğru sınıflandırması neden yeterli kanıt değildir?

**Alıştırmalar**

1. İlk pencerede `ham_puan` değerlerine `-4` ve `4` ekle. Olasılıklar hangi yöne değişiyor?
2. İkinci pencerede eşiği `0.7` yap. Hangi öğrencilerin sınıf kararı değişiyor? Olasılıkları da değişti mi?
3. Eğitim penceresinde `range(1000)` yerine `range(10)` yaz. Tahmin olasılıkları neden başlangıçtaki `0.5` değerlerine daha yakın kalıyor?
4. (İsteğe bağlı) Birinci öğrencinin etiketini `1` yap. Modelin hangi örneği öğrendiğini ve tahminlerin nasıl değiştiğini karşılaştır.
5. (İsteğe bağlı) Başarısız tahminin maliyeti yüksekse neden daha düşük bir eşik seçmek isteyebilirsin?

??? success "Quiz cevapları"
    1. Bir girdinin iki sınıftan hangisine ait olabileceğini olasılıkla tahmin edip sınıf seçmek.
    2. Ham puanı `0` ile `1` arasında bir olasılığa çevirir.
    3. Başarılı sınıfı (`1`) seçer; çünkü `0.73`, `0.5` eşiğinin üzerindedir.
    4. Hayır. Eşik yalnızca olasılığı sınıfa çevirme kararını etkiler.
    5. Yeni verideki başarısı farklı olabilir; eğitimde kullanılmayan örneklerde de ölçülmelidir.

## Özet

Lojistik regresyon önce doğrusal bir ham puan hesaplar, sigmoid ile bunu sınıf olasılığına dönüştürür ve eşikle sınıf seçer. Eğitim sırasında model, çapraz entropi gradyanını kullanarak ağırlık ve sabit terimi günceller. Bu dersteki küçük örnek yöntemin temelini gösterir; başarıyı kanıtlamak için modelin görmediği verileri de sınamak gerekir.

## Kaynaklar

- [Google Machine Learning Crash Course: Logistic regression](https://developers.google.com/machine-learning/crash-course/logistic-regression)
- [Python resmî belgesi: `math.exp`](https://docs.python.org/3/library/math.html#math.exp)
- [NumPy resmî belgesi: `exp`](https://numpy.org/doc/stable/reference/generated/numpy.exp.html)
