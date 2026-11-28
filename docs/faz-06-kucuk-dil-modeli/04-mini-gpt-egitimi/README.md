# Faz 6 – Ders 4: Mini GPT eğitimi

> ⏱️ Tahmini süre: 60-80 dk · 📚 Ön koşul: 5.6 Mini transformer, 6.1 Sonraki token tahmini · 💻 Gereksinim: Python 3.11+; sayfadaki pencereler ek paketsiz çalışır, asıl model için PyTorch kurulmalıdır

## Bu derste ne öğreneceksin?

- Gerçek bir metni dil modeli için hazırlamayı: sözlük, sayıya çevirme, eğitim/doğrulama ayrımı
- Uzun bir metinden **rastgele pencerelerle** batch almayı
- 5.6'daki transformer'ı Türkçe bir metinde **karakter karakter** eğitmeyi
- **Eğitim kaybı** ile **doğrulama kaybını** birlikte izlemeyi ve kayıp eğrisini okumayı
- Eğitilmiş modelle Türkçeye benzeyen metin üretmeyi

## 1. Problem

5.6'daki model yapay bir görevi (`a b a b ...`) öğrendi. Şimdi aynı mimariyi gerçek bir işe koşalım: **Türkçe metin yazmayı** öğrensin. Bu, GPT gibi modellerin yaptığı işin küçük bir kopyasıdır: Bir metin verilir, model her konumda **sonraki token'ı** tahmin etmeyi öğrenir (6.1).

Bunun için birkaç yeni parça gerekiyor:

- **Veri hazırlığı:** Metni token'lara bölüp sayılara çevirmek. Bu derste işi basit tutmak için **karakter düzeyinde** çalışacağız: Her harf, boşluk ve nokta bir token. (6.2'deki BPE de kullanılabilirdi; mantık aynıdır.)
- **Batch alma:** Metin tek ve uzun bir dizi. Modele her adımda bu dizinin rastgele yerlerinden kısa **pencereler** vereceğiz.
- **Doğrulama:** Model metni ezberleyebilir. Ezberlemek yerine gerçekten öğrenip öğrenmediğini görmek için metnin bir parçasını eğitimde **hiç göstermeyip** kaybı orada da ölçeceğiz.

Veri olarak, ders için yazılmış küçük bir Türkçe metin kullanacağız: bir kasabada geçen kısa bir hikâye (`kod/veri/kasaba.txt`, yaklaşık 3000 karakter). Şöyle başlıyor:

```text
küçük bir kasabada sabah erkenden başlar. fırıncı ekmekleri fırına koyar. çocuklar okula gider. ...
```

## 2. Kendin yaz

### 2.1 Metni sayılara çevirmek ve ikiye bölmek

Önce metindeki farklı karakterleri bulup her birine bir numara veririz (4.1). Sonra metni sayı listesine çevirir, başından **%90'ını eğitim**, kalan **%10'unu doğrulama** için ayırırız:

```python {.python-playground}
metin = "ali okula gider. ayşe okula gider. ali ile ayşe aynı sınıftadır."

karakterler = sorted(set(metin))
stoi = {k: i for i, k in enumerate(karakterler)}   # karakter → sayı
veri = [stoi[k] for k in metin]

print("Sözlük:", "".join(karakterler))
print("Sözlük boyutu:", len(karakterler))
print("İlk 10 sayı:", veri[:10])
print("Geri çevirince:", "".join(karakterler[i] for i in veri[:10]))

sinir = int(len(veri) * 0.9)
egitim, dogrulama = veri[:sinir], veri[sinir:]
print("Eğitim:", len(egitim), "token, doğrulama:", len(dogrulama), "token")
print("Doğrulama kısmı:", "".join(karakterler[i] for i in dogrulama))
```
```text {.python-playground-expected}
Sözlük:  .adefgiklnorstuyış
Sözlük boyutu: 19
İlk 10 sayı: [2, 9, 7, 0, 11, 8, 15, 9, 2, 0]
Geri çevirince: ali okula 
Eğitim: 57 token, doğrulama: 7 token
Doğrulama kısmı: ftadır.
```
```text {.python-playground-help}
`sorted(set(metin))` | Metindeki farklı karakterler, sıralı. Boşluk ve nokta da birer karakterdir.
`stoi = {k: i ...}` | Her karaktere bir sayı verir ("string to integer"). Geri çevirmek için `karakterler[i]` yeter.
`veri = [stoi[k] for k in metin]` | Metnin her karakteri sayısıyla değiştirilir.
`int(len(veri) * 0.9)` | Metnin %90'ının bittiği yer. `int` tam sayıya çevirir.
`veri[:sinir], veri[sinir:]` | Başı eğitim, sonu doğrulama. Doğrulama kısmını model eğitimde hiç görmez.
```

