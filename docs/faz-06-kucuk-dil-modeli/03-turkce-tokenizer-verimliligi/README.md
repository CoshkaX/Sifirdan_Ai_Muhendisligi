# Faz 6 – Ders 3: Türkçe'de tokenizer verimliliği

> ⏱️ Tahmini süre: 45-60 dk · 📚 Ön koşul: 4.1 Metni sayılara dönüştürmek, 6.2 BPE tokenizer · 💻 Gereksinim: Python 3.11+, ek paket yok; Hugging Face örneği için `tokenizers` kurulmalıdır

## Bu derste ne öğreneceksin?

- Bir tokenizer'ın verimliliğini **token/sözcük oranıyla** ölçmeyi
- Aynı anlamın farklı tokenizer'larda kaç token tuttuğunu karşılaştırmayı
- Verimsiz bir tokenizer'ın **maliyet**, **bağlam uzunluğu** ve **hız** üzerindeki etkisini
- Sorunun Türkçede değil, tokenizer'ın eğitildiği veride olduğunu görmeyi
- Bayt düzeyinde tokenizer'larda Türkçe harflerin neden fazladan token tuttuğunu

## 1. Problem

Bir dil modeli için her şey **token** cinsinden ölçülür:

- **Maliyet:** Dil modeli API'leri genellikle token başına ücret alır.
- **Bağlam:** Model bir seferde belli sayıda token görebilir (örneğin birkaç bin ya da yüz binlerce). Token'lar ne kadar uzun metin parçası taşırsa o kadar çok metin sığar.
- **Hız:** Model metni token token üretir; aynı metin için daha çok token, daha uzun bekleme demektir.

Yani aynı cümle bir tokenizer'da 13, başka birinde 34 token tutuyorsa, ikincisi aynı iş için yaklaşık **2.6 kat** daha pahalı, daha yavaş ve bağlama 2.6 kat daha az metin sığdırıyor demektir. Türkçe ekli bir dil olduğundan sözcükler uzundur. Tokenizer bu sözcükleri iyi parçalara bölemiyorsa Türkçe metin gereksiz yere çok token'a dönüşür.

Bu derste bunu küçük bir deneyle ölçeceğiz: Aynı içeriği taşıyan bir Türkçe ve bir İngilizce metin yazıp her birinde ayrı bir BPE eğiteceğiz ve iki tokenizer'ı iki dilde karşılaştıracağız.

## 2. Kendin yaz

### 2.1 Verimliliği ölçmek

İki basit ölçü kullanacağız:

- **Token/sözcük oranı** (İngilizce kaynaklarda *fertility*): Bir sözcük ortalama kaç token'a bölünüyor? Küçük olması iyidir.
- **Token başına karakter:** Bir token ortalama kaç karakter taşıyor? Büyük olması iyidir.

```python {.python-playground}
cumle = "öğretmenler çocuklarla okulda konuşuyor"
bolmeler = {
    "Türkçe bilen tokenizer": ["öğretmen", "ler", "çocuk", "lar", "la", "okul", "da", "konuş", "uyor"],
    "Türkçe bilmeyen tokenizer": ["ö", "ğ", "re", "t", "m", "en", "ler", "ç", "o", "c", "uk",
                                  "lar", "la", "ok", "ul", "da", "k", "on", "u", "ş", "u", "yor"],
}

sozcuk_sayisi = len(cumle.split())
karakter_sayisi = len(cumle.replace(" ", ""))
for ad, tokenlar in bolmeler.items():
    print(f"{ad}: {len(tokenlar)} token, "
          f"token/sözcük {len(tokenlar) / sozcuk_sayisi:.2f}, "
          f"token başına karakter {karakter_sayisi / len(tokenlar):.1f}")
```
```text {.python-playground-expected}
Türkçe bilen tokenizer: 9 token, token/sözcük 2.25, token başına karakter 4.0
Türkçe bilmeyen tokenizer: 22 token, token/sözcük 5.50, token başına karakter 1.6
```
```text {.python-playground-help}
`bolmeler = {...}` | Aynı cümlenin iki farklı tokenizer'la bölünmüş hâli (elle yazdık). İkisi de birleşince aynı cümleyi verir.
`len(cumle.split())` | Sözcük sayısı: 4.
`cumle.replace(" ", "")` | Boşlukları atarak yalnızca harfleri sayarız.
`len(tokenlar) / sozcuk_sayisi` | Token/sözcük oranı: bir sözcük ortalama kaç token'a bölünmüş.
`karakter_sayisi / len(tokenlar)` | Bir token ortalama kaç harf taşıyor.
```

