# Faz 1 – Ders 4: Olasılık ve olasılık dağılımları

> ⏱️ Tahmini süre: 40-55 dk · 📚 Ön koşul: 0.2 Python hızlı tekrar · 💻 Gereksinim: Python 3.11+, ek paket yok

## Bu derste ne öğreneceksin?

- Bir olayın olasılığını, eşit şanslı sonuçları sayarak bulmayı
- Olası sonuçları ve her birinin olasılığını birlikte gösteren dağılımı okumayı
- Gerçek olasılıkla az sayıdaki denemede gözlenen oranı birbirinden ayırmayı

## 1. Problem

Bir zar attığında hangi yüzün geleceğini önceden bilemezsin. Ancak zar adilse altı yüzün her birinin gelme şansı eşittir. Bu bilgiyle, örneğin çift sayı gelme olasılığını hesaplayabiliriz.

- **Deney:** Sonucu belirsiz olan işlemi yapmak; burada zarı bir kez atmak.
- **Sonuç:** Deneyden çıkabilecek tek bir değer; örneğin `4`.
- **Örnek uzay:** Deneyde mümkün olan bütün sonuçlar; zar için `1, 2, 3, 4, 5, 6`.
- **Olay:** İlgilendiğimiz sonuç veya sonuç grubu; burada “çift sayı gelmesi”.

Her sonucun gelme şansı eşitse:

`Olasılık = olaya uygun sonuç sayısı / mümkün olan bütün sonuçların sayısı`

Çift yüzler `2`, `4` ve `6` olduğundan olasılık `3 / 6 = 0.5`, yani yüzde `50` olur. Bu sayma yöntemi yalnızca sonuçların eşit şanslı olduğu durumda geçerlidir.

## 2. Kendin yaz

### 2.1 Çift sayı gelme olasılığını hesapla

Önce zarın gelebilecek yüzlerini listeliyoruz. Sonra çift olanları seçip, uygun sonuç sayısını toplam sonuç sayısına bölüyoruz.

```python {.python-playground}
zar_yuzleri = [1, 2, 3, 4, 5, 6]
cift_yuzler = []

for yuz in zar_yuzleri:
    if yuz % 2 == 0:
        cift_yuzler.append(yuz)

olasilik = len(cift_yuzler) / len(zar_yuzleri)
print("Olası yüzler:", zar_yuzleri)
print("Çift yüzler:", cift_yuzler)
print("Çift gelme olasılığı:", olasilik)
print("Yüzde:", int(olasilik * 100))
```
```text {.python-playground-expected}
Olası yüzler: [1, 2, 3, 4, 5, 6]
Çift yüzler: [2, 4, 6]
Çift gelme olasılığı: 0.5
Yüzde: 50
```
```text {.python-playground-help}
`zar_yuzleri = [1, 2, 3, 4, 5, 6]` | Adil zarın altı mümkün sonucunu listede tutarız. Bu hesapta her yüzün şansının eşit olduğunu varsayıyoruz.
`cift_yuzler = []` | Çift olduğunu bulduğumuz yüzleri eklemek için boş bir liste açarız.
`for yuz in zar_yuzleri:` | Listedeki yüzleri sırayla `yuz` değişkenine alırız; girintili satırlar her yüz için çalışır.
`if yuz % 2 == 0:` | `%` bölme işleminden kalanı bulur. Bir sayı ikiye bölündüğünde kalan `0` ise sayı çifttir; `==` burada kalanın sıfıra eşit olup olmadığını kontrol eder.
`cift_yuzler.append(yuz)` | Koşul doğruysa o yüzü çift yüzler listesine ekleriz. Bu satır yalnızca çift sayılar için çalışır.
`olasilik = len(cift_yuzler) / len(zar_yuzleri)` | Uygun sonuç sayısını (`3`), toplam sonuç sayısına (`6`) böler ve oranı `olasilik` değişkenine kaydederiz. Sonuç `0.5` çıkar.
`print("Olası yüzler:", zar_yuzleri)` | Deneyde kullanacağımız bütün zar yüzlerini gösterir.
`print("Çift yüzler:", cift_yuzler)` | Koşula uyan, yani çift olan yüzleri gösterir.
`print("Çift gelme olasılığı:", olasilik)` | Hesaplanan olasılığı `0` ile `1` arasında bir sayı olarak yazar. `0.5`, yüzde `50` demektir.
`print("Yüzde:", int(olasilik * 100))` | Olasılığı yüzdeye çevirip yazarız: `0.5 × 100 = 50`. `int` sonucu tam sayı olarak gösterir.
```

Koşul satırındaki `yuz % 2 == 0` ifadesi, “yüz ikiye kalansız bölünüyor mu?” diye sorar. `yuz % 2 == 1` yaparsan tek yüzler seçilir. Adil zar için tek gelme olasılığı da `0.5` olur.

