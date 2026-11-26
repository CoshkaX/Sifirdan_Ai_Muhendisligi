# Faz 1 – Ders 2: Matris çarpımı

> ⏱️ Tahmini süre: 50-65 dk · 📚 Ön koşul: 1.1 Vektörler ve matrisler · 💻 Gereksinim: Python 3.11+, ek paket yok

## Bu derste ne öğreneceksin?

- Bir satır ile bir sütunun çarpımından nasıl tek sayı çıktığını
- Matris çarpımında satır ve sütunların nasıl eşleştiğini
- Çarpımın yapılabilmesi için gereken boyut koşulunu
- Aynı işlemi NumPy ile nasıl kısa biçimde yazacağını

## 1. Problem

Bir model, her ev için üç özelliği (metrekare, oda sayısı ve yaş) kullanarak tek bir puan üretmek istesin. Her özelliğin etkisi farklı olabilir. Örneğin metrekarenin katsayısı `2`, oda sayısının katsayısı `10`, yaşın katsayısı `-1` olsun.

Bir evin özelliklerini `[100, 3, 5]`, katsayıları da `[2, 10, -1]` olarak yazarsak puan şöyle bulunur:

`100 × 2 + 3 × 10 + 5 × (-1) = 225`

Bu işlem **noktasal çarpım**dır (iç çarpım veya *dot product* olarak da geçer). Matris çarpımı, bu hesabı satır ve sütunlar üzerinde düzenli biçimde tekrarlar.

## 2. Kendin yaz

### 2.1 İki vektörün noktasal çarpımı

Noktasal çarpımda aynı konumdaki sayıları çarpar, çarpımları toplarız. Sonuç yeni bir liste değil, tek bir sayıdır.

```python {.python-playground}
ozellikler = [100, 3, 5]
katsayilar = [2, 10, -1]
puan = 0

for i in range(len(ozellikler)):
    puan += ozellikler[i] * katsayilar[i]

print("Puan:", puan)
```
```text {.python-playground-expected}
Puan: 225
```
```text {.python-playground-help}
`ozellikler = [100, 3, 5]` | Bir evin üç sayısal özelliğini belirli sırayla saklarız; her konum bir katsayıyla eşleşecek.
`katsayilar = [2, 10, -1]` | Her özelliğin puana etkisini aynı sırada yazarız; ilk katsayı ilk özellikle çarpılır.
`puan = 0` | Toplamı biriktireceğimiz başlangıç değeridir; henüz hiçbir çarpım eklenmediği için sıfırdan başlarız.
`range(len(ozellikler))` | Özellik listesindeki üç konumu, `0`, `1` ve `2` olarak sırayla üretir.
`ozellikler[i] * katsayilar[i]` | Aynı konumdaki özelliği ve katsayıyı çarpar; her özellik kendi katsayısıyla eşleşir.
`puan += ozellikler[i] * katsayilar[i]` | Bulduğumuz çarpımı önceki puana ekler. `+=` toplama yapıp sonucu yine `puan` değişkenine kaydeder.
`print("Puan:", puan)` | Döngü tamamlanınca üç çarpımın toplamını gösterir; bu örnekte sonuç `225` olur.
```

İki listenin uzunluğu aynı olmalı; yoksa bazı özelliklerin eşleşen katsayısı bulunmaz. Bir özelliğin katsayısını değiştirip puanın nasıl etkilendiğini dene.

### 2.2 İki matrisi çarp

Birinci matrisin her satırı bir örneğin özelliklerini, ikinci matrisin sütunları ise katsayı gruplarını içerebilir. Her sonuç hücresi, birinci matrisin bir satırı ile ikinci matrisin bir sütununun noktasal çarpımıdır.

Uyumsuz boyutta işlem yapmayı durdurmak için `raise ValueError(...)` kullanacağız. `raise`, anlaşılır bir hata üretip işlemi durdurur. Hatanın beklenen bir durum olduğunu denetlemek için `try` içine işlemi, `except ValueError` içine de hata oluştuğunda çalışacak kodu yazarız; hata oluşmazsa `else` bölümü çalışır. Burada bu yapıyı, hatalı boyutun sessizce yanlış sonuç üretmediğini göstermek için kullanıyoruz.