Türkçe bilen tokenizer'da bir sözcük ortalama 2.25 token; bilmeyende 5.5 token. Aynı cümle ikincisinde iki kattan fazla token tutuyor.

### 2.2 Deney: hangi dilde eğitildiği belirler

Şimdi 6.2'deki BPE'yi iki ayrı metinde eğitelim. İki metin aynı içeriği anlatıyor: biri Türkçe, biri İngilizce. Sonra her tokenizer'a her iki dilden aynı anlamdaki bir cümleyi verip token sayılarını tablo olarak yazalım:

```python {.python-playground}
from collections import Counter

TR = ("çocuklar okula gidiyor öğretmenler okulda ders veriyor çocuklar derste kitap okuyor "
      "öğretmenler çocuklara soru soruyor akşam çocuklar evlerine dönüyor evlerde aileler yemek yiyor "
      "aileler çocuklarla konuşuyor çocuklar kitaplarını okuyor ve uyuyor")
EN = ("the children are going to school the teachers are teaching lessons at school "
      "the children are reading books in the lesson the teachers are asking the children questions "
      "in the evening the children are returning to their homes at home the families are eating dinner "
      "the families are talking with the children the children are reading their books and sleeping")


def birlestir(p, cift):
    yeni, i = [], 0
    while i < len(p):
        if i < len(p) - 1 and (p[i], p[i + 1]) == cift:
            yeni.append(p[i] + p[i + 1])
            i += 2
        else:
            yeni.append(p[i])
            i += 1
    return tuple(yeni)


def egit(metin, n=60):
    sozcukler = Counter(tuple(s) for s in metin.split())
    birlestirmeler = []
    for _ in range(n):
        sayilar = Counter()
        for p, s in sozcukler.items():
            for i in range(len(p) - 1):
                sayilar[(p[i], p[i + 1])] += s
        en_sik = max(sayilar, key=sayilar.get)
        if sayilar[en_sik] < 2:
            break
        birlestirmeler.append(en_sik)
        sozcukler = Counter({birlestir(p, en_sik): s for p, s in sozcukler.items()})
    return birlestirmeler


def token_sayisi(cumle, birlestirmeler):
    toplam = 0
    for sozcuk in cumle.split():
        parcalar = tuple(sozcuk)
        for cift in birlestirmeler:
            parcalar = birlestir(parcalar, cift)
        toplam += len(parcalar)
    return toplam


tr_tok, en_tok = egit(TR), egit(EN)
cumleler = {"Türkçe": "öğretmenler çocuklarla okulda konuşuyor",
            "İngilizce": "the teachers are talking with the children at school"}

print(f"{'cümle':10} {'TR tokenizer':>13} {'EN tokenizer':>13}")
for dil, cumle in cumleler.items():
    print(f"{dil:10} {token_sayisi(cumle, tr_tok):>13} {token_sayisi(cumle, en_tok):>13}")
```
```text {.python-playground-expected}
cümle       TR tokenizer  EN tokenizer
Türkçe                13            34
İngilizce             42            15
```
```text {.python-playground-help}
`TR` ve `EN` | Aynı içeriği anlatan iki küçük metin. Her biriyle ayrı bir tokenizer eğiteceğiz.
`def egit(metin, n=60):` | 6.2'deki BPE eğitimi: en sık çifti en fazla `n` kez birleştirir.
`def token_sayisi(cumle, birlestirmeler):` | Cümlenin her sözcüğünü öğrenilen birleştirmelerle böler ve toplam token sayısını verir.
`tr_tok, en_tok = egit(TR), egit(EN)` | İki tokenizer: biri Türkçe metinden, biri İngilizce metinden öğrendi.
`f"{...:>13}"` | Sayıyı 13 karakterlik alana sağa yaslı yazar; tablo düzgün görünür.
```

Tabloyu oku:

- **Türkçe cümle**, Türkçe tokenizer'da 13, İngilizce tokenizer'da 34 token. İngilizce tokenizer Türkçe sözcükleri neredeyse harf harf bölüyor.
- **İngilizce cümle** için durum tersine: İngilizce tokenizer'da 15, Türkçe tokenizer'da 42 token.
- **Her dil kendi tokenizer'ında** benzer sayıda token tutuyor (13 ve 15). Türkçenin daha az sözcükle (4) ifade ettiğini İngilizce 9 sözcükle söylüyor.

