# Faz 6 – Ders 6: Küçük Türkçe veriyle deney

> ⏱️ Tahmini süre: 60-80 dk · 📚 Ön koşul: 6.4 Mini GPT eğitimi, 6.5 Metin üretimi · 💻 Gereksinim: Python 3.11+; sayfadaki pencereler ek paketsiz çalışır, deney için PyTorch kurulmalıdır

## Bu derste ne öğreneceksin?

- Bir deneyi **tek bir şeyi değiştirerek** tasarlamayı
- Kayıp eğrilerinden **aşırı uyumu** (overfitting) tanımayı
- **Erken durdurma** ile en iyi modeli saklamayı
- Model boyutu, dropout ve veri miktarının sonuca etkisini ölçmeyi
- Sonuçları bir tabloda toplayıp dürüstçe yorumlamayı

## 1. Problem

6.4'te mini GPT'yi bir ayarla eğittik ve doğrulama kaybı 1.39'a indi. Peki bu iyi mi? Daha büyük bir model daha iyi olur muydu? Dropout gerçekten işe yarıyor mu? Daha az veriyle ne olurdu?

Bu soruların cevabını tahmin etmek yerine **ölçeriz**. Makine öğrenmesinde çalışmanın büyük kısmı budur: bir şeyi değiştirip modeli yeniden eğitmek, sonuçları karşılaştırmak ve ne olduğunu anlamak. İyi bir deneyin birkaç kuralı var:

- **Her seferinde tek bir şeyi değiştir.** Hem modeli büyütüp hem dropout'u kaldırırsan sonucun hangisinden geldiğini bilemezsin.
- **Geri kalan her şeyi sabit tut:** aynı veri, aynı adım sayısı, aynı rastgele tohum (`torch.manual_seed`).
- **Doğrulama kaybına bak.** Eğitim kaybı yalnızca modelin eğitim metnini ne kadar iyi bildiğini gösterir.
- **Sonuçları yaz.** Bir tabloda toplamadığın deneyi bir hafta sonra hatırlamazsın.

Bu derste 6.4'teki modeli dört farklı ayarla eğitip sonuçları karşılaştıracağız. Önce deneyin sonuçlarını okumayı öğrenelim; deneyin kodu 3. bölümde.

## 2. Kendin yaz

### 2.1 Kayıp eğrisini okumak

Aşağıda 6.4'teki modelin **dropout olmadan** eğitildiğinde her 250 adımda ölçülen doğrulama kayıpları var (3. bölümdeki deneyden). En iyi noktayı ve aşırı uyumun başladığı yeri bulalım:

```python {.python-playground}
dogrulama = [3.59, 2.01, 1.71, 1.52, 1.58, 1.61, 1.73, 1.83, 2.02, 2.24, 2.25, 2.50, 2.58]
aralik = 250

en_iyi = min(dogrulama)
en_iyi_adim = dogrulama.index(en_iyi) * aralik
print(f"En iyi doğrulama kaybı: {en_iyi} (adım {en_iyi_adim})")
print(f"Son doğrulama kaybı: {dogrulama[-1]} (adım {(len(dogrulama) - 1) * aralik})")
print(f"Sonda en iyiye göre {dogrulama[-1] - en_iyi:.2f} daha kötü")
print()
for i, kayip in enumerate(dogrulama):
    cubuk = "█" * round(kayip * 10)
    print(f"adım {i * aralik:4}  {kayip:.2f}  {cubuk}")
```
```text {.python-playground-expected}
En iyi doğrulama kaybı: 1.52 (adım 750)
Son doğrulama kaybı: 2.58 (adım 3000)
Sonda en iyiye göre 1.06 daha kötü

adım    0  3.59  ████████████████████████████████████
adım  250  2.01  ████████████████████
adım  500  1.71  █████████████████
adım  750  1.52  ███████████████
adım 1000  1.58  ████████████████
adım 1250  1.61  ████████████████
adım 1500  1.73  █████████████████
adım 1750  1.83  ██████████████████
adım 2000  2.02  ████████████████████
adım 2250  2.24  ██████████████████████
adım 2500  2.25  ██████████████████████
adım 2750  2.50  █████████████████████████
adım 3000  2.58  ██████████████████████████
```
```text {.python-playground-help}
`min(dogrulama)` | En küçük doğrulama kaybı: modelin yeni metinde en iyi olduğu an.
`dogrulama.index(en_iyi) * aralik` | En iyi kaybın listedeki sırası; her ölçüm 250 adımda bir yapıldığı için 250 ile çarparız.
`"█" * round(kayip * 10)` | Kaybı bir çubuk olarak çizer: kayıp ne kadar büyükse çubuk o kadar uzun.
```

