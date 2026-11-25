# Faz 4 – Ders 3: Türkçe metni temizlemek ve normalleştirmek

> ⏱️ Tahmini süre: 45-60 dk · 📚 Ön koşul: 4.1 Metni sayılara dönüştürmek · 💻 Gereksinim: Python 3.11+, ek paket yok

## Bu derste ne öğreneceksin?

- Metin normalleştirmenin ne işe yaradığını ve neden tek bir “temizleme” kuralı olmadığını
- Türkçe `I/İ` harflerini doğru biçimde küçük harfe çevirmeyi
- Unicode NFC ile aynı görünen farklı metin gösterimlerini eşitlemeyi
- Boşlukları düzenlerken sözcüklerin anlamını korumayı

## 1. Problem

Bir kullanıcı `"  İSTANBUL   çok güzel "` yazabilir; başka biri `"İstanbul çok güzel"` yazabilir. Bu iki metni aramada karşılaştırmak istiyorsak büyük-küçük harf ve fazla boşluk farklarını giderebiliriz.

Ancak “temizlemek”, metindeki her farklılığı silmek demek değildir. Türkçe karakterleri kaldırırsak `"gül"` ile `"gul"` aynı hale gelir; oysa bunlar farklı yazımlardır. İyi bir normalleştirme adımı, uygulamanın ihtiyacı olan farkları azaltırken anlam taşıyan bilgiyi korur.

## 2. Kendin yaz

### 2.1 Türkçe küçük harf ve boşluklar

Bu örnekte önce Türkçe `İ` ve `I` harflerini doğru biçime dönüştürüyoruz, sonra çevredeki ve art arda gelen boşlukları tek boşluk yapıyoruz:

```python {.python-playground}
def turkce_metin_normallestir(metin):
    metin = metin.replace("İ", "i").replace("I", "ı").lower()
    return " ".join(metin.split())


ornekler = [
    "  İSTANBUL\tçok   güzel ",
    "IĞDIR ve İZMİR",
]

for metin in ornekler:
    print(turkce_metin_normallestir(metin))
```
```text {.python-playground-expected}
istanbul çok güzel
ığdır ve izmir
```
```text {.python-playground-help}
`def turkce_metin_normallestir(metin):` | Bir işlev tanımlar. Parantezdeki `metin`, işlevin düzenleyeceği yazıyı alır.
`metin = metin.replace("İ", "i").replace("I", "ı").lower()` | İlk `replace` noktalı büyük `İ` harfini `i`, ikincisi noktasız büyük `I` harfini `ı` yapar. Sonundaki `lower()` diğer büyük harfleri küçültür; düzenlenen yazı yeniden `metin` değişkenine kaydedilir.
`return " ".join(metin.split())` | `split()` yazıyı boşluk ve tablardan sözcüklere ayırır; `" ".join(...)` sözcükleri aralarına tek boşluk koyarak birleştirir. `return` bu yeni yazıyı işlevi çağıran yere verir.
`for metin in ornekler:` | Döngü listedeki her yazıyı sırayla `metin` değişkenine koyar ve gövdesini her biri için çalıştırır.
`print(turkce_metin_normallestir(metin))` | O anki yazıyı temizleme işlevine gönderir; `print` işlevden geri gelen sonucu ekranda gösterir.
```

`split()` boşluk türlerini ayırt etmeden sözcüklere ayırır; `" ".join(...)` de bu sözcükleri tek boşlukla birleştirir. Bu örnek noktalama işaretlerini silmez ve Türkçe harfleri Latin harflerine indirgemez.

### 2.2 Aynı görünen metinler neden eşit olmayabilir?

`ü` tek bir Unicode kod noktasıyla veya `u` harfi ile birleşen iki nokta işaretinin birlikte kullanılmasıyla saklanabilir. Ekranda aynı görünseler bile Python bu dizileri farklı sayar. NFC normalleştirmesi, bu örnekte iki gösterimi aynı biçime getirir:

```python {.python-playground}
import unicodedata

tek_parca = "güzel"
birlesik_isaretli = "gu\u0308zel"

print("NFC öncesi eşit mi?", tek_parca == birlesik_isaretli)
tek_nfc = unicodedata.normalize("NFC", tek_parca)
diger_nfc = unicodedata.normalize("NFC", birlesik_isaretli)
print("NFC sonrası eşit mi?", tek_nfc == diger_nfc)
```
```text {.python-playground-expected}
NFC öncesi eşit mi? False
NFC sonrası eşit mi? True
```
```text {.python-playground-help}
`import unicodedata` | Python'ın Unicode yazı biçimleriyle çalışan hazır aracını kullanıma açar; birazdan `normalize` işlevini buradan alacağız.
`tek_parca = "güzel"` | Bu yazımdaki `ü`, Python'ın tek bir işaret olarak sakladığı harftir.
`birlesik_isaretli = "gu\u0308zel"` | `\u0308`, `u` harfinin üstüne gelen iki nokta işaretidir. Bilgisayar bunu `u` ve işaret olarak ayrı saklar; ekranda yine `ü` gibi görünür.
`print("NFC öncesi eşit mi?", tek_parca == birlesik_isaretli)` | `==` iki saklanmış metni karşılaştırır. Görünüşleri aynı olsa da yazılış biçimleri farklı olduğundan `False` gösterilir.
`tek_nfc = unicodedata.normalize("NFC", tek_parca)` | `normalize` metni ortak bir Unicode yazım biçimine çevirir; burada sonucu `tek_nfc` değişkenine kaydederiz.
`diger_nfc = unicodedata.normalize("NFC", birlesik_isaretli)` | Aynı işlemi ikinci yazıma da uygularız. Artık iki değişkende de aynı biçimde saklanan yazılar bulunur.
`print("NFC sonrası eşit mi?", tek_nfc == diger_nfc)` | Ortak biçime getirilmiş iki metni karşılaştırır ve eşit oldukları için `True` sonucunu ekrana yazar.
```

Bu iki adımı tek işlevde birleştirebiliriz:

```python {.python-playground}
import unicodedata


def turkce_metin_normallestir(metin):
    metin = unicodedata.normalize("NFC", metin)
    metin = metin.replace("İ", "i").replace("I", "ı").lower()
    return " ".join(metin.split())


girdi = "  I\u0307STANBUL\tçok   güzel "
print(turkce_metin_normallestir(girdi))
```
```text {.python-playground-expected}
istanbul çok güzel
```
```text {.python-playground-help}
`import unicodedata` | Unicode yazı biçimlerini düzenleyen aracı kullanıma açar.
`def turkce_metin_normallestir(metin):` | Temizlenecek yazıyı `metin` adıyla alan işlevi başlatır; aşağıdaki adımlar bu değişkeni sırayla düzenler.
`metin = unicodedata.normalize("NFC", metin)` | Yazıyı ortak bir Unicode biçimine çevirir. Bu örnekte `I\u0307`, tek bir büyük `İ` harfi olur ve sonuç `metin` değişkenine kaydedilir.
`metin = metin.replace("İ", "i").replace("I", "ı").lower()` | Türkçeye uygun `İ` ve `I` dönüşümlerini yapar, sonra kalan büyük harfleri küçültür; yeni metni aynı değişkende tutar.
`return " ".join(metin.split())` | `split()` sözcükleri boşluk ve tablardan ayırır; `" ".join(...)` aralarına tek boşluk koyar. `return` temizlenmiş yazıyı işlev dışına verir.
`girdi = "  I\u0307STANBUL\tçok   güzel "` | Bu örnekte başta boşluk, `\t` ile gösterilen bir tab ve art arda boşluklar vardır; `\u0307` büyük I harfinin üstündeki nokta işaretidir.
`print(turkce_metin_normallestir(girdi))` | Örnek yazıyı işlevimize gönderir ve dönen temiz metni ekrana basar.
```

Burada NFC, `I` ile birleşen noktayı tek bir `İ` kod noktasına dönüştürür; ardından Türkçe harf eşlemesi `i` sonucunu üretir. Normalleştirme ve harf dönüşümünün sırası bu nedenle önemlidir.

!!! note "Ham metni sakla"
    Arama veya karşılaştırma için normalleştirilmiş bir alan oluşturabilirsin; ancak kullanıcı girdisinin özgün halini de korumak çoğu uygulamada yararlıdır. Böylece gösterim ve denetim için orijinal metne geri dönebilirsin.

## 3. Kütüphaneyle yap

