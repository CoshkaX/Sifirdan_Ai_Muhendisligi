# Faz 4 – Ders 1: Metni sayılara dönüştürmek: Türkçe neden zor?

> ⏱️ Tahmini süre: 60-75 dk · 📚 Ön koşul: Faz 0 (Python temelleri) · 💻 Gereksinim: Python 3.11+, ek paket yok

## Bu derste ne öğreneceksin?

- Bir dil modelinin metni neden doğrudan okuyamadığını
- Tokenizer'ın ne olduğunu ve neden gerektiğini
- Karakter, kelime ve alt-kelime (subword) bölmenin farklarını
- Türkçe'nin ekli yapısının tokenizer'lar için neden ilginç bir problem olduğunu
- Türkçe metinde iki sinsi hata kaynağını: `lower()` ve aynı görünen iki farklı `ü`

## 1. Problem

Bir sinir ağı metni insan gibi harflerin anlamını okuyarak işlemez; modele verilecek girdi sayılardan oluşur. Bu yüzden `"evlerimizden"` gibi bir sözcüğü önce **token** adı verilen parçalara ayırır, sonra her parçayı bir sayıyla eşleriz.

```
"evlerimizden"  →  parçalar  →  numaralar
                   ['ev','ler','imiz','den']  →  [12, 87, 301, 45]
```

