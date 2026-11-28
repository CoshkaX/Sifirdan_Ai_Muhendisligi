# Faz 6 – Ders 5: Metin üretimi

> ⏱️ Tahmini süre: 45-60 dk · 📚 Ön koşul: 6.1 Sonraki token tahmini, 6.4 Mini GPT eğitimi · 💻 Gereksinim: Python 3.11+; sayfadaki pencereler ek paketsiz çalışır, kütüphane örneği için PyTorch kurulmalıdır

## Bu derste ne öğreneceksin?

- Modelin verdiği olasılıklardan bir sonraki token'ı **seçmenin** farklı yollarını
- **Açgözlü seçimin** neden tekrara düştüğünü
- **Sıcaklığın** (temperature) olasılıkları nasıl keskinleştirip yumuşattığını
- **Top-k** ve **top-p** ile saçma seçenekleri nasıl elediğimizi
- Aynı modelden bu ayarlarla çok farklı metinler üretmeyi

## 1. Problem

Eğitilmiş bir dil modeli bize doğrudan metin vermez; her adımda sözlükteki her token için bir **puan** (logit) verir. Softmax bu puanları olasılığa çevirir (1.6). Sonra bir token **seçmemiz** gerekir. Seçilen token metne eklenir ve iş tekrarlanır.

Bu seçimi nasıl yaptığımız, aynı modelin ürettiği metni büyük ölçüde değiştirir:

- Her seferinde **en olası** token'ı seçersek metin tutarlı ama sıkıcı olur ve kendini tekrar etmeye başlar.
- Olasılıklara göre **rastgele** seçersek metin çeşitlenir, ama arada olasılığı düşük, saçma token'lar da seçilir.

Sohbet uygulamalarındaki "temperature", "top-p" gibi ayarlar tam olarak bu seçimi kontrol eder. Bu derste her birini elle yazıp sonra 6.4'teki modelde deneyeceğiz.

## 2. Kendin yaz

Bütün örneklerde aynı durumu kullanacağız: Model `"çocuklar okula "` metninden sonra dört sözcük için şu puanları vermiş olsun. (Gerçek modellerde binlerce token vardır; burada işi görmek için dört tane yeterli.)

### 2.1 Açgözlü seçim ve örnekleme

```python {.python-playground}
import math
import random

puanlar = {"gider": 2.0, "gidiyor": 1.5, "koşar": 0.5, "uçar": -1.0}

toplam = sum(math.exp(p) for p in puanlar.values())
olasiliklar = {t: math.exp(p) / toplam for t, p in puanlar.items()}
for t, o in olasiliklar.items():
    print(f"{t:8} {o:.2f}")

print("Açgözlü seçim:", max(olasiliklar, key=olasiliklar.get))

random.seed(0)
secimler = random.choices(list(olasiliklar), weights=list(olasiliklar.values()), k=10)
print("10 örnekleme:", secimler)
```
```text {.python-playground-expected}
gider    0.53
gidiyor  0.32
koşar    0.12
uçar     0.03
Açgözlü seçim: gider
10 örnekleme: ['gidiyor', 'gidiyor', 'gider', 'gider', 'gider', 'gider', 'gidiyor', 'gider', 'gider', 'gidiyor']
```
```text {.python-playground-help}
`math.exp(p) / toplam` | Softmax: puanları 0 ile 1 arasında, toplamı 1 olan olasılıklara çevirir (1.6).
`max(olasiliklar, key=olasiliklar.get)` | Açgözlü seçim: olasılığı en yüksek token. Her seferinde aynı sonucu verir.
`random.choices(..., weights=..., k=10)` | Olasılıklara göre 10 kez rastgele seçer. Olasılığı yüksek olan daha sık çıkar.
`random.seed(0)` | Rastgele sayıları sabitler; her çalıştırmada aynı sonuç çıkar.
```

Açgözlü seçim her zaman `gider` der. Örnekleme çoğunlukla `gider` ve `gidiyor` seçer, ama arada `uçar` gibi saçma bir seçenek de çıkabilir (olasılığı %3). Uzun bir metinde yüzlerce seçim yapıldığından bu küçük olasılıklar toplanır ve metin bir yerde mutlaka saçmalar.