### 2.2 Olasılık dağılımını oku

**Olasılık dağılımı**, bir deneyin mümkün sonuçlarını ve her sonucun olasılığını birlikte gösterir. Yazı-tura için adil bir madeni parada iki sonuç vardır ve ikisinin de olasılığı `0.5`tir:

```python {.python-playground}
para_dagilimi = {
    "yazı": 0.5,
    "tura": 0.5,
}

toplam_olasilik = 0.0
for sonuc in para_dagilimi:
    olasilik = para_dagilimi[sonuc]
    toplam_olasilik += olasilik
    print(sonuc, "olasılığı:", olasilik)

print("Olasılıkların toplamı:", toplam_olasilik)
```
```text {.python-playground-expected}
yazı olasılığı: 0.5
tura olasılığı: 0.5
Olasılıkların toplamı: 1.0
```
```text {.python-playground-help}
`para_dagilimi = {` | Süslü ayraçlarla bir sözlük başlatırız. Bu sözlükte her sonuç, kendi olasılığıyla eşleştirilir.
`"yazı": 0.5` | Madeni paranın yazı gelme olasılığını `0.5` olarak yazarız; bu, yüzde `50` demektir.
`"tura": 0.5` | Adil para varsayımında tura için de aynı olasılık geçerlidir.
`}` | Süslü ayraçla sözlüğü kapatırız; iki sonuç ve olasılıkları artık `para_dagilimi` değişkenindedir.
`toplam_olasilik = 0.0` | Olasılıkları toplayacağımız değişkeni sıfırdan başlatırız.
`for sonuc in para_dagilimi:` | Sözlükteki sonuç adlarını, önce `"yazı"` sonra `"tura"` olacak şekilde sırayla ele alırız.
`olasilik = para_dagilimi[sonuc]` | O anki sonucun sözlükte saklanan olasılığını alırız.
`toplam_olasilik += olasilik` | Olasılığı toplama ekleriz. `+=`, mevcut değerin üzerine ekleme yapar.
`print(sonuc, "olasılığı:", olasilik)` | Sonuç adını ve ona ait olasılığı ekrana yazarız.
`print("Olasılıkların toplamı:", toplam_olasilik)` | Bütün mümkün sonuçların olasılıklarını toplarız. Eksiksiz bir dağılımda bu toplam `1` olmalıdır.
```

Burada mümkün sonuç sayısı sınırlı olduğu için buna **kesikli dağılım** denir. Olasılıklar `0` ile `1` arasında olmalı ve bütün mümkün sonuçların olasılıkları toplamı `1` etmelidir. Yazı ya da tura sonuçlarından biri mutlaka geleceği için toplam olasılık yüzde `100`, yani `1` olur. Örneğin toplam `0.8` çıkarsa bazı olasılıklar eksik kalmış olabilir; `1.2` çıkarsa değerlerden biri fazla yazılmış olabilir.

### 2.3 Hesaplanan olasılık ile gözlenen oranı ayır

Adil para için yazı gelme olasılığı `0.5`tir. Ama parayı yalnızca altı kez attığında altı atışın tam üçünün yazı gelmesi garanti değildir. Denemelerde gördüğün sonuçların oranı **gözlenen oran**dır; az sayıdaki denemede bu oran teorik olasılıkla aynı çıkmayabilir.

Örneğin altı atışta beş kez yazı geldiyse, bu deneydeki yazı oranı `5 / 6` olur. Bu tek küçük deney, paranın gerçek olasılığının `5 / 6` olduğunu kanıtlamaz. Teorik olasılık, deneyin kurallarına dayanır; gözlenen oran ise yaptığın denemelerin sonucudur.

### Şimdi sen yaz: iki zar

İki zar atıldığında toplamın 10 veya daha büyük gelme olasılığını say. Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur, sonra çalıştır.

```python {.python-playground-task}
uygun = 0
toplam_sonuc = 0

# İç içe iki döngü: iki zarın 36 olası çiftini sırayla dener.
for z1 in range(1, 7):
    for z2 in range(1, 7):
        toplam_sonuc += 1
        # TODO: İki zarın toplamı 10 veya daha büyükse uygun sonucu say.
        if ___:
            uygun += 1

# TODO: Olasılık = uygun sonuç sayısı / bütün sonuçların sayısı.
olasilik = ___
print("Uygun:", uygun, "Toplam:", toplam_sonuc)
print("Olasılık:", round(olasilik, 3))
```
```text {.python-playground-expected}
Uygun: 6 Toplam: 36
Olasılık: 0.167
```
```text {.python-playground-help}
`if ___:` | Koşul, iki zarın toplamının en az `10` olmasıdır: `z1 + z2 >= 10`.
`olasilik = ___` | Olasılık = uygun sonuç sayısı / bütün sonuçların sayısı.
```
```python {.python-playground-solution}
uygun = 0
toplam_sonuc = 0

# İç içe iki döngü: iki zarın 36 olası çiftini sırayla dener.
for z1 in range(1, 7):
    for z2 in range(1, 7):
        toplam_sonuc += 1
        # İki zarın toplamı 10 veya daha büyükse uygun sonucu say.
        if z1 + z2 >= 10:
            uygun += 1

# Olasılık = uygun sonuç sayısı / bütün sonuçların sayısı.
olasilik = uygun / toplam_sonuc
print("Uygun:", uygun, "Toplam:", toplam_sonuc)
print("Olasılık:", round(olasilik, 3))
```

