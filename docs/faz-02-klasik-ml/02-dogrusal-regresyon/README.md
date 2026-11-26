# Faz 2 – Ders 2: Doğrusal regresyon

> ⏱️ Tahmini süre: 55-70 dk · 📚 Ön koşul: 0.2 Python hızlı tekrar, Faz 1 matematik dersleri, 2.1 NumPy ile veri · 💻 Gereksinim: Python 3.11+; temel örnekler ek paketsiz, NumPy örneği için NumPy kurulmalıdır

## Bu derste ne öğreneceksin?

- Sayısal bir sonucu düz çizgiyle tahmin etmeyi
- Ağırlık ve sabit terimin tahmini nasıl değiştirdiğini
- Tahmin hatasını ortalama kare hata ile ölçmeyi
- Gradyan inişiyle model parametrelerini hatayı azaltacak yönde güncellemeyi
- Küçük bir modeli Python listeleriyle yazıp aynı hesabı NumPy ile kısaltmayı

## 1. Problem

Bir ürünün kaç kilogram olduğunu bilip fiyatını tahmin etmek istediğimizi düşün. Örnek verimizde `1` kilogram ürün `2` TL, `2` kilogram ürün `4` TL ve `3` kilogram ürün `6` TL olsun. Bu değerler bilerek kolay seçildi: her bir kilogram fiyatı `2` TL artırıyor.

!!! note "İki farklı “ağırlık”"
    Bu derste **ağırlık** sözcüğü modelin parametresi anlamına gelir (İngilizcesi *weight*). Ürünün kaç kilogram olduğunu ise hep **kilogram** diye yazacağız; ikisini karıştırma.

**Doğrusal regresyon**, sayısal bir sonucu düz çizgi kullanarak tahmin eder. Tek bir girdi için çizgiyi şöyle yazarız:

`tahmin = ağırlık × girdi + sabit`

- **Girdi (`x`)**: modele verdiğimiz bilgi; burada ürünün kilogramı.
- **Ağırlık (`w`)**: girdi bir arttığında tahminin ne kadar değiştiği; burada kilogram başına fiyat.
- **Sabit terim (`b`)**: girdi `0` iken çizginin verdiği başlangıç tahmini.
- **Tahmin (`ŷ`)**: modelin hesapladığı değer; gerçek ölçüm değildir.

Model başlangıçta doğru ağırlığı ve sabit terimi bilmez. Bu sayıları değiştirerek tahminlerinin gerçek fiyatlara yaklaşmasını sağlayacağız. Önce tek tahminin nasıl hesaplandığını, sonra modelin hatasını ve bu sayıları nasıl öğrendiğini göreceğiz.

## 2. Kendin yaz

### 2.1 Çizginin tahminini hesapla

Ağırlığı `2`, sabit terimi `1` seçersek `3` kilogram için tahmin `2 × 3 + 1 = 7` olur. Bu küçük örnekte parametreleri biz veriyoruz; model henüz öğrenme yapmıyor.

```python {.python-playground}
agirlik = 2
sabit = 1
kilogram = 3

tahmin = agirlik * kilogram + sabit
print("Tahmin edilen fiyat:", tahmin, "TL")
```
```text {.python-playground-expected}
Tahmin edilen fiyat: 7 TL
```
```text {.python-playground-help}
`agirlik = 2` | Her kilogramın tahmine `2` TL eklediğini varsayarız. Bu sayı modelin ayarlayacağı parametrelerden biridir.
`sabit = 1` | Girdi sıfır olsa bile çizginin vereceği başlangıç değerini belirleriz. Bu örnekte `1` TL'dir.
`kilogram = 3` | Fiyatını tahmin edeceğimiz ürünün ağırlığını gireriz.
`tahmin = agirlik * kilogram + sabit` | Ağırlığı kilogramla çarpar, sabit değeri ekleriz: `2 × 3 + 1 = 7`.
`print("Tahmin edilen fiyat:", tahmin, "TL")` | Hesaplanan tahmini açıklamayla birlikte ekrana yazarız.
```