```python {.python-playground}
def matris_carp(a, b):
    if not a or not b:
        raise ValueError("Matrisler boş olamaz.")

    a_sutun_sayisi = len(a[0])
    b_sutun_sayisi = len(b[0])
    for satir in a:
        if len(satir) != a_sutun_sayisi:
            raise ValueError("a matrisi dikdörtgen olmalı.")
    for satir in b:
        if len(satir) != b_sutun_sayisi:
            raise ValueError("b matrisi dikdörtgen olmalı.")
    if a_sutun_sayisi != len(b):
        raise ValueError("a matrisinin sütun sayısı b matrisinin satır sayısına eşit olmalı.")

    sonuc = []
    for satir in a:
        yeni_satir = []
        for sutun_no in range(len(b[0])):
            toplam = 0
            for k in range(len(b)):
                toplam += satir[k] * b[k][sutun_no]
            yeni_satir.append(toplam)
        sonuc.append(yeni_satir)
    return sonuc


a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]
print(matris_carp(a, b))

try:
    matris_carp([[1, 2, 3]], [[1, 2], [3, 4]])
except ValueError as hata:
    print("Boyut kontrolü testi:", type(hata).__name__)
else:
    print("Boyut kontrolü testi: hata oluşmadı")
```
```text {.python-playground-expected}
[[19, 22], [43, 50]]
Boyut kontrolü testi: ValueError
```
```text {.python-playground-help}
`def matris_carp(a, b):` | İki matris alıp yeni bir matris döndürecek fonksiyonu tanımlarız; `a` soldaki, `b` sağdaki matristir.
`if not a or not b:` | Matrislerden biri boşsa ilk satırını bulamayız; böyle bir girdiyi hesaplamaya başlamadan reddederiz.
`raise ValueError("Matrisler boş olamaz.")` | `raise` bir hata oluşturup işlemi durdurur. `ValueError`, verilen değerlerin bu işlem için uygun olmadığını bildirir.
`a_sutun_sayisi = len(a[0])` ve `b_sutun_sayisi = len(b[0])` | İlk satırların uzunluğu, her matrisin sütun sayısını verir. Aşağıda bütün satırların bu uzunlukta olup olmadığını kontrol edeceğiz.
`for satir in a:` ve `for satir in b:` | Her matrisin satırlarını sırayla dolaşarak satır uzunluklarını karşılaştırırız.
`if len(satir) != ...:` | Bir satırın uzunluğu ilk satırdan farklıysa matrisin satırları aynı sütun sayısına sahip değildir.
`raise ValueError("... matrisi dikdörtgen olmalı.")` | Satır uzunlukları eşleşmediğinde anlaşılır bir hata veririz; böylece belirsiz bir indeks hatası oluşmaz.
`if a_sutun_sayisi != len(b):` | Çarpımın temel koşulunu denetleriz: soldaki matrisin sütun sayısı, sağdaki matrisin satır sayısına eşit olmalıdır.
`raise ValueError("a matrisinin sütun sayısı ...")` | Boyutlar uyumsuzsa işlemi durdurup hangi sayıların eşleşmesi gerektiğini belirten bir hata veririz.
`sonuc = []` | Sonuç matrisinin satırlarını bu boş listede biriktiririz.
`for satir in a:` | Soldaki matristeki satırları sırayla ele alırız; her biri sonuçta bir satır oluşturur.
`yeni_satir = []` | O anki satırın hücrelerini biriktirmek için yeni bir liste açarız.
`range(len(b[0]))` | Sağdaki matrisin ilk satırındaki hücre sayısı sütun sayısını verir; her sütun için bir sonuç hücresi hesaplanır.
`toplam = 0` | Geçerli satır-sütun eşleşmesinin çarpımlarını toplamak için sıfırdan başlarız.
`range(len(b))` | Sağdaki matrisin satırlarını sırayla dolaşırız; bunlar soldaki satırın bileşenleriyle eşleşir.
`satir[k] * b[k][sutun_no]` | Soldaki satırın `k` bileşenini, sağdaki matrisin seçili sütunundaki aynı sıradaki değerle çarparız.
`yeni_satir.append(toplam)` | Bir sütun için bulunan noktasal çarpımı mevcut sonuç satırına ekleriz.
`sonuc.append(yeni_satir)` | Bütün sütunlar hesaplanınca tamamlanan satırı sonuç matrisine ekleriz.
`return sonuc` | Tüm satırlar hesaplanınca yeni matrisi fonksiyonu çağıran koda geri veririz.
`print(matris_carp(a, b))` | Fonksiyonu iki örnek matrisle çağırır ve dönen matrisi ekrana yazar.
`try:` ve `matris_carp([[1, 2, 3]], [[1, 2], [3, 4]])` | Üç sütunlu ilk matrisi iki satırlı ikinci matrisle çarpmayı deneriz. Boyut kontrolü olmasaydı döngü `a` matrisinin üçüncü sütununu sessizce atlayıp yanlış sonuç üretebilirdi.
`except ValueError as hata:` | Boyut kontrolü beklediğimiz `ValueError` hatasını üretirse bu bölüm çalışır ve hatayı `hata` adıyla alırız.
`print("Boyut kontrolü testi:", type(hata).__name__)` | Yakalanan hatanın türünü yazarız. Beklenen çıktı görünmüyorsa boyut kontrolü çalışmıyor demektir; 0.5'te gördüğün test yaklaşımıyla bu sonucu denetleyebiliriz.
`else:` | `try` içindeki işlem hiç hata vermeden tamamlanırsa çalışır.
`print("Boyut kontrolü testi: hata oluşmadı")` | Uyumsuz boyutlar yanlışlıkla kabul edilirse bunu görünür kılar; çıktı beklenen sonuçla eşleşmez.
```

