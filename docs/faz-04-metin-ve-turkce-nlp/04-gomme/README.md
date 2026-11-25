# Faz 4 – Ders 4: Gömme (embedding): sözcüğü vektöre çevirmek

> ⏱️ Tahmini süre: 50-65 dk · 📚 Ön koşul: 1.1 Vektörler ve matrisler, 4.1 Metni sayılara dönüştürmek, Faz 3 önerilir · 💻 Gereksinim: Python 3.11+, ek paket yok; PyTorch örneği isteğe bağlı

## Bu derste ne öğreneceksin?

- Token numaralarının ve one-hot vektörlerin neden anlam taşımadığını
- **Gömme** (embedding) vektörünün ne olduğunu ve bir tablodan nasıl okunduğunu
- İki vektörün benzerliğini kosinüs benzerliğiyle ölçmeyi
- "Aynı bağlamda geçen sözcükler benzer anlamlıdır" fikriyle küçük bir metinden vektör çıkarmayı
- Türkçenin ekli yapısının gömmeleri nasıl etkilediğini

## 1. Problem

4.1 dersinde metni token'lara bölüp her token'a bir numara verdik: belki `kedi → 12`, `köpek → 87`, `araba → 301`. Bu numaralar yalnızca birer kimliktir. `12` ile `87`'nin birbirine yakın olması, kedi ile köpeğin benzer olduğu anlamına gelmez.

Bir model ise "kedi" ile "köpek"in birbirine "araba"dan daha yakın olduğunu bilebilmeli. Bunun için her token'ı tek bir sayıyla değil, birkaç sayıdan oluşan bir **vektörle** temsil ederiz. Benzer anlamlı sözcüklerin vektörleri birbirine yakın olur. Bu vektörlere **gömme** (embedding) denir; sözcüğü bir sayı uzayına "gömdüğümüz" için.

Bu derste önce neden basit yolların işe yaramadığını göreceğiz, sonra küçük bir metinden kendi gömmelerimizi çıkaracağız. 4.5 dersinde bu vektörlerle arama yapacağız.

## 2. Kendin yaz

### 2.1 One-hot: herkes herkese eşit uzaklıkta

Numaralardan kurtulmanın ilk yolu **one-hot** gösterimdir (1.6 dersinde etiketler için görmüştük). Sözlükte kaç sözcük varsa o uzunlukta bir vektör kurarız; sözcüğün kendi konumunda `1`, diğer her yerde `0` olur.

```python {.python-playground}
sozluk = ["kedi", "köpek", "araba"]


def one_hot(sozcuk):
    return [1 if s == sozcuk else 0 for s in sozluk]


def nokta_carpim(a, b):
    return sum(x * y for x, y in zip(a, b))


for sozcuk in sozluk:
    print(sozcuk, one_hot(sozcuk))

print("kedi · köpek =", nokta_carpim(one_hot("kedi"), one_hot("köpek")))
print("kedi · araba =", nokta_carpim(one_hot("kedi"), one_hot("araba")))
```
```text {.python-playground-expected}
kedi [1, 0, 0]
köpek [0, 1, 0]
araba [0, 0, 1]
kedi · köpek = 0
kedi · araba = 0
```
```text {.python-playground-help}
`sozluk = ["kedi", "köpek", "araba"]` | Tanıdığımız sözcüklerin listesi. Her sözcüğün konumu onun numarasıdır.
`[1 if s == sozcuk else 0 for s in sozluk]` | Liste üreteci: sözlükteki her sözcük için, aradığımız sözcükse `1`, değilse `0` yazar.
`def nokta_carpim(a, b):` | 1.2 dersindeki noktasal çarpım: aynı konumdaki sayıları çarpıp toplar.
`zip(a, b)` | İki vektörün aynı konumdaki sayılarını eşleştirir.
`nokta_carpim(one_hot("kedi"), one_hot("köpek"))` | İki farklı sözcüğün `1`'leri farklı konumlarda olduğu için çarpımların hepsi `0` olur.
```

İki farklı sözcüğün noktasal çarpımı her zaman `0`. One-hot gösterimde kedi, köpeğe ne kadar yakınsa arabaya da o kadar yakındır; yani hiç benzerlik bilgisi yoktur. Ayrıca 50.000 sözcüklük bir sözlükte her vektör 50.000 sayı uzunluğunda olur ve bunların neredeyse hepsi `0`'dır.

### 2.2 Gömme tablosu: her sözcüğe kısa bir vektör

Şimdi her sözcüğe yalnızca üç sayıdan oluşan bir vektör verelim. Bu örnekte sayıları biz seçiyoruz ve her konuma bir anlam veriyoruz: **canlı mı?**, **evde beslenir mi?**, **taşıt mı?**