## 3. Kütüphaneyle yap

Python'ın standart `random` modülü, bilgisayar içinde örnek rastgele sonuçlar üretir. Aşağıdaki kodu çalıştırdığında her seferinde `1` ile `6` arasında bir sayı görürsün; sonuç her çalıştırmada değişebileceği için burada tek bir beklenen çıktı yoktur.

```python
import random

zar_sonucu = random.randint(1, 6)
print("Zar sonucu:", zar_sonucu)
```

`randint(1, 6)` hem `1` hem `6` dahil olacak şekilde bu aralıktan bir tam sayı seçer. Tek bir atışın sonucunu verir; olasılık dağılımını veya adil bir zar olduğunu kendi başına kanıtlamaz.

## 4. Sık yapılan hatalar

- **`0.5` değerini yüzde `0.5` sanmak.** Olasılık `0` ile `1` arasında yazıldığında `0.5`, yüzde `50` demektir; yüzdeye çevirmek için `100` ile çarp.
- **Sonuçların eşit şanslı olmadığını unutmak.** `uygun sonuç sayısı / bütün sonuç sayısı` hesabı yalnızca her sonucun eşit şansı varsa doğrudan kullanılabilir.
- **Dağılımda mümkün bir sonucu atlamak.** Her mümkün sonucu ve ona ait olasılığı yaz; olasılıkların toplamı `1` olmalı.
- **Az denemede görülen oranı gerçek olasılık sanmak.** Altı atışta beş kez yazı gelmesi, adil paranın yazı olasılığının kesin olarak `5/6` olduğunu göstermez.

## 5. Pekiştir

**Quiz**

1. Zar atma deneyinin örnek uzayı nedir?
2. Adil bir zarda çift sayı gelme olasılığını nasıl buluruz?
3. Bir olasılık dağılımındaki bütün sonuçların olasılıkları toplamı kaç olmalıdır?
4. Altı para atışında beş kez yazı gelmesi, yazı olasılığının kesin olarak `5/6` olduğunu kanıtlar mı?

**Alıştırmalar**

1. İlk penceredeki koşulu tek sayıları seçecek şekilde değiştir ve olasılığın neden değişmediğini açıkla.
2. Dört eşit dilimli bir çarkta üç dilim mavi, bir dilim kırmızı olsun. Olasılık dağılımını yaz; olasılıkların toplamının `1` olduğunu kontrol et.
3. Adil bir zar için altı yüzün her birine `1/6` olasılığı veren bir sözlük oluştur. Dağılımın toplamı neden `1` eder?
4. (İsteğe bağlı) Bir dağılımdaki olasılıkları `0.7` ve `0.4` yap. Toplamın `1` olmadığını bul ve değerleri geçerli bir dağılım oluşturacak şekilde düzelt.

??? success "Quiz cevapları"
    1. `{1, 2, 3, 4, 5, 6}`; zarın gelebilecek bütün yüzleri.
    2. Üç çift yüzü (2, 4, 6) altı mümkün yüze böleriz: `3/6 = 0.5`, yani yüzde `50`.
    3. `1` olmalıdır; bu, mümkün sonuçlardan birinin gerçekleşeceğini ifade eder.
    4. Hayır. Bu, yalnızca altı atışta görülen orandır; küçük bir deney gerçek olasılığı kanıtlamaz.

## Özet

Olasılık, belirsiz bir olayın ne kadar mümkün olduğunu sayıyla anlatır. Sonuçlar eşit şanslıysa olaya uygun sonuç sayısını bütün sonuçların sayısına bölebiliriz. Olasılık dağılımı, mümkün sonuçları ve her birinin olasılığını birlikte gösterir; eksiksiz bir dağılımda olasılıkların toplamı `1` olur. Az sayıdaki denemede gözlenen oran, teorik olasılıkla aynı olmak zorunda değildir.

## Kaynaklar

- [OpenStax: Introduction to Probability](https://openstax.org/books/introductory-statistics/pages/3-introduction)
- [Python resmî belgesi: `random`](https://docs.python.org/3/library/random.html)