Açgözlü seçimin sorunu da şu: Model aynı bağlama hep aynı cevabı verdiği için bir kez kendini tekrar ederse döngüye girer ve bir daha çıkamaz. 3. bölümde bunu gerçek modelde göreceğiz.

### 2.2 Sıcaklık

**Sıcaklık** (temperature, `T`), softmax'tan önce bütün puanları aynı sayıya bölmektir: `softmax(puan / T)`.

```python {.python-playground}
import math

puanlar = {"gider": 2.0, "gidiyor": 1.5, "koşar": 0.5, "uçar": -1.0}


def sicaklikla_softmax(puanlar, sicaklik):
    olcekli = {t: p / sicaklik for t, p in puanlar.items()}
    toplam = sum(math.exp(p) for p in olcekli.values())
    return {t: math.exp(p) / toplam for t, p in olcekli.items()}


for sicaklik in [0.25, 0.5, 1.0, 2.0, 5.0]:
    o = sicaklikla_softmax(puanlar, sicaklik)
    print(f"T={sicaklik:<4}", "  ".join(f"{t} {v:.2f}" for t, v in o.items()))
```
```text {.python-playground-expected}
T=0.25 gider 0.88  gidiyor 0.12  koşar 0.00  uçar 0.00
T=0.5  gider 0.70  gidiyor 0.26  koşar 0.04  uçar 0.00
T=1.0  gider 0.53  gidiyor 0.32  koşar 0.12  uçar 0.03
T=2.0  gider 0.40  gidiyor 0.31  koşar 0.19  uçar 0.09
T=5.0  gider 0.31  gidiyor 0.28  koşar 0.23  uçar 0.17
```
```text {.python-playground-help}
`p / sicaklik` | Bütün puanları sıcaklığa böleriz. `T < 1` puanlar arasındaki farkı büyütür, `T > 1` küçültür.
`sicaklikla_softmax(...)` | Ölçeklenmiş puanların softmax'ı.
`f"{sicaklik:<4}"` | Sayıyı 4 karakterlik alana sola yaslı yazar.
```

- **`T < 1` (soğuk):** Farklar büyür, en olası token daha da baskın olur. `T = 0.25`'te `gider` neredeyse %90. Sıcaklık sıfıra yaklaştıkça açgözlü seçime döner.
- **`T = 1`:** Modelin kendi olasılıkları.
- **`T > 1` (sıcak):** Farklar küçülür, olasılıklar eşitlenir. `T = 5`'te `uçar` bile %17. Metin çeşitlenir ama saçmalamaya başlar.

Kısacası sıcaklık bir **tutarlılık ↔ yaratıcılık** düğmesidir.

### 2.3 Top-k ve top-p

Sıcaklık bütün olasılıkları birlikte değiştirir; düşük olasılıklı saçma token'lar hâlâ seçilebilir. Bunları tamamen elemek için iki yöntem var:

- **Top-k:** Yalnızca en olası `k` token'ı tut, gerisini at.
- **Top-p** (nucleus örnekleme): Token'ları olasılığa göre sırala, olasılıkları toplamı `p`'ye ulaşana kadar al, gerisini at.

Kalan token'ların olasılıkları yeniden toplamı 1 olacak şekilde ölçeklenir ve seçim bunların arasında yapılır.