`agirlik` değerini değiştirince her kilogram başına eklenen tutar, `sabit` değerini değiştirince çizginin tamamının başlangıç noktası değişir. Bir sonraki adımda bu değerleri gerçek örneklere bakarak ayarlayacağız.

### 2.2 Tahmin hatasını ölç

Modelin tahmini tek başına yeterli değildir; gerçek değerle karşılaştırmalıyız. **Hata**, tahmin ile gerçek değer arasındaki farktır:

`hata = tahmin - gerçek değer`

Pozitif hata modelin yüksek, negatif hata düşük tahmin yaptığını gösterir. Hataları toplarken pozitif ve negatif değerlerin birbirini silmesini istemeyiz. Bu nedenle her hatanın karesini alır, sonra bu karelerin ortalamasını buluruz. Bu ölçüye **ortalama kare hata** (MSE) denir.

```python {.python-playground}
kilogramlar = [1, 2, 3]
gercek_fiyatlar = [2, 4, 6]
agirlik = 1
sabit = 0

tahminler = []
kareli_hatalar = []
for i in range(len(kilogramlar)):
    tahmin = agirlik * kilogramlar[i] + sabit
    hata = tahmin - gercek_fiyatlar[i]
    tahminler.append(tahmin)
    kareli_hatalar.append(hata ** 2)

ortalama_kare_hata = sum(kareli_hatalar) / len(kareli_hatalar)
print("Tahminler:", tahminler)
print("Kareli hatalar:", kareli_hatalar)
print("Ortalama kare hata:", round(ortalama_kare_hata, 2))
```
```text {.python-playground-expected}
Tahminler: [1, 2, 3]
Kareli hatalar: [1, 4, 9]
Ortalama kare hata: 4.67
```
```text {.python-playground-help}
`kilogramlar = [1, 2, 3]` | Modelin göreceği üç girdi değerini sırayla saklarız.
`gercek_fiyatlar = [2, 4, 6]` | Bu girdilere karşılık gelen ölçülmüş fiyatları aynı sırada yazarız; ilk kilogram değeri ilk fiyatla eşleşir.
`agirlik = 1` | Şimdilik her kilogram başına `1` TL tahmin ettiren bir çizgi seçeriz.
`sabit = 0` | Başlangıç tahminine ek bir değer koymayız; böylece tahmin yalnızca kilogramla ağırlığın çarpımı olur.
`tahminler = []` | Modelin her girdi için hesaplayacağı tahminleri biriktirmek için boş liste açarız.
`kareli_hatalar = []` | Tahmin ile gerçek değer arasındaki farkların karelerini burada saklarız.
`for i in range(len(kilogramlar)):` | `i`, `0`, `1`, `2` konumlarını sırayla alır. Aynı konumdaki kilogram ve fiyat bir örneğe aittir.
`tahmin = agirlik * kilogramlar[i] + sabit` | O örnek için çizginin tahminini hesaplarız. İlk girdide `1 × 1 + 0 = 1` çıkar.
`hata = tahmin - gercek_fiyatlar[i]` | Tahminden gerçek fiyatı çıkarırız. İlk örnekte `1 - 2 = -1`; model fiyatı bir birim düşük tahmin etmiştir.
`tahminler.append(tahmin)` | Bulduğumuz tahmini sonuç listesine ekleriz.
`kareli_hatalar.append(hata ** 2)` | Hatayı kendisiyle çarpıp listeye ekleriz. Örneğin `(-1) ** 2 = 1`; böylece eksi işaret kaybolur.
`ortalama_kare_hata = sum(kareli_hatalar) / len(kareli_hatalar)` | Kareli hataları toplar ve örnek sayısına böleriz: `(1 + 4 + 9) / 3`, yaklaşık `4.67` eder.
`print("Tahminler:", tahminler)` | Üç girdi için modelin ürettiği değerleri gösteririz.
`print("Kareli hatalar:", kareli_hatalar)` | Her hatanın karesini gösteririz.
`print("Ortalama kare hata:", round(ortalama_kare_hata, 2))` | MSE değerini virgülden sonra iki basamakla gösteririz. Bu değer küçüldükçe, bu örneklerdeki tahminler genellikle gerçeğe yaklaşır.
```

