# Faz 0 – Ders 2: Python hızlı tekrar

> ⏱️ Tahmini süre: 60-75 dk · 📚 Ön koşul: 0.1 Geliştirme ortamı · 💻 Gereksinim: Python 3.11+, ek paket yok

## Bu derste ne öğreneceksin?

- Değişkenlerle bilgiyi adlandırmayı ve ekrana yazdırmayı
- Listeler ile birden fazla değeri sırayla saklamayı
- Sözlüklerle adlandırılmış bilgileri tutmayı
- Fonksiyon yazıp bir sonucu `return` ile geri vermeyi
- Basit bir sınıf ve ondan üretilen nesneyi anlamayı
- Koşullarla karar vermeyi, döngülerle işleri tekrarlamayı ve eşleşen değerleri birlikte işlemeyi

## 1. Problem

Bir programda `"Ayşe"`, `3` ve `["Python", "veri"]` gibi bilgiler vardır. Bunları yalnızca ekrana yazmak yetmez; sonra kullanmak ve aralarında işlem yapmak isteriz. Python'da bunun için değişken, liste, sözlük, fonksiyon ve sınıf gibi yapı taşları bulunur.

Bu ders sıfırdan her ayrıntıyı öğretmeye çalışmaz. Her yapıyı küçük bir örnekle hatırlatır; sonraki derslerde bu parçaları bir arada kullanacağız.

## 2. Kendin yaz

### 2.1 Değişkenler: değerlere ad ver

Değişken, bir değere verdiğimiz addır. Aşağıdaki örnekte ürünün adı, fiyatı ve adedi ayrı değişkenlerde durur:

```python {.python-playground}
urun = "defter"
fiyat = 35
adet = 2
toplam = fiyat * adet
print(f"{adet} {urun}: {toplam} TL")
```
```text {.python-playground-expected}
2 defter: 70 TL
```
```text {.python-playground-help}
`urun = "defter"` | Tırnak içindeki metni `urun` adlı değişkende saklarız; eşittir işareti burada bir değer atar.
`fiyat = 35` | Ürünün birim fiyatını sayı olarak tutarız; sayılar tırnaksız yazılır.
`adet = 2` | Kaç tane alındığını başka bir değişkende saklarız; böylece miktarı değiştirmek kolay olur.
`toplam = fiyat * adet` | `*` çarpma yapar. Sonuç olan `70`, daha sonra gösterebilmek için `toplam` değişkenine kaydedilir.
`print(f"{adet} {urun}: {toplam} TL")` | `f` metnindeki süslü parantezler değişkenlerin değerleriyle doldurulur; `print` oluşan cümleyi ekrana yazar.
```

`fiyat` veya `adet` değerini değiştirip tekrar çalıştır. Toplamın da değiştiğini görmelisin.

### 2.2 Listeler: değerleri sırayla sakla

Bir liste, birden fazla değeri belirli bir sırayla tutar. Python saymaya sıfırdan başlar; bu nedenle ilk öğenin konumu `0` olur.

```python {.python-playground}
konular = ["değişken", "liste", "sözlük"]
konular.append("fonksiyon")
print("İlk konu:", konular[0])
print("Son konu:", konular[-1])
print("Konu sayısı:", len(konular))
```
```text {.python-playground-expected}
İlk konu: değişken
Son konu: fonksiyon
Konu sayısı: 4
```
```text {.python-playground-help}
`konular = ["değişken", "liste", "sözlük"]` | Köşeli ayraçlar bir liste oluşturur; virgülle ayrılan bu üç metin listedeki öğelerdir.
`konular.append("fonksiyon")` | `append` yeni bir öğeyi listenin sonuna ekler. Bundan sonra son öğe `"fonksiyon"` olur.
`konular[0]` | Köşeli ayraç içindeki `0`, ilk öğenin sırasını belirtir; Python listelerinde ilk sıra sıfırdır.
`konular[-1]` | `-1`, listenin sonundaki öğeyi seçmenin kısa yoludur.
`len(konular)` | `len` listedeki öğe sayısını verir; burada dört konu vardır.
```

Kendin dene: `print("İlk konu:", konular[0])` satırındaki `0` yerine `10` yaz. Listede yalnızca `0`, `1`, `2` ve `3` konumları olduğu için Python `IndexError` verir. Düzeltmek için var olan bir konumu kullan.