Eğri tipik bir **U** şekli çiziyor:

- **Adım 0 → 750:** Model genel kuralları öğreniyor (sık harfler, heceler, ekler). Doğrulama kaybı düşüyor.
- **Adım 750:** En iyi nokta (1.52).
- **Adım 750 → 3000:** Eğitim kaybı düşmeye devam ediyor (sonda 0.38), ama doğrulama kaybı **yükseliyor**. Model artık genel kuralları değil, eğitim metninin kendisini öğreniyor: hangi cümleden sonra hangi cümlenin geldiğini **ezberliyor**. Bu bilgi yeni metinde işe yaramaz, hatta zarar verir. Buna **aşırı uyum** (overfitting) denir.

3000. adımdaki model, 750. adımdakinden çok daha kötü. Eğitimi uzun tutmak her zaman iyi değildir.

### 2.2 Deneyleri karşılaştırmak

Dört deneyin sonuçlarını bir tabloya koyup en iyiden en kötüye sıralayalım. `en iyi` sütunu, eğitim boyunca görülen en düşük doğrulama kaybıdır:

```python {.python-playground}
sonuclar = [
    # ad, parametre, en iyi doğrulama kaybı, en iyi adım, son doğrulama kaybı
    ("temel (D=32, dropout 0.2)", 28511, 1.39, 1500, 1.55),
    ("dropout yok", 28511, 1.52, 750, 2.58),
    ("büyük model (D=64), dropout yok", 106143, 1.61, 250, 3.18),
    ("yarım veri", 28511, 2.11, 750, 3.09),
]

sonuclar.sort(key=lambda s: s[2])
print(f"{'deney':33} {'parametre':>9} {'en iyi':>6} {'adım':>5} {'son':>5}")
for ad, parametre, en_iyi, adim, son in sonuclar:
    print(f"{ad:33} {parametre:>9} {en_iyi:>6.2f} {adim:>5} {son:>5.2f}")

kazanan = sonuclar[0]
print()
print("En iyi deney:", kazanan[0])
```
```text {.python-playground-expected}
deney                             parametre en iyi  adım   son
temel (D=32, dropout 0.2)             28511   1.39  1500  1.55
dropout yok                           28511   1.52   750  2.58
büyük model (D=64), dropout yok      106143   1.61   250  3.18
yarım veri                            28511   2.11   750  3.09

En iyi deney: temel (D=32, dropout 0.2)
```
```text {.python-playground-help}
`sonuclar.sort(key=lambda s: s[2])` | Listeyi her satırın 3. elemanına (en iyi doğrulama kaybı) göre küçükten büyüğe sıralar.
`f"{ad:33}"` | Metni 33 karakterlik alana yazar; sütunlar hizalanır.
`sonuclar[0]` | Sıralamadan sonra ilk satır en düşük kayıplı, yani en iyi deneydir.
```

Tabloyu satır satır okuyalım:

- **Dropout yok vs. temel:** Tek fark dropout. Dropout'suz model daha erken (750. adım) ve daha kötü bir noktada (1.52) zirveye ulaştı, sonra hızla ezberledi (son kayıp 2.58). Dropout ezberlemeyi yavaşlattı ve en iyi kaybı iyileştirdi (1.39).
- **Büyük model:** Dört kat fazla parametre, ama sonuç **daha kötü** (1.61). 3000 karakterlik metin bu kadar parametre için çok az; model 250. adımda zirveye ulaşıp ezberlemeye başladı. **Daha büyük model her zaman daha iyi değildir**; model büyüklüğü veriyle orantılı olmalı.
- **Yarım veri:** Aynı model, eğitim metninin yarısı. En iyi kayıp 2.11; açık ara en kötü. Az veri, modelin öğrenebileceği genel kural miktarını sınırlar.

Bu tablodan çıkan en önemli ders: **Bu modelin önündeki asıl engel veri azlığı.** Gerçek dil modelleri bu yüzden milyarlarca token'lık metinle eğitilir.

### 2.3 Erken durdurma

Doğrulama kaybı yükselmeye başlayınca eğitimi durdurup **en iyi noktadaki** modeli saklamaya **erken durdurma** (early stopping) denir. Doğrulama kaybı ölçümden ölçüme biraz oynadığı için ilk yükselişte hemen durmayız; birkaç ölçüm daha bekleriz. Beklediğimiz ölçüm sayısına **sabır** (patience) denir.

### Şimdi sen yaz: erken durdurma

**Görev:** Temel deneyin her 250 adımda ölçülen doğrulama kayıpları kodda hazır. Kayıpları sırayla gezip en iyi kaybı takip edecek, iyileşme olmayan ölçümleri sayacak ve sayaç sabra ulaşınca eğitimi durduracaksın. Ekranda eğitimin durduğu adım ile en iyi adım ve kayıp görünmeli.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
dogrulama = [3.59, 2.06, 1.82, 1.62, 1.53, 1.44, 1.39, 1.44, 1.44, 1.43, 1.50, 1.56, 1.55]
aralik = 250
sabir = 2

en_iyi, en_iyi_adim, sayac = float("inf"), 0, 0
for i, kayip in enumerate(dogrulama):
    adim = i * aralik
    # TODO 1: Bu kayıp şimdiye kadarki en iyiden küçük mü?
    if ___:
        en_iyi, en_iyi_adim, sayac = kayip, adim, 0
    else:
        # TODO 2: İyileşme yok; sayacı bir artır.
        sayac = ___
    # TODO 3: Sayaç sabra ulaştı mı?
    if ___:
        print("Eğitim durdu: adım", adim)
        break

print("En iyi adım:", en_iyi_adim, "kayıp:", en_iyi)
```
```text {.python-playground-expected}
Eğitim durdu: adım 2000
En iyi adım: 1500 kayıp: 1.39
```
```text {.python-playground-help}
`if ___:` | Yeni kaybı şimdiye kadarki en iyiyle karşılaştır: `kayip < en_iyi`.
`sayac = ___` | Bir önceki değere bir ekle: `sayac + 1`.
`if ___:` | `sayac >= sabir` ise art arda `sabir` ölçüm boyunca iyileşme olmamıştır.
```
```python {.python-playground-solution}
dogrulama = [3.59, 2.06, 1.82, 1.62, 1.53, 1.44, 1.39, 1.44, 1.44, 1.43, 1.50, 1.56, 1.55]
aralik = 250
sabir = 2

en_iyi, en_iyi_adim, sayac = float("inf"), 0, 0
for i, kayip in enumerate(dogrulama):
    adim = i * aralik
    # Bu kayıp şimdiye kadarki en iyiden küçük mü?
    if kayip < en_iyi:
        en_iyi, en_iyi_adim, sayac = kayip, adim, 0
    else:
        # İyileşme yok; sayacı bir artır.
        sayac = sayac + 1
    # Sayaç sabra ulaştı mı?
    if sayac >= sabir:
        print("Eğitim durdu: adım", adim)
        break

