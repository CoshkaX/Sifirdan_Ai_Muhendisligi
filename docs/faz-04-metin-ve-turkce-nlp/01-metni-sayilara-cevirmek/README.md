# Faz 4 – Ders 1: Metni sayılara çevirmek (ve Türkçe neden zor?)

> ⏱️ Tahmini süre: 60-75 dk · 📚 Ön koşul: Faz 0 (Python temelleri) · 💻 Gereksinim: Python 3.11+, ek paket yok

## Bu derste ne öğreneceksin?

- Bir dil modelinin metni neden doğrudan okuyamadığını
- Tokenizer'ın ne olduğunu ve neden gerektiğini
- Karakter, kelime ve alt-kelime (subword) bölmenin farklarını
- Türkçe'nin ekli yapısının tokenizer'lar için neden ilginç bir problem olduğunu
- Türkçe metinde iki sinsi hata kaynağını: `lower()` ve aynı görünen iki farklı `ü`

## 1. Problem

Bir sinir ağı sayılarla çalışır. Ona `"evlerimizden"` yazamazsın; önce metni **sayılara** çevirmen gerekir. Bunun ilk adımı metni parçalara (**token**'lara) bölmek, ikinci adımı her parçaya bir numara vermektir.

```
"evlerimizden"  →  parçalar  →  numaralar
                   ['ev','ler','imiz','den']  →  [12, 87, 301, 45]
```

(Numaralar sadece örnektir; gerçek numaralar tokenizer'ın sözlüğüne göre belirlenir.)

Soru şu: metni **nasıl** bölmelisin? Üç doğal seçenek var:

| Yöntem | Örnek (`evlerimizden`) | Artısı | Eksisi |
|---|---|---|---|
| **Karakter** | `e v l e r i m i z d e n` (12 parça) | Sözlük çok küçük, bilinmeyen kelime olmaz | Diziler çok uzar, her karakter tek başına az anlam taşır |
| **Kelime** | `evlerimizden` (1 parça) | Diziler kısa | Sözlük patlar; sözlükte olmayan kelime "bilinmeyen" olur |
| **Alt-kelime** | `ev` `ler` `imiz` `den` (4 parça) | İkisinin dengesi | Sözlüğü nasıl seçeceğini bilmen gerekir |

Türkçe'de kelime yöntemi özellikle zayıf kalır. Çünkü bir kökten yüzlerce biçim türetilir: *ev, evler, evlerimiz, evlerimizden, evlerimizdekiler...* Her biri ayrı bir kelime sayılırsa sözlük kontrolsüz büyür ve yeni bir biçimle karşılaşıldığında model onu hiç tanımaz.

Modern dil modelleri üçüncü yolun, yani alt-kelime bölmenin varyantlarını kullanır. Bu derste bu fikri kendi ellerimizle, küçük ölçekte yazacağız.

## 2. Kendin yaz

Kodun tamamı [`kod/tokenizer_demo.py`](kod/tokenizer_demo.py) dosyasında. Parça parça bakalım.

### 2.1 En basit bölmeler

```python
def karakter_tokenizer(metin):
    return list(metin)

def kelime_tokenizer(metin):
    return metin.split()
```

`"saç"` karakter olarak `['s', 'a', 'ç']` olur. Basit, ama önce bilgisayarın harfleri nasıl sakladığına bakalım.

### 2.2 Bilgisayar harfleri nasıl saklar? (UTF-8)

Bilgisayar harfleri **baytlar** olarak saklar. İngilizce harfler UTF-8'de 1 bayt tutar, ama `ç, ğ, ı, ö, ş, ü` gibi harfler **2 bayt** tutar.

```python
def utf8_bayt_sayisi(metin):
    return len(metin.encode("utf-8"))
```

| Metin | Karakter | Bayt |
|---|---|---|
| `sac` | 3 | 3 |
| `saç` | 3 | 4 |
| `Türkçe` | 6 | 8 |
| `Turkce` | 6 | 6 |

Bu önemli, çünkü bazı tokenizer'lar metni karakter değil **bayt** düzeyinde işler. O zaman Türkçe harfler fazladan yer kaplar. (Gerçek tokenizer'larda bunun etkisini Faz 6'da ölçeceğiz; burada sadece fikri görüyoruz.)

### 2.3 Tuzak 1: küçük harf

Metni küçük harfe çevirmek, ilk temizlik adımlarından biridir. Ama Türkçe'de iki harf çifti özeldir: **I/ı** ve **İ/i**.

```python
"ISPARTA".lower()   # 'isparta'    → Türkçe'de 'ısparta' olmalı
"İSTANBUL".lower()  # 'i̇stanbul'   → fazladan bir "nokta" karakteri geliyor!
```

Python'un `lower()` metodu İngilizce kuralını uygular. İkinci örnekte `İ` harfi **iki karakter** olur (`i` + birleşen nokta). Çıktı gözle `istanbul` gibi görünür ama `== "istanbul"` karşılaştırması `False` döner. Arama ve eşleştirmede çok kafa karıştıran bir hata.

Çözüm: bu iki harfi önce kendin çevir.

```python
def turkce_kucuk_harf(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()
```

Sıra önemli: önce `İ` ve `I` değişir, sonra kalan harfler için `lower()` kullanılır.

### 2.4 Tuzak 2: aynı görünen iki farklı "ü"

`ü` harfi bilgisayarda iki farklı şekilde saklanabilir:

- **Tek karakter:** `ü` (2 bayt)
- **İki parça:** `u` + birleşen iki nokta (3 bayt)

İkisi ekranda **birebir aynı** görünür ama bilgisayar için farklıdır. Bu, özellikle farklı işletim sistemlerinden veya kopyalanıp yapıştırılmış metinlerde karşına çıkabilir.

```python
tek = "ü"
iki_parca = "u\u0308"
print(tek == iki_parca)      # False
```

Çözüm: metni tek bir biçime (**NFC**) normalleştir.

```python
import unicodedata

def unicode_normallestir(metin):
    return unicodedata.normalize("NFC", metin)

print(tek == unicode_normallestir(iki_parca))   # True
```

!!! tip "Kural"
    Türkçe metinle çalışırken ilk adımın, metni NFC'ye normalleştirmek olsun. Aksi halde "aynı" kelimeler birbirine eşit çıkmaz ve arama, sözlük eşleştirme, tekrar eden kayıt kontrolü sessizce bozulur.

### 2.5 Açgözlü alt-kelime tokenizer'ı

Fikir şu: kelimenin başından başla, sözlükte bulunan **en uzun** parçayı al, kalan kısımla devam et. Hiç parça bulamazsan o karakteri "bilinmeyen" say.

```python
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
```

`for ... else` Python'da ilginç bir yapıdır: `else` bloğu yalnızca `for` döngüsü `break` ile **kesilmezse** çalışır; yani hiçbir aday eşleşmediyse.

Elle hazırladığımız küçük sözlük:

```python
ORNEK_SOZLUK = {"ev", "ler", "imiz", "den", "kitap", "lar", "ımız", "dan",
                "göz", "lük", "çü"}
```

**Adım adım izleyelim.** `"evlerimizden"` kelimesi şöyle bölünür:

| Adım | Kalan kısım | Denenen en uzun adaylar | Seçilen |
|---|---|---|---|
| 1 | `evlerimizden` | `evlerimizden` ✗ `evlerimizde` ✗ ... `ev` ✓ | `ev` |
| 2 | `lerimizden` | `lerimizden` ✗ ... `ler` ✓ | `ler` |
| 3 | `imizden` | `imizden` ✗ ... `imiz` ✓ | `imiz` |
| 4 | `den` | `den` ✓ | `den` |

Çalıştır:

```bash
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

Üç şeye dikkat et:

1. **Ekler yeniden kullanılıyor.** `dan` ve `den` farklı kelimelerde tekrar çıkıyor. Bu, alt-kelime yaklaşımının gücü.
2. **Ünlü uyumu sözlüğü büyütüyor.** `ler`/`lar`, `den`/`dan`, `imiz`/`ımız` aynı ekin farklı biçimleri. Sözlükte hepsinin yer alması gerekiyor. Bu, Türkçe'ye özgü bir problem.
3. **Sözlükte olmayan kelime sorun çıkarıyor.** `okul` sözlükte yok, bu yüzden `okuldan` kelimesinin başı "bilinmeyen" oldu. Gerçek tokenizer'lar bunu çözmek için sözlüğü **veriden öğrenir** ve her karakteri en azından bir parça olarak içerir. Bunu Ders 6.2'de (BPE) yazacağız.

### 2.6 Testler

```bash
python -m unittest discover -s test -v
```

On testin hepsi `ok` demeli. Testlere göz at: `test/test_tokenizer_demo.py` dosyası, yukarıda gösterdiğimiz davranışların her birini otomatik doğrular. Kodu değiştirirsen testleri yeniden çalıştırarak bir şeyi bozup bozmadığını görebilirsin.

## 3. Kütüphaneyle yap

Bu dersi bilerek kütüphanesiz bıraktık. Gerçek tokenizer'ları (Hugging Face `tokenizers` gibi) Faz 4'ün sonraki derslerinde ve Faz 6'da kullanacağız. O zaman burada yazdığın fikrin onların içinde nasıl çalıştığını görürsün.

Şimdilik bir şeyi aklında tut: gerçek tokenizer'lar sözlüğü elle yazmaz, büyük bir metin yığınından **istatistiksel olarak** öğrenir. Bizim açgözlü yöntemimiz, öğrenilmiş bir sözlükle de aynı mantıkla çalışabilir.

## 4. Sık yapılan hatalar

- **`str.lower()` ile Türkçe metin temizlemek.** `İ`/`I` hatası. Metin eşleştirme yapıyorsan mutlaka kontrol et.
- **Karakter sayısı ile bayt sayısını karıştırmak.** `len("saç")` 3 verir, ama UTF-8'de 4 bayttır.
- **Unicode normalleştirmeyi unutmak.** Aynı görünen iki metnin `==` ile eşit çıkmaması çok kafa karıştırır. İlk adım olarak NFC'ye çevir.
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

    **3.** Sonuç `['ab', '[BİLİNMEYEN]', '[BİLİNMEYEN]']` olur. Oysa `a` + `bcd` kusursuz bir bölme olurdu. Açgözlü yöntem önce en uzun eşleşmeyi (`ab`) seçer ve geri dönüp başka bir yolu denemez. Bu yüzden daha gelişmiş yöntemlere ihtiyaç var (Ders 6.2'de göreceğiz).

    **4.** `"istanbul".upper()` sonucu `'ISTANBUL'` olur, ama Türkçe'de `'İSTANBUL'` olmalı. Çözüm: önce `i`→`İ` ve `ı`→`I` değişimini yap, sonra `upper()` çağır.

## Özet

Modeller sayılarla çalışır, bu yüzden metni önce token'lara bölüp numaralandırırız. Karakter bölmesi dizileri uzatır, kelime bölmesi sözlüğü şişirir, alt-kelime ikisini dengeler. Türkçe gibi ekli dillerde bu denge özellikle önemlidir: ekler yeniden kullanılır ama ünlü uyumu yüzünden çok biçimleri vardır. Ayrıca `lower()` ve Unicode normalleştirme gibi günlük işlemler bile Türkçe'de dikkat ister.

## Kaynaklar

- Python resmî dokümanı: `str.lower()`, `str.upper()` ve "Unicode HOWTO" bölümü (docs.python.org)
- Python resmî dokümanı: `unicodedata` modülü ve `normalize` fonksiyonu
- Sennrich, Haddow, Birch (2016), *Neural Machine Translation of Rare Words with Subword Units* (alt-kelime/BPE fikrinin kaynağı)
- Unicode standardı: büyük/küçük harf eşleme kuralları ve Türkçe'de noktalı/noktasız I için özel durumlar (unicode.org)

## Quiz cevapları

1. Sinir ağları sayısal işlem yapar; metni önce sayılara dönüştürmek gerekir.
2. 3 karakter, 4 bayt.
3. Bir kökten çok sayıda ek birleşimi türetilir ve her biçim ayrı bir kelime sayılır.
4. `İ` harfi `lower()` ile `i` + birleşen nokta (iki karakter) olur; bu yüzden sonuç `"istanbul"` ile eşit değildir.
5. Aynı ekin ünlü uyumuna göre farklı biçimleri vardır; sözlükte hepsinin bulunması gerekir, aksi halde ek bölünemez.
6. Biri tek karakter, diğeri `u` + birleşen nokta olarak saklanır; bilgisayar ikisini farklı sayar. `unicodedata.normalize("NFC", metin)` ile ikisini aynı biçime getirirsin.
