# Faz 2 – Ders 1: NumPy ile veri

> ⏱️ Tahmini süre: 40-55 dk · 📚 Ön koşul: 0.2 Python hızlı tekrar, 1.1 Vektörler ve matrisler, 1.2 Matris çarpımı · 💻 Gereksinim: Python 3.11+; etkileşimli örnekler ek paketsiz, NumPy örneği için NumPy kurulmalıdır

## Bu derste ne öğreneceksin?

- Bir listede aynı sıradaki sayıları döngüyle eşleştirmeyi
- Dilimleme ile listenin belirli bir bölümünü seçmeyi
- NumPy dizilerinde işlemlerin nasıl topluca uygulandığını görmeyi
- Yayınlama (broadcasting) ile tek bir sayının dizi elemanlarına nasıl uygulandığını anlamayı

## 1. Problem

Bir grup öğrencinin sınav notlarına herkese aynı ek puanı vermek istediğini düşün. Üç kişi varsa bunu tek tek yapmak kolaydır; binlerce sayı olduğunda ise her değer için ayrı satır yazmak hem yorucu hem hata yapmaya açıktır.

Python listeleri veriyi küçük örneklerde düzenlemek için kullanışlıdır. Ancak iki listeyi `+` ile toplamak sayılarını eşleştirmez; listeleri arka arkaya ekler. **NumPy**, sayısal veriler için tasarlanmış bir Python kütüphanesidir. Bir NumPy dizisindeki sayıları tek işlemle eşleştirebilir, bir bölümünü seçebilir ve aynı sayıyı bütün elemanlara uygulayabiliriz.

1.1 dersinde NumPy dizisi oluşturmayı ve `shape` değerini, 1.2 dersinde de `@` ile matris çarpımını gördün. Bu derste aynı konuları baştan anlatmak yerine, aynı konumdaki değerleri toplama, dilimleme ve yayınlama üzerinde duracağız. Önce temel fikri Python listeleriyle yazıp sonra NumPy'deki kısa karşılığını göreceğiz.

## 2. Kendin yaz

### 2.1 Aynı sıradaki sayıları topla

İki listedeki aynı konumda duran sayılar birbirine karşılık gelsin. Örneğin ilk listedeki ilk nota ikinci listedeki ilk ek puanı ekleriz. Listelerin aynı uzunlukta olması gerekir; aksi hâlde bir listedeki sayı için eşleşecek başka bir sayı bulamayız.

```python {.python-playground}
sinav_notlari = [60, 70, 80]
ek_puanlar = [5, 10, 15]
son_notlar = []

for i in range(len(sinav_notlari)):
    yeni_not = sinav_notlari[i] + ek_puanlar[i]
    son_notlar.append(yeni_not)

print("Son notlar:", son_notlar)
```
```text {.python-playground-expected}
Son notlar: [65, 80, 95]
```
```text {.python-playground-help}
`sinav_notlari = [60, 70, 80]` | Üç öğrencinin sınav notunu sırayla saklarız. İlk sayı birinci öğrencinin notudur.
`ek_puanlar = [5, 10, 15]` | Aynı üç öğrenci için eklenecek puanları aynı sırada tutarız; ilk ek puan ilk nota aittir.
`son_notlar = []` | Hesapladığımız yeni notları biriktirmek için boş liste oluştururuz.
`for i in range(len(sinav_notlari)):` | `len` listedeki sayı adedini, yani `3`'ü bulur. `range(3)`, sırayla `0`, `1`, `2` konumlarını verir.
`yeni_not = sinav_notlari[i] + ek_puanlar[i]` | Aynı konumdaki notla ek puanı toplarız. İlk turda `60 + 5 = 65` hesaplanır.
`son_notlar.append(yeni_not)` | Bulduğumuz sonucu listenin sonuna ekleriz; döngü bitince üç yeni not da bu listede bulunur.
`print("Son notlar:", son_notlar)` | Hesapladığımız yeni not listesini ekrana yazarız.
```

Burada `i`, listenin konum numarasıdır ve Python'da sayım `0`'dan başlar. İlk tur `i = 0`, ikinci tur `i = 1`, üçüncü tur `i = 2` olur. Döngü, her turda aynı konumdaki not ve ek puanı eşleştirir.

### 2.2 Dilimleme: listenin bir bölümünü seç

Bir listenin yalnızca bazı elemanlarını almak için dilimleme kullanabiliriz. Aşağıdaki listede `[1:4]`, `1` numaralı konumdan başlar ve `4` numaralı konuma gelmeden durur. Başlangıç konumu seçime dahildir, bitiş konumu dahil değildir.

