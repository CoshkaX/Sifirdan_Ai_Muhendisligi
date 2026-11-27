# Faz 5 – Ders 6: Mini transformer

> ⏱️ Tahmini süre: 60-80 dk · 📚 Ön koşul: 5.2–5.5, 3.6 PyTorch'a geçiş · 💻 Gereksinim: Python 3.11+; sayfadaki pencereler ek paketsiz çalışır, asıl model için PyTorch kurulmalıdır

## Bu derste ne öğreneceksin?

- Bütün parçaları (gömme, konum, bloklar, çıkış katmanı) tek bir modelde birleştirmeyi
- Modeli sonraki token'ı tahmin etmeye **çapraz entropi** ile eğitmeyi
- Maskenin eğitimde neden zorunlu olduğunu: maskesiz model geleceğe bakıp kopya çeker
- Kaybın neden `0`'a inmediğini ve bunun neyi gösterdiğini
- Eğitilmiş modelden token **üretmeyi**

## 1. Problem

5.1'de bigram modeli "su içti" ile "süt içti" arasındaki farkı göremiyordu, çünkü yalnızca bir önceki token'a bakıyordu. Şimdi attention, konum, blok ve normalizasyonu elimizde tutuyoruz. Bunlarla kurulan bir modelin gerçekten daha iyi olduğunu görelim.

Küçük, ama bağlama bakmayı zorunlu kılan bir görev seçtik: **dizi `a b a b a b a b` biçimindedir ve `a` ile `b` her dizide rastgele seçilir.** İlk iki token'dan sonrasını tahmin etmek için modelin "iki önce ne vardı?" diye bakması gerekir. Tek bir önceki token yetmez, çünkü `a` sonrasında `b`'nin ne olduğu diziye göre değişir.

Bu, günümüzün dil modellerinin yaptığı işin minyatürüdür: bağlama bakıp sıradaki token'ı tahmin etmek. Fark yalnızca ölçektir.

## 2. Kendin yaz

### 2.1 Görev ve bigram'ın başarısızlığı

Önce verinin nasıl göründüğüne ve 5.1'deki bigram'ın bu görevde ne kadar başarılı olduğuna bakalım. Bigram her token'dan sonra en sık gelen token'ı tahmin eder:

```python {.python-playground}
import random

SOZLUK = 8
r = random.Random(0)


def dizi_uret():
    a, b = r.randrange(SOZLUK), r.randrange(SOZLUK)
    return [a, b] * 4


for _ in range(3):
    print(dizi_uret())

sayac = {}
for dizi in [dizi_uret() for _ in range(2000)]:
    for onceki, sonraki in zip(dizi, dizi[1:]):
        sayac.setdefault(onceki, {})
        sayac[onceki][sonraki] = sayac[onceki].get(sonraki, 0) + 1

dogru = toplam = 0
for dizi in [dizi_uret() for _ in range(1000)]:
    for t in range(1, len(dizi) - 1):
        secenekler = sayac[dizi[t]]
        tahmin = max(secenekler, key=secenekler.get)
        toplam += 1
        dogru += tahmin == dizi[t + 1]

print("Bigram doğruluğu:", round(dogru / toplam, 2), "(rastgele tahmin: 0.12)")
```
```text {.python-playground-expected}
[6, 6, 6, 6, 6, 6, 6, 6]
[0, 4, 0, 4, 0, 4, 0, 4]
[7, 6, 7, 6, 7, 6, 7, 6]
Bigram doğruluğu: 0.11 (rastgele tahmin: 0.12)
```
```text {.python-playground-help}
`random.Random(0)` | Sabit tohumlu bir rastgele sayı üreteci; her çalıştırmada aynı diziler çıkar.
`[a, b] * 4` | İki token'lık listeyi 4 kez tekrarlar: `a b a b a b a b`.
`zip(dizi, dizi[1:])` | Her token'ı kendinden sonra gelenle eşleştirir (5.1'deki bigram sayımı).
`max(secenekler, key=secenekler.get)` | Sözlükte sayısı en yüksek olan seçeneği bulur.
`dogru += tahmin == dizi[t + 1]` | Doğruysa `True` (`1`), yanlışsa `False` (`0`) toplanır.
`for t in range(1, len(dizi) - 1)` | İlk hedef (`b`) rastgele olduğu için tahmin etmiyoruz; ikinci hedeften başlıyoruz.
```