Neden rastgele değil de **sondan** ayırıyoruz? Karakterleri rastgele seçseydik doğrulama karakterleri eğitim metninin tam ortasında kalırdı ve model komşularından onları kolayca tahmin ederdi. Metnin sonunu ayırmak, modelin hiç görmediği **cümlelerde** ne yaptığını ölçer.

### 2.2 Rastgele pencerelerle batch almak

Metin binlerce karakter, ama model bir seferde yalnızca `blok` kadar karakter görebilir (konum tablosu o kadar uzun, 5.4). Her adımda metnin rastgele bir yerinden `blok` uzunluğunda bir pencere keseriz. **Hedef**, aynı pencerenin bir sağa kaymış hâlidir:

```python {.python-playground}
metin = "ali okula gider. ayşe okula gider."
blok = 8

i = 4   # pencerenin başladığı yer (eğitimde rastgele seçilir)
girdi = metin[i:i + blok]
hedef = metin[i + 1:i + blok + 1]
print("girdi:", repr(girdi))
print("hedef:", repr(hedef))
print()
for t in range(blok):
    print(f"{girdi[:t + 1]!r:12} → {hedef[t]!r}")
```
```text {.python-playground-expected}
girdi: 'okula gi'
hedef: 'kula gid'

'o'          → 'k'
'ok'         → 'u'
'oku'        → 'l'
'okul'       → 'a'
'okula'      → ' '
'okula '     → 'g'
'okula g'    → 'i'
'okula gi'   → 'd'
```
```text {.python-playground-help}
`metin[i:i + blok]` | `i`. karakterden başlayan `blok` uzunluğunda pencere.
`metin[i + 1:i + blok + 1]` | Aynı pencere, bir karakter sağa kaymış: her konumun hedefi bir sonraki karakter.
`girdi[:t + 1]` | `t`. konumdaki model, maske sayesinde yalnızca buraya kadarını görür (5.2).
`!r` | Metni tırnaklarıyla yazar; boşlukların nerede olduğu görünür.
```

Tek bir pencere modele aslında **8 ayrı soru** sorar: 1 karakterlik bağlamdan 8 karakterlik bağlama kadar. Böylece model hem kısa hem uzun bağlamla tahmin yapmayı öğrenir. Bir batch'te bu pencerelerden birkaç tane (örneğin 32) yan yana verilir.

### 2.3 Kayıp neyi anlatıyor?

Eğitimde kaybı izleyeceğiz. Sayıların anlamını önceden bilmek, eğriyi okumayı kolaylaştırır. 6.1'den hatırla: perplexity `e ** kayıp`, modelin her adımda ortalama **kaç karakter arasında kararsız kaldığını** anlatır.

```python {.python-playground}
import math

sozluk = 31   # bizim metindeki farklı karakter sayısı
print(f"Rastgele tahmin: kayıp ln({sozluk}) = {math.log(sozluk):.2f}")
print()
for kayip in [3.43, 2.0, 1.4, 1.0, 0.2]:
    print(f"kayıp {kayip:.2f} → perplexity {math.exp(kayip):5.1f} karakter arasında kararsız")
```
```text {.python-playground-expected}
Rastgele tahmin: kayıp ln(31) = 3.43

kayıp 3.43 → perplexity  30.9 karakter arasında kararsız
kayıp 2.00 → perplexity   7.4 karakter arasında kararsız
kayıp 1.40 → perplexity   4.1 karakter arasında kararsız
kayıp 1.00 → perplexity   2.7 karakter arasında kararsız
kayıp 0.20 → perplexity   1.2 karakter arasında kararsız
```
```text {.python-playground-help}
`math.log(sozluk)` | Model her karaktere eşit olasılık verirse doğru karakterin olasılığı `1/31`, kaybı `ln(31)`. Eğitim buradan başlar.
`math.exp(kayip)` | Perplexity: kaybı sezgisel bir sayıya çevirir.
```