Python'ın standart `unicodedata` modülü Unicode normalleştirmeyi sağlar. Boşlukları düzenlemek için `str.split()` ve `str.join()` yeterlidir. Türkçe büyük-küçük harf dönüşümü için ise uygulamanın dil kurallarını açıkça belirtmek gerekir; genel Unicode işlemleri tek başına Türkçeye özel davranacağı anlamına gelmez.

Büyük projelerde normalleştirme kurallarını tek bir yerde tut, hangi alanlara uygulandığını belgeleyip gerçek örneklerle test et. Kullanıcı adı, arama sorgusu ve gösterilecek metin aynı temizleme adımlarına ihtiyaç duymayabilir.

## 4. Sık yapılan hatalar

- **Türkçe harfleri silmek.** `ş` harfini `s` yapmak `"şiş"` ile `"sis"` gibi farklı dizileri karıştırabilir.
- **Her şeyi `lower()` ile çözmeye çalışmak.** Python Türkçe yerel ayarına göre `I/İ` eşlemesi yapmaz.
- **NFC'yi harf düzeltme sanmak.** NFC bazı birleşik gösterimleri eşitler; Türkçe harf kurallarını veya bütün görsel benzerlikleri çözmez.
- **Özgün girdiyi kaybetmek.** Normalleştirilmiş biçimi aramada kullan, ama ihtiyaç varsa kullanıcının yazdığı metni ayrıca sakla.
- **Aynı kuralları her alana uygulamak.** Arama metniyle ekranda gösterilecek metnin ihtiyaçları farklı olabilir.

## 5. Pekiştir

**Quiz**

1. `"İSTANBUL"` sözcüğünü yalnızca `lower()` ile küçültmek Türkçe açısından neden yeterli değildir?
2. NFC normalleştirmesi hangi tür farkı gidermeye yardımcı olur?
3. Türkçe harfleri `ascii` harflerine çevirmek hangi riski taşır?
4. Normalleştirilmiş metin yanında ham girdiyi saklamak neden yararlı olabilir?

**Alıştırmalar**

1. İlk çalışma alanına `"  ŞİŞE\tve   GÜL  "` metnini ver. Çıktıda boşlukların ve Türkçe harflerin korunduğunu doğrula.
2. `"ö"` ve `"o\u0308"` metinlerini NFC öncesi ve sonrası karşılaştır.
3. Normalleştirme işlevini virgül ve noktayı koruyacak şekilde test et; `"Merhaba, dünya!"` çıktısının beklendiği gibi kaldığını doğrula.
4. (Zor) Ham kullanıcı girdisi ve normalleştirilmiş arama alanı için iki ayrı değişken kullanan küçük bir örnek yaz.

??? success "Quiz cevapları"
    1. `lower()` Türkçeye özel kural uygulamaz; `I` harfini `ı` yerine `i` yapar ve `İ` harfini `i` + birleşen nokta olarak iki karaktere çevirir.
    2. Aynı görünen bir harfin tek kod noktası veya temel harf ile birleşen işaretlerden oluşan gösterimleri arasındaki farkı eşitlemeye yardımcı olur.
    3. `ş/s`, `ç/c`, `ı/i` gibi ayrımları silerek farklı sözcükleri (`şiş`/`sis`, `kır`/`kir`) aynı yazıma indirebilir.
    4. Arama kolaylığı sağlarken özgün yazımı göstermek, incelemek veya daha sonra farklı kurallarla işlemek mümkün kalır.

## Özet

Metin normalleştirme; karşılaştırma ve aramayı kolaylaştırabilir, ancak metindeki anlamlı farkları silmemelidir. Türkçe `I/İ` dönüşümünü açıkça yönet, eşdeğer Unicode gösterimlerinde NFC kullan ve gereksiz boşlukları düzenle. Normalleştirme kurallarını verinin kullanım amacına göre seç ve özgün metni gerektiğinde koru.

## Kaynaklar

- Python resmî belgesi: [`unicodedata.normalize`](https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize)
- Python resmî belgesi: [`str.lower`, `str.split` ve `str.join`](https://docs.python.org/3/library/stdtypes.html#string-methods)
- Unicode Standard Annex #15, Unicode Normalization Forms: [unicode.org/reports/tr15](https://unicode.org/reports/tr15/)
