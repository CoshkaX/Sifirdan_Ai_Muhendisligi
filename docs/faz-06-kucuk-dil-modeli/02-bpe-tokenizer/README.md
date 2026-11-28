# Faz 6 – Ders 2: BPE tokenizer

> ⏱️ Tahmini süre: 60-75 dk · 📚 Ön koşul: 4.1 Metni sayılara dönüştürmek, 4.2 Türkçe biçimbilim, 6.1 Sonraki token tahmini · 💻 Gereksinim: Python 3.11+, ek paket yok; Hugging Face örneği için `tokenizers` kurulmalıdır

## Bu derste ne öğreneceksin?

- Alt-kelime sözlüğünün elle değil **veriden öğrenilmesini**
- **BPE** (Byte Pair Encoding) algoritmasını adım adım
- En sık çifti bulup birleştirmeyi ve bunu tekrarlamayı
- Öğrenilen birleştirmelerle yeni bir sözcüğü token'lara bölmeyi
- Görülmemiş karakterlerin neden sessizce kaybolabileceğini ve çözümünü

## 1. Problem

4.1'de açgözlü bir alt-kelime tokenizer'ı yazdık, ama sözlüğü **elle** hazırladık: `ev`, `ler`, `imiz`, `den`... Gerçek bir dil modeli yüz binlerce sözcük biçimi görür; sözlüğü elle yazmak imkânsızdır. Ayrıca 4.1'de sözlükte olmayan bir kök `[BİLİNMEYEN]` oluyordu.

İstediğimiz şey, sözlüğü **metnin kendisinden** öğrenen bir yöntem. **BPE** (Byte Pair Encoding, "bayt çifti kodlaması") bunu çok basit bir fikirle yapar:

1. Her sözcüğü karakterlerine böl.
2. Metinde en sık yan yana gelen iki parçayı bul.
3. Bu ikisini tek bir parçaya **birleştir** ve sözlüğe ekle.
4. Yeterince birleştirme yapana kadar 2. adıma dön.

Sık geçen karakter dizileri (Türkçede kökler ve ekler) zamanla tek bir token olur. GPT ailesi gibi pek çok dil modeli BPE'nin bir türünü kullanır.

## 2. Kendin yaz

### 2.1 Bir birleştirme adımı

Sözcükleri parça demetleri olarak, kaç kez geçtikleriyle birlikte tutarız. Her sözcükte yan yana gelen parça çiftlerini, sözcüğün sıklığı kadar sayarız. En sık çifti birleştiririz:

```python {.python-playground}
from collections import Counter

sozcukler = {("k", "e", "d", "i"): 3, ("k", "e", "l", "e", "r"): 2, ("e", "l"): 1}

sayilar = Counter()
for parcalar, sayi in sozcukler.items():
    for i in range(len(parcalar) - 1):
        sayilar[(parcalar[i], parcalar[i + 1])] += sayi

print("Çift sayıları:", dict(sayilar.most_common(4)))
en_sik = max(sayilar, key=sayilar.get)
print("Birleştirilecek:", en_sik)

yeni = {}
for parcalar, sayi in sozcukler.items():
    birlesik = []
    i = 0
    while i < len(parcalar):
        if i < len(parcalar) - 1 and (parcalar[i], parcalar[i + 1]) == en_sik:
            birlesik.append(parcalar[i] + parcalar[i + 1])
            i += 2
        else:
            birlesik.append(parcalar[i])
            i += 1
    yeni[tuple(birlesik)] = sayi
print("Birleştirmeden sonra:", list(yeni))
```
```text {.python-playground-expected}
Çift sayıları: {('k', 'e'): 5, ('e', 'd'): 3, ('d', 'i'): 3, ('e', 'l'): 3}
Birleştirilecek: ('k', 'e')
Birleştirmeden sonra: [('ke', 'd', 'i'), ('ke', 'l', 'e', 'r'), ('e', 'l')]
```
```text {.python-playground-help}
`sozcukler = {("k", "e", "d", "i"): 3, ...}` | Her sözcük karakterlerinin demeti; değeri metinde kaç kez geçtiği. `kedi` 3 kez geçiyor.
`sayilar[(parcalar[i], parcalar[i + 1])] += sayi` | Yan yana iki parça bir çift olur. Sözcük 3 kez geçiyorsa içindeki her çift 3 kez sayılır.
`sayilar.most_common(4)` | En sık 4 çifti verir; yalnızca göstermek için.
`max(sayilar, key=sayilar.get)` | Sayısı en büyük olan çift. Eşitlikte ilk görülen kazanır.
`while i < len(parcalar):` | Sözcüğü soldan sağa dolaşırız. Birleştirilecek çifti görürsek iki parçayı tek parça yapıp iki adım atlarız.
`birlesik.append(parcalar[i] + parcalar[i + 1])` | İki metni `+` ile birleştirmek, ikisini yapıştırır: `"k" + "e" = "ke"`.
```