- Eğitime **3.43** civarından başlamayı bekliyoruz: model henüz hiçbir şey bilmiyor.
- **1.4** civarı: Model her adımda yaklaşık 4 karakter arasında kararsız. Kelimeleri ve ekleri öğrenmeye başlamış demektir.
- **0.2**: Neredeyse her karakteri biliyor. Eğitim metninde böyle bir kayıp, büyük olasılıkla metni **ezberlediğini** gösterir. Bunu doğrulama kaybıyla anlarız.

### Şimdi sen yaz: batch al

**Görev:** Kısa bir metin ve onu sayılara çeviren kod hazır. Metni %90 eğitim, %10 doğrulama diye bölecek, sonra eğitim kısmından rastgele bir pencere ve onun bir sağa kaymış hedefini keseceksin. Ekranda iki kısmın uzunlukları ile girdi ve hedef metinleri görünmeli.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
import random

metin = "çocuklar okula gider. öğretmen kapıda bekler. ali ile ayşe aynı sınıftadır."
karakterler = sorted(set(metin))
stoi = {k: i for i, k in enumerate(karakterler)}
veri = [stoi[k] for k in metin]
blok = 10

# TODO 1: Metnin %90'ının bittiği yeri bul (int ile tam sayıya çevir).
sinir = ___
egitim, dogrulama = veri[:sinir], veri[sinir:]
print("Eğitim:", len(egitim), "doğrulama:", len(dogrulama))

random.seed(3)
i = random.randint(0, len(egitim) - blok - 1)
# TODO 2: i'den başlayan blok uzunluğunda pencereyi kes.
girdi = ___
# TODO 3: Aynı pencereyi bir sağa kaydırarak kes.
hedef = ___

print("girdi:", repr("".join(karakterler[k] for k in girdi)))
print("hedef:", repr("".join(karakterler[k] for k in hedef)))
```
```text {.python-playground-expected}
Eğitim: 67 doğrulama: 8
girdi: 'gider. öğr'
hedef: 'ider. öğre'
```
```text {.python-playground-help}
`sinir = ___` | Veri uzunluğunu 0.9 ile çarp ve `int(...)` içine al: `int(len(veri) * 0.9)`.
`girdi = ___` | Dilimleme: `egitim[i:i + blok]` `i`. elemandan başlayıp `blok` eleman alır.
`hedef = ___` | Başlangıcı ve sonu bir artır: `egitim[i + 1:i + blok + 1]`.
```
```python {.python-playground-solution}
import random

metin = "çocuklar okula gider. öğretmen kapıda bekler. ali ile ayşe aynı sınıftadır."
karakterler = sorted(set(metin))
stoi = {k: i for i, k in enumerate(karakterler)}
veri = [stoi[k] for k in metin]
blok = 10

# Metnin %90'ının bittiği yeri bul (int ile tam sayıya çevir).
sinir = int(len(veri) * 0.9)
egitim, dogrulama = veri[:sinir], veri[sinir:]
print("Eğitim:", len(egitim), "doğrulama:", len(dogrulama))

random.seed(3)
i = random.randint(0, len(egitim) - blok - 1)
# i'den başlayan blok uzunluğunda pencereyi kes.
girdi = egitim[i:i + blok]
# Aynı pencereyi bir sağa kaydırarak kes.
hedef = egitim[i + 1:i + blok + 1]

