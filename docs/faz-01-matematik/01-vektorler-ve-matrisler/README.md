# Faz 1 – Ders 1: Vektörler ve matrisler

> ⏱️ Tahmini süre: 45-60 dk · 📚 Ön koşul: 0.2 Python hızlı tekrar · 💻 Gereksinim: Python 3.11+, ek paket yok

## Bu derste ne öğreneceksin?

- Bir vektörü sıralı sayılarla temsil etmeyi
- Vektörlerin aynı konumdaki değerleri üzerinde işlem yapmayı
- Bir matrisi satır ve sütunlardan oluşan bir tablo gibi okumayı
- Vektör ve matrisleri yapay zekâda veriyi düzenlemek için kullanmayı

## 1. Problem

Bir tahmin modeli bir evin büyüklüğü, oda sayısı ve yaşını kullanarak fiyat tahmini yapabilir. Bu bilgileri tek tek değişkenlerde tutmak küçük örnekte kolaydır; yüzlerce özellik olduğunda ise düzenli bir yapıya ihtiyaç duyarız.

Örneğin tek bir evin sayısal özelliklerini `[120, 3, 10]` biçiminde, birden fazla evin özelliklerini de satırlardan oluşan bir tabloda saklayabiliriz. Bu yapılara **vektör** ve **matris** denir.

## 2. Kendin yaz

### 2.1 Vektör: tek bir örneğin sayısal özellikleri

Vektör, sırası anlam taşıyan sayıların dizisidir. Aşağıda her konum farklı bir özelliği gösterir: önce metrekare, sonra oda sayısı, sonra bina yaşı. Sıralamayı değiştirirsen sayıların anlamı da değişir.

```python {.python-playground}
ev = [120, 3, 10]
print("Metrekare:", ev[0])
print("Oda sayısı:", ev[1])
print("Bina yaşı:", ev[2])
```
```text {.python-playground-expected}
Metrekare: 120
Oda sayısı: 3
Bina yaşı: 10
```
```text {.python-playground-help}
`ev = [120, 3, 10]` | Köşeli ayraçlar bir liste oluşturur. Bu örnekte listedeki her sayı, aynı eve ait bir özelliği sırayla temsil eder.
`ev[0]` | Python sıfırdan saydığı için `0` ilk öğenin konumudur; burada ilk özellik metrekaredir.
`ev[1]` | `1` ikinci öğenin konumudur; bu sırayı baştan belirlediğimiz için oda sayısını temsil eder.
`ev[2]` | `2` üçüncü öğeyi verir; bu örnekte bina yaşıdır.
`print("Oda sayısı:", ev[1])` | `print` açıklama metniyle seçilen değeri birlikte gösterir. Listedeki sırayı değiştirirsen hangi özelliğin yazdırıldığı da değişir.
```

`ev` Python'da bir listedir; sayısal özellikleri ve sıralarını belirli bir kuralla kullandığımızda onu vektör gibi düşünebiliriz. Gerçek uygulamalarda her konumun ne anlama geldiğini ayrıca bilmek gerekir.

### 2.2 Vektörleri aynı konumlarda toplamak

İki vektörü toplarken aynı konumdaki sayıları toplarız: ilk sayı ilk sayıyla, ikinci sayı ikinci sayıyla. Örneğin bir öğrenci matematik ve fizikten vizede `[2, 3]`, finalde `[4, 1]` ek puan almış olsun. Her dersin toplam ek puanını bulmak için matematiği matematikle, fiziği fizikle toplarız.

```python {.python-playground}
a = [2, 3]
b = [4, 1]
toplam = []

for i in range(len(a)):
    toplam.append(a[i] + b[i])

print("Toplam vektör:", toplam)
```
```text {.python-playground-expected}
Toplam vektör: [6, 4]
```
```text {.python-playground-help}
`a = [2, 3]` | İlk vektör iki sayı saklar. Listedeki ilk sayı birinci özellikle, ikinci sayı ikinci özellikle eşleşir.
`b = [4, 1]` | İkinci vektör de aynı sırada iki sayı içerir; toplama yapabilmek için iki listenin uzunluğu ve özellik sırası eşleşmelidir.
`toplam = []` | Sonuçları koyacağımız boş listeyi hazırlarız; her hesaplanan bileşen bu listeye eklenecek.
`range(len(a))` | `len(a)` iki öğe olduğunu bulur, `range` da `0` ve `1` konumlarını sırayla üretir.
`a[i] + b[i]` | Aynı konumdaki iki sayıyı toplarız; önce `2 + 4`, sonra `3 + 1` hesaplanır.
`toplam.append(a[i] + b[i])` | Bulduğumuz bileşeni sonuç listesinin sonuna ekleriz. Döngü bitince iki konum da hesaplanmış olur.
`print("Toplam vektör:", toplam)` | Sonuç listesini ekrana yazar; köşeli ayraçlar bunun birden fazla öğeli liste olduğunu gösterir.
```