Bu örnekte doğru fiyatlar bilerek `2 × kilogram` olarak seçildi; gerçek hayattaki veriler bu kadar kusursuz bir çizgi üzerinde olmayabilir. MSE, modelin seçilen örneklerde ne kadar yanıldığını özetler; tek başına tahminlerin her yeni üründe doğru olacağını garanti etmez.

### 2.3 Gradyan inişiyle ağırlıkları öğren

Şimdi başlangıçta `agirlik` ve `sabit` değerlerini `0` seçelim. Model her örnekte bir tahmin yapar, hatayı bulur ve bu hatanın ortalama kare hatayı hangi yönde değiştirdiğini hesaplar. Bu değişim bilgisine **gradyan** denir. Gradyan inişi, parametreleri kaybı azaltmaya çalışacak yönde küçük adımlarla günceller. Türev ve gradyan fikrini 1.3 dersinde görmüştün.

MSE için bu örnekte kullandığımız gradyanlar şunlardır:

`ağırlık gradyanı = (2 / örnek sayısı) × Σ(hata × girdi)`

`sabit gradyanı = (2 / örnek sayısı) × Σ(hata)`

`Σ`, her örnekten gelen parçaları toplamak demektir. Ağırlık gradyanında hatayı girdiyle de çarparız; çünkü ağırlık bir miktar değişince tahmin, girdinin büyüklüğüne bağlı olarak değişir. Sabit terim ise tüm tahminleri aynı miktarda kaydırdığı için onun gradyanında yalnızca hataları toplarız.