```python {.python-playground}
import math

puanlar = {"gider": 2.0, "gidiyor": 1.5, "koşar": 0.5, "uçar": -1.0}
toplam = sum(math.exp(p) for p in puanlar.values())
olasiliklar = {t: math.exp(p) / toplam for t, p in puanlar.items()}
sirali = sorted(olasiliklar, key=olasiliklar.get, reverse=True)


def yeniden_olcekle(secilenler):
    t = sum(olasiliklar[s] for s in secilenler)
    return {s: round(olasiliklar[s] / t, 2) for s in secilenler}


print("top-k 2:", yeniden_olcekle(sirali[:2]))

birikimli, secilenler = 0.0, []
for token in sirali:
    secilenler.append(token)
    birikimli += olasiliklar[token]
    if birikimli >= 0.9:
        break
print("top-p 0.9:", yeniden_olcekle(secilenler))
```
```text {.python-playground-expected}
top-k 2: {'gider': 0.62, 'gidiyor': 0.38}
top-p 0.9: {'gider': 0.55, 'gidiyor': 0.33, 'koşar': 0.12}
```
```text {.python-playground-help}
`sorted(olasiliklar, key=olasiliklar.get, reverse=True)` | Token'ları olasılığa göre büyükten küçüğe sıralar.
`sirali[:2]` | Top-k: ilk `k = 2` token.
`if birikimli >= 0.9: break` | Top-p: olasılıklar toplamı 0.9'a ulaşınca durur. O ana kadar eklenenler kalır.
`yeniden_olcekle(...)` | Kalanların olasılıklarını, toplamları 1 olacak şekilde yeniden ölçekler.
```

Top-p'nin avantajı, kaç token tutacağını duruma göre ayarlamasıdır. Model eminse (bir token %95 ise) yalnızca o kalır; kararsızsa (birçok token birbirine yakınsa) birçoğu kalır. Top-k ise her durumda tam `k` tane tutar. Gerçek uygulamalarda genellikle sıcaklık ile top-p birlikte kullanılır: önce sıcaklık uygulanır, sonra top-p ile kuyruk kesilir.

### Şimdi sen yaz: sıcaklık ve top-k

**Görev:** Modelin dört sözcüğe verdiği puanlar kodda hazır. Önce puanlara sıcaklık uygulayacak, sonra en yüksek iki token'ı seçecek (top-k) ve yalnızca bu ikisi arasında olasılıkları hesaplayacaksın. Ekranda seçilen iki token ve olasılıkları görünmeli.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
import math

puanlar = {"gider": 2.0, "gidiyor": 1.5, "koşar": 0.5, "uçar": -1.0}
sicaklik = 0.5
k = 2

# TODO 1: Her puanı sıcaklığa böl.
olcekli = {t: ___ for t, p in puanlar.items()}

# TODO 2: Puanı en yüksek k token'ı seç (sorted ile büyükten küçüğe sırala, ilk k tanesini al).
secilenler = ___

toplam = sum(math.exp(olcekli[t]) for t in secilenler)
for t in secilenler:
    # TODO 3: Softmax: bu token'ın e üstü puanını toplama böl.
    olasilik = ___
    print(t, round(olasilik, 3))
```
```text {.python-playground-expected}
gider 0.731
gidiyor 0.269
```
```text {.python-playground-help}
`olcekli = {t: ___ ...}` | Sıcaklık puanlara uygulanır: `p / sicaklik`.
`secilenler = ___` | `sorted(olcekli, key=olcekli.get, reverse=True)` token'ları puana göre büyükten küçüğe sıralar; sonuna `[:k]` ekle.
`olasilik = ___` | `math.exp(olcekli[t]) / toplam`. Toplam yalnızca seçilenlerden hesaplandığı için iki olasılığın toplamı 1 olur.
```
```python {.python-playground-solution}
import math

puanlar = {"gider": 2.0, "gidiyor": 1.5, "koşar": 0.5, "uçar": -1.0}
sicaklik = 0.5
k = 2

# Her puanı sıcaklığa böl.
olcekli = {t: p / sicaklik for t, p in puanlar.items()}

# Puanı en yüksek k token'ı seç (sorted ile büyükten küçüğe sırala, ilk k tanesini al).
secilenler = sorted(olcekli, key=olcekli.get, reverse=True)[:k]

toplam = sum(math.exp(olcekli[t]) for t in secilenler)
for t in secilenler:
    # Softmax: bu token'ın e üstü puanını toplama böl.
    olasilik = math.exp(olcekli[t]) / toplam
    print(t, round(olasilik, 3))