`k` ile `e` toplam 5 kez yan yana geldiği için ilk birleştirme `ke` oldu. Artık `kedi` 4 değil 3 parçadan, `keler` 5 değil 4 parçadan oluşuyor. BPE bu adımı yüzlerce, binlerce kez tekrarlar.

### 2.2 BPE'yi eğitmek ve kullanmak

Şimdi adımı tekrarlayan bir döngü kuralım ve Türkçe ekler içeren küçük bir metinde ne öğrendiğine bakalım. Öğrenilen birleştirmeler **sırasıyla** saklanır. Yeni bir sözcüğü bölmek için onu karakterlerine ayırıp aynı birleştirmeleri aynı sırayla uygularız:

```python {.python-playground}
from collections import Counter

DERLEM = (
    "ev evler evde evden evlerde evlerden evlerimiz evimiz "
    "kitap kitaplar kitapta kitaptan kitaplarda kitaplardan kitaplarımız kitabımız "
    "okul okullar okulda okuldan okullarda okullardan okullarımız okulumuz"
)


def cift_sayilari(sozcukler):
    sayilar = Counter()
    for parcalar, sayi in sozcukler.items():
        for i in range(len(parcalar) - 1):
            sayilar[(parcalar[i], parcalar[i + 1])] += sayi
    return sayilar


def birlestir(parcalar, cift):
    yeni, i = [], 0
    while i < len(parcalar):
        if i < len(parcalar) - 1 and (parcalar[i], parcalar[i + 1]) == cift:
            yeni.append(parcalar[i] + parcalar[i + 1])
            i += 2
        else:
            yeni.append(parcalar[i])
            i += 1
    return tuple(yeni)


def egit(metin, birlestirme_sayisi):
    sozcukler = Counter(tuple(s) for s in metin.split())
    birlestirmeler = []
    for _ in range(birlestirme_sayisi):
        sayilar = cift_sayilari(sozcukler)
        en_sik = max(sayilar, key=sayilar.get)
        if sayilar[en_sik] < 2:
            break
        birlestirmeler.append(en_sik)
        sozcukler = Counter({birlestir(p, en_sik): s for p, s in sozcukler.items()})
    return birlestirmeler


def kodla(sozcuk, birlestirmeler):
    parcalar = tuple(sozcuk)
    for cift in birlestirmeler:
        parcalar = birlestir(parcalar, cift)
    return list(parcalar)


birlestirmeler = egit(DERLEM, 30)
print("Birleştirme sayısı:", len(birlestirmeler))
print("İlk 10:", ["".join(c) for c in birlestirmeler[:10]])
for sozcuk in ["evlerimizden", "kitaplarımızda", "okulumuzdan", "bahçelerde"]:
    print(f"{sozcuk:15} → {kodla(sozcuk, birlestirmeler)}")
```
```text {.python-playground-expected}
Birleştirme sayısı: 27
İlk 10: ['ta', 'ev', 'ki', 'kita', 'la', 'lar', 'ok', 'oku', 'okul', 'kitap']
evlerimizden    → ['evler', 'imiz', 'de', 'n']
kitaplarımızda  → ['kitaplar', 'ımız', 'da']
okulumuzdan     → ['okul', 'u', 'm', 'u', 'z', 'dan']
bahçelerde      → ['b', 'a', 'h', 'ç', 'e', 'l', 'e', 'r', 'de']
```
```text {.python-playground-help}
`Counter(tuple(s) for s in metin.split())` | Metindeki her sözcüğü karakter demetine çevirip kaç kez geçtiğini sayar.
`for _ in range(birlestirme_sayisi):` | En fazla bu kadar birleştirme yaparız; `_` döngü sayacını kullanmayacağımızı söyler.
`if sayilar[en_sik] < 2: break` | En sık çift bile tek bir kez geçiyorsa birleştirmenin anlamı yok; durarak sözlüğün gereksiz şişmesini önleriz.
`sozcukler = Counter({birlestir(p, en_sik): s ...})` | Bütün sözcüklerde aynı çifti birleştirip sözcük listesini güncelleriz.
`kodla(sozcuk, birlestirmeler)` | Yeni bir sözcüğü önce karakterlere ayırır, sonra öğrenilen birleştirmeleri **eğitimdeki sırayla** uygular.
```