```python {.python-playground}
kilogramlar = [1.0, 2.0, 3.0]
gercek_fiyatlar = [2.0, 4.0, 6.0]
agirlik = 0.0
sabit = 0.0
ogrenme_hizi = 0.05

for adim in range(1000):
    agirlik_gradyani = 0.0
    sabit_gradyani = 0.0

    for i in range(len(kilogramlar)):
        tahmin = agirlik * kilogramlar[i] + sabit
        hata = tahmin - gercek_fiyatlar[i]
        agirlik_gradyani += 2 * hata * kilogramlar[i]
        sabit_gradyani += 2 * hata

    agirlik_gradyani /= len(kilogramlar)
    sabit_gradyani /= len(kilogramlar)
    agirlik -= ogrenme_hizi * agirlik_gradyani
    sabit -= ogrenme_hizi * sabit_gradyani

tahminler = []
for kilogram in kilogramlar:
    tahminler.append(round(agirlik * kilogram + sabit, 2))

print("Öğrenilen ağırlık:", round(agirlik, 2))
print("Öğrenilen sabit:", round(sabit, 2))
print("Tahminler:", tahminler)
```
```text {.python-playground-expected}
Öğrenilen ağırlık: 2.0
Öğrenilen sabit: 0.0
Tahminler: [2.0, 4.0, 6.0]
```
```text {.python-playground-help}
`kilogramlar = [1.0, 2.0, 3.0]` | Üç örneğin girdilerini saklarız. Ondalıklı yazım, hesap sırasında değerlerin kayan noktalı sayı olacağını açıkça gösterir.
`gercek_fiyatlar = [2.0, 4.0, 6.0]` | Her girdiye karşılık gelen gerçek fiyatları aynı sırada tutarız.
`agirlik = 0.0` | Modelin başlangıç ağırlığını sıfır seçeriz; model henüz veriye göre ayarlanmamıştır.
`sabit = 0.0` | Çizginin başlangıç sabitini de sıfırdan başlatırız.
`ogrenme_hizi = 0.05` | Her güncellemede gradyanın ne kadarının uygulanacağını seçeriz. Çok büyük değer modelin hedefi aşmasına, çok küçük değer ise öğrenmenin yavaşlamasına yol açabilir.
`for adim in range(1000):` | Parametreleri 1000 kez güncelleriz. `adim` güncellemenin kaçıncı tekrar olduğunu gösterir.
`agirlik_gradyani = 0.0` | Bu turdaki örneklerden ağırlık gradyanını toplayacağımız değişkeni sıfırdan başlatırız.
`sabit_gradyani = 0.0` | Sabit terimin gradyanını da her turda yeniden sıfırdan toplarız; önceki turun toplamını taşımayız.
`for i in range(len(kilogramlar)):` | Her güncelleme turunda üç örneği de birer birer inceleriz.
`tahmin = agirlik * kilogramlar[i] + sabit` | O anki ağırlık ve sabit değerleriyle, seçili örneğin fiyatını tahmin ederiz.
`hata = tahmin - gercek_fiyatlar[i]` | Tahminin gerçek fiyattan ne kadar ve hangi yönde saptığını buluruz.
`agirlik_gradyani += 2 * hata * kilogramlar[i]` | Hatanın ağırlık üzerindeki etkisini girdiyle çarpıp toplama ekleriz. Büyük girdilerde ağırlık değişikliği tahmini daha fazla etkiler.
`sabit_gradyani += 2 * hata` | Hatanın sabit terim üzerindeki etkisini toplarız; sabit değişince bütün tahminler aynı miktarda kayar.
`agirlik_gradyani /= len(kilogramlar)` | Toplamı örnek sayısına bölerek ortalama gradyanı buluruz. `2` katsayısı, kare alma işleminin türevinden gelir.
`sabit_gradyani /= len(kilogramlar)` | Sabit terim için toplanan gradyanı da örnek sayısına böleriz.
`agirlik -= ogrenme_hizi * agirlik_gradyani` | Ağırlığı gradyanın ters yönünde güncelleriz. `-=` mevcut değerden öğrenme hızıyla ölçeklenmiş gradyanı çıkarıp sonucu aynı değişkende saklar.
`sabit -= ogrenme_hizi * sabit_gradyani` | Aynı güncellemeyi çizginin sabit terimine uygularız.
`tahminler = []` | Öğrenme tamamlandıktan sonra son tahminleri saklamak için yeni, boş bir liste açarız.
`for kilogram in kilogramlar:` | Her girdi için öğrenilmiş çizginin tahminini yeniden hesaplarız.
`tahminler.append(round(agirlik * kilogram + sabit, 2))` | Öğrenilmiş ağırlık ve sabitle tahmin yapar, sonucu iki basamağa yuvarlayıp listeye ekleriz.
`print("Öğrenilen ağırlık:", round(agirlik, 2))` | Veriye göre ayarlanmış ağırlığı gösteririz; bu örnekte yaklaşık `2` olur.
`print("Öğrenilen sabit:", round(sabit, 2))` | Ayarlanmış sabit terimi gösteririz; bu örnekte yaklaşık `0` olur.
`print("Tahminler:", tahminler)` | Öğrenilmiş çizginin üç örnek için son tahminlerini gösteririz.
```

Bu veri bilerek tam doğrusal seçildiği için çizgi yaklaşık `y = 2x` olur. Gerçek veride noktalar çizginin tam üzerinde bulunmaz; amaç her noktayı kusursuz yakalamak değil, genel eğilimi iyi açıklayan parametreleri bulmaktır. `ogrenme_hizi` veya veri değerlerini değiştirirsen beklenen çıktı da değişir; bu, tek başına kodun bozulduğu anlamına gelmez.

### Şimdi sen yaz: tahmin ve hata

Doğrusal modelin tahminini ve ortalama kare hatasını hesapla. Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur, sonra çalıştır.