```python {.python-playground}
gunluk_sicakliklar = [17, 19, 21, 24, 23]
secilen_sicakliklar = gunluk_sicakliklar[1:4]

print("Bütün sıcaklıklar:", gunluk_sicakliklar)
print("Seçilen bölüm:", secilen_sicakliklar)
```
```text {.python-playground-expected}
Bütün sıcaklıklar: [17, 19, 21, 24, 23]
Seçilen bölüm: [19, 21, 24]
```
```text {.python-playground-help}
`gunluk_sicakliklar = [17, 19, 21, 24, 23]` | Beş günün sıcaklıklarını sırayla listede tutarız. İlk gün `0`, ikinci gün `1` konumundadır.
`gunluk_sicakliklar[1:4]` | `1` numaralı konumdan başlarız ama `4` numaralı konumu almayız. Bu yüzden `19`, `21` ve `24` seçilir.
`secilen_sicakliklar = gunluk_sicakliklar[1:4]` | Seçtiğimiz üç değeri yeni bir listeye kaydederiz; ilk liste değişmeden kalır.
`print("Bütün sıcaklıklar:", gunluk_sicakliklar)` | Kaynak listenin tamamını gösteririz.
`print("Seçilen bölüm:", secilen_sicakliklar)` | Dilimlemenin oluşturduğu yeni listeyi gösteririz.
```

Dilimlemede bitiş konumunun seçime girmemesi özellikle önemlidir. Örneğin `[2:5]`, `2`, `3` ve `4` konumlarını seçer. Aynı dilimleme yazımı NumPy'nin tek boyutlu dizilerinde de kullanılır.

### Şimdi sen yaz: ortalama ve dilimleme

İki sınavın ortalamasını bul ve ortadaki iki değeri dilimle seç. Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur, sonra çalıştır.

```python {.python-playground-task}
sinav1 = [60, 70, 80, 90]
sinav2 = [70, 75, 85, 95]
ortalamalar = []

for i in range(len(sinav1)):
    # TODO: İki sınavın aynı konumdaki notlarının ortalamasını bul.
    ortalamalar.append(___)

# TODO: Dilimle ortalamalar listesinden yalnızca 2. ve 3. öğeyi seç.
ortadakiler = ortalamalar[___:___]

print("Ortalamalar:", ortalamalar)
print("Ortadakiler:", ortadakiler)
```
```text {.python-playground-expected}
Ortalamalar: [65.0, 72.5, 82.5, 92.5]
Ortadakiler: [72.5, 82.5]
```
```text {.python-playground-help}
`ortalamalar.append(___)` | Aynı konumdaki iki notu topla ve `2`'ye böl.
`ortalamalar[___:___]` | Saymaya 0'dan başlanır: 2. öğe `1`, 3. öğe `2` konumundadır. Bitiş dahil olmadığı için bitişe `3` yaz.
```
```python {.python-playground-solution}
sinav1 = [60, 70, 80, 90]
sinav2 = [70, 75, 85, 95]
ortalamalar = []

for i in range(len(sinav1)):
    # İki sınavın aynı konumdaki notlarının ortalamasını bul.
    ortalamalar.append((sinav1[i] + sinav2[i]) / 2)

# Dilimle ortalamalar listesinden yalnızca 2. ve 3. öğeyi seç.
ortadakiler = ortalamalar[1:3]

print("Ortalamalar:", ortalamalar)
print("Ortadakiler:", ortadakiler)
```

## 3. Kütüphaneyle yap

NumPy dizisi (`array`), sayısal verileri düzenli biçimde saklar ve aynı işlemi bütün elemanlara uygular. NumPy'yi ilk kez kullanıyorsan bilgisayarındaki Python ortamına kur:

```bash
python -m pip install numpy
```

Sonra aşağıdaki kodu `numpy_veri.py` adlı dosyaya kaydet ve dosyanın bulunduğu klasörde `python numpy_veri.py` komutuyla çalıştır:

```python
import numpy as np

sinav_notlari = np.array([60, 70, 80])
ek_puanlar = np.array([5, 10, 15])

print("Son notlar:", sinav_notlari + ek_puanlar)
print("Beş puan eklenmiş notlar:", sinav_notlari + 5)
print("İkinci ve üçüncü not:", sinav_notlari[1:3])
print("Dizinin boyutu:", sinav_notlari.shape)
```

Beklenen çıktı:

```text
Son notlar: [65 80 95]
Beş puan eklenmiş notlar: [65 75 85]
İkinci ve üçüncü not: [70 80]
Dizinin boyutu: (3,)
```

`np.array(...)`, Python listesindeki sayıları NumPy dizisine dönüştürür. Aynı uzunluktaki iki diziyi `+` ile topladığımızda karşılıklı konumlardaki sayılar toplanır. Bir diziye tek sayı eklediğimizde NumPy o sayıyı her elemana uygular; buna **yayınlama (broadcasting)** denir. `shape` olan `(3,)`, dizide bir boyut ve üç eleman bulunduğunu belirtir.