print("girdi:", repr("".join(karakterler[k] for k in girdi)))
print("hedef:", repr("".join(karakterler[k] for k in hedef)))
```

## 3. Kütüphaneyle yap

Aşağıda eksiksiz program var. Kodu `mini_gpt.py` adıyla kaydet, yanına bir `veri` klasörü açıp metin dosyasını `veri/kasaba.txt` adıyla koy ve `python mini_gpt.py` ile çalıştır. (Kodu, metni ve testleri proje klasöründe `docs/faz-06-kucuk-dil-modeli/04-mini-gpt-egitimi/kod/` içinde bulabilirsin.) PyTorch'u 3.6'daki gibi kur. Eğitim sıradan bir bilgisayarda yarım dakika kadar sürer.

```python
"""Ders 6.4 – Mini GPT: küçük bir Türkçe metinde karakter düzeyinde dil modeli eğitmek.

PyTorch gerekir. Çalıştır:  python kod/mini_gpt.py

Adımlar: metni oku → karakterleri sayılara çevir → eğitim/doğrulama diye ikiye böl →
rastgele pencerelerden batch al → 5.6'daki transformer'ı sonraki karakteri tahmin etmeye eğit →
belirli aralıklarla iki kaybı da ölç → eğitilmiş modelle metin üret.
"""

import math
import pathlib

import torch
from torch import nn

VERI_YOLU = pathlib.Path(__file__).parent / "veri" / "kasaba.txt"
BLOK, D, KAFA, KATMAN, DROPOUT = 32, 32, 4, 2, 0.2


# ---------- Veri ----------

def veri_hazirla(metin):
    """Karakter sözlüğünü kurar; metni sayılara çevirip %90 eğitim, %10 doğrulama diye böler."""
    karakterler = sorted(set(metin))
    stoi = {k: i for i, k in enumerate(karakterler)}
    veri = torch.tensor([stoi[k] for k in metin])
    sinir = int(len(veri) * 0.9)
    return karakterler, stoi, veri[:sinir], veri[sinir:]


def batch_al(veri, batch, blok=BLOK):
    """Metnin rastgele yerlerinden `batch` tane pencere alır. Hedef, girdinin bir sağa kaymışıdır."""
    baslar = torch.randint(0, len(veri) - blok - 1, (batch,))
    girdi = torch.stack([veri[i:i + blok] for i in baslar])
    hedef = torch.stack([veri[i + 1:i + blok + 1] for i in baslar])
    return girdi, hedef


# ---------- Model (5.6'daki transformer) ----------

class Blok(nn.Module):
    def __init__(self, d, kafa_sayisi):
        super().__init__()
        self.norm1 = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, kafa_sayisi, dropout=DROPOUT, batch_first=True)
        self.norm2 = nn.LayerNorm(d)
        self.ffn = nn.Sequential(nn.Linear(d, 4 * d), nn.ReLU(), nn.Linear(4 * d, d), nn.Dropout(DROPOUT))

    def forward(self, x, maske):
        h = self.norm1(x)
        x = x + self.attn(h, h, h, attn_mask=maske, need_weights=False)[0]
        return x + self.ffn(self.norm2(x))


class MiniGPT(nn.Module):
    def __init__(self, sozluk_boyutu):
        super().__init__()
        self.token_gomme = nn.Embedding(sozluk_boyutu, D)
        self.konum_gomme = nn.Embedding(BLOK, D)
        self.bloklar = nn.ModuleList([Blok(D, KAFA) for _ in range(KATMAN)])
        self.norm = nn.LayerNorm(D)
        self.cikis = nn.Linear(D, sozluk_boyutu)

    def forward(self, idler):
        t = idler.shape[1]
        x = self.token_gomme(idler) + self.konum_gomme(torch.arange(t))
        maske = torch.triu(torch.ones(t, t, dtype=torch.bool), diagonal=1)
        for blok in self.bloklar:
            x = blok(x, maske)
        return self.cikis(self.norm(x))


def kayip_hesapla(model, girdi, hedef):
    logitler = model(girdi)
    return nn.functional.cross_entropy(logitler.reshape(-1, logitler.shape[-1]), hedef.reshape(-1))