Bu vektörleri bir tabloda tutarız. Bir sözcüğün gömmesini almak, tablodaki satırını okumaktan ibarettir. Kütüphanelerde de gömme katmanı tam olarak budur: numarası verilen satırı döndüren bir tablo.

```python {.python-playground}
gomme_tablosu = {
    "kedi":    [0.9, 0.8, 0.0],
    "köpek":   [0.9, 0.7, 0.0],
    "aslan":   [0.9, 0.1, 0.0],
    "araba":   [0.0, 0.1, 0.9],
    "otobüs":  [0.0, 0.0, 1.0],
}


def nokta_carpim(a, b):
    return sum(x * y for x, y in zip(a, b))


for diger in ["köpek", "aslan", "araba"]:
    benzerlik = nokta_carpim(gomme_tablosu["kedi"], gomme_tablosu[diger])
    print(f"kedi · {diger} = {benzerlik:.2f}")
```
```text {.python-playground-expected}
kedi · köpek = 1.37
kedi · aslan = 0.89
kedi · araba = 0.08
```
```text {.python-playground-help}
`gomme_tablosu = {...}` | Her sözcüğün üç sayılık vektörü. Birinci sayı "canlı", ikinci "evde beslenir", üçüncü "taşıt" özelliğine ne kadar uyduğunu anlatıyor.
`"kedi": [0.9, 0.8, 0.0]` | Kedi canlıdır, evde beslenir, taşıt değildir.
`"aslan": [0.9, 0.1, 0.0]` | Aslan da canlıdır ama evde beslenmez; ikinci sayı küçük.
`gomme_tablosu["kedi"]` | Gömmeyi almak = tablodan satır okumak.
`nokta_carpim(...)` | Aynı konumlardaki sayılar birlikte büyükse sonuç büyük olur; vektörler benzer yönü gösteriyor demektir.
`f"{benzerlik:.2f}"` | Sonucu iki ondalık basamakla gösterir.
```

Artık benzerlik anlamlı: kedi köpeğe en yakın, aslana daha uzak, arabaya neredeyse hiç benzemiyor. 1.1 dersinde ev özelliklerini vektörde tuttuğumuz gibi, burada da sözcüğün "özelliklerini" tutuyoruz.

Ama gerçek gömmelerde sayıları biz seçmeyiz; model eğitim sırasında öğrenir. Öğrenilmiş gömmelerde genellikle 100 ile birkaç bin arasında sayı bulunur ve tek tek konumların "canlı mı?" gibi açık bir anlamı yoktur. Anlam, vektörlerin birbirine göre konumunda saklıdır.

### 2.3 Uzunluktan bağımsız benzerlik: kosinüs

Noktasal çarpımın bir sorunu var: Vektör uzunsa (sayıları büyükse) sonuç da büyür. Sık geçen bir sözcüğün vektörü uzun olabilir ve her şeye "benzer" görünür. Bunun yerine iki vektör arasındaki **açıya** bakarız:

`kosinüs benzerliği = (a · b) / (|a| × |b|)`

Burada `|a|`, vektörün uzunluğudur: sayıların karelerinin toplamının karekökü. Sonuç `-1` ile `1` arasındadır; aynı yönü gösteren vektörlerde `1`, dik vektörlerde `0` olur. Ayrıntısını 4.5 dersinde göreceğiz; burada bir sonraki adımda kullanmak için tanımlıyoruz.

### 2.4 Bağlamdan öğrenmek: "bana arkadaşını söyle"

Dilbilimci J. R. Firth'in 1957'deki sözü bu alanın özeti olarak bilinir: *"Bir sözcüğü, arkadaşlarından tanırsın."* Benzer anlamlı sözcükler benzer cümlelerde, benzer sözcüklerin yanında geçer. Kedi de köpek de "mama yedi", "evde uyudu" gibi bağlamlarda görülür; araba ise "yolda gitti" bağlamında.

Bu fikre **dağılımsal varsayım** denir. En basit uygulaması: Her sözcük için, aynı cümlede hangi sözcüklerle kaç kez geçtiğini sayarız. Bu sayılar o sözcüğün vektörü olur.