`a` ile `b` listelerindeki sayıları değiştirip tekrar çalıştır. İki listenin uzunluğu aynı olmalı. Örneğin `a` daha uzunsa döngü `b` içinde olmayan bir konumu okumaya çalışır ve Python `IndexError` verir; `b` daha uzunsa sondaki fazla sayı hiç hesaba katılmaz. Her iki vektörde de aynı sayıda ve aynı sırada özellik olduğundan emin ol.

### 2.3 Matris: birden fazla örneği satırlara yerleştir

Matris, sayıları satır ve sütunlardan oluşan dikdörtgen bir düzende tutar. Aşağıdaki tabloda her satır bir evi, her sütun ise aynı özelliği gösterir:

```python {.python-playground}
evler = [
    [120, 3, 10],
    [85, 2, 5],
]

print("İlk evin oda sayısı:", evler[0][1])
print("Ev sayısı:", len(evler))
print("Özellik sayısı:", len(evler[0]))
```
```text {.python-playground-expected}
İlk evin oda sayısı: 3
Ev sayısı: 2
Özellik sayısı: 3
```
```text {.python-playground-help}
`evler = [` | Dıştaki köşeli ayraç, birden fazla satırı tutan ana listeyi başlatır.
`[120, 3, 10]` | İçteki liste bir satırdır; bu satır tek bir evin üç özelliğini aynı sırayla saklar.
`[85, 2, 5]` | İkinci satır başka bir evi temsil eder. Her satırda aynı özelliklerin aynı sırada bulunması gerekir.
`evler[0][1]` | İlk köşeli ayraç ilk satırı, ikincisi o satırdaki ikinci özelliği seçer; sonuç oda sayısı olan `3` olur.
`len(evler)` | Dış listedeki satırları sayar; burada iki ev vardır.
`len(evler[0])` | İlk satırdaki değerleri sayar; her ev için üç özellik tutulur.
```

Bu örnekte matrisin boyutu **2 satır × 3 sütun**dur. Matrisin boyutu, hangi işlemlerin yapılabileceğini belirler; örneğin her satırın aynı sayıda sütunu olmalıdır.

### Şimdi sen yaz: vektör topla, matristen seç

**Görev:** İki vektörü aynı konumlarından toplayacak ve bir matristen belirli bir sayıyı seçeceksin. Ekranda toplam vektör, matrisin boyutu ve seçtiğin sayı görünmeli.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
a = [1, 2, 3]
b = [10, 20, 30]
toplam = []

for i in range(len(a)):
    # TODO: Aynı konumdaki iki sayıyı topla ve listeye ekle.
    toplam.append(___)

matris = [[1, 2], [3, 4], [5, 6]]
# TODO: 3. satırın 2. sütunundaki sayıyı seç (konumlar 0'dan başlar).
deger = matris[___][___]

print("Toplam:", toplam)
print("Matris boyutu:", len(matris), "x", len(matris[0]))
print("Seçilen sayı:", deger)
```
```text {.python-playground-expected}
Toplam: [11, 22, 33]
Matris boyutu: 3 x 2
Seçilen sayı: 6
```
```text {.python-playground-help}
`toplam.append(___)` | `a[i]` ve `b[i]`, aynı konumdaki iki sayıdır. İkisini topla.
`matris[___][___]` | İlk ayraç satırı, ikinci ayraç sütunu seçer. Saymaya 0'dan başlanır: 3. satır için `2`, 2. sütun için `1` yaz.
```
```python {.python-playground-solution}
a = [1, 2, 3]
b = [10, 20, 30]
toplam = []

for i in range(len(a)):
    # Aynı konumdaki iki sayıyı topla ve listeye ekle.
    toplam.append(a[i] + b[i])

matris = [[1, 2], [3, 4], [5, 6]]
# 3. satırın 2. sütunundaki sayıyı seç (konumlar 0'dan başlar).
deger = matris[2][1]

print("Toplam:", toplam)
print("Matris boyutu:", len(matris), "x", len(matris[0]))
print("Seçilen sayı:", deger)
```

## 3. Kütüphaneyle yap

Python listeleri öğrenmek için yeterlidir; büyük sayısal dizilerle çalışırken **NumPy** kullanılır. NumPy, dizilerin boyutunu (`shape`) gösterir ve çok sayıda sayısal işlemi verimli biçimde yapar. Kurulum komutu terminal içindir; tarayıcıdaki çalışma alanında NumPy kurulu değildir.

```bash
python -m pip install numpy
```

Bu örneği paketi kurduktan sonra bilgisayarındaki Python dosyasında çalıştır:

```python
import numpy as np

evler = np.array([
    [120, 3, 10],
    [85, 2, 5],
])

print(evler.shape)
print(evler[0, 1])
```

`shape`, `(2, 3)` sonucuyla iki satır ve üç sütun olduğunu söyler. NumPy'de `evler[0, 1]` yazımı da ilk satırın ikinci sütununu seçer. Python listesindeki `evler[0][1]` ile aynı değeri verir.

## 4. Sık yapılan hatalar

- **İlk öğenin konumunu `1` sanmak.** Python'da ilk öğe `0` konumundadır. Bu yüzden `ev[0]` ilk özelliği seçer.
- **Özellik sırasını karıştırmak.** Bir satırda oda sayısı ikinci sıradaysa, bütün satırlarda ikinci sırada kalmalıdır.
- **Farklı uzunluktaki vektörleri toplamak.** Her bileşenin karşısında eşleşeceği bir bileşen olmalıdır; önce uzunlukları ve sıraları kontrol et.
- **Matrisin satır ve sütunlarını ters söylemek.** İç listeler satırlardır; satır sayısı dış listenin, sütun sayısı bir iç listenin uzunluğudur.
- **Her sayı listesini kendiliğinden anlamlı bir vektör sanmak.** Listeyi vektör gibi kullanmak için her konumun neyi temsil ettiğini bilmelisin.

## 5. Pekiştir

**Quiz**

1. `[8, 2, 4]` vektöründe ikinci öğenin Python konumu nedir?
2. İki vektörü bileşen bileşen toplamak için hangi koşul gerekir?
3. İki satır ve dört sütundan oluşan bir matrisin boyutu nasıl yazılır?
4. `matris[1][0]` hangi değeri seçer?

**Alıştırmalar**

1. Bir öğrencinin üç sınav notunu `[78, 85, 92]` biçiminde yaz. İlk notu ve üçüncü notu ayrı ayrı yazdır.
2. İki üç boyutlu vektörü aynı konumlardaki değerleri toplayarak birleştir.
3. Üç öğrencinin iki sınav notunu iki boyutlu bir listede sakla. İkinci öğrencinin ilk notunu yazdır.
4. (İsteğe bağlı) Bir matrisin her satırında iki sayı olduğunu doğrulayan bir kontrol yaz.

??? success "Quiz cevapları"
    1. `1`; Python saymayı sıfırdan başlatır.
    2. Uzunlukları aynı olmalı ve aynı konumlar aynı özelliği temsil etmeli.
    3. `2 × 4` (iki satır, dört sütun).
    4. İkinci satırın ilk değeri.

## Özet

Vektör, sırası anlam taşıyan sayıların dizisidir; matris ise birden fazla vektörü satırlar halinde düzenler. Python listeleri bu yapıları küçük örneklerde görmemizi sağlar. Bir vektör veya matrisle işlem yaparken uzunluk, satır-sütun boyutu ve her konumun anlamı önemlidir. NumPy, aynı fikri büyük sayısal dizilerde daha kullanışlı hale getirir.

## Kaynaklar

- [NumPy: Mutlak başlangıç rehberi](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [NumPy: Hızlı başlangıç](https://numpy.org/doc/stable/user/quickstart.html)