```

## 3. Kütüphaneyle yap

Şimdi bu yöntemleri PyTorch'ta yazıp 6.4'teki mini GPT'de deneyelim. Kod, 6.4'teki `mini_gpt.py`'yi kullanır; ikisini aynı proje klasöründe tutman yeterli (`docs/faz-06-kucuk-dil-modeli/05-metin-uretimi/kod/uretim.py`). Kodu `python uretim.py` ile çalıştır; önce modeli 6.4'teki gibi eğitir (yarım dakika kadar), sonra aynı başlangıçtan altı farklı ayarla 200 karakter üretir:

```python
"""Ders 6.5 – Metin üretimi: açgözlü seçim, sıcaklık, top-k ve top-p.

PyTorch gerekir. Çalıştır:  python kod/uretim.py

6.4'teki mini GPT'yi eğitir, sonra aynı modelden farklı üretim ayarlarıyla metin üretir.
"""

import pathlib
import sys

import torch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "04-mini-gpt-egitimi" / "kod"))
import mini_gpt as mg  # noqa: E402


def sonraki_token(logitler, sicaklik=1.0, top_k=None, top_p=None):
    """Tek bir konumun logitlerinden (1 boyutlu tensör) bir sonraki token'ı seçer.

    sicaklik=0 açgözlü seçimdir: en yüksek puanlı token.
    """
    if sicaklik == 0:
        return int(logitler.argmax())
    logitler = logitler / sicaklik
    if top_k is not None:
        esik = torch.topk(logitler, top_k).values[-1]
        logitler = logitler.masked_fill(logitler < esik, float("-inf"))
    if top_p is not None:
        sirali, sira = torch.sort(logitler, descending=True)
        birikimli = torch.softmax(sirali, dim=-1).cumsum(dim=-1)
        at = birikimli - torch.softmax(sirali, dim=-1) >= top_p  # öncekiler zaten p'yi doldurduysa at
        logitler = logitler.clone()
        logitler[sira[at]] = float("-inf")
    olasiliklar = torch.softmax(logitler, dim=-1)
    return int(torch.multinomial(olasiliklar, 1))


@torch.no_grad()
def uret(model, baslangic, stoi, karakterler, uzunluk=80, **ayarlar):
    model.eval()
    idler = [stoi[k] for k in baslangic]
    for _ in range(uzunluk):
        logitler = model(torch.tensor([idler[-mg.BLOK:]]))[0, -1]
        idler.append(sonraki_token(logitler, **ayarlar))
    return "".join(karakterler[i] for i in idler)


def main():
    metin = mg.VERI_YOLU.read_text(encoding="utf-8")
    karakterler, stoi, egitim, dogrulama = mg.veri_hazirla(metin)
    torch.manual_seed(0)
    model = mg.MiniGPT(len(karakterler))
    mg.egit(model, egitim, dogrulama)

    denemeler = [
        ("açgözlü", dict(sicaklik=0)),
        ("sıcaklık 0.5", dict(sicaklik=0.5)),
        ("sıcaklık 1.0", dict(sicaklik=1.0)),
        ("sıcaklık 2.0", dict(sicaklik=2.0)),
        ("top-k 3", dict(top_k=3)),
        ("top-p 0.8", dict(top_p=0.8)),
    ]
    for ad, ayarlar in denemeler:
        torch.manual_seed(1)
        print(f"{ad}:")
        print("  " + uret(model, "çocuklar ", stoi, karakterler, uzunluk=200, **ayarlar).replace("\n", " "))


if __name__ == "__main__":
    main()
```

Beklenen çıktı (PyTorch sürümüne göre farklı metinler çıkabilir; ayarlar arasındaki fark aynı kalır):

```text
açgözlü:
  çocuklar ağaçları kapır. ali olur. ali dereren ardır. kasabaharda kütüphanes onra sabahı kada sabahı kayazarda kütüphar yeni gider. ali alırda kütüphanes onara sabahı kayazarda kütüphar yeni gider. ali alırda 
sıcaklık 0.5:
  çocuklar ağaçları an herkes bir derini de kitap okur. soru çocuklar bir der. her kasabahayarda herken herkes anın anında kapı okula çocuklar kar sabarda yam sabahçede kitap ayşe kitap okuma vardır. soruyu yazı