Yani **sorun Türkçenin kendisi değil, tokenizer'ın hangi dilde eğitildiği.** Yaygın dil modellerinin tokenizer'ları, eğitim verilerinin büyük kısmı İngilizce olduğu için çoğunlukla İngilizce parçaları öğrenir. Türkçe metin böyle bir tokenizer'da daha çok token tutar. Türkçe için eğitilmiş ya da çok dilli verinin dengeli kullanıldığı tokenizer'lar bu farkı küçültür.

### 2.3 Bu fark neye mal olur?

Bir modelin bağlam penceresi 1000 token olsun. Token/sözcük oranı ne kadar yüksekse, bu pencereye o kadar az sözcük sığar:

```python {.python-playground}
baglam = 1000
cumle_sozcuk = 4

for ad, token in [("Türkçe tokenizer", 13), ("İngilizce tokenizer", 34)]:
    oran = token / cumle_sozcuk
    sigan_sozcuk = int(baglam / oran)
    print(f"{ad:20} token/sözcük {oran:.2f} → bağlama ~{sigan_sozcuk} sözcük sığar")

print(f"Aynı metin için maliyet ve süre farkı: {34 / 13:.1f} kat")
```
```text {.python-playground-expected}
Türkçe tokenizer     token/sözcük 3.25 → bağlama ~307 sözcük sığar
İngilizce tokenizer  token/sözcük 8.50 → bağlama ~117 sözcük sığar
Aynı metin için maliyet ve süre farkı: 2.6 kat
```
```text {.python-playground-help}
`oran = token / cumle_sozcuk` | 2.2'deki Türkçe cümle 4 sözcük; token/sözcük oranını hesaplarız.
`int(baglam / oran)` | 1000 token'lık pencereye kaç sözcük sığar? `int` ondalığı atar.
`34 / 13` | Aynı cümle bir tokenizer'da 34, öbüründe 13 token: maliyet ve üretim süresi bu oranda artar.
```

Verimsiz tokenizer'da aynı pencereye üçte bir kadar Türkçe metin sığıyor. Uzun bir belgeyi özetletmek ya da sohbet geçmişini saklamak istediğinde bu fark doğrudan hissedilir.

### Şimdi sen yaz: verimliliği hesapla

**Görev:** Bir cümlenin Türkçe bilen bir tokenizer'la bölünmüş hâli kodda hazır. Token/sözcük oranını, 1000 token'lık bağlama kaç sözcük sığdığını ve aynı cümleyi 34 token'a bölen bir tokenizer'ın kaç kat pahalı olduğunu hesaplayacaksın.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
tokenlar = ["öğretmen", "ler", "çocuk", "lar", "la", "okul", "da", "konuş", "uyor"]
sozcukler = "öğretmenler çocuklarla okulda konuşuyor".split()
baglam = 1000

# TODO: Token sayısını sözcük sayısına böl.
oran = ___
print("Token/sözcük:", oran)

# TODO: Bağlamı orana böl ve int ile tam sayıya çevir.
sigan = ___
print("1000 token'a sığan sözcük:", sigan)

# TODO: Başka bir tokenizer bu cümleyi 34 token'a bölüyor. Kaç kat fazla?
kat = ___
print("Kat farkı:", round(kat, 2))
```
```text {.python-playground-expected}
Token/sözcük: 2.25
1000 token'a sığan sözcük: 444
Kat farkı: 3.78
```
```text {.python-playground-help}
`oran = ___` | `len(tokenlar)` token sayısını, `len(sozcukler)` sözcük sayısını verir; birini öbürüne böl.
`sigan = ___` | Her sözcük `oran` kadar token tutuyorsa 1000 token'a `baglam / oran` sözcük sığar. Başına `int(...)` koy.
`kat = ___` | 34'ü bizim tokenizer'ın token sayısına (`len(tokenlar)`) böl.
```
```python {.python-playground-solution}
tokenlar = ["öğretmen", "ler", "çocuk", "lar", "la", "okul", "da", "konuş", "uyor"]
sozcukler = "öğretmenler çocuklarla okulda konuşuyor".split()
baglam = 1000

# Token sayısını sözcük sayısına böl.
oran = len(tokenlar) / len(sozcukler)
print("Token/sözcük:", oran)

# Bağlamı orana böl ve int ile tam sayıya çevir.
sigan = int(baglam / oran)
print("1000 token'a sığan sözcük:", sigan)