```python {.python-playground-task}
kilogramlar = [1, 2, 3]
gercek_fiyatlar = [3, 5, 7]
agirlik = 2
sabit = 0

kareli_hatalar = []
for i in range(len(kilogramlar)):
    # TODO: Tahmin = ağırlık × kilogram + sabit.
    tahmin = ___
    # TODO: Hata = tahmin - gerçek fiyat.
    hata = ___
    kareli_hatalar.append(hata ** 2)

print("Kareli hatalar:", kareli_hatalar)
print("Ortalama kare hata:", sum(kareli_hatalar) / len(kareli_hatalar))
```
```text {.python-playground-expected}
Kareli hatalar: [1, 1, 1]
Ortalama kare hata: 1.0
```
```text {.python-playground-help}
`tahmin = ___` | Doğru çizginin formülü: ağırlık × girdi + sabit. Girdi `kilogramlar[i]`.
`hata = ___` | Hata, tahmin ile gerçek değer arasındaki farktır. Burada `tahmin - gercek_fiyatlar[i]`.
```
```python {.python-playground-solution}
kilogramlar = [1, 2, 3]
gercek_fiyatlar = [3, 5, 7]
agirlik = 2
sabit = 0

kareli_hatalar = []
for i in range(len(kilogramlar)):
    # Tahmin = ağırlık × kilogram + sabit.
    tahmin = agirlik * kilogramlar[i] + sabit
    # Hata = tahmin - gerçek fiyat.
    hata = tahmin - gercek_fiyatlar[i]
    kareli_hatalar.append(hata ** 2)

print("Kareli hatalar:", kareli_hatalar)
print("Ortalama kare hata:", sum(kareli_hatalar) / len(kareli_hatalar))
```

## 3. Kütüphaneyle yap

NumPy, aynı hesabı sayıları tek tek döngüyle dolaşmadan yazmamızı sağlar. Aşağıdaki kod önceki bölümdeki gradyan inişini NumPy dizileriyle uygular. NumPy kurulumu ve dizilerin temel kullanımı için 2.1 dersine bak.

```python
import numpy as np

kilogramlar = np.array([1.0, 2.0, 3.0])
gercek_fiyatlar = np.array([2.0, 4.0, 6.0])
agirlik = 0.0
sabit = 0.0
ogrenme_hizi = 0.05

for adim in range(1000):
    tahminler = agirlik * kilogramlar + sabit
    hatalar = tahminler - gercek_fiyatlar
    agirlik_gradyani = 2 * np.mean(hatalar * kilogramlar)
    sabit_gradyani = 2 * np.mean(hatalar)
    agirlik -= ogrenme_hizi * agirlik_gradyani
    sabit -= ogrenme_hizi * sabit_gradyani

print("Ağırlık:", round(agirlik, 2))
print("Sabit:", round(sabit, 2))
```

Beklenen çıktı:

```text
Ağırlık: 2.0
Sabit: 0.0
```

`np.array(...)` listeleri NumPy dizisine çevirir. Döngünün her turunda model tüm girdiler için tahmin ve hata hesaplar; dizi işlemleri aynı konumdaki değerleri birlikte işler. `np.mean` gradyan değerlerinin ortalamasını bulur, `-=` ise ağırlık ve sabit terimi bu ortalama gradyanla günceller. Böylece önceki bölümdeki hesabı daha kısa yazarız; yapılan matematik değişmez.

NumPy kodu tarayıcıdaki Python penceresinde çalışmaz; çünkü bu çalışma alanında NumPy kurulu değildir. 2.1 dersindeki kurulum adımını uygula, bu kodu `dogrusal_regresyon_numpy.py` adıyla kaydet ve dosyanın bulunduğu klasörde `python dogrusal_regresyon_numpy.py` komutuyla çalıştır.

## 4. Sık yapılan hatalar