BPE hiçbir dil bilgisi kullanmadan kökleri (`ev`, `kitap`, `okul`) ve ekleri (`lar`, `imiz`, `ımız`, `de`, `da`, `dan`) buldu, çünkü bunlar metinde sık tekrar ediyor. Eğitimde hiç görmediği `evlerimizden` sözcüğünü bile anlamlı parçalara böldü.

`bahçelerde` ise ilginç: `bahçe` kökü metinde hiç geçmediği için harflerine ayrıldı, ama **hiçbir şey kaybolmadı**. 4.1'deki `[BİLİNMEYEN]` sorunu burada yok; çünkü en kötü durumda tek tek karakterlere düşeriz. Buna karşın uzun bir dizi token'a dönüştü. Az görülen sözcükler daha çok token tutar: bunu 6.3'te ölçeceğiz.

### 2.3 Ders kodu

Aynı BPE'nin düzenli hâli [`kod/bpe.py`](kod/bpe.py) dosyasında; token'ları yeniden metne çeviren `coz` işlevi de orada. Testler, geri çevirmenin kayıpsız olduğunu ve BPE'nin metni sıkıştırdığını denetler.

```bash
cd docs/faz-06-kucuk-dil-modeli/02-bpe-tokenizer
python kod/bpe.py
python -m unittest discover -s test -v
```

### Şimdi sen yaz: bir BPE adımı

**Görev:** Üç sözcük ve kaç kez geçtikleri kodda hazır. Yan yana gelen parça çiftlerini sayacak, en sık çifti seçecek ve onu `keler` sözcüğünde birleştireceksin. Ekranda en sık çift ve `keler`'in yeni parçaları görünmeli.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
from collections import Counter

sozcukler = {("k", "e", "d", "i"): 3, ("k", "e", "l", "e", "r"): 2, ("e", "l"): 1}

sayilar = Counter()
for parcalar, sayi in sozcukler.items():
    for i in range(len(parcalar) - 1):
        # TODO: Yan yana iki parçayı bir çift (demet) olarak say; sözcüğün sıklığı kadar ekle.
        sayilar[___] += sayi

# TODO: En sık görülen çifti seç (max ile, sayılara göre).
en_sik = ___
print("En sık çift:", en_sik, "→", sayilar[en_sik], "kez")

parcalar = ("k", "e", "l", "e", "r")
yeni = []
i = 0
while i < len(parcalar):
    if i < len(parcalar) - 1 and (parcalar[i], parcalar[i + 1]) == en_sik:
        # TODO: İki parçayı birleştirip tek parça olarak ekle.
        yeni.append(___)
        i += 2
    else:
        yeni.append(parcalar[i])
        i += 1
print("keler →", yeni)
```
```text {.python-playground-expected}
En sık çift: ('k', 'e') → 5 kez
keler → ['ke', 'l', 'e', 'r']
```
```text {.python-playground-help}
`sayilar[___]` | Çift, `i`. ve `i + 1`. parçadan oluşan bir demettir: `(parcalar[i], parcalar[i + 1])`.
`en_sik = ___` | `max`'a hangi değere göre karşılaştıracağını söyle: `key=sayilar.get` her çiftin sayısını verir.
`yeni.append(___)` | İki metni `+` ile yapıştır: `parcalar[i] + parcalar[i + 1]`.
```
```python {.python-playground-solution}
from collections import Counter

sozcukler = {("k", "e", "d", "i"): 3, ("k", "e", "l", "e", "r"): 2, ("e", "l"): 1}

sayilar = Counter()
for parcalar, sayi in sozcukler.items():
    for i in range(len(parcalar) - 1):
        # Yan yana iki parçayı bir çift (demet) olarak say; sözcüğün sıklığı kadar ekle.
        sayilar[(parcalar[i], parcalar[i + 1])] += sayi

# En sık görülen çifti seç (max ile, sayılara göre).
en_sik = max(sayilar, key=sayilar.get)
print("En sık çift:", en_sik, "→", sayilar[en_sik], "kez")