@torch.no_grad()
def kayip_olc(model, veri, tekrar=20, batch=32):
    """Kaybı tek batch yerine birkaç batch'in ortalamasıyla ölçer; daha az gürültülü olur."""
    model.eval()
    kayiplar = [kayip_hesapla(model, *batch_al(veri, batch)).item() for _ in range(tekrar)]
    model.train()
    return sum(kayiplar) / len(kayiplar)


# ---------- Eğitim ve üretim ----------

def egit(model, egitim, dogrulama, adim_sayisi=1500, batch=32, ogrenme_hizi=1e-3, aralik=250):
    optimizer = torch.optim.AdamW(model.parameters(), lr=ogrenme_hizi)
    gecmis = []
    for adim in range(adim_sayisi + 1):
        if adim % aralik == 0:
            gecmis.append((adim, kayip_olc(model, egitim), kayip_olc(model, dogrulama)))
        if adim == adim_sayisi:
            break
        kayip = kayip_hesapla(model, *batch_al(egitim, batch))
        optimizer.zero_grad()
        kayip.backward()
        optimizer.step()
    return gecmis


@torch.no_grad()
def uret(model, baslangic, stoi, karakterler, uzunluk=120):
    """Her adımda olasılıklara göre bir sonraki karakteri örnekler (6.1'deki gibi)."""
    model.eval()
    idler = torch.tensor([[stoi[k] for k in baslangic]])
    for _ in range(uzunluk):
        logitler = model(idler[:, -BLOK:])[:, -1]
        olasiliklar = torch.softmax(logitler, dim=-1)
        sonraki = torch.multinomial(olasiliklar, 1)
        idler = torch.cat([idler, sonraki], dim=1)
    return "".join(karakterler[i] for i in idler[0].tolist())


def main():
    metin = VERI_YOLU.read_text(encoding="utf-8")
    karakterler, stoi, egitim, dogrulama = veri_hazirla(metin)
    print(f"Karakter sayısı: {len(metin)}, sözlük: {len(karakterler)}")
    print(f"Eğitim: {len(egitim)}, doğrulama: {len(dogrulama)}")

    torch.manual_seed(0)
    model = MiniGPT(len(karakterler))
    print("Parametre sayısı:", sum(p.numel() for p in model.parameters()))
    print(f"Rastgele tahminin kaybı: ln({len(karakterler)}) = {math.log(len(karakterler)):.2f}")

    for adim, e, d in egit(model, egitim, dogrulama):
        print(f"Adım {adim:4}: eğitim kaybı {e:.2f}, doğrulama kaybı {d:.2f}")

    torch.manual_seed(1)
    print("Üretilen metin:")
    print(uret(model, "ali ", stoi, karakterler))


if __name__ == "__main__":
    main()