- **Regresyonu sınıflandırmayla karıştırmak.** Bu model bir sayı, örneğin fiyat tahmin eder. “Kedi mi köpek mi?” gibi sınıf seçmek farklı bir problemdir.
- **Ağırlığı gerçek fiyat sanmak.** Ağırlık, girdideki bir birim artışın tahmini ne kadar değiştirdiğini belirler; tahmin edilen sonucun kendisi değildir.
- **Sabit terimi atlamak.** Sabit terim sıfır değilse çizgi başlangıçta orijinden geçmek zorunda değildir.
- **Tahmin ile gerçeği ters çıkarmak.** Burada hata `tahmin - gerçek` olarak tanımlanır. Tersini seçmek de başka formüllerle mümkündür; ancak gradyan güncellemesiyle işaretlerin tutarlı olması gerekir.
- **Hataları kare almadan toplamak.** Pozitif ve negatif hatalar birbirini silebilir; MSE her hatanın karesini alır.
- **MSE'yi doğrudan para birimi sanmak.** Hata karelendiği için MSE'nin birimi de fiyat biriminin karesidir; onu fiyat gibi yorumlama.
- **Gradyanı ağırlıktan çıkarmak yerine eklemek.** Bu dersteki gradyan yönü kaybın arttığı yönü gösterir; azaltmaya çalışırken öğrenme hızıyla çarpıp parametreden çıkarırız.
- **Öğrenme hızını aşırı büyük seçmek.** Parametreler doğru değerin çevresinde zıplayabilir veya uzaklaşabilir. Küçük adımlarla başla ve kaybın nasıl değiştiğini izle.
- **Az sayıda örnekte iyi sonucu her yerde doğru sanmak.** Modelin bu eğitim örneklerini iyi açıklaması, yeni verilerde aynı başarıyı garanti etmez; bunu sonraki derslerde ayrı veri kümeleriyle inceleyeceğiz.

## 5. Pekiştir

**Quiz**

1. Doğrusal regresyon hangi tür değerleri tahmin etmek için kullanılır?
2. `agirlik` ve `sabit` tahmini nasıl etkiler?
3. Tahmin `7`, gerçek değer `10` ise hata (`tahmin - gerçek`) kaçtır ve ne anlatır?
4. Hataların karelerini almamızın bir nedeni nedir?
5. Gradyan inişinde öğrenme hızı neyi belirler?

**Alıştırmalar**

1. İlk pencerede ağırlığı `3`, sabiti `2` yap. `3` kilogram için tahminin neden `11` olduğunu açıkla.
2. MSE penceresinde ağırlığı `2`, sabiti `0` yap. Tahminler gerçek fiyatlarla eşleştiğinde MSE kaç olmalı?
3. Gradyan inişi penceresinde `range(1000)` değerini `range(10)` yap. Ağırlık yaklaşık `1.71`, sabit yaklaşık `0.65` çıkar. Parametreler neden hedefe daha az yaklaştı?
4. (İsteğe bağlı) Gerçek fiyatları `[3, 5, 7]` yap. Öğrenilen ağırlık ve sabit nasıl değişir?
5. (İsteğe bağlı) MSE penceresinde `hata = tahmin - gercek_fiyatlar[i]` satırındaki çıkarma sırasını değiştir. Hata işaretleri değişse de kareli hataların neden aynı kaldığını açıkla.

??? success "Quiz cevapları"
    1. Fiyat veya uzunluk gibi sayısal sonuçları tahmin etmek için.
    2. Ağırlık, girdi bir birim artınca tahminin ne kadar değiştiğini belirler. Sabit terim, girdi sıfırken tahmini ve çizginin başlangıç noktasını belirler.
    3. `7 - 10 = -3`; model gerçek değerden `3` birim düşük tahmin etmiştir.
    4. Negatif ve pozitif hataların birbirini silmesini önler ve büyük hataları daha fazla cezalandırır.
    5. Her güncellemede gradyan yönünde atılacak adımın büyüklüğünü belirler.

## Özet

Doğrusal regresyon, bir girdi ile sayısal sonuç arasındaki ilişkiyi ağırlık ve sabit terimle tanımlanan bir çizgiyle tahmin eder. MSE, tahminlerle gerçek değerler arasındaki kareli farkların ortalamasıdır. Gradyan inişi, bu hatayı azaltmak için ağırlık ve sabit terimi küçük adımlarla günceller. Modelin eğitim örneklerindeki başarısı yeni verilerde doğru tahmin yapacağını tek başına garanti etmez.

## Kaynaklar

- [Google Machine Learning Crash Course: Linear regression](https://developers.google.com/machine-learning/crash-course/linear-regression)
- [NumPy resmî belgesi: `mean`](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)
- [NumPy resmî belgesi: `ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html)