parcalar = ("k", "e", "l", "e", "r")
yeni = []
i = 0
while i < len(parcalar):
    if i < len(parcalar) - 1 and (parcalar[i], parcalar[i + 1]) == en_sik:
        # İki parçayı birleştirip tek parça olarak ekle.
        yeni.append(parcalar[i] + parcalar[i + 1])
        i += 2
    else:
        yeni.append(parcalar[i])
        i += 1
print("keler →", yeni)
```

## 3. Kütüphaneyle yap

Hugging Face'in `tokenizers` kütüphanesi BPE'yi hızlı bir Rust koduyla eğitir; büyük dil modellerinin tokenizer'ları böyle hazırlanır. Kur:

```bash
python -m pip install tokenizers
```

Kodu ders klasöründe `hf_bpe.py` adıyla kaydet ve `python hf_bpe.py` ile çalıştır:

```python
import sys

sys.path.insert(0, "kod")
from bpe import DERLEM

from tokenizers import Tokenizer, models, pre_tokenizers, trainers


def tokenizer_egit(bilinmeyen=None):
    model = models.BPE(unk_token=bilinmeyen) if bilinmeyen else models.BPE()
    tok = Tokenizer(model)
    tok.pre_tokenizer = pre_tokenizers.Whitespace()
    ozel = [bilinmeyen] if bilinmeyen else []
    trainer = trainers.BpeTrainer(vocab_size=60, min_frequency=2, special_tokens=ozel, show_progress=False)
    tok.train_from_iterator([DERLEM], trainer=trainer)
    return tok


tok = tokenizer_egit()
print("Sözlük boyutu:", tok.get_vocab_size())
for sozcuk in ["evlerimizden", "kitaplarımızda", "bahçelerde"]:
    print(f"{sozcuk:15} → {tok.encode(sozcuk).tokens}")