İlk sonuç hücresinin nasıl bulunduğunu kontrol et: `1 × 5 + 2 × 7 = 19`. Aynı satırın ikinci hücresi için sağdaki matrisin ikinci sütunu kullanılır: `1 × 6 + 2 × 8 = 22`.

Fonksiyon önce boş matrisleri, eşit uzunlukta olmayan satırları ve çarpım için uyumsuz boyutları kontrol eder. Örneğin `a` matrisinde üç sütun, `b` matrisinde iki satır varsa işlem `ValueError` ile durur. Bu kontrol olmasaydı döngü `b`'nin satır sayısı kadar ilerleyip `a`'nın üçüncü sütununu sessizce atlayabilir ve yanlış bir sonuç verebilirdi; `b`'nin satır sayısı `a`'nın sütun sayısından büyük olduğunda ise `IndexError` oluşabilirdi. `try-except` bölümünde hatayı yakalayıp türünü yazdırıyoruz; böylece bu kontrolü 0.5 dersinde öğrendiğin test yaklaşımıyla doğrulayabiliriz.

### Şimdi sen yaz: noktasal çarpım

**Görev:** Noktasal çarpımda aynı konumdaki sayılar çarpılıp toplanır. Fonksiyonu tamamlayıp bir evin özellikleri ile katsayılarından tek bir puan hesaplayacaksın; ekranda bu puan görünmeli.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
def noktasal_carpim(a, b):
    toplam = 0
    for i in range(len(a)):
        # TODO: Aynı konumdaki iki sayıyı çarp ve toplama ekle.
        toplam += ___
    return toplam


ozellikler = [2, 3, 4]
katsayilar = [5, -1, 2]
# TODO: Fonksiyonu özellikler ve katsayılarla çağır.
puan = noktasal_carpim(___, ___)
print("Puan:", puan)
```
```text {.python-playground-expected}
Puan: 15
```
```text {.python-playground-help}
`toplam += ___` | Noktasal çarpımda aynı konumdaki sayılar çarpılır: `a[i] * b[i]`.
`noktasal_carpim(___, ___)` | Fonksiyon iki liste bekler: önce özellikleri, sonra katsayıları ver.
```
```python {.python-playground-solution}
def noktasal_carpim(a, b):
    toplam = 0
    for i in range(len(a)):
        # Aynı konumdaki iki sayıyı çarp ve toplama ekle.
        toplam += a[i] * b[i]
    return toplam