print("En iyi adım:", en_iyi_adim, "kayıp:", en_iyi)
```

## 3. Kütüphaneyle yap

Aşağıda deneyin eksiksiz kodu var. 6.4'teki `mini_gpt.py`'yi kullanır; proje klasöründeki yerinde (`docs/faz-06-kucuk-dil-modeli/06-kucuk-turkce-veri-deneyi/kod/deney.py`) çalıştırman yeterli: `python deney.py`. Dört model, her biri 3000 adım eğitildiği için sıradan bir bilgisayarda birkaç dakika sürer.

```python
"""Ders 6.6 – Küçük Türkçe veriyle deney: model boyutu, dropout ve veri miktarının etkisi.

PyTorch gerekir. Çalıştır:  python kod/deney.py   (birkaç dakika sürer)

6.4'teki mini GPT'yi dört farklı ayarla eğitir. Her 250 adımda doğrulama kaybını ölçer,
en iyi doğrulama kaybını ve o anki modeli saklar (erken durdurma), sonunda sonuç tablosu yazar.
"""

import copy
import pathlib
import sys

import torch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "04-mini-gpt-egitimi" / "kod"))
import mini_gpt as mg  # noqa: E402

DENEYLER = [
    # ad, gömme boyutu, dropout, eğitim verisinin kullanılan oranı
    ("temel (D=32, dropout 0.2)", 32, 0.2, 1.0),
    ("dropout yok", 32, 0.0, 1.0),
    ("büyük model (D=64), dropout yok", 64, 0.0, 1.0),
    ("yarım veri", 32, 0.2, 0.5),
]


def model_kur(sozluk_boyutu, d, dropout):
    """mini_gpt'deki ayarları değiştirip yeni bir model kurar."""
    mg.D, mg.DROPOUT = d, dropout
    return mg.MiniGPT(sozluk_boyutu)


def deney_yap(egitim, dogrulama, sozluk_boyutu, d, dropout, oran,
              adim_sayisi=3000, aralik=250, batch=32, ogrenme_hizi=1e-3):
    torch.manual_seed(0)
    model = model_kur(sozluk_boyutu, d, dropout)
    egitim = egitim[: int(len(egitim) * oran)]
    optimizer = torch.optim.AdamW(model.parameters(), lr=ogrenme_hizi)
    gecmis, en_iyi = [], (float("inf"), 0, None)
    for adim in range(adim_sayisi + 1):
        if adim % aralik == 0:
            e, v = mg.kayip_olc(model, egitim), mg.kayip_olc(model, dogrulama)
            gecmis.append((adim, e, v))
            if v < en_iyi[0]:
                en_iyi = (v, adim, copy.deepcopy(model.state_dict()))
        if adim == adim_sayisi:
            break
        kayip = mg.kayip_hesapla(model, *mg.batch_al(egitim, batch))
        optimizer.zero_grad()
        kayip.backward()
        optimizer.step()
    parametre = sum(p.numel() for p in model.parameters())
    return gecmis, en_iyi, parametre


def main():
    metin = mg.VERI_YOLU.read_text(encoding="utf-8")
    karakterler, stoi, egitim, dogrulama = mg.veri_hazirla(metin)
    sonuclar = []
    for ad, d, dropout, oran in DENEYLER:
        gecmis, (en_iyi_kayip, en_iyi_adim, _), parametre = deney_yap(
            egitim, dogrulama, len(karakterler), d, dropout, oran)
        print(ad)
        print("  doğrulama kaybı:", " ".join(f"{v:.2f}" for _, _, v in gecmis))
        sonuclar.append((ad, parametre, en_iyi_kayip, en_iyi_adim, gecmis[-1][1], gecmis[-1][2]))

    print()
    print(f"{'deney':33} {'parametre':>9} {'en iyi doğr.':>12} {'adım':>5} {'son eğitim':>10} {'son doğr.':>9}")
    for ad, parametre, en_iyi_kayip, adim, son_e, son_v in sonuclar:
        print(f"{ad:33} {parametre:>9} {en_iyi_kayip:>12.2f} {adim:>5} {son_e:>10.2f} {son_v:>9.2f}")


if __name__ == "__main__":
    main()