tok_unk = tokenizer_egit(bilinmeyen="[UNK]")
print("[UNK] ile       →", tok_unk.encode("bahçelerde").tokens)
```

Beklenen çıktı:

```text
Sözlük boyutu: 46
evlerimizden    → ['evler', 'imiz', 'de', 'n']
kitaplarımızda  → ['kitap', 'larımız', 'da']
bahçelerde      → ['b', 'a', 'e', 'ler', 'de']
[UNK] ile       → ['b', 'a', '[UNK]', '[UNK]', 'e', 'ler', 'de']
```

- `models.BPE()`: BPE modeli. `Whitespace()` metni önce sözcüklere ayırır; birleştirmeler sözcük sınırını geçmez (bizimki gibi).
- `BpeTrainer(vocab_size=60, min_frequency=2)`: Sözlük en fazla 60 token olur; 2'den az görülen çiftler birleştirilmez.
- Sonuçlar bizimkine çok benzer ama birebir aynı değil (`kitap` + `larımız`). Kütüphane eşitlikleri farklı bozar ve sözlük boyutuna göre durur.

!!! warning "`h` ve `ç` nereye gitti?"
    İlk tokenizer `bahçelerde` sözcüğünü `['b', 'a', 'e', 'ler', 'de']` olarak böldü: **`h` ve `ç` sessizce kayboldu.** Bu harfler eğitim metninde hiç geçmediği için sözlükte yoklar ve bilinmeyen token tanımlanmadığı için kütüphane onları atladı. `[UNK]` (bilinmeyen) token'ı tanımlayınca en azından bir şeyin eksik olduğu görünür oluyor.

    Gerçek dil modelleri bu sorunu **bayt düzeyinde BPE** ile çözer (GPT-2 ve sonrası): Başlangıç sözlüğü karakterler değil, 256 olası **bayttır**. Her metin UTF-8 baytlarına (4.1) çevrilebildiği için hiçbir karakter bilinmeyen olmaz. Bedeli: Türkçe `ç`, `ğ`, `ş` gibi harfler ikişer bayt olduğundan, öğrenilmemişlerse iki token tutar.

## 4. Sık yapılan hatalar

- **Birleştirmeleri sırasız uygulamak.** Kodlama, eğitimdeki **sırayla** yapılmalıdır; çünkü sonraki birleştirmeler öncekilerin ürettiği parçaları kullanır (`ki` + `ta` → `kita`, sonra `kita` + `p`).
- **Çift sayarken sözcük sıklığını unutmak.** Metinde 1000 kez geçen bir sözcüğün çiftleri, bir kez geçenden çok daha önemlidir.
- **Birleştirmeyi sözcük sınırından geçirmek.** "ev de" ile "evde" karışmasın diye birleştirmeleri sözcüklerin içinde tutarız; boşluk ayrı ele alınır.
- **Bilinmeyen karakterleri düşünmemek.** Eğitim metninde görülmemiş bir karakter, tokenizer'a göre sessizce kaybolabilir. Bayt düzeyinde BPE ya da `[UNK]` token'ı kullan ve geri çevirmenin (kodla → çöz) özgün metni verdiğini test et.
- **Tokenizer'ı modelden ayrı düşünmek.** Model, tokenizer'ın ürettiği numaralarla eğitilir. Eğitimden sonra tokenizer'ı değiştirirsen model anlamsızlaşır; ikisi birlikte saklanır.
- **Daha büyük sözlüğün her zaman daha iyi olduğunu sanmak.** Büyük sözlük dizileri kısaltır, ama gömme tablosu büyür ve nadir token'lar az öğrenilir. Sözlük boyutu bir dengedir.

## 5. Pekiştir

**Quiz**

1. BPE'nin her adımında ne yapılır?
2. Neden çift sayarken sözcüğün sıklığını kullanırız?
3. Yeni bir sözcüğü bölerken birleştirmeleri neden eğitimdeki sırayla uygularız?
4. Bizim BPE'mizde eğitimde görülmemiş bir kök neden `[BİLİNMEYEN]` olmaz?
5. Bayt düzeyinde BPE hangi sorunu çözer, Türkçeye etkisi nedir?

**Alıştırmalar**

1. 2.1'de `sozcukler`'e `("k", "e", "l"): 4` ekle. Birleştirilecek çift değişti mi?
2. 2.2'de `egit(DERLEM, 30)` yerine `10` ve `5` dene. `evlerimizden` nasıl bölünüyor?
3. 2.2'deki derleme `bahçe bahçeler bahçede` sözcüklerini ekle. `bahçelerde` artık nasıl bölünüyor?
4. (İsteğe bağlı) `kod/bpe.py` dosyasına, bir metnin karakter sayısının token sayısına oranını (sıkıştırma oranı) hesaplayan bir işlev ekle.
5. (İsteğe bağlı) 3. bölümdeki kodda `vocab_size` değerini `40` ve `100` yap. Bölmeler nasıl değişti?

??? success "Quiz cevapları"
    1. Metinde en sık yan yana gelen iki parça bulunur ve her yerde tek bir parçaya birleştirilir; bu yeni parça sözlüğe eklenir.
    2. Sık geçen sözcüklerin parçaları daha önemlidir; sıklıkla ağırlıklandırınca birleştirmeler gerçek metindeki dağılımı yansıtır.
    3. Sonraki birleştirmeler öncekilerin ürettiği parçalardan oluşur. Sıra bozulursa beklenen parçalar oluşmaz ve bölme eğitimdekiyle tutarsız olur.
    4. Başlangıç sözlüğü bütün karakterleri içerir; birleştirilemeyen bir kök en kötü durumda tek tek karakterlere ayrılır.
    5. Her metin bayt dizisine çevrilebildiği için hiçbir karakter bilinmeyen olmaz. Türkçe harflerin çoğu iki bayt olduğundan, öğrenilmemiş Türkçe parçalar daha çok token tutar.

## Özet

BPE, metindeki en sık yan yana gelen parçaları tekrar tekrar birleştirerek alt-kelime sözlüğünü veriden öğrenir. Türkçe bir metinde kökler ve ekler kendiliğinden token olur. Yeni bir sözcük, karakterlerine ayrılıp öğrenilen birleştirmeler sırayla uygulanarak bölünür; görülmemiş parçalar daha küçük parçalara, en kötü durumda karakterlere düşer. Bayt düzeyinde BPE hiçbir karakterin kaybolmamasını garanti eder. Sıradaki derste farklı tokenizer'ların Türkçe metni kaç token'a böldüğünü ve bunun neden önemli olduğunu ölçeceğiz.

## Kaynaklar

- Rico Sennrich, Barry Haddow ve Alexandra Birch (2016), *Neural Machine Translation of Rare Words with Subword Units* (BPE'nin dil işlemede kullanımı)
- Philip Gage (1994), *A New Algorithm for Data Compression* (BPE'nin ilk hâli: sıkıştırma algoritması)
- Alec Radford ve ark. (2019), *Language Models are Unsupervised Multitask Learners* (GPT-2; bayt düzeyinde BPE)
- [Hugging Face `tokenizers` belgeleri](https://huggingface.co/docs/tokenizers)