```python {.python-playground}
import math

cumleler = [
    "kedi süt içti", "köpek su içti",
    "kedi evde uyudu", "köpek evde uyudu",
    "kedi mama yedi", "köpek mama yedi",
    "araba yolda gitti", "otobüs yolda gitti",
    "araba benzin aldı", "otobüs yolcu aldı",
]

sozcukler = sorted({s for c in cumleler for s in c.split()})
vektorler = {s: [0] * len(sozcukler) for s in sozcukler}

for cumle in cumleler:
    parcalar = cumle.split()
    for sozcuk in parcalar:
        for komsu in parcalar:
            if komsu != sozcuk:
                vektorler[sozcuk][sozcukler.index(komsu)] += 1


def kosinus(a, b):
    nokta = sum(x * y for x, y in zip(a, b))
    uzunluk_a = math.sqrt(sum(x * x for x in a))
    uzunluk_b = math.sqrt(sum(y * y for y in b))
    return nokta / (uzunluk_a * uzunluk_b)


for a, b in [("kedi", "köpek"), ("araba", "otobüs"), ("kedi", "araba")]:
    print(f"{a} - {b}: {kosinus(vektorler[a], vektorler[b]):.2f}")
```
```text {.python-playground-expected}
kedi - köpek: 0.83
araba - otobüs: 0.75
kedi - araba: 0.00
```
```text {.python-playground-help}
`cumleler = [...]` | Küçük bir "metin derlemi". Gerçek gömmeler milyonlarca cümleden öğrenilir.
`sorted({s for c in cumleler for s in c.split()})` | Bütün cümlelerdeki sözcükleri toplar; küme tekrarları atar, `sorted` alfabetik sıraya koyar. Bu liste vektörlerin konumlarını belirler.
`vektorler = {s: [0] * len(sozcukler) for s in sozcukler}` | Her sözcük için sözlük uzunluğunda, sıfırlardan oluşan bir sayaç vektörü açarız.
`for sozcuk in parcalar: for komsu in parcalar:` | Aynı cümledeki her sözcük çiftine bakarız.
`vektorler[sozcuk][sozcukler.index(komsu)] += 1` | "Bu sözcük, şu komşuyla bir kez daha birlikte geçti." `index` komşunun vektördeki konumunu bulur.
`def kosinus(a, b):` | 2.3'teki formül: noktasal çarpımı iki vektörün uzunluklarının çarpımına böleriz.
`math.sqrt(sum(x * x for x in a))` | Vektörün uzunluğu: sayıların karelerinin toplamının karekökü.
```

Hiçbir sözcüğün anlamını programa söylemedik; yalnızca hangi sözcüklerin birlikte geçtiğini saydık. Yine de kedi köpeğe, araba otobüse benziyor; kedi ile araba ise hiç ortak bağlama sahip olmadığı için benzerlikleri `0`.

Word2Vec ve GloVe gibi yöntemler bu fikrin gelişmiş hâlleridir: Sayma yerine, bir sinir ağına "bu sözcüğün yanında hangi sözcükler geçer?" sorusunu tahmin ettirir ve 3. fazdaki gibi geri yayılımla vektörleri öğrenirler. Modern dil modellerinin ilk katmanı da böyle öğrenilmiş bir gömme tablosudur.

### 2.5 Türkçe ve gömmeler

Türkçede `kedi`, `kediler`, `kediye`, `kedimizin` farklı yazımlardır. Sözcük düzeyinde çalışan bir yöntem bunların her birine ayrı bir vektör öğrenir ve nadir biçimler için yeterli örnek bulamaz. 2.4'teki koda `"kediler süt içti"` cümlesini eklersen `kediler`, `kedi` ile hiçbir bağı olmayan yepyeni bir sözcük olarak görünür.

Bu sorunu azaltmanın iki yaygın yolu var:

- **Alt-kelime token'ları** (4.1 dersi): `kedi + ler` gibi bölündüğünde `kedi` parçasının vektörü bütün biçimler arasında paylaşılır.
- **Karakter parçaları:** FastText gibi yöntemler bir sözcüğün vektörünü içindeki harf dizilerinin (`ked`, `edi`, `dil`...) vektörlerinden oluşturur. Böylece daha önce hiç görülmemiş bir biçim için bile anlamlı bir vektör üretilebilir. Ekli diller için bu özellikle yararlıdır.

## 3. Kütüphaneyle yap

PyTorch'ta gömme tablosu `nn.Embedding` katmanıdır. İki sayı alır: sözlükteki token sayısı ve her vektörün uzunluğu. Başlangıçta sayılar rastgeledir; model eğitilirken diğer ağırlıklar gibi geri yayılımla güncellenir.

```python
import torch
from torch import nn

sozluk = {"kedi": 0, "köpek": 1, "araba": 2}
gomme = nn.Embedding(num_embeddings=len(sozluk), embedding_dim=4)

numaralar = torch.tensor([sozluk["kedi"], sozluk["araba"]])
vektorler = gomme(numaralar)

print(vektorler.shape)
```

Beklenen çıktı:

```text
torch.Size([2, 4])
```

İki token numarası verdik, her biri için 4 sayılık bir vektör geldi. `gomme.weight` tablonun kendisidir ve `3 × 4` boyutundadır. Bu kodu 3.6 dersindeki gibi PyTorch kurulu bir ortamda çalıştır.

Hazır eğitilmiş Türkçe gömmeler de vardır. Örneğin FastText projesi Türkçe dahil 157 dil için Common Crawl ve Wikipedia'dan eğitilmiş vektörler yayımlamıştır. Bunları indirmek büyük dosyalar gerektirir; 4.5 dersinde önce kendi küçük vektörlerimizle arama yapacağız.