Bigram'ın doğruluğu şansa yakın (`1/8 = 0.125`). Her token'dan sonra hangi token'ın geleceği diziye göre değiştiği için bir önceki token yeterli değil. Model, **iki önce** gelen token'a bakmalı.

### 2.2 Attention bu işi nasıl çözer?

5.2'de her token'ın bağlamdaki başka bir token'a ne kadar dikkat edeceğini ağırlıklarla belirlemiştik. Burada ideal bir attention şöyle olurdu: `t` konumundaki token, **bir önceki konuma** (`t - 1`) tam dikkat verir, diğerlerine hiç. Ağırlıklı toplam, o token'ın kopyasıdır. İşte bunu elle kurup, eğitimde modelin neyi öğrenmesi gerektiğini görelim:

```python {.python-playground}
dizi = [3, 5, 3, 5, 3, 5, 3, 5]
girdi, hedef = dizi[:-1], dizi[1:]

dogru = 0
for t in range(1, len(girdi)):
    agirliklar = [1.0 if j == t - 1 else 0.0 for j in range(t + 1)]
    tahmin = round(sum(w * girdi[j] for j, w in enumerate(agirliklar)))
    dogru += tahmin == hedef[t]
    print(f"konum {t}: ağırlıklar {agirliklar} → tahmin {tahmin}, hedef {hedef[t]}")

print("Doğru:", dogru, "/", len(girdi) - 1)
```
```text {.python-playground-expected}
konum 1: ağırlıklar [1.0, 0.0] → tahmin 3, hedef 3
konum 2: ağırlıklar [0.0, 1.0, 0.0] → tahmin 5, hedef 5
konum 3: ağırlıklar [0.0, 0.0, 1.0, 0.0] → tahmin 3, hedef 3
konum 4: ağırlıklar [0.0, 0.0, 0.0, 1.0, 0.0] → tahmin 5, hedef 5
konum 5: ağırlıklar [0.0, 0.0, 0.0, 0.0, 1.0, 0.0] → tahmin 3, hedef 3
konum 6: ağırlıklar [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0] → tahmin 5, hedef 5
Doğru: 6 / 6
```
```text {.python-playground-help}
`girdi, hedef = dizi[:-1], dizi[1:]` | Girdi, son token hariç dizi; hedef, ilk token hariç dizi. Her konumda hedef, girdinin **bir sonraki** token'ıdır.
`for j in range(t + 1)` | `t` konumundaki token yalnızca kendine ve öncesine bakabilir (maske, 5.2).
`1.0 if j == t - 1 else 0.0` | `t - 1` konumuna tam dikkat, diğerlerine sıfır.
`sum(w * girdi[j] ...)` | 5.2'deki ağırlıklı toplam. Ağırlıklar `1` ve `0` olduğu için bir önceki token'ın kendisi çıkar.
`round(...)` | Toplam bir ondalıklı sayıdır; token numarasına yuvarlarız.
```

Bu elle kurulmuş attention görevi eksiksiz çözüyor: 6 tahminin 6'sı doğru. Gerçek bir modelde bu ağırlıkları kimse elle yazmaz: model **eğitimde** kendisi bulur. Bizim işimiz modelin bunu öğrenebileceği yapıyı kurmak ve eğitim sinyali (kayıp) vermek.

### Şimdi sen yaz: elle kopyalama ve kaçınılmaz kayıp

**Görev:** Bir dizi kodda hazır (`4 1 4 1 4 1 4 1`). Modelin öğrendiği işi elle yapacaksın: her konumda bir önceki token'a bakıp onu kopyalayarak sonrakini tahmin edeceksin. Sonra eğitimde kaybın neden `0`'a inmediğini hesaplayacaksın. Ekranda doğru tahmin sayısı ve kaçınılmaz kayıp görünmeli.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
import math

dizi = [4, 1, 4, 1, 4, 1, 4, 1]
dogru = 0
toplam = 0