ozellikler = [2, 3, 4]
katsayilar = [5, -1, 2]
# Fonksiyonu özellikler ve katsayılarla çağır.
puan = noktasal_carpim(ozellikler, katsayilar)
print("Puan:", puan)
```

## 3. Kütüphaneyle yap

NumPy'de matris çarpımı için `@` işleci kullanılır. Burada `*` yerine `@` yazmak önemlidir: NumPy'de `*` aynı konumlardaki elemanları çarpar, `@` ise matris çarpımını yapar.

Önce NumPy kur:

```bash
python -m pip install numpy
```

Sonra aşağıdaki örneği bilgisayarındaki Python dosyasında çalıştır:

```python
import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print(a @ b)
```

NumPy boyutları kontrol eder ve büyük dizilerde işlemleri verimli yürütür. Elle yazdığımız döngüler, `@` işleminin arkasındaki temel fikri görmemizi sağladı.

## 4. Sık yapılan hatalar

- **Sütun yerine satırı eşleştirmek.** Her sonuç hücresi için soldan bir satır, sağdan bir sütun seçilir.
- **Çarpım sırasını karıştırmak.** `A @ B` ile `B @ A` genellikle aynı sonucu vermez; boyutları uygun olsa bile sonuçları farklı olabilir.
- **Boyut koşulunu unutmak.** Soldaki matrisin sütun sayısı, sağdaki matrisin satır sayısına eşit olmalıdır. Örneğin `(2, 3) @ (3, 4)` mümkündür; sonuç `(2, 4)` olur.
- **NumPy'de `*` işlecini matris çarpımı sanmak.** `*` elemanları eşleşen konumlarda çarpar; matris çarpımı için `@` kullan.
- **Her sonucu aynı hücrede biriktirmek.** Her yeni satır-sütun çarpımı için `toplam` sıfırlanmalıdır; yoksa önceki hücrenin değeri de eklenir.

## 5. Pekiştir

**Quiz**

1. `[2, 3]` ile `[4, 5]` vektörlerinin noktasal çarpımı kaçtır?
2. `(2, 3)` boyutlu bir matris `(3, 4)` boyutlu bir matrisle çarpılırsa sonuç kaç satır ve kaç sütun olur?
3. NumPy'de matris çarpımı için hangi işleç kullanılır?
4. Matris çarpımında bir sonuç hücresi nasıl hesaplanır?

**Alıştırmalar**

1. Noktasal çarpım örneğinde bir evin özelliklerini `[80, 2, 8]` yap. Puanı elle hesaplayıp programın sonucuyla karşılaştır.
2. İki `2 × 2` matrisin bir hücresini seç ve kullanılan satır-sütun çarpımını kâğıt üzerinde göster.
3. (İsteğe bağlı) `matris_carp` fonksiyonunu bir `2 × 3` matris ve bir `3 × 2` matrisle dene. Sonuç boyutunun neden `2 × 2` olduğunu açıkla.

??? success "Quiz cevapları"
    1. `2 × 4 + 3 × 5 = 23`.
    2. İki satır ve dört sütun; sonuç boyutu `(2, 4)` olur.
    3. `@`.
    4. Soldaki matrisin seçilen satırı ile sağdaki matrisin seçilen sütunundaki aynı konumlu sayılar çarpılır ve sonuçlar toplanır.

## Özet

Noktasal çarpım, aynı konumdaki sayıların çarpımlarını toplayarak tek bir sonuç verir. Matris çarpımı, her satır-sütun eşleşmesi için bu işlemi tekrarlar. İşlemin tanımlı olması için soldaki matrisin sütun sayısı sağdakinin satır sayısına eşit olmalıdır. NumPy'de `@` bu hesabı yapar; küçük bir döngüyle yazmak ise hesabın nasıl kurulduğunu gösterir.

## Kaynaklar

- [NumPy: `matmul` (matris çarpımı)](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html)
- [NumPy: `@` işleci ve matris çarpımı](https://numpy.org/doc/stable/user/quickstart.html)