### 2.3 Sözlükler: bilgiyi anahtarla bul

Bir listede öğeyi sırasıyla ararsın. Sözlükte ise her değere bir anahtar verirsin; böylece örneğin ürünün fiyatını adıyla bulabilirsin.

```python {.python-playground}
urun = {
    "ad": "kalem",
    "fiyat": 12,
    "stokta": True,
}
print(urun["ad"])
print(urun["fiyat"])
print(urun.get("renk", "Renk belirtilmemiş"))
```
```text {.python-playground-expected}
kalem
12
Renk belirtilmemiş
```
```text {.python-playground-help}
`urun = {` | Süslü ayraçlar bir sözlük başlatır; içinde her anahtarın karşısında bir değer bulunur.
`"ad": "kalem"` | `"ad"` anahtarı ürünün adını, `"kalem"` ise bu anahtara bağlı değeri belirtir.
`"fiyat": 12` | Aynı sözlüğe sayı türünde bir değer de koyabiliriz; bu fiyatla hesaplama yapılabilir.
`"stokta": True` | `True`, doğru/yanlış bilgisini tutan iki özel değerden biridir; ürünün stokta olduğunu anlatır.
`urun["ad"]` | Anahtarı köşeli ayraçta vererek o alandaki değeri okuruz.
`urun.get("renk", "Renk belirtilmemiş")` | `get`, anahtar varsa değerini, yoksa ikinci metni verir. Böylece sözlükte olmayan `"renk"` için hata almak yerine anlaşılır bir sonuç görürüz.
```

Sözlükte olmayan bir anahtarı köşeli ayraçla okumak, Python o adla kayıtlı bir değer bulamadığı için `KeyError` verir. Örneğin `urun["renk"]`, sözlükte `"renk"` anahtarı yoksa durur. Bilgi isteğe bağlıysa `.get("renk", "Renk belirtilmemiş")` kullan; anahtar bulunmadığında bu varsayılan metin gösterilir.

### 2.4 Fonksiyonlar: işi adlandır ve yeniden kullan

Fonksiyon, bir işi adlandırıp ihtiyaç olduğunda çalıştırmamızı sağlar. Bir fonksiyon değer hesaplıyorsa `return` ile sonucu geri verir:

```python {.python-playground}
def indirimli_fiyat(fiyat, indirim_yuzdesi):
    indirim = fiyat * indirim_yuzdesi / 100
    return fiyat - indirim


sonuc = indirimli_fiyat(100, 15)
print(f"İndirimli fiyat: {sonuc} TL")
```
```text {.python-playground-expected}
İndirimli fiyat: 85.0 TL
```
```text {.python-playground-help}
`def indirimli_fiyat(fiyat, indirim_yuzdesi):` | `def` bir fonksiyon tanımlar. Parantez içindeki iki ad, çağırırken vereceğimiz fiyatı ve indirim oranını alır.
`indirim = fiyat * indirim_yuzdesi / 100` | Önce fiyatın istenen yüzdesini hesaplarız. Örnekte 100 TL'nin yüzde 15'i, 15 TL'dir.
`return fiyat - indirim` | İndirim miktarını fiyattan çıkarır ve sonucu fonksiyonu çağıran yere geri gönderir.
`sonuc = indirimli_fiyat(100, 15)` | Fonksiyonu 100 ve 15 değerleriyle çağırırız; geri gelen 85.0 değeri `sonuc` değişkenine kaydolur.
`print(f"İndirimli fiyat: {sonuc} TL")` | Hesaplanan sonucu f-metninin içine koyup ekranda gösteririz.
```

`return` ile `print` aynı şey değildir: `return` sonucu programın başka bir bölümüne verir; `print` yalnızca ekranda gösterir. İndirim oranını değiştirerek sonucu dene.

### 2.5 Sınıflar: aynı türden nesneler üret

Bir sınıf, benzer nesnelerin hangi bilgilere ve davranışlara sahip olacağını tanımlar. Burada `Kitap` sınıfı başlığı ve yazarı saklayan nesneler üretir:

```python {.python-playground}
class Kitap:
    def __init__(self, baslik, yazar):
        self.baslik = baslik
        self.yazar = yazar

    def tanit(self):
        return f"{self.baslik} — {self.yazar}"


kitap = Kitap("Küçük Prens", "Antoine de Saint-Exupéry")
print(kitap.tanit())
```
```text {.python-playground-expected}
Küçük Prens — Antoine de Saint-Exupéry
```
```text {.python-playground-help}
`class Kitap:` | `class` benzer kitap nesnelerinin nasıl oluşturulacağını tanımlar; bu satır henüz belirli bir kitap üretmez.
`def __init__(self, baslik, yazar):` | `__init__`, yeni nesne yaratılırken çalışan özel bir işlevdir. `baslik` ve `yazar` değerlerini nesne oluştururken alır.
`self.baslik = baslik` | `self`, o anda oluşturulan tek kitabı gösterir; aldığımız başlığı bu kitabın içinde saklarız.
`self.yazar = yazar` | Yazar bilgisini de aynı nesnede saklarız; böylece iki bilgi birbirine ait kalır.
`def tanit(self):` | Her `Kitap` nesnesinin çağırabileceği bir davranış tanımlar; `self`, hangi kitabı tanıtacağımızı belirtir.
`return f"{self.baslik} — {self.yazar}"` | Kitabın sakladığı başlık ve yazarı bir metinde birleştirip geri verir.
`kitap = Kitap("Küçük Prens", "Antoine de Saint-Exupéry")` | Sınıftan bir nesne üretir ve parantezdeki iki bilgiyi `__init__` işlevine gönderir.
`print(kitap.tanit())` | O nesnenin `tanit` davranışını çağırır ve dönen metni ekranda gösterir.
```

Şimdilik şunu hatırla: sınıf bir kalıp, `kitap` ise o kalıptan üretilmiş tek bir nesnedir. Sınıf ayrıntılarını ihtiyaç oldukça yeniden ele alacağız.

### 2.6 Koşullar: farklı duruma göre karar ver

Bir programın her durumda aynı işi yapması gerekmez. `if` bir koşulu sınar; koşul doğruysa ilk bölüm çalışır. `elif`, önceki koşul yanlış çıktığında başka bir koşulu sınar. `else` ise önceki koşulların hiçbiri doğru değilse çalışır.

```python {.python-playground}
puan = 78

if puan >= 85:
    sonuc = "Çok iyi"
elif puan >= 60:
    sonuc = "Geçti"
else:
    sonuc = "Tekrar çalış"

print("Sonuç:", sonuc)
```
```text {.python-playground-expected}
Sonuç: Geçti
```
```text {.python-playground-help}
`puan = 78` | Karar vermek için kullanacağımız puanı belirleriz.
`if puan >= 85:` | İlk koşulu sınarız. `>=`, “büyük veya eşit” demektir; koşul doğruysa altındaki girintili satır çalışır.
`elif puan >= 60:` | İlk koşul yanlışsa bu ikinci koşul sınanır. Puan en az `60` ise bu bölüm çalışır.
`else:` | Önceki koşulların hiçbiri doğru değilse çalışacak son bölümü başlatırız.
`print("Sonuç:", sonuc)` | Koşulların seçtiği sonucu ekrana yazarız.
```

`puan` değerini `90`, `50` ve `60` yapıp yeniden çalıştır. Sınırdaki `60`, ikinci koşula girer; çünkü `>=` eşitliği de kapsar.

### 2.7 Döngüler: `for` ve `range` ile sırayla ilerle

Bir işi listedeki her öğe için tekrarlamak üzere `for` döngüsü kullanırız. `range(len(liste))`, listenin geçerli konumlarını üretir: ilk konum `0`'dır.

```python {.python-playground}
konular = ["değişken", "liste", "sözlük"]

for i in range(len(konular)):
    print(f"{i + 1}. konu: {konular[i]}")
```
```text {.python-playground-expected}
1. konu: değişken
2. konu: liste
3. konu: sözlük
```
```text {.python-playground-help}
`konular = [...]` | Üç konu başlığını belirli bir sırayla listede saklarız.
`range(len(konular))` | `len(konular)` üç olduğu için `range(3)`, `0`, `1` ve `2` konumlarını sırayla üretir.
`for i in ...:` | Her turda sıradaki konum `i` olur; altındaki girintili satır her konum için bir kez çalışır.
`konular[i]` | O konumdaki konu başlığını alırız. İlk turda `konular[0]`, yani ilk öğe seçilir.
`i + 1` | Ekranda insana uygun sıra numarası göstermek için Python'ın `0`'dan başlayan konumuna `1` ekleriz.
```

Liste öğesinin kendisi yeterliyse konum kullanmadan da yazabilirsin: `for konu in konular:`. `range` ise bir işlemi belirli sayıda tekrarlamak veya konumları kullanmak istediğinde yararlıdır.

### 2.8 Eşleşen değerler: tuple açma ve `zip`

Tuple (demet), birbiriyle ilişkili birkaç değeri tek bir kayıt gibi tutabilir. Bir tuple'ı ayrı değişkenlere açmaya **tuple açma** denir. `zip`, iki listedeki aynı konumları eşleştirir; döngüde her eşleşmeyi ayrı değişkene açabiliriz.

```python {.python-playground}
kayit = ("Ece", 85)
ad, notu = kayit
print(f"Tek kayıt: {ad} - {notu}")

ogrenciler = ["Ece", "Mert", "Ada"]
notlar = [85, 72, 94]
for ad, notu in zip(ogrenciler, notlar):
    print(f"{ad}: {notu}")
```
```text {.python-playground-expected}
Tek kayıt: Ece - 85
Ece: 85
Mert: 72
Ada: 94
```
```text {.python-playground-help}
`kayit = ("Ece", 85)` | Parantez içindeki iki değeri tek tuple'da tutarız; bu örnekte ad ile not aynı öğrenciye aittir.
`ad, notu = kayit` | Tuple'daki ilk değeri `ad`, ikinci değeri `notu` değişkenine açarız. Soldaki değişken sayısı ile tuple'daki değer sayısı eşleşmelidir.
`zip(ogrenciler, notlar)` | Aynı konumdaki ad ve notu bir çift olarak verir; ilk ad ilk notla eşleşir.
`for ad, notu in ...:` | Her eşleşen çifti döngü sırasında iki ayrı değişkene açarız. Böylece adları ve notları aynı öğrenci için birlikte kullanırız.
```

`zip` ile eşleştirdiğin listelerin uzunluğu ve sırası aynı olmalı. Aksi hâlde değerler yanlış kişiye bağlanabilir veya kısa listenin bittiği yerde eşleştirme durur.

### Şimdi sen yaz: ortalama fonksiyonu

Bir sınıftaki öğrencilerin not ortalamasını bulan fonksiyonu tamamla. `# TODO` yazan yerlerdeki `___` boşluklarını tamamla, sonra çalıştır.

```python {.python-playground-task}
def ortalama(notlar):
    # TODO: Notların toplamını not sayısına böl ve sonucu geri ver.
    return ___


sinif = {"Ece": [80, 90, 100], "Mert": [60, 70, 80]}

for ad in sinif:
    # TODO: Öğrencinin notlarını ortalama() fonksiyonuna ver.
    sonuc = ortalama(___)
    print(f"{ad}: {sonuc}")
```
```text {.python-playground-expected}
Ece: 90.0
Mert: 70.0
```
```text {.python-playground-help}
`return ___` | `sum(notlar)` toplamı, `len(notlar)` not sayısını verir. Toplamı sayıya böl.
`ortalama(___)` | Sözlükte her öğrencinin notları ad anahtarının karşısında durur; `sinif[ad]` o listeyi verir.
```
```python {.python-playground-solution}
def ortalama(notlar):
    # Notların toplamını not sayısına böl ve sonucu geri ver.
    return sum(notlar) / len(notlar)


sinif = {"Ece": [80, 90, 100], "Mert": [60, 70, 80]}

for ad in sinif:
    # Öğrencinin notlarını ortalama() fonksiyonuna ver.
    sonuc = ortalama(sinif[ad])
    print(f"{ad}: {sonuc}")
```

## 3. Kütüphaneyle yap

Bu örnekler Python'ın yerleşik özelliklerini kullanır; ek paket kurmaya gerek yoktur. Listeler, sözlükler ve fonksiyonlar Python'ın temel parçalarıdır. Sonraki derslerde NumPy veya PyTorch gibi kütüphaneler, bu tür işlemleri büyük veri ve modeller üzerinde daha verimli yapmamıza yardım edecek.

## 4. Sık yapılan hatalar

- **Metni sayı sanmak.** `"12"` metindir; `12` sayıdır. Metin üzerinde toplama yapmak, sayısal toplama ile aynı değildir.
- **Listenin ilk sırasında `1` kullanmak.** İlk öğe `liste[0]` konumundadır.
- **Sözlükte olmayan anahtarı okumak.** Python aradığın anahtara bağlı bir değer bulamazsa `KeyError` verir. Bilgi isteğe bağlıysa `.get(anahtar, varsayılan_değer)` kullanarak eksik durumda ne gösterileceğini belirt.
- **Fonksiyonun sonucunu kaybetmek.** `return` yoksa hesaplanan değer çağıran koda geri dönmez.
- **`print` ve `return` ifadelerini karıştırmak.** Ekranda görünen bir değer her zaman başka hesaplamalarda kullanılabilir bir sonuç değildir.
- **`self` sözcüğünü özel bir sabit sanmak.** Bu, sınıf içindeki yöntemin üzerinde çalıştığı nesneyi gösteren geleneksel parametre adıdır.

## 5. Pekiştir

**Quiz**

1. `fiyat = 35` satırında `=` ne yapar?
2. `konular[-1]` hangi öğeyi seçer?
3. Bir sözlük anahtarı bulunmazsa `.get()` ne döndürebilir?
4. `return` ile `print` arasındaki fark nedir?
5. Sınıf ile nesne arasındaki farkı kendi cümlenle anlat.
6. `if`, `elif` ve `else` hangi sırayla ve ne zaman çalışır?
7. `range(len(konular))` hangi değerleri üretir?
8. `zip` ile döngüde `for ad, notu in ...` yazmak ne işe yarar?

**Alıştırmalar**

1. Bir ürünün fiyatını ve adedini değiştirip toplamı yeniden hesapla.
2. Bir not listesine yeni not ekle ve ortalamayı `sum(notlar) / len(notlar)` ile bul.
3. Bir öğrenci sözlüğüne `"sinif"` anahtarı ekleyip değerini yazdır.
4. İki sayı alan ve toplamını geri veren `topla` adlı fonksiyon yaz.
5. (İsteğe bağlı) `Kitap` nesnesine `sayfa_sayisi` bilgisi ekle ve `tanit` sonucunda göster.
6. Bir puana göre `"Geçti"` veya `"Kaldı"` yazdıran koşul kur.
7. İki listeyi `zip` ile eşleştirip her kişinin adını ve puanını yazdır.

??? success "Quiz cevapları"
    1. Sağdaki değeri soldaki değişken adına atar.
    2. Listenin son öğesini.
    3. Anahtar yoksa kendisine verdiğin varsayılan değeri; varsayılan vermezsen `None`.
    4. `return` sonucu programa geri verir; `print` ekrana yazar.
    5. Sınıf nesne oluşturma tanımıdır; nesne o tanıma göre oluşturulmuş belirli bir örnektir.
    6. Önce `if`, gerekirse sıradaki `elif` koşulları sınanır; hiçbiri doğru değilse `else` çalışır.
    7. Liste üç öğeliyse `0`, `1` ve `2` konumlarını üretir.
    8. Aynı konumdaki ad ve puanı çiftler; döngüde bu iki değeri ayrı değişkenlere açar.

## Özet

Değişkenler değerlere ad verir; listeler sıralı öğeleri, sözlükler anahtar-değer çiftlerini saklar. Koşullar karar vermeyi, `for` döngüsü ve `range` tekrarı, `zip` ise eşleşen değerleri birlikte işlemeyi sağlar. Fonksiyonlar bir işi tekrar kullanılabilir kılar; sınıflar da benzer özellik ve davranış taşıyan nesneleri tanımlar. Bu parçaları küçük örneklerde değiştirip çalıştırmak, sonraki yapay zekâ dersleri için sağlam bir Python temeli oluşturur.

## Kaynaklar

- [Python öğreticisi: Veri yapıları](https://docs.python.org/3/tutorial/datastructures.html)
- [Python öğreticisi: Sınıflar](https://docs.python.org/3/tutorial/classes.html)
- [Python yerleşik fonksiyonları](https://docs.python.org/3/library/functions.html)