sıcaklık 1.0:
  çocuklar ağaçları an herkmekesinde der. bokumşlur yaperetler. ayşe iler alinemet alı yazar. öğiçiçler. eklerines olunr. bahm kakinı çocukla bir okurl okur. yazardamlta yeinder. ali ede er. am ayşedere kitap ağ
sıcaklık 2.0:
  çocuklar ağraymapyara hemmek tedkmedenler apaşplata per. kşamda dardaftauır. heri çocuöğden öğrmsçübüşmeklevminefta küçıcırbak kisı çitcude çar. bero okuyndara mıövlerkleindur eğlek de er.kizeukl dapar çük adı
top-k 3:
  çocuklar ağaçları an yar. çocuklar bazarı kayşam hayakı kar. sabında bir varda kitap vardır. ayşe sok herkes ona sabahçı kar badan sırınını sada kar. bahçederki her kasabininde küri gütir. ayşe ayşe ayşer. ayş
top-p 0.8:
  çocuklar ağaçları an bir gün aline de alır. ayşe meklerin sorularar. akşam saki ekleri ekmekleri sıcak sakı sanında kütüphar küphanes onada baharda herker verker kütüphanemen gir. kapı dan anın dever. kabapada
```

### Kodu parça parça okumak

- **`sicaklik == 0`**: Sıfıra bölemeyiz; sıfır sıcaklığı açgözlü seçim olarak yorumlarız (`argmax`).
- **`logitler / sicaklik`**: 2.2'deki gibi bütün puanları sıcaklığa böler.
- **Top-k**: `torch.topk(logitler, top_k).values[-1]`, `k`. en büyük puandır. Ondan küçük puanları `-inf` yaparız; softmax'ta `e ** -inf = 0` olur, yani bu token'lar asla seçilmez.
- **Top-p**: Puanları sıralar, olasılıkların birikimli toplamını (`cumsum`) bulur. Kendisinden önceki token'ların toplamı zaten `p`'ye ulaşmışsa token atılır (2.3'teki döngünün tensör hâli). En olası token hiçbir zaman atılmaz.
- **`torch.multinomial`**: Kalan olasılıklara göre bir token örnekler (6.1).

### Sonuçları yorumlamak

- **Açgözlü:** İlk cümleler fena değil, ama sonra `kütüphanes onara sabahı kayazarda kütüphar yeni gider. ali alırda` parçası **tekrar tekrar** gelir. Model bu döngüden çıkamaz.
- **Sıcaklık 0.5:** Döngü yok; metin açgözlüye yakın tutarlılıkta ama çeşitli. `kitap okur`, `çocuklar` gibi doğru sözcükler çok.
- **Sıcaklık 1.0:** Modelin kendi olasılıkları. Daha çeşitli, ama uydurma sözcükler (`bokumşlur`) artıyor.
- **Sıcaklık 2.0:** Olasılıklar neredeyse eşitlendi; düşük olasılıklı harfler sık seçiliyor ve metin anlamsız harf yığınına dönüyor.
- **Top-k 3 ve top-p 0.8:** Sıcaklık 1'deki çeşitliliği korurken saçma harfleri eliyor; metin `T = 1`'e göre daha düzgün.

Hangi ayarın "doğru" olduğu işe bağlıdır: Kod yazdırırken ya da bir soruyu cevaplatırken düşük sıcaklık, hikâye ya da fikir ürettirirken daha yüksek sıcaklık tercih edilir.

## 4. Sık yapılan hatalar

- **Sıcaklığı softmax'tan sonra uygulamak.** Sıcaklık puanlara (logitlere) uygulanır: `softmax(puan / T)`. Olasılıkları `T`'ye bölmek, yeniden ölçeklenince hiçbir şey değiştirmez.
- **Sıcaklığı sıfır vermek.** `puan / 0` hata verir ya da sonsuz üretir. Sıfır sıcaklığı ayrıca açgözlü seçim olarak ele al.
- **Top-k ya da top-p'den sonra yeniden ölçeklememek.** Atılan token'ların olasılıkları sıfırlanınca kalanların toplamı 1'den küçük olur. `-inf` ile softmax kullanmak bunu kendiliğinden çözer.
- **Top-p'de en olası token'ı da atmak.** En olası token tek başına `p`'yi aşıyorsa bile tutulmalıdır; yoksa seçilecek token kalmaz.
- **Açgözlü seçimin "en iyi" metni verdiğini sanmak.** Her adımda en olası token'ı seçmek, bütün metnin en olası olmasını sağlamaz; üstelik tekrara düşer.
- **Rastgeleliği sabitlemeden ayarları karşılaştırmak.** Örneklemeli üretim her çalıştırmada farklıdır. Karşılaştırırken `torch.manual_seed` kullan ya da birçok örneğe bak.

## 5. Pekiştir

**Quiz**

1. Açgözlü seçimin iki sorunu nedir?
2. Sıcaklık `0.25` olunca en olası token'ın olasılığı artar mı, azalır mı? Neden?
3. Top-k ile top-p arasındaki fark nedir? Model çok eminse top-p kaç token tutar?
4. Top-k'da atılan token'ların puanlarını neden `-inf` yapıyoruz?
5. Bir soruya kesin bir cevap istiyorsan sıcaklığı düşük mü yüksek mi seçersin? Ya bir şiir yazdırırken?

**Alıştırmalar**

1. 2.1'de `k=10` yerine `k=1000` örnekle ve her token'ın kaç kez seçildiğini `Counter` ile say. Oranlar olasılıklara yakın mı?
2. 2.2'de `T = 0.1` ve `T = 100` dene. Sonuçlar neye benziyor?
3. 2.3'te top-p'yi `0.5` ve `0.99` yap. Kaç token kalıyor?
4. Kütüphane kodunda `dict(sicaklik=0.7, top_p=0.9)` ayarını ekle. Bu, sohbet uygulamalarında sık kullanılan bir ayardır. Metin nasıl görünüyor?
5. (İsteğe bağlı) Açgözlü üretimde döngünün kaçıncı karakterde başladığını bulan küçük bir kod yaz.

??? success "Quiz cevapları"
    1. Her zaman aynı metni üretir (çeşitlilik yok) ve kendini tekrar etmeye başlayınca döngüden çıkamaz.
    2. Artar. Puanlar `0.25`'e bölününce (yani 4 ile çarpılınca) aralarındaki farklar büyür; softmax en yüksek puana çok daha fazla olasılık verir.
    3. Top-k her zaman sabit sayıda (`k`) token tutar; top-p, olasılıkları toplamı `p`'ye ulaşana kadar token tutar. Model çok eminse (en olası token tek başına `p`'yi aşıyorsa) top-p yalnızca o bir token'ı tutar.
    4. `e ** -inf = 0` olduğu için softmax bu token'lara sıfır olasılık verir; kalanlar kendiliğinden yeniden ölçeklenir.
    5. Kesin cevap için düşük sıcaklık (tutarlılık); şiir için daha yüksek sıcaklık (çeşitlilik).

## Özet

Dil modeli her adımda olasılıklar verir; metni üretmek için bunlardan bir token seçmemiz gerekir. Açgözlü seçim tutarlı ama tekdüzedir ve tekrara düşer. Olasılıklara göre örnekleme çeşitlilik getirir ama düşük olasılıklı saçma token'ları da seçebilir. Sıcaklık, puanları bölerek olasılıkları keskinleştirir (`T < 1`) ya da yumuşatır (`T > 1`). Top-k ve top-p, kuyruktaki düşük olasılıklı token'ları tamamen eler. Aynı modelde bu ayarlarla döngüye giren, tutarlı, çeşitli ya da anlamsız metinler ürettik. Sıradaki derste küçük bir Türkçe veri deneyi tasarlayıp sonuçlarını yorumlayacağız.

## Kaynaklar

- Ari Holtzman ve ark. (2020), *The Curious Case of Neural Text Degeneration*, ICLR (top-p / nucleus örnekleme)
- Angela Fan, Mike Lewis, Yann Dauphin (2018), *Hierarchical Neural Story Generation*, ACL (top-k örnekleme)
- [Hugging Face: How to generate text](https://huggingface.co/blog/how-to-generate)