NumPy kodu ek paket gerektirdiği için bu sayfadaki tarayıcı çalışma pencerelerinde çalışmaz. Buradaki ilk iki pencere, aynı eşleştirme ve dilimleme fikirlerini Python listeleriyle denetmene yarar; NumPy örneğini kendi bilgisayarında çalıştırabilirsin. NumPy dizilerinde `*` aynı konumlardaki elemanları çarpar; matris çarpımı için önceki derste gördüğümüz `@` kullanılır.

## 4. Sık yapılan hatalar

- **Python listelerini `+` ile sayısal olarak toplamak.** `[60, 75] + [5, 10]`, `[65, 85]` değil `[60, 75, 5, 10]` sonucunu verir; listeler arka arkaya eklenir. Sayıları eşleştirmek için döngü kullan veya NumPy dizilerini topla.
- **İki listeyi yanlış sırada eşleştirmek.** Aynı konumdaki değerler aynı kişiye ait olmalıdır; önce listelerin sırasını ve uzunluğunu kontrol et.
- **Dilimlemede bitiş konumunu dahil sanmak.** `[1:4]`, `1`, `2` ve `3` konumlarını alır; `4` numaralı konumu almaz.
- **NumPy'de `*` işlecini matris çarpımı sanmak.** `*` elemanları aynı konumda çarpar; matris çarpımında `@` kullanılır.
- **Her NumPy dizisi işleminin uyumlu olduğunu sanmak.** İki dizinin şekilleri eşleşmiyorsa NumPy onları toplayamaz. `ValueError: operands could not be broadcast together` hatası, dizilerin boyutlarının bu işlem için uyumlu olmadığını söyler; şekilleri ve eleman sayılarını kontrol et.
- **Yayınlamanın her boyut uyumsuzluğunu çözeceğini sanmak.** Tek bir sayı diziye uygulanabilir; fakat farklı uzunluktaki iki dizi kendiliğinden eşleşmez.
- **`shape` değerini eleman sayısıyla karıştırmak.** `(3,)` bir boyutlu dizide üç eleman olduğunu söyler; iki boyutlu `(2, 3)` dizi ise iki satır ve üç sütun içerir.

## 5. Pekiştir

**Quiz**

1. Python'da `[1, 2] + [3, 4]` işlemi ne yapar?
2. `[1:4]` dilimlemesinde hangi konumlar seçilir?
3. NumPy'de aynı şekle sahip iki dizinin `+` işlemi ne yapar?
4. NumPy'de tek bir sayıyı bir dizinin bütün elemanlarına uygulamak ne olarak adlandırılır?
5. NumPy'de eleman bazlı çarpma ile matris çarpımında hangi işleçler kullanılır?

**Alıştırmalar**

1. İlk penceredeki ek puanları `[2, 3, 4]` yap. Her yeni notu elle kontrol et.
2. Sıcaklık penceresinde `[0:2]` ve `[3:5]` dilimlerini dene. Hangi günlerin seçildiğini konum numaralarını kullanarak açıkla.
3. NumPy kodunda `sinav_notlari + 5` satırını `sinav_notlari * 2` yap. Her not neden iki katına çıkar?
4. (İsteğe bağlı) NumPy örneğinde `sinav_notlari.shape` çıktısının `(3,)` olması ne anlatıyor?

??? success "Quiz cevapları"
    1. İki listeyi birleştirerek `[1, 2, 3, 4]` sonucunu üretir; aynı konumdaki sayıları toplamaz.
    2. `1`, `2` ve `3` konumlarını seçer; bitiş olan `4` dahil değildir.
    3. Aynı konumdaki elemanları toplar ve yeni bir dizi üretir.
    4. Yayınlama (broadcasting).
    5. Eleman bazlı çarpma için `*`, matris çarpımı için `@`.

## Özet

Python listeleri küçük örneklerde veriyi saklamaya ve döngüyle işlemeye yeter. NumPy dizileri aynı türden sayısal veriler üzerinde toplu işlemleri, dilimlemeyi ve bir sayının tüm elemanlara uygulanmasını kolaylaştırır. Dilimlemede başlangıç konumu alınır, bitiş konumu alınmaz. NumPy'de `*` eleman bazlı çarpma, `@` ise matris çarpımı yapar; işlemden önce dizilerin şekillerinin uyumlu olduğundan emin olmak gerekir.

## Kaynaklar

- [NumPy resmî belgesi: Mutlak başlangıç rehberi](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [NumPy resmî belgesi: Hızlı başlangıç](https://numpy.org/doc/stable/user/quickstart.html)