# Başka bir tokenizer bu cümleyi 34 token'a bölüyor. Kaç kat fazla?
kat = 34 / len(tokenlar)
print("Kat farkı:", round(kat, 2))
```

## 3. Kütüphaneyle yap

Gerçek dil modellerinin çoğu, 6.2'de anlattığımız **bayt düzeyinde BPE** kullanır. Aynı deneyi Hugging Face `tokenizers` ile bayt düzeyinde yapalım. `tokenizers`'ı 6.2'deki gibi kur, kodu `verimlilik.py` adıyla kaydet ve `python verimlilik.py` ile çalıştır:

```python
from tokenizers import Tokenizer, models, pre_tokenizers, trainers

TR = ("çocuklar okula gidiyor öğretmenler okulda ders veriyor çocuklar derste kitap okuyor "
      "öğretmenler çocuklara soru soruyor akşam çocuklar evlerine dönüyor evlerde aileler yemek yiyor "
      "aileler çocuklarla konuşuyor çocuklar kitaplarını okuyor ve uyuyor")
EN = ("the children are going to school the teachers are teaching lessons at school "
      "the children are reading books in the lesson the teachers are asking the children questions "
      "in the evening the children are returning to their homes at home the families are eating dinner "
      "the families are talking with the children the children are reading their books and sleeping")


def bayt_bpe(metin):
    tok = Tokenizer(models.BPE())
    tok.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    trainer = trainers.BpeTrainer(vocab_size=320, min_frequency=2, show_progress=False,
                                  initial_alphabet=pre_tokenizers.ByteLevel.alphabet())
    tok.train_from_iterator([metin], trainer=trainer)
    return tok


tr_tok, en_tok = bayt_bpe(TR), bayt_bpe(EN)
for ad, cumle in [("Türkçe", "öğretmenler çocuklarla okulda konuşuyor"),
                  ("İngilizce", "the teachers are talking with the children at school")]:
    print(f"{ad:9} cümle → Türkçe tokenizer: {len(tr_tok.encode(cumle).ids):2} token, "
          f"İngilizce tokenizer: {len(en_tok.encode(cumle).ids):2} token")