for t in range(1, len(dizi) - 1):
    # TODO: Model, t konumunda bir önceki konumdaki token'ı kopyalar.
    tahmin = dizi[___]
    toplam += 1
    # TODO: Gerçek sonraki token dizi[t + 1]'dir. Tahmin ona eşitse doğru say.
    if tahmin == ___:
        dogru += 1

# TODO: İlk hedef rastgele, tahmin edilemez ve kaybı ln(8)'dir. 7 hedefin ortalaması: ln(8) / 7.
kacinilmaz_kayip = ___

print("Doğruluk:", dogru, "/", toplam)
print("Kaçınılmaz kayıp:", round(kacinilmaz_kayip, 3))
```
```text {.python-playground-expected}
Doğruluk: 6 / 6
Kaçınılmaz kayıp: 0.297
```
```text {.python-playground-help}
`tahmin = dizi[___]` | Bir önceki konum, `t`'den bir geridedir: `t - 1`.
`if tahmin == ___:` | Hedef, `t` konumundaki token'ın hemen sonrasıdır: `dizi[t + 1]`.
`kacinilmaz_kayip = ___` | Doğal logaritma için `math.log(8)` kullan; 7 hedefin ortalaması için `7`'ye böl.
```
```python {.python-playground-solution}
import math

dizi = [4, 1, 4, 1, 4, 1, 4, 1]
dogru = 0
toplam = 0

for t in range(1, len(dizi) - 1):
    # Model, t konumunda bir önceki konumdaki token'ı kopyalar.
    tahmin = dizi[t - 1]
    toplam += 1
    # Gerçek sonraki token dizi[t + 1]'dir. Tahmin ona eşitse doğru say.
    if tahmin == dizi[t + 1]:
        dogru += 1

# İlk hedef rastgele, tahmin edilemez ve kaybı ln(8)'dir. 7 hedefin ortalaması: ln(8) / 7.
kacinilmaz_kayip = math.log(8) / 7

print("Doğruluk:", dogru, "/", toplam)
print("Kaçınılmaz kayıp:", round(kacinilmaz_kayip, 3))
```

## 3. Kütüphaneyle yap

Aşağıda bütün parçaları birleştiren eksiksiz program var. Kodu `mini_transformer.py` adıyla kaydet ve `python mini_transformer.py` ile çalıştır. (Aynı kodu ve testlerini proje klasöründe `docs/faz-05-transformer/06-mini-transformer/kod/` içinde bulabilirsin.) PyTorch'u 3.6'daki gibi kur.

```python
"""Ders 5.6 – Mini transformer: sonraki token'ı tahmin etmeyi öğrenen küçük bir model.

PyTorch gerekir. Çalıştır:  python kod/mini_transformer.py

Görev: Dizi "a b a b a b a b" biçimindedir ve a ile b her dizide rastgele seçilir.
Model, her konumda sonraki token'ı tahmin eder. Bunun için bağlamda geriye bakması gerekir.
"""

import math

import torch
from torch import nn

SOZLUK, UZUNLUK, D, KAFA, KATMAN = 8, 8, 32, 2, 2