(Numaralar sadece örnektir; gerçek numaralar tokenizer'ın sözlüğüne göre belirlenir.)

Bu numaralar parçaların sözlükteki kimlikleri gibidir; `301` numaralı parça, sırf numarası `12`'den büyük diye daha önemli veya anlamlı değildir.

Soru şu: metni **nasıl** bölmelisin? Üç doğal seçenek var:

| Yöntem | Örnek (`evlerimizden`) | Artısı | Eksisi |
|---|---|---|---|
| **Karakter** | `e v l e r i m i z d e n` (12 parça) | Sözlük çok küçük, bilinmeyen kelime olmaz | Diziler çok uzar, her karakter tek başına az anlam taşır |
| **Kelime** | `evlerimizden` (1 parça) | Diziler kısa | Sözlük patlar; sözlükte olmayan kelime "bilinmeyen" olur |
| **Alt-kelime** | `ev` `ler` `imiz` `den` (4 parça) | İkisinin dengesi | Sözlüğü nasıl seçeceğini bilmen gerekir |

Türkçe'de kelime yöntemi özellikle zorlanır. Çünkü bir kökten pek çok biçim türetilebilir: *ev, evler, evlerimiz, evlerimizden, evlerimizdekiler...* Her biçim sözlükte ayrı bir madde olursa sözlük çok büyür; yeni bir biçim geldiğinde model onu tanımayabilir.

Birçok modern dil modeli alt-kelime bölmenin farklı yöntemlerini kullanır. Bu derste, bu fikrin küçük ve öğretici bir örneğini kendimiz yazacağız.

## 2. Kendin yaz

Kodun tamamı [`kod/tokenizer_demo.py`](kod/tokenizer_demo.py) dosyasında. Parça parça bakalım.

Önce aşağıdaki örneği çalıştır. Sonra kendi seçtiğin Türkçe sözcükleri `metinler` listesine ekle ve Python'ın saydığı karakterlerle UTF-8 bayt sayısının farkını gözlemle:

```python {.python-playground}
def utf8_bayt_sayisi(metin):
    return len(metin.encode("utf-8"))


metinler = ["sac", "saç", "Türkçe"]
for metin in metinler:
    print(f"{metin}: {len(metin)} karakter, {utf8_bayt_sayisi(metin)} bayt")
```
```text {.python-playground-expected}
sac: 3 karakter, 3 bayt
saç: 3 karakter, 4 bayt
Türkçe: 6 karakter, 8 bayt
```
```text {.python-playground-help}
`def utf8_bayt_sayisi(metin):` | `def` yeniden kullanacağımız bir işlev tanımlar. `metin` parantez içindeki addır; işlev çağrılırken buraya bir sözcük gelir.
`metin.encode("utf-8")` | `encode` sözcüğü UTF-8 biçimindeki baytlara çevirir. Örneğin Türkçe `ç` harfi ASCII harfi gibi tek bayt değildir.
`return len(...)` | `len` dönüştürülmüş baytların kaç tane olduğunu sayar; `return` bu sayıyı işlevi çağıran koda geri verir.
`metinler = ["sac", "saç", "Türkçe"]` | Köşeli ayraçlar bir liste oluşturur. Üç yazımı art arda koyarak aynı kodla karşılaştıracağız.
`for metin in metinler:` | Döngü listedeki her sözcüğü sırayla `metin` değişkenine koyar; altındaki satır her sözcük için yeniden çalışır.
`print(f"...")` | `f` metnindeki `{...}` alanları değerlerle doldurulur. `len(metin)` Python'ın karakter/kod noktası sayısını, `utf8_bayt_sayisi(metin)` ise bayt sayısını verir.
```

Bu pencere bağımsız bir Python örneğidir; aşağıdaki ders kodu bilgisayarında da çalıştırılabilir.

### 2.1 En basit bölmeler

```python {.python-playground}
def karakter_tokenizer(metin):
    return list(metin)

def kelime_tokenizer(metin):
    return metin.split()


metin = "saç çok"
print("Karakterler:", karakter_tokenizer(metin))
print("Sözcükler:", kelime_tokenizer(metin))
```
```text {.python-playground-expected}
Karakterler: ['s', 'a', 'ç', ' ', 'ç', 'o', 'k']
Sözcükler: ['saç', 'çok']
```
```text {.python-playground-help}
`def karakter_tokenizer(metin):` | İlk işlev, parantez içinde verdiğimiz metni `metin` adıyla alır.
`return list(metin)` | `list` metni harflere ayırır; boşluk da bir karakter olduğu için listede yer alır.
`def kelime_tokenizer(metin):` | İkinci işlev de aynı metni alır ama bu kez sözcüklere ayırmayı amaçlar.
`return metin.split()` | `split()` boşlukları ayraç kabul eder ve sözcükleri liste halinde geri verir; ayraç olan boşluklar listeye girmez.
`metin = "saç çok"` | İki sözcüklü bir deneme metni belirleriz. Tırnak içini değiştirerek başka bir metni deneyebilirsin.
`print("Karakterler:", karakter_tokenizer(metin))` | Metni ilk işlevden geçirip harfleri ve aradaki boşluğu gösterir.
`print("Sözcükler:", kelime_tokenizer(metin))` | Aynı metni ikinci işlevden geçirir; bu kez her sözcük ayrı bir öğe olur.
```

`"saç"` karakter olarak `['s', 'a', 'ç']` olur. Basit, ama önce bilgisayarın harfleri nasıl sakladığına bakalım.

### 2.2 Bilgisayar harfleri nasıl saklar? (UTF-8)

Metni dosyaya yazarken bilgisayar onu baytlarla kodlar. ASCII aralığındaki `a`, `b`, `1` gibi karakterler UTF-8'de birer bayttır; `ç, ğ, ı, ö, ş, ü` harflerinin her biri ikişer bayt kullanır.

```python
def utf8_bayt_sayisi(metin):
    return len(metin.encode("utf-8"))
```

| Metin | Python `len()` sonucu | UTF-8 baytı |
|---|---|---|
| `sac` | 3 | 3 |
| `saç` | 3 | 4 |
| `Türkçe` | 6 | 8 |
| `Turkce` | 6 | 6 |

Bu önemli, çünkü bazı tokenizer'lar metni karakter değil **bayt** düzeyinde işler. O zaman Türkçe harfler fazladan yer kaplar. (Gerçek tokenizer'larda bunun etkisini Faz 6'da ölçeceğiz; burada sadece fikri görüyoruz.)

Buradaki “karakter sayısı”, Python'ın `len()` ile saydığı Unicode kod noktası sayısıdır. Kullanıcının ekranda tek harf gibi gördüğü birleşik işaretler birden fazla kod noktası içerebilir; bunu NFC örneğinde göreceğiz.

### 2.3 Tuzak 1: küçük harf

Metni küçük harfe çevirmek, ilk temizlik adımlarından biridir. Ama Türkçe'de iki harf çifti özeldir: **I/ı** ve **İ/i**.

```python {.python-playground}
print("ISPARTA doğru küçüldü mü?", "ISPARTA".lower() == "ısparta")
print("İSTANBUL doğru küçüldü mü?", "İSTANBUL".lower() == "istanbul")
```
```text {.python-playground-expected}
ISPARTA doğru küçüldü mü? False
İSTANBUL doğru küçüldü mü? False
```
```text {.python-playground-help}
`print("ISPARTA doğru küçüldü mü?", "ISPARTA".lower() == "ısparta")` | `lower()` sonucu ile Türkçede beklediğimiz yazımı `==` ile karşılaştırırız. Genel dönüşüm `I` harfini `ı` yapmadığı için sonuç `False` olur.
`print("İSTANBUL doğru küçüldü mü?", "İSTANBUL".lower() == "istanbul")` | İkinci karşılaştırma da `False` çıkar; `İ` küçük harfe çevrilirken birleşen nokta işareti korunur.
```

Python'un `lower()` metodu Unicode'un varsayılan küçük-harf eşlemesini uygular; Türkçe yerel ayarına göre özel bir eşleme yapmaz. Bu yüzden `"I"` harfi `"i"` olur; Türkçedeki karşılığı `"ı"` olmalı. `"İ"` ise küçük harfe çevrilince `"i"` ve birleşen nokta olmak üzere iki kod noktasına dönüşür. Ekranda `"istanbul"` gibi görünse de `"İSTANBUL".lower() == "istanbul"` sonucu `False` olur.

Çözüm: bu iki harfi önce kendin çevir.

```python {.python-playground}
def turkce_kucuk_harf(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()


for metin in ["ISPARTA", "İSTANBUL"]:
    print(turkce_kucuk_harf(metin))
```
```text {.python-playground-expected}
ısparta
istanbul
```
```text {.python-playground-help}
`def turkce_kucuk_harf(metin):` | Bir işlev tanımlar; parantezdeki `metin`, dönüştürmek istediğimiz yazıyı alır.
`return metin.replace("İ", "i").replace("I", "ı").lower()` | Önce noktalı `İ` harfini `i`, noktasız `I` harfini `ı` yapar. Sonra `lower()` diğer büyük harfleri küçültür ve yeni yazıyı geri verir.
`for metin in ["ISPARTA", "İSTANBUL"]:` | Döngü iki deneme yazısını sırayla `metin` değişkenine koyar; altındaki satır her biri için çalışır.
`print(turkce_kucuk_harf(metin))` | O anki yazıyı işlevimize gönderir ve Türkçeye uygun küçük harfli sonucu gösterir.
```

Sıra önemli: önce `İ` ve `I` değişir, sonra kalan harfler için `lower()` kullanılır.

### 2.4 Tuzak 2: aynı görünen iki farklı "ü"

`ü` harfi bilgisayarda iki farklı şekilde saklanabilir:

- **Tek karakter:** `ü` (2 bayt)
- **İki parça:** `u` + birleşen iki nokta (3 bayt)

İkisi ekranda **birebir aynı** görünür ama bilgisayar için farklıdır. Bu, özellikle farklı işletim sistemlerinden veya kopyalanıp yapıştırılmış metinlerde karşına çıkabilir.

```python {.python-playground}
tek = "ü"
iki_parca = "u\u0308"
print(tek == iki_parca)      # False
```
```text {.python-playground-expected}
False
```
```text {.python-playground-help}
`tek = "ü"` | Bu yazımda `ü` tek bir karakter olarak saklanır; `tek` değişkeni bu yazıyı tutar.
`iki_parca = "u\u0308"` | `\u0308`, `u` harfinin üstüne gelen iki nokta işaretidir. Python bu yazımı `u` ve işaret olarak ayrı saklar.
`print(tek == iki_parca)` | `==` bilgisayarda saklanan metinleri karşılaştırır. Ekranda aynı görünseler de saklanma biçimleri farklı olduğu için `False` yazdırılır.
```

Çözüm: metni tek bir biçime (**NFC**) normalleştir.

```python {.python-playground}
import unicodedata

def unicode_normallestir(metin):
    return unicodedata.normalize("NFC", metin)


tek = "ü"
iki_parca = "u\u0308"
print("NFC öncesi:", tek == iki_parca)
tek_nfc = unicode_normallestir(tek)
iki_nfc = unicode_normallestir(iki_parca)
print("NFC sonrası:", tek_nfc == iki_nfc)
```
```text {.python-playground-expected}
NFC öncesi: False
NFC sonrası: True
```
```text {.python-playground-help}
`import unicodedata` | Python'ın Unicode metinlerini düzenleyen standart aracını kullanıma açar.
`def unicode_normallestir(metin):` | Bir metni alan ve ortak Unicode biçiminde geri verecek işlevi tanımlar.
`return unicodedata.normalize("NFC", metin)` | `normalize` metni NFC biçimine çevirir; `return` bu yeni metni işlevi çağıran yere gönderir.
`tek = "ü"` | Bu örnekteki ilk yazımı `tek` adlı değişkende tutarız.
`iki_parca = "u\u0308"` | İkinci yazımı ayrı değişkene kaydederiz; ikisini de dönüştürüp adil bir karşılaştırma yapacağız.
`print("NFC öncesi:", tek == iki_parca)` | Normalleştirmeden önce iki değeri karşılaştırır; saklanma biçimleri farklı olduğu için sonuç `False` olur.
`tek_nfc = unicode_normallestir(tek)` | İlk yazımı normalleştirip sonucu `tek_nfc` değişkenine kaydederiz.
`iki_nfc = unicode_normallestir(iki_parca)` | İkinci yazımı da aynı biçime dönüştürürüz; iki değeri de dönüştürmek karşılaştırmayı adil kılar.
`print("NFC sonrası:", tek_nfc == iki_nfc)` | Dönüştürülmüş değerleri karşılaştırır. Artık aynı biçimde saklandıkları için `True` görürüz.
```

!!! tip "Ne zaman NFC?"
    Metinleri karşılaştırmadan, aramadan veya eşleştirmeden önce iki tarafı da aynı Unicode biçimine getir. NFC yaygın bir tercihtir; ancak normalleştirmeyi uygulamanın veri kurallarına göre yap ve gerekiyorsa özgün metni de koru.

### 2.5 Açgözlü alt-kelime tokenizer'ı

Fikir şu: kelimenin başından başla, sözlükte bulunan **en uzun** parçayı al, kalan kısımla devam et. Hiç parça bulamazsan o karakteri "bilinmeyen" say.

```python {.python-playground}
def acgozlu_altkelime(kelime, sozluk, bilinmeyen="[BİLİNMEYEN]"):
    parcalar = []
    i = 0
    while i < len(kelime):
        for son in range(len(kelime), i, -1):
            aday = kelime[i:son]
            if aday in sozluk:
                parcalar.append(aday)
                i = son
                break
        else:
            parcalar.append(bilinmeyen)
            i += 1
    return parcalar


ORNEK_SOZLUK = {"ev", "ler", "imiz", "den", "kitap", "lar", "ımız", "dan", "göz", "lük", "çü"}
for kelime in ["evlerimizden", "okuldan"]:
    print(f"{kelime} -> {acgozlu_altkelime(kelime, ORNEK_SOZLUK)}")
```
```text {.python-playground-expected}
evlerimizden -> ['ev', 'ler', 'imiz', 'den']
okuldan -> ['[BİLİNMEYEN]', '[BİLİNMEYEN]', '[BİLİNMEYEN]', '[BİLİNMEYEN]', 'dan']
```
```text {.python-playground-help}
`def acgozlu_altkelime(kelime, sozluk, bilinmeyen="[BİLİNMEYEN]"):` | İşlev, bölünecek kelimeyi, tanınan parçaların kümesini ve bulunamazsa kullanılacak işareti alır.
`parcalar = []` | Bulduğumuz parçaları sırasıyla eklemek için boş bir liste açarız.
`i = 0` | `i`, kelimenin hangi harfinden aramaya başlayacağımızı tutar; başlangıçta ilk harfin konumu olan sıfırdır.
`while i < len(kelime):` | Kelimede incelenecek harf kaldığı sürece bölme işlemine devam ederiz.
`for son in range(len(kelime), i, -1):` | `son` konumunu kelimenin sonundan `i` konumuna doğru geri alırız; böylece önce en uzun parçayı deneriz.
`aday = kelime[i:son]` | Başlangıç ve bitiş konumları arasındaki harfleri alıp bu turda sözlükte arayacağımız adayı oluştururuz.
`if aday in sozluk:` | Adayın tanıdığımız parçalardan biri olup olmadığını kontrol ederiz.
`parcalar.append(aday)` | Sözlükte bulduğumuz parçayı sonuç listesinin sonuna ekleriz.
`i = son` | Aramanın başlangıcını, bulunan parçanın bittiği yere taşırız; sonraki tur bu konumdan devam eder.
`break` | En uzun eşleşmeyi bulduğumuz için daha kısa adayları denemeyi bırakırız.
`else:` | Döngü hiçbir aday bulamadan biterse burası çalışır; `break` olmadığından elimizde eşleşen parça yoktur.
`parcalar.append(bilinmeyen)` | Hiçbir aday sözlükte yoksa bilinmeyen parçasını sonuca ekleriz.
`i += 1` | Eşleşme bulamadığımız harfi atlayıp kelimenin bir sonraki harfinden aramaya devam ederiz.
`return parcalar` | Kelimenin tamamını inceledikten sonra bulunan parçaların listesini işlevi çağıran yere veririz.
`ORNEK_SOZLUK = {"ev", "ler", "imiz", "den", "kitap", "lar", "ımız", "dan", "göz", "lük", "çü"}` | Bu küme örneğin tanıyacağı parçaları içerir. `"okul"` sözcüğünü de tanıtmak için kümeye `"okul"` ekleyebilirsin.
`for kelime in ["evlerimizden", "okuldan"]:` | Döngü listedeki iki örnek kelimeyi sırayla alır; böylece bilinen ve sözlükte olmayan bir kökü karşılaştırırız.
`print(f"{kelime} -> {acgozlu_altkelime(kelime, ORNEK_SOZLUK)}")` | Her kelimeyi işlevimize verir ve dönen parça listesini ekrana yazar.
```

`for ... else` Python'da ilginç bir yapıdır: `else` bloğu yalnızca `for` döngüsü `break` ile **kesilmezse** çalışır; yani hiçbir aday eşleşmediyse.

Deneme sözlüğü, penceredeki `ORNEK_SOZLUK` kümesinde elle hazırlanır. Küme, bu örnekte tanınan parçaları tutar.

**Adım adım izleyelim.** `"evlerimizden"` kelimesi şöyle bölünür:

| Adım | Kalan kısım | Denenen en uzun adaylar | Seçilen |
|---|---|---|---|
| 1 | `evlerimizden` | `evlerimizden` ✗ `evlerimizde` ✗ ... `ev` ✓ | `ev` |
| 2 | `lerimizden` | `lerimizden` ✗ ... `ler` ✓ | `ler` |
| 3 | `imizden` | `imizden` ✗ ... `imiz` ✓ | `imiz` |
| 4 | `den` | `den` ✓ | `den` |

Proje klasöründeyken çalıştır:

```bash
cd docs/faz-04-metin-ve-turkce-nlp/01-metni-sayilara-cevirmek
python kod/tokenizer_demo.py
```

Çıktıdan bazı satırlar:

```
evlerimizden
  alt-kelime: ['ev', 'ler', 'imiz', 'den']

kitaplarımızdan
  alt-kelime: ['kitap', 'lar', 'ımız', 'dan']

okuldan
  alt-kelime: ['[BİLİNMEYEN]', '[BİLİNMEYEN]', '[BİLİNMEYEN]', '[BİLİNMEYEN]', 'dan']
```

Bu örnekten üç noktayı çıkar:

1. **Ekler yeniden kullanılıyor.** `dan` ve `den` farklı kelimelerde tekrar çıkıyor. Bu, alt-kelime yaklaşımının gücü.
2. **Ünlü uyumu sözlüğü büyütüyor.** `ler`/`lar`, `den`/`dan`, `imiz`/`ımız` aynı ekin farklı biçimleri. Sözlükte hepsinin yer alması gerekiyor. Bu, Türkçe'ye özgü bir problem.
3. **Sözlükte olmayan kelime sorun çıkarıyor.** `okul` sözlükte yok; bu nedenle `okuldan` sözcüğünün ilk dört harfi bilinmeyen olarak işaretlendi. Tokenizer'lar bu durumu farklı biçimlerde ele alır: bazıları bilinmeyen token üretir, bazıları sözcüğü daha küçük parçalara veya baytlara ayırır. Bu yaklaşımlardan birini, BPE'yi, Faz 6'nın 6.2. dersinde inceleyeceğiz.

### 2.6 Testler

Aynı klasördeyken:

```bash
python -m unittest discover -s test -v
```

On testin de `ok` ile tamamlanması gerekir. [`test/test_tokenizer_demo.py`](test/test_tokenizer_demo.py) dosyası, örneklerdeki temel davranışları otomatik olarak denetler. Kodu değiştirdiğinde testleri yeniden çalıştırıp beklenmedik bir değişiklik olup olmadığını kontrol edebilirsin.

## 3. Kütüphaneyle yap

Bu dersi bilerek kütüphanesiz bıraktık. Gerçek tokenizer'ları (Hugging Face `tokenizers` gibi) Faz 6'da kullanacağız. O zaman burada yazdığın fikrin onların içinde nasıl çalıştığını görürsün.

Şimdilik bir şeyi aklında tut: gerçek tokenizer'lar sözlüğü elle yazmaz, büyük bir metin yığınından **istatistiksel olarak** öğrenir. Bizim açgözlü yöntemimiz, öğrenilmiş bir sözlükle de aynı mantıkla çalışabilir.

## 4. Sık yapılan hatalar

- **`str.lower()` sonucunu Türkçe küçük harf kabul etmek.** Python Türkçeye özel bir eşleme yapmaz; `I/ı` ve `İ/i` dönüşümünü göz önünde bulundur.
- **Karakter sayısı ile bayt sayısını karıştırmak.** `len("saç")` 3 verir, ama UTF-8'de 4 bayttır.
- **Unicode normalleştirmeyi unutmak.** Aynı görünen iki metin farklı kod noktalarıyla saklanabilir. Karşılaştırma veya aramadan önce ikisini de NFC'ye dönüştür.
- **Kelime sözlüğünün her şeyi kapsayacağını sanmak.** Ekli dillerde yeni kelime biçimleri sürekli türer.
- **Açgözlü yöntemin her zaman en iyi bölmeyi bulacağını sanmak.** Alıştırma 3'te bunun neden doğru olmadığını göreceksin.

## 5. Pekiştir

**Quiz**

1. Bir sinir ağı neden metni doğrudan işleyemez?
2. `"saç"` kelimesi kaç karakter ve kaç UTF-8 bayttır?
3. Türkçe'de kelime düzeyinde tokenizer neden sözlüğü çok şişirir?
4. `"İSTANBUL".lower() == "istanbul"` ifadesi neden `False` döner?
5. `ler` ve `lar` ekleri bir tokenizer sözlüğü için neden önemli bir ayrıntıdır?
6. `"ü"` ile `"u\u0308"` neden `==` ile eşit çıkmaz ve bunu nasıl düzeltirsin?

**Alıştırmalar**

1. `ORNEK_SOZLUK` kümesine `"okul"` ekle ve `okuldan` kelimesini tekrar böl. Sonuç ne oldu?
2. Kendi seçtiğin 5 Türkçe kelimeyi (örn. *gözlüklerimizdeki*, *arkadaşlarımızla*) alt-kelime tokenizer'ına ver. Hangilerini bölebilmek için sözlüğe hangi parçaları eklemen gerekti?
3. (Zor) `acgozlu_altkelime` fonksiyonunun açgözlü olması bazen yanlış bölmeye yol açar. Sözlüğü `{"a", "ab", "bcd"}` yap ve `"abcd"` kelimesini böl. Sonuç ne oldu? Sence "en iyi" bölme nedir ve neden bulunamadı?
4. (İsteğe bağlı) `turkce_kucuk_harf` fonksiyonuna benzeyen bir `turkce_buyuk_harf` yaz (`i → İ`, `ı → I`). Önce `lower()`'ın yaptığı hatanın büyük harf karşılığını `"istanbul".upper()` ile gör.

??? success "Alıştırma ipuçları ve çözümler"
    **1.** Sonuç `['okul', 'dan']` olur. Sözlükte `okul` ve `dan` olduğu için kelime iki parçaya ayrılır.

    **2.** `gözlüklerimizdeki` kelimesi sözlükle şöyle bölünür: `['göz', 'lük', 'ler', 'imiz', '[BİLİNMEYEN]', ...]`. Sonundaki `deki` eki sözlükte olmadığı için bilinmeyen çıkar. Sözlüğe `deki` eklemelisin. Ek biçimleri (`deki`/`daki`/`teki`/`taki`) ünlü ve ünsüz uyumu yüzünden çok olduğundan, el ile sözlük yazmanın neden zor olduğunu bu şekilde görürsün.

    **3.** Sonuç `['ab', '[BİLİNMEYEN]', '[BİLİNMEYEN]']` olur. Oysa `a` + `bcd` geçerli bir bölme olabilirdi. Açgözlü yöntem önce en uzun eşleşme olan `ab` parçasını seçer ve başka bir yolu denemez. Bu nedenle daha gelişmiş yöntemlere ihtiyaç vardır; Faz 6'nın 6.2. dersinde BPE yaklaşımını ele alacağız.

    **4.** `"istanbul".upper()` sonucu `'ISTANBUL'` olur, ama Türkçe'de `'İSTANBUL'` olmalı. Çözüm: önce `i`→`İ` ve `ı`→`I` değişimini yap, sonra `upper()` çağır.

## Özet

Modeller sayılarla çalışır, bu yüzden metni önce token'lara bölüp numaralandırırız. Karakter bölmesi dizileri uzatır, kelime bölmesi sözlüğü şişirir, alt-kelime ikisini dengeler. Türkçe gibi ekli dillerde bu denge özellikle önemlidir: ekler yeniden kullanılır ama ünlü uyumu yüzünden çok biçimleri vardır. Ayrıca `lower()` ve Unicode normalleştirme gibi günlük işlemler bile Türkçe'de dikkat ister.

## Kaynaklar

- Python resmî dokümanı: `str.lower()`, `str.upper()` ve "Unicode HOWTO" bölümü (docs.python.org)
- Python resmî dokümanı: `unicodedata` modülü ve `normalize` fonksiyonu
- Sennrich, Haddow, Birch (2016), *Neural Machine Translation of Rare Words with Subword Units* (alt-kelime/BPE fikrinin kaynağı)
- Unicode standardı: büyük/küçük harf eşleme kuralları ve Türkçe'de noktalı/noktasız I için özel durumlar (unicode.org)

??? success "Quiz cevapları"
    1. Sinir ağları sayısal işlem yapar; metni önce sayılara dönüştürmek gerekir.
    2. 3 karakter, 4 bayt.
    3. Bir kökten çok sayıda ek birleşimi türetilir ve her biçim ayrı bir kelime sayılır.
    4. `İ` harfi `lower()` ile `i` + birleşen nokta (iki karakter) olur; bu yüzden sonuç `"istanbul"` ile eşit değildir.
    5. Aynı ekin ünlü uyumuna göre farklı biçimleri vardır; sözlükte hepsinin bulunması gerekir, aksi halde ek bölünemez.
    6. Biri tek karakter, diğeri `u` + birleşen iki nokta olarak saklanır; bilgisayar ikisini farklı sayar. `unicodedata.normalize("NFC", metin)` ile ikisini aynı biçime getirirsin.