print("'ğ' harfi İngilizce tokenizer'da:", len(en_tok.encode("ğ").ids), "token")
```

Beklenen çıktı:

```text
Türkçe    cümle → Türkçe tokenizer: 15 token, İngilizce tokenizer: 41 token
İngilizce cümle → Türkçe tokenizer: 46 token, İngilizce tokenizer: 17 token
'ğ' harfi İngilizce tokenizer'da: 2 token
```

- `pre_tokenizers.ByteLevel(...)`: Metni UTF-8 baytlarına çevirir; başlangıç sözlüğü 256 bayttır (`initial_alphabet`). Hiçbir karakter bilinmeyen olmaz.
- Sonuç 2.2'dekiyle aynı tabloyu verir: Her dil kendi tokenizer'ında az, öbürününkinde 2.5–3 kat fazla token tutuyor. (Sayılar biraz farklı, çünkü bayt düzeyinde sözcük başındaki boşluk da token'ın parçasıdır.)
- `'ğ'` İngilizce tokenizer'da **2 token**: `ğ` UTF-8'de 2 bayttır (4.1) ve İngilizce metinde hiç geçmediği için iki bayt hiç birleştirilmemiştir. Türkçe harflerin çoğu bu yüzden İngilizce ağırlıklı tokenizer'larda pahalıdır.

Hazır bir modelin tokenizer'ını Türkçe metinde denemek istersen, Hugging Face'teki modellerin tokenizer'larını `AutoTokenizer.from_pretrained(...)` ile indirip aynı ölçüleri (token/sözcük) hesaplayabilirsin. Bunun için `transformers` kütüphanesi ve internet bağlantısı gerekir.

## 4. Sık yapılan hatalar

- **Farklı dillerin sözcük sayılarını doğrudan karşılaştırmak.** Türkçe aynı anlamı daha az ama daha uzun sözcükle söyler. Adil karşılaştırma, **aynı anlamdaki** metinlerin token sayılarıdır.
- **Tokenizer'ı modelden bağımsız değiştirebileceğini sanmak.** Bir modelin tokenizer'ı onunla birlikte eğitilmiştir; daha verimli bir tokenizer kullanmak için modelin de onunla eğitilmesi gerekir.
- **Perplexity'leri farklı tokenizer'lar arasında karşılaştırmak.** Bir token'ın ne kadar metin taşıdığı değiştiği için token başına kayıp karşılaştırılamaz (6.1). Karakter ya da sözcük başına ölçmek gerekir.
- **Yalnızca küçük örneklere bakmak.** Bu dersteki metinler çok küçük; gerçek ölçüm için binlerce cümlelik, gerçek kullanımı temsil eden bir metinde ölç.
- **Türkçeyi "token'a pahalı bir dil" sanmak.** Deneyde gördüğün gibi Türkçeyle eğitilmiş bir tokenizer, Türkçe metni İngilizcenin kendi tokenizer'ındaki kadar verimli böler.

## 5. Pekiştir

**Quiz**

1. Token/sözcük oranı neyi ölçer? Küçük mü olması iyidir, büyük mü?
2. Aynı cümle bir tokenizer'da 13, öbüründe 34 token tutuyorsa bunun maliyet ve bağlam üzerindeki etkisi nedir?
3. 2.2'deki deneyde Türkçe cümle İngilizce tokenizer'da neden çok token tuttu?
4. `ğ` harfi bayt düzeyinde bir İngilizce tokenizer'da neden 2 token tutar?
5. Farklı tokenizer'lara sahip iki modelin perplexity'si neden doğrudan karşılaştırılamaz?

**Alıştırmalar**

1. 2.1'deki bölmelere üçüncü bir tokenizer ekle: her sözcüğü tek token sayan bir bölme (`cumle.split()`). Oranlar ne oluyor? Bu tokenizer'ın sorunu ne olurdu?
2. 2.2'de `egit(metin, n=60)` yerine `n=20` dene. Tablo nasıl değişti?
3. 2.2'deki Türkçe metni iki katına çıkar (birkaç yeni cümle ekle: `öğretmenler evlerine dönüyor` gibi). Türkçe cümlenin token sayısı azaldı mı?
4. 2.3'te bağlamı `8000` token yap. İki tokenizer'a kaç sözcük sığar?
5. (İsteğe bağlı) 3. bölümdeki kodda bir Türkçe tokenizer'a `"ğ"` ver. Kaç token tutuyor? Neden?

??? success "Quiz cevapları"
    1. Bir sözcüğün ortalama kaç token'a bölündüğünü. Küçük olması iyidir: aynı metin daha az token tutar.
    2. İkinci tokenizer aynı iş için yaklaşık 2.6 kat daha fazla ücret ve süre gerektirir; bağlam penceresine 2.6 kat daha az metin sığar.
    3. İngilizce tokenizer Türkçe sözcük parçalarını (ekler, kökler) hiç görmediği için onları birleştirmeyi öğrenmedi; sözcükler neredeyse harf harf bölündü.
    4. `ğ`, UTF-8'de 2 bayttır. İngilizce eğitim metninde hiç geçmediği için bu iki bayt hiç birleştirilmedi ve iki ayrı token olarak kaldı.
    5. Perplexity token başına ölçülür; tokenizer'lar farklıysa bir token'ın taşıdığı metin miktarı farklıdır. Karşılaştırma için karakter ya da sözcük başına ölçü gerekir.

## Özet

Bir tokenizer'ın verimliliği, aynı metni kaç token'a böldüğüyle ölçülür; token/sözcük oranı ve token başına karakter iki basit ölçüdür. Token sayısı doğrudan maliyeti, bağlama sığan metin miktarını ve üretim süresini belirler. Deneyde gördük ki bir tokenizer, eğitildiği dildeki metni verimli, başka dildeki metni verimsiz böler: Türkçe metin, İngilizce ağırlıklı bir tokenizer'da 2.5–3 kat fazla token tutabilir. Sorun Türkçenin kendisinde değil; Türkçeyle eğitilmiş bir tokenizer bu farkı kapatır. Sıradaki derste kendi Türkçe dil modelimizi eğiteceğiz.

## Kaynaklar

- Aleksandar Petrov ve ark. (2023), *Language Model Tokenizers Introduce Unfairness Between Languages*, NeurIPS
- Phillip Rust ve ark. (2021), *How Good is Your Tokenizer? On the Monolingual Performance of Multilingual Language Models*, ACL
- [Hugging Face `tokenizers` belgeleri: bayt düzeyinde BPE](https://huggingface.co/docs/tokenizers/api/pre-tokenizers#tokenizers.pre_tokenizers.ByteLevel)