def veri_uret(n):
    """n tane (n, UZUNLUK) boyutlu dizi üretir: a b a b a b a b."""
    a = torch.randint(0, SOZLUK, (n, 1))
    b = torch.randint(0, SOZLUK, (n, 1))
    return torch.cat([a, b] * (UZUNLUK // 2), dim=1)


class Blok(nn.Module):
    def __init__(self, d, kafa_sayisi):
        super().__init__()
        self.norm1 = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, kafa_sayisi, batch_first=True)
        self.norm2 = nn.LayerNorm(d)
        self.ffn = nn.Sequential(nn.Linear(d, 4 * d), nn.ReLU(), nn.Linear(4 * d, d))

    def forward(self, x, maske):
        h = self.norm1(x)
        x = x + self.attn(h, h, h, attn_mask=maske, need_weights=False)[0]
        return x + self.ffn(self.norm2(x))


class MiniTransformer(nn.Module):
    def __init__(self, maskeli=True):
        super().__init__()
        self.maskeli = maskeli
        self.token_gomme = nn.Embedding(SOZLUK, D)
        self.konum_gomme = nn.Embedding(UZUNLUK - 1, D)
        self.bloklar = nn.ModuleList([Blok(D, KAFA) for _ in range(KATMAN)])
        self.norm = nn.LayerNorm(D)
        self.cikis = nn.Linear(D, SOZLUK)

    def forward(self, idler):
        n, t = idler.shape
        x = self.token_gomme(idler) + self.konum_gomme(torch.arange(t))
        maske = torch.triu(torch.ones(t, t, dtype=torch.bool), diagonal=1) if self.maskeli else None
        for blok in self.bloklar:
            x = blok(x, maske)
        return self.cikis(self.norm(x))


def kayip_hesapla(model, dizi):
    girdi, hedef = dizi[:, :-1], dizi[:, 1:]
    return nn.functional.cross_entropy(model(girdi).reshape(-1, SOZLUK), hedef.reshape(-1))


def egit(model, adim_sayisi=800, batch=64, ogrenme_hizi=3e-3, kayit_adimlari=(1, 100, 800)):
    optimizer = torch.optim.Adam(model.parameters(), lr=ogrenme_hizi)
    kayitlar = {}
    for adim in range(1, adim_sayisi + 1):
        kayip = kayip_hesapla(model, veri_uret(batch))
        optimizer.zero_grad()
        kayip.backward()
        optimizer.step()
        if adim in kayit_adimlari:
            kayitlar[adim] = kayip.item()
    return kayitlar


def dogruluk(model, n=1000):
    """Tahmin edilebilir hedeflerde (3. token'dan itibaren) doğruluk."""
    with torch.no_grad():
        dizi = veri_uret(n)
        tahmin = model(dizi[:, :-1]).argmax(dim=-1)
    return (tahmin[:, 1:] == dizi[:, 2:]).float().mean().item()


def uret(model, bas, uzunluk=UZUNLUK):
    """Verilen başlangıç token'larından açgözlü (en olası token) üretim."""
    idler = torch.tensor([bas])
    with torch.no_grad():
        while idler.shape[1] < uzunluk:
            sonraki = model(idler)[:, -1].argmax(dim=-1, keepdim=True)
            idler = torch.cat([idler, sonraki], dim=1)
    return idler[0].tolist()


def main():
    torch.manual_seed(0)
    model = MiniTransformer()
    print("Parametre sayısı:", sum(p.numel() for p in model.parameters()))
    print("Kaçınılmaz kayıp:", round(math.log(SOZLUK) / (UZUNLUK - 1), 2))
    for adim, kayip in egit(model).items():
        print(f"Adım {adim}: kayıp {kayip:.1f}")
    torch.manual_seed(123)
    print("Doğruluk:", round(dogruluk(model), 2))
    print("Üretim:", uret(model, [2, 5]))


if __name__ == "__main__":
    main()
```

Beklenen çıktı (sayılar PyTorch sürümüne göre çok küçük farklar gösterebilir; kayıpları bilerek tek basamağa yuvarladık):

```text
Parametre sayısı: 26216
Kaçınılmaz kayıp: 0.3
Adım 1: kayıp 2.3
Adım 100: kayıp 0.3
Adım 800: kayıp 0.3
Doğruluk: 1.0
Üretim: [2, 5, 2, 5, 2, 5, 2, 5]
```

### Modeli parça parça okumak

- **`Blok`**: 5.5'teki blokla aynı; yalnızca `attn_mask` ile maske alır ve ileri besleme ara boyutu girdinin 4 katıdır.
- **`token_gomme` ve `konum_gomme`**: 5.1'deki gömme tablosu ve 5.4'teki öğrenilen konum tablosu. İkisi toplanır.
- **`maske`**: `torch.triu(..., diagonal=1)` bir matrisin üst üçgenini (gelecek) `True` yapar. PyTorch'ta maskede `True`, "buraya bakma" demektir (5.2'deki `-1e9` işi).
- **`self.cikis`**: Her konumdaki vektörü, sözlük boyutunda (8) bir puan listesine çevirir. Bu puanlara **logit** denir (1.6).
- **`veri_uret`** ve **`kayip_hesapla`**: Girdi `dizi[:, :-1]`, hedef `dizi[:, 1:]`: her konum sonrakini tahmin eder. Çapraz entropi (1.6, 3.6) tahminle hedefi karşılaştırır.
- **`reshape(-1, SOZLUK)`**: `(örnek, konum, sözlük)` şeklindeki puanları, çapraz entropinin beklediği `(örnek × konum, sözlük)` şekline düzler.
- **`uret`**: Her adımda modelin **son konumdaki** tahminini (`[:, -1]`) alıp en yüksek puanlı token'ı (`argmax`) diziye ekler. Bu, açgözlü üretimdir; Faz 6'da çeşitli üretim yöntemlerini göreceğiz.

### Sonuçları yorumlamak

- **26216 parametre**: Bu model, gerçek dil modellerinin milyarlarca parametresinin yanında minicik, ama aynı mimari.
- **Adım 1: kayıp 2.3**: Eğitimden önce model sözlükteki 8 token'a eşit olasılık verir; kayıp `ln(8) ≈ 2.08` civarındadır (rastgele tahmin).
- **Adım 100 ve 800: kayıp 0.3**: Kayıp hızla düşüyor, ama `0`'a inmiyor. Bunun nedeni modelin başarısız olması değil: dizinin **ikinci token'ı rastgele**, kimse tahmin edemez. 7 hedefin biri tahmin edilemez ve bu hedefte kayıp `ln(8) ≈ 2.08`; ortalama `2.08 / 7 ≈ 0.3`. Bu, **kaçınılmaz kayıptır**; model onun altına inemez. (Bunu yukarıdaki görevde kendin hesapladın.)
- **Doğruluk 1.0**: Tahmin edilebilen bütün hedefleri doğru buluyor.
- **Üretim**: `[2, 5]` ile başlattığımızda model diziyi doğru biçimde `2 5 2 5 2 5 2 5` olarak sürdürüyor. Elle kurduğumuz attention'ı kendi öğrendi.

!!! warning "Maske olmadan model kopya çeker"
    `MiniTransformer(maskeli=False)` ile aynı eğitimi yaparsan kayıp `0.3`'te takılmaz, `0`'a iner. Bu bir başarı değil, **hile**: maskesiz modelde `t` konumu `t + 1` konumundaki hedef token'ı doğrudan görebilir ve kopyalar. Kayıp, kaçınılmaz kaybın **altına** iniyorsa bir yerde geleceği görüyorsun demektir; bu, kod hatasının klasik belirtisidir. Alıştırma 1'de dene.

!!! note "Konum gömmesi bu görevde şart değil"
    Denememizde konum gömmesi olmadan da model bu görevi öğrendi (doğruluk `1.0`, kayıp biraz daha yüksek). Maskeli attention, bir token'ın kaç token'a baktığından konumu dolaylı olarak çıkarabilir. Bu basit görev için yeterli; gerçek metinde sıra bilgisini modele açıkça vermek (5.4) yine de çok önemlidir.

## 4. Sık yapılan hatalar

- **Maskeyi unutmak ya da yanlış vermek.** Eğitimde en tehlikeli hata budur: kayıp harika görünür, model ise gelecekte işe yaramaz. Kayıp, kaçınılmaz kaybın altındaysa şüphelen.
- **Hedefi kaydırmamak.** Girdi ve hedef aynı diziyse model her konumda **kendi token'ını** tahmin eder; hiçbir şey öğrenmeden mükemmel olur. Hedef girdinin bir sonraki token'ıdır.
- **`reshape(-1, SOZLUK)` yapmamak.** `cross_entropy` puanların `(N, sınıf sayısı)` şeklinde olmasını bekler; üç boyutlu tensörü doğrudan verirsen şekil hatası alırsın.
- **Üretimde son konumu almamak.** Model her konum için tahmin üretir; yeni token için yalnızca **son** konumun tahmini (`[:, -1]`) kullanılır.
- **Üretimde `torch.no_grad()` kullanmamak.** Türev takibi gereksiz bellek ve zaman harcar (3.6).
- **Konum tablosundan uzun dizi vermek.** Tablo `UZUNLUK - 1 = 7` konumluk; daha uzun girdi `IndexError` verir (5.4).
- **Yalnızca eğitim kaybına bakmak.** Kayıp tek başına yetmez; yeni verilerde doğruluğu da ölç (2.4 dersindeki gibi eğitim ve test ayrımı).

## 5. Pekiştir

**Quiz**

1. Girdi ve hedef dizileri bir dizi için nasıl oluşturulur?
2. Maskesiz eğitilen model neden kayıp tabanının altına inebilir?
3. Kayıp `0.3`'te neden takılıyor?
4. `uret` fonksiyonu her adımda modelin hangi konumdaki tahminini kullanır?
5. Bigram bu görevde neden başarısız oldu, mini transformer neden başardı?

**Alıştırmalar**

1. `main()` içinde `MiniTransformer()` yerine `MiniTransformer(maskeli=False)` yaz. Kayıp ve doğruluk nasıl değişiyor? Bu neden başarı değil?
2. `veri_uret`'te diziyi üçlü tekrara çevir (`a b c a b c a b c`) ve `UZUNLUK = 9` yap. Kaçınılmaz kayıp nasıl değişir? (İpucu: kaç hedef rastgele?)
3. `KATMAN = 1` yap. Model hâlâ öğreniyor mu? `D = 16` ile dene.
4. `ogrenme_hizi`'ni `0.3` yap. Eğitim ne oluyor?
5. (İsteğe bağlı) `forward` içinde konum gömmesini kaldır (`self.konum_gomme(...)` toplamını sil). Doğruluk ve kayıp nasıl değişiyor?

??? success "Quiz cevapları"
    1. Girdi, dizinin son token'ı hariç hâli; hedef, ilk token'ı hariç hâli. Her konumda hedef, girdideki sonraki token'dır.
    2. Maskesiz modelde `t` konumu, `t + 1` konumundaki hedef token'ı doğrudan görür ve kopyalar. Kayıp, gerçekte yapılamayacak bir tahminle düşer.
    3. Dizinin ikinci token'ı rastgele ve tahmin edilemez. 7 hedefin birinde kayıp `ln(8)` olduğu için ortalama `ln(8) / 7 ≈ 0.3` altına inemez.
    4. Son konumdaki (`[:, -1]`) tahmini; bu, şimdiye kadarki bütün token'lara bakarak sıradaki token için üretilmiştir.
    5. Bigram yalnızca bir önceki token'a bakar; bu görevde cevap iki önceki token'da olduğu için şansa yakın tahmin eder. Transformer attention ile bağlamdaki istediği konuma bakabilir ve bir önceki konumu kopyalamayı öğrenir.

## Özet

Mini transformer; token ve konum gömmesini toplar, maskeli bloklardan geçirir, bir çıkış katmanıyla sözlükteki her token için puan (logit) üretir. Eğitimde girdi, dizinin bir kaydırılmış hâli olan hedefe çapraz entropiyle yaklaştırılır. Model, 5.1'deki bigram'ın göremediği "iki önce ne vardı?" bilgisini attention ile bulmayı kendisi öğrendi. Kaybın `0`'a inmemesi kaçınılmaz belirsizliği gösterir; kaçınılmaz kaybın altına inen bir kayıp ise maskesiz bakış gibi bir hatanın işaretidir. Bu mimari ve eğitim biçimi, büyük dil modellerinden yalnızca ölçekte farklıdır. Sıradaki fazda (Faz 6) aynı fikri gerçek metinle, gerçek bir tokenizer'la ve daha büyük bir modelle kuracağız.

## Kaynaklar

- Ashish Vaswani ve ark. (2017), *Attention Is All You Need*, NeurIPS
- Catherine Olsson ve ark. (2022), *In-context Learning and Induction Heads* (bağlamdan kopyalama davranışı)
- Andrej Karpathy, *Let's build GPT: from scratch, in code, spelled out* (video ders ve kod, İngilizce)
- [PyTorch resmî belgesi: `nn.MultiheadAttention` ve `attn_mask`](https://pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