## 4. Sık yapılan hatalar

- **Token numarasını anlam taşıyan bir sayı sanmak.** `301 > 12` olması hiçbir şey ifade etmez; numara yalnızca tablodaki satırı gösterir.
- **Gömmelerin tek tek konumlarına anlam yüklemek.** Bu derste konumlara anlam verdik, ama öğrenilmiş gömmelerde "3. sayı canlılığı gösterir" gibi bir kural yoktur.
- **Uzunluğu farklı vektörleri noktasal çarpımla karşılaştırmak.** Sık geçen sözcüklerin vektörleri uzun olabilir; kosinüs benzerliği bu etkiyi ortadan kaldırır.
- **Benzerliği eş anlamlılık sanmak.** "iyi" ve "kötü" çok benzer bağlamlarda geçer ("film çok ..."); bu yüzden gömmeleri birbirine yakın çıkabilir. Benzer bağlam, aynı anlam demek değildir.
- **Gömmelerin önyargıdan bağımsız olduğunu sanmak.** Gömmeler, öğrenildikleri metinlerdeki kalıpları taşır. Metinlerde bir meslek hep tek bir cinsiyetle anılıyorsa vektörler de bunu yansıtır.

## 5. Pekiştir

**Quiz**

1. Token numaraları neden doğrudan benzerlik ölçmek için kullanılamaz?
2. One-hot gösterimde iki farklı sözcüğün noktasal çarpımı neden hep `0`'dır?
3. Gömme tablosundan bir sözcüğün vektörünü almak ne anlama gelir?
4. Dağılımsal varsayım ne söyler?
5. `kediler` ve `kedi` sözcük düzeyindeki bir yöntemde neden ayrı vektörler alır? Bu nasıl azaltılabilir?

**Alıştırmalar**

1. 2.2'deki tabloya `"tavşan"` ekle ve vektörünü sen seç. Kedi ile benzerliği köpekten daha mı yüksek, daha mı düşük olmalı?
2. 2.2'deki benzerlikleri noktasal çarpım yerine 2.4'teki `kosinus` fonksiyonuyla hesapla. Sıralama değişiyor mu?
3. 2.4'teki cümlelere `"kedi yolda gitti"` ekle. Kedi-araba benzerliği nasıl değişti? Neden?
4. 2.4'e `"kediler süt içti"` ekle ve `kedi` ile `kediler` arasındaki benzerliği yazdır. Sonucu 2.5 bölümüyle ilişkilendir.
5. (İsteğe bağlı) 2.4'te bütün cümlelerin sonundaki fiillerin (`içti`, `uyudu`...) bağlam olarak sayılmamasını sağla. Benzerlikler nasıl değişti? Hangi sözcükler en çok bilgi taşıyor?

??? success "Quiz cevapları"
    1. Numaralar yalnızca kimliktir; iki numaranın birbirine yakın olması anlamların yakın olduğunu göstermez.
    2. Her sözcüğün `1`'i farklı bir konumdadır; aynı konumda ikisinin de sıfırdan farklı sayısı olmaz.
    3. Tabloda o sözcüğün numarasına karşılık gelen satırı okumak.
    4. Benzer anlamlı sözcüklerin benzer bağlamlarda, benzer komşu sözcüklerle birlikte geçtiğini.
    5. Yazımları farklı olduğu için iki ayrı token'dır. Alt-kelime bölmesi (`kedi + ler`) veya karakter parçalarından vektör kurmak (FastText) ortak kökü paylaştırır.

## Özet

Token numaraları ve one-hot vektörler sözcükler arasındaki benzerliği taşımaz. Gömmeler, her token'ı kısa bir sayı vektörüyle temsil eder; benzer anlamlı token'ların vektörleri birbirine yakın olur. Bir gömme katmanı, numarası verilen satırı döndüren bir tablodur. Vektörler, sözcüklerin hangi bağlamlarda geçtiğinden öğrenilir; benzerliklerini uzunluktan bağımsız ölçmek için kosinüs benzerliği kullanılır. Türkçede ekli biçimler, alt-kelime veya karakter parçalarıyla ortak bir kök vektörü paylaşabilir.

## Kaynaklar

- J. R. Firth (1957), *A synopsis of linguistic theory 1930–1955*
- Mikolov ve ark. (2013), *Efficient Estimation of Word Representations in Vector Space* (Word2Vec)
- Bojanowski ve ark. (2017), *Enriching Word Vectors with Subword Information* (FastText)
- [FastText: 157 dil için hazır sözcük vektörleri](https://fasttext.cc/docs/en/crawl-vectors.html)
- [PyTorch resmî belgesi: `nn.Embedding`](https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html)