```

Beklenen çıktı (kayıplar PyTorch sürümüne ve bilgisayara göre küçük farklar gösterebilir; deneyler arasındaki sıralama aynı kalmalıdır):

```text
temel (D=32, dropout 0.2)
  doğrulama kaybı: 3.59 2.06 1.82 1.62 1.53 1.44 1.39 1.44 1.44 1.43 1.50 1.56 1.55
dropout yok
  doğrulama kaybı: 3.59 2.01 1.71 1.52 1.58 1.61 1.73 1.83 2.02 2.24 2.25 2.50 2.58
büyük model (D=64), dropout yok
  doğrulama kaybı: 3.57 1.61 1.64 1.97 2.32 2.57 2.84 2.96 2.86 3.11 3.09 3.12 3.18
yarım veri
  doğrulama kaybı: 3.59 2.21 2.14 2.11 2.15 2.20 2.34 2.62 2.66 2.74 2.85 3.06 3.09

deney                             parametre en iyi doğr.  adım son eğitim son doğr.
temel (D=32, dropout 0.2)             28511         1.39  1500       0.58      1.55
dropout yok                           28511         1.52   750       0.38      2.58
büyük model (D=64), dropout yok      106143         1.61   250       0.20      3.18
yarım veri                            28511         2.11   750       0.28      3.09
```

### Kodu parça parça okumak

- **`DENEYLER`**: Her satır bir deney. Temel ayara göre **yalnızca bir şey** değişiyor (büyük model satırında dropout da kapalı; onu "dropout yok" satırıyla karşılaştırıyoruz).
- **`model_kur`**: `mini_gpt` modülündeki `D` ve `DROPOUT` ayarlarını değiştirip yeni model kurar. Model kurulurken bu ayarlar okunduğu için her deneyden önce değiştirmek yeterli.
- **`torch.manual_seed(0)`**: Her deney aynı başlangıç ağırlıkları ve aynı batch'lerle başlar. Farkın rastgelelikten değil, değiştirdiğimiz ayardan geldiğinden emin oluruz.
- **`egitim[: int(len(egitim) * oran)]`**: Yarım veri deneyinde eğitim metninin ilk yarısını kullanır. Doğrulama metni her deneyde **aynıdır**; yoksa sonuçlar karşılaştırılamazdı.
- **`copy.deepcopy(model.state_dict())`**: Doğrulama kaybı o ana kadarki en iyiyse modelin ağırlıklarının bir kopyasını saklar. Eğitim bitince `model.load_state_dict(...)` ile en iyi modele dönülebilir. Bu, erken durdurmanın kütüphane hâlidir: Eğitimi durdurmasak bile en iyi modeli kaybetmeyiz.

### Sonuçları dürüstçe yorumlamak

- **Tek tohum, tek koşu.** Her deneyi bir kez çalıştırdık. Farklı bir `manual_seed` ile sayılar biraz değişir. Buradaki farklar (1.39'a karşı 2.11) büyük olduğu için sonuç güvenilir, ama 1.39 ile 1.41 gibi küçük farklara dayanarak karar vermek için deneyi birkaç tohumla tekrarlayıp ortalamaya bakmak gerekir.
- **Küçük doğrulama kümesi.** Doğrulama metni yalnızca 306 karakter. Gerçek bir değerlendirme için çok daha büyük olmalı.
- **Sonuçlar bu veriye özgü.** "Büyük model daha kötü" sonucu yalnızca bu kadar az veri için geçerli. Veri arttıkça büyük modeller öne geçer; gerçek dil modellerinin büyük olmasının nedeni budur.

## 4. Sık yapılan hatalar

- **Aynı anda birden fazla şeyi değiştirmek.** Sonucun hangi değişiklikten geldiğini bilemezsin.
- **Rastgele tohumu sabitlememek.** İki deney arasındaki fark, değiştirdiğin ayardan değil, şanstan gelebilir.
- **Son modeli kullanmak.** Eğitimin sonundaki model en iyisi olmayabilir. En iyi doğrulama kaybındaki modeli sakla.
- **Doğrulama verisine göre çok fazla ayar yapmak.** Yüzlerce deney yapıp doğrulama kaybına göre en iyisini seçersen, doğrulama verisine de uyum sağlarsın. Büyük projelerde bu yüzden en sonda bir kez kullanılan üçüncü bir **test** kümesi ayrılır (2.4).
- **Deneyleri farklı doğrulama verileriyle karşılaştırmak.** Doğrulama metni her deneyde aynı olmalı.
- **Az veriyle büyük model eğitmek.** Model ezberler. Önce veri miktarına uygun küçük bir modelle başla.

## 5. Pekiştir

**Quiz**

1. Bir deneyde neden her seferinde yalnızca bir şeyi değiştiririz?
2. Kayıp eğrisinde aşırı uyumu nasıl tanırsın?
3. Erken durdurmada "sabır" ne işe yarar?
4. Deneyde büyük model neden küçük modelden kötü çıktı? Bu her zaman böyle midir?
5. Deneylere göre bu modeli iyileştirmenin en etkili yolu ne olurdu?

**Alıştırmalar**

1. 2.1'deki listeyi "büyük model" deneyinin kayıplarıyla değiştir (3. bölümdeki çıktıdan). En iyi adım kaçıncı? Eğri nasıl görünüyor?
2. 2.3'teki görevde `sabir = 2` yerine `sabir = 4` yap. Eğitim nerede durdu? En iyi kayıp değişti mi?
3. `DENEYLER` listesine `("küçük model (D=16)", 16, 0.2, 1.0)` ekle. Daha küçük model nasıl sonuç verdi?
4. Temel deneyi `torch.manual_seed(1)` ve `torch.manual_seed(2)` ile tekrarla. En iyi doğrulama kaybı ne kadar değişiyor?
5. (İsteğe bağlı) `kasaba.txt`'ye kendi yazdığın birkaç yüz karakterlik yeni cümleler ekle ve temel deneyi tekrarla. Doğrulama kaybı iyileşti mi?

??? success "Quiz cevapları"
    1. Aynı anda birden fazla şey değişirse sonucun hangisinden geldiğini bilemeyiz.
    2. Eğitim kaybı düşmeye devam ederken doğrulama kaybı yükselmeye başlar; iki kayıp arasındaki fark açılır.
    3. Doğrulama kaybı ölçümden ölçüme biraz oynar. Tek bir kötü ölçümde durmak yerine birkaç ölçüm bekleyerek gerçek bir yükselişi gürültüden ayırırız.
    4. 3000 karakterlik metin, 106 bin parametreli bir model için çok az; model genel kuralları öğrenmek yerine metni hızla ezberledi. Veri arttıkça büyük modeller genellikle daha iyi sonuç verir; bu sonuç az veriye özgüdür.
    5. Daha fazla veri: yarım veri deneyi, veri azaldığında sonucun ne kadar kötüleştiğini gösterdi. Model büyütmek tek başına işe yaramadı.

## Özet

İyi bir deney her seferinde tek bir şeyi değiştirir, geri kalanını (veri, tohum, adım sayısı) sabit tutar ve sonuçları doğrulama kaybıyla karşılaştırır. Kayıp eğrisinde doğrulama kaybı düşüp sonra yükseliyorsa model aşırı uyum sağlıyordur; erken durdurma en iyi noktadaki modeli saklar. Küçük Türkçe metnimizdeki deneyde dropout sonucu iyileştirdi, büyük model ise az veri yüzünden ezberledi ve verinin yarısıyla eğitilen model açık ara en kötüsü oldu: Bu boyutta bir modelin önündeki asıl engel veri azlığıdır. Böylece Faz 6'yı bitirdin: Sıfırdan bir tokenizer, bir dil modeli, üretim yöntemleri ve bir deney düzeni kurdun.

## Kaynaklar

- Lutz Prechelt (1998), *Early Stopping – But When?*, Neural Networks: Tricks of the Trade
- Jordan Hoffmann ve ark. (2022), *Training Compute-Optimal Large Language Models* (Chinchilla: model boyutu ve veri miktarı dengesi)
- Andrej Karpathy, [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/)