```

Beklenen çıktı (kayıplar PyTorch sürümüne ve bilgisayara göre küçük farklar gösterebilir; üretilen metin büyük olasılıkla farklı olacaktır):

```text
Karakter sayısı: 3057, sözlük: 31
Eğitim: 2751, doğrulama: 306
Parametre sayısı: 28511
Rastgele tahminin kaybı: ln(31) = 3.43
Adım    0: eğitim kaybı 3.62, doğrulama kaybı 3.59
Adım  250: eğitim kaybı 2.10, doğrulama kaybı 2.06
Adım  500: eğitim kaybı 1.82, doğrulama kaybı 1.82
Adım  750: eğitim kaybı 1.56, doğrulama kaybı 1.62
Adım 1000: eğitim kaybı 1.37, doğrulama kaybı 1.53
Adım 1250: eğitim kaybı 1.19, doğrulama kaybı 1.44
Adım 1500: eğitim kaybı 1.05, doğrulama kaybı 1.39
Üretilen metin:
ali ağaçları anıfınım çocuklarda babahçarasında bazar. sabazardafrda sabahi küşün ekmekleri çocukl çocuklar olunca bir çöden
```

### Kodu parça parça okumak

- **`veri_hazirla`**: 2.1'deki işin aynısı; tek fark, sayıların bir PyTorch tensörü olması.
- **`batch_al`**: 2.2'deki pencereleri `batch` kez rastgele seçer ve `torch.stack` ile `(batch, BLOK)` şeklinde üst üste koyar.
- **`MiniGPT`**: 5.6'daki model. Değişenler: sözlük boyutu metne göre belirleniyor (31) ve **dropout** eklendi.
- **Dropout (`nn.Dropout`, `dropout=0.2`)**: Eğitimde her adımda değerlerin rastgele %20'sini sıfırlar. Model tek bir yola güvenemez, bu da ezberlemeyi zorlaştırır. `model.eval()` dropout'u kapatır, `model.train()` yeniden açar. Ölçerken ve üretirken bu yüzden `eval()` kullanıyoruz.
- **`kayip_olc`**: Kaybı tek batch yerine 20 batch'in ortalamasıyla ölçer. Tek batch'in kaybı şansa göre çok oynar; ortalama eğriyi daha okunur yapar.
- **`egit`**: Her 250 adımda bir hem eğitim hem doğrulama kaybını kaydeder. Optimizasyon için **AdamW** kullanıyoruz: Adam'ın (3.4) ağırlıkları biraz küçülten, dil modellerinde standart olan sürümü.
- **`uret`**: 6.1'deki gibi her adımda olasılıklara göre bir karakter **örnekler** (`torch.multinomial`). Bağlam `BLOK`'tan uzun olunca yalnızca son `BLOK` karakteri modele verir (`idler[:, -BLOK:]`); konum tablosu daha uzununu bilmez.

### Kayıp eğrisini okumak

- **Adım 0, kayıp 3.6:** Rastgele tahmin seviyesi (`ln(31) = 3.43`, 2.3). Beklediğimiz gibi.
- **Adım 0 → 500:** İki kayıp birlikte hızla düşüyor. Model en sık karakterleri, boşlukları, sık heceleri öğreniyor.
- **Adım 500 → 1500:** Eğitim kaybı düşmeye devam ediyor (1.05). Doğrulama kaybı da düşüyor (1.39) ama daha yavaş; aradaki **fark açılıyor**. Model eğitim metnine özgü şeyleri de öğrenmeye başladı.
- **Üretilen metin:** Gerçek bir hikâye değil, ama Türkçeye benziyor: boşluklarla ayrılmış sözcükler, `çocuklar`, `ekmekleri` gibi doğru sözcükler, `-lar`, `-da` gibi ekler ve noktalar. 28 bin parametreli, 3000 karakterle eğitilmiş bir modelden beklenebilecek en iyisi budur.

Doğrulama kaybı, eğitim kaybından **daha önemlidir**: Modeli hiç görmediği metinde ne kadar iyi olduğunu o gösterir.

!!! warning "Uzun eğitim ezber getirir"
    Bu derste ilk denememizde dropout yoktu ve model daha büyüktü (`D = 64`). 2000 adım sonra eğitim kaybı **0.20**'ye indi ama doğrulama kaybı 500. adımdaki 2.19'dan **2.95**'e çıktı. Üretilen metin de eğitim metninin kelimesi kelimesine kopyasıydı: Model metni **ezberlemişti**. Eğitim kaybına bakan biri modeli harika sanardı. Bu duruma **aşırı uyum** (overfitting) denir; 6.6'da ayrıntısıyla inceleyeceğiz.

## 4. Sık yapılan hatalar

- **Yalnızca eğitim kaybına bakmak.** Eğitim kaybı her zaman düşer; model ezberliyor da olabilir. Doğrulama kaybını mutlaka izle.
- **Doğrulama verisini rastgele karakterlerden seçmek.** Doğrulama parçası eğitim metninin içine dağılırsa model onu komşularından tahmin eder; kayıp gerçekte olduğundan iyi görünür. Metnin ayrı bir parçasını ayır.
- **Hedefi kaydırmamak.** Hedef, girdinin bir sağa kaymış hâlidir (`veri[i + 1:i + blok + 1]`). Kaydırmazsan model kendi karakterini tahmin eder ve hiçbir şey öğrenmeden kayıp sıfıra iner.
- **Ölçerken `model.eval()` kullanmamak.** Dropout ölçüm sırasında da çalışır ve kaybı olduğundan kötü gösterir; üretimi de bozar.
- **Üretimde bağlamı kırpmamak.** Üretilen metin `BLOK`'tan uzun olunca konum tablosu yetmez ve `IndexError` alırsın. Son `BLOK` token'ı ver.
- **Çok küçük metinle büyük model eğitmek.** 3000 karakterlik metin için 100 bin parametre fazla; model hızla ezberler. Model büyüklüğü veriyle orantılı olmalı.

## 5. Pekiştir

**Quiz**

1. Neden metnin bir kısmını eğitimde kullanmayıp doğrulamaya ayırıyoruz?
2. `blok = 8` uzunluğunda tek bir pencere modele kaç tahmin sorusu sorar? Neden?
3. Sözlükte 31 karakter varsa eğitime başlarken kaybın kaç civarında olmasını beklersin?
4. Eğitim kaybı düşerken doğrulama kaybı yükseliyorsa ne oluyordur?
5. Dropout nedir ve ölçüm yaparken neden kapatılır?

**Alıştırmalar**

1. 2.2'de `i = 4` yerine farklı başlangıçlar dene. Hangi pencerede hedeflerin çoğu boşluk ya da nokta oluyor?
2. Kütüphane kodunda `uret` fonksiyonuna farklı başlangıçlar ver: `"ayşe "`, `"kışın "`. Model başlangıca uygun devam ediyor mu?
3. `DROPOUT = 0.0` yapıp `egit(..., adim_sayisi=3000)` ile eğit. Doğrulama kaybı ne zaman yükselmeye başlıyor? Üretilen metin nasıl değişiyor?
4. `BLOK = 8` yap. Kayıplar ve üretilen metin nasıl değişti? Neden?
5. (İsteğe bağlı) Kendi Türkçe metnini (birkaç bin karakter) `veri` klasörüne koyup `VERI_YOLU`'nu değiştir ve modeli onunla eğit.

??? success "Quiz cevapları"
    1. Model eğitim metnini ezberleyebilir. Hiç görmediği metindeki kayıp, gerçekten öğrenip öğrenmediğini gösterir.
    2. 8 soru: her konum, kendisine kadarki karakterlerle bir sonraki karakteri tahmin eder (1 karakterlik bağlamdan 8 karakterliğe kadar). Maske, her konumun yalnızca geçmişi görmesini sağlar.
    3. `ln(31) ≈ 3.43` civarında: eğitilmemiş model her karaktere yaklaşık eşit olasılık verir.
    4. Model eğitim metnine aşırı uyum sağlıyor (ezberliyor): eğitim metninde iyileşirken yeni metinde kötüleşiyor.
    5. Eğitimde değerlerin bir kısmını rastgele sıfırlayan, ezberlemeyi zorlaştıran bir yöntemdir. Ölçerken rastgelelik istemeyiz; modelin tam hâlinin kaybını ölçmek isteriz, bu yüzden `model.eval()` ile kapatılır.

## Özet

Gerçek metinde bir dil modeli eğitmek için metni token'lara bölüp sayılara çevirir, bir kısmını doğrulamaya ayırır ve her adımda metnin rastgele yerlerinden pencereler alırız; hedef, pencerenin bir sağa kaymış hâlidir. 5.6'daki transformer'ı bu şekilde küçük bir Türkçe hikâyede eğittik: kayıp rastgele tahmin seviyesinden (`ln(31)`) 1.4'e indi ve model Türkçeye benzeyen metin üretmeye başladı. Eğitim ve doğrulama kaybını birlikte izlemek, modelin öğrenip öğrenmediğini ya da ezberleyip ezberlemediğini gösterir. Sıradaki derste üretim yöntemlerini (sıcaklık, top-k, top-p) inceleyeceğiz.

## Kaynaklar

- Andrej Karpathy, [nanoGPT](https://github.com/karpathy/nanoGPT) ve "Let's build GPT: from scratch, in code, spelled out" videosu
- Alec Radford ve ark. (2018), *Improving Language Understanding by Generative Pre-Training* (GPT-1)
- Nitish Srivastava ve ark. (2014), *Dropout: A Simple Way to Prevent Neural Networks from Overfitting*, JMLR
