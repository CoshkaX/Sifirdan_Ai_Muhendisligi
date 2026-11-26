# Faz 4 – Ders 7: Veri setleri: nereden bulunur, lisans ve etik

> ⏱️ Tahmini süre: 50-65 dk · 📚 Ön koşul: 2.4 Eğitim, doğrulama ve test, 4.3 Metin temizleme, 4.6 Duygu analizi · 💻 Gereksinim: Python 3.11+, ek paket yok; `datasets` örneği için Hugging Face `datasets` kurulmalıdır

## Bu derste ne öğreneceksin?

- Türkçe metin verisinin nerelerden bulunabileceğini
- Bir veri setini kullanmadan önce lisansına neden ve nasıl bakacağını
- Boş kayıt, tekrar, hatalı etiket ve sınıf dengesizliği gibi sorunları kodla bulmayı
- Eğitim ve test kümeleri arasındaki sızıntıyı yakalamayı
- Kişisel verileri maskelemeyi ve KVKK'nın neden önemli olduğunu

## 1. Problem

4.6 dersinde 16 yorumla bir duygu analizi modeli eğittik ve modelin ne kadar az şey öğrenebildiğini gördük. Gerçek bir model için binlerce, hatta milyonlarca örnek gerekir. Bu veriyi nereden bulacağız?

Veri bulmak yalnızca işin başı. Bir veri setini kullanmadan önce üç soruyu cevaplamak gerekir:

1. **Kullanabilir miyim?** Lisansı neye izin veriyor?
2. **Güvenilir mi?** İçinde tekrarlar, boş kayıtlar, yanlış etiketler var mı?
3. **Zarar verir mi?** Kişisel bilgi içeriyor mu? Belirli grupları yanlış temsil ediyor mu?

Yapay zekâ projelerindeki sorunların büyük bölümü modelden değil, veriden kaynaklanır. Bu ders, model eğitmeden önce yapılması gereken kontrolleri anlatıyor.

## 2. Türkçe veri nereden bulunur?

Aşağıdakiler başlangıç için bilinen kaynaklardır. Her birinde, hangi veri setini kullanırsan kullan, o setin kendi lisansını ayrıca kontrol etmelisin.

| Kaynak | Ne bulursun? | Not |
|---|---|---|
| [Hugging Face Hub](https://huggingface.co/datasets) | Binlerce veri seti; dil filtresinden "Turkish" seçilebilir | Her setin sayfasında bir **veri kartı** ve lisans bilgisi bulunur |
| [Universal Dependencies](https://universaldependencies.org/) | Türkçe cümlelerin dilbilgisel çözümlemeleri (örneğin IMST ve BOUN ağaç bankaları) | 4.2 dersindeki biçimbilim konusuyla ilgilenenler için |
| [OPUS](https://opus.nlpl.eu/) | Türkçe ve başka dillerde karşılıklı (paralel) cümleler | Makine çevirisi için |
| [Wikipedia dökümleri](https://dumps.wikimedia.org/trwiki/) | Türkçe Vikipedi'nin bütün metni | CC BY-SA lisanslıdır; gömme veya dil modeli eğitimi için sık kullanılır |
| Kendi verin | Şirketinin destek kayıtları, kendi topladığın anketler | Kişisel veri ve izin konusuna özellikle dikkat et |

!!! warning "Web'den veri toplamak"
    Bir sitedeki metni görebiliyor olman, onu kopyalayıp model eğitiminde kullanabileceğin anlamına gelmez. Sitenin kullanım koşullarına, telif haklarına ve kişisel veri içerip içermediğine bak. Emin değilsen lisansı açık olan bir veri setiyle başla.

### 2.1 Lisanslar: "açık" her zaman "serbest" demek değildir

İnternette bulduğun bir veri setinin lisansı, onunla neler yapabileceğini belirler. Sık karşılaşılan lisanslar:

| Lisans | Ne izin verir? | Dikkat |
|---|---|---|
| **CC0** | Her türlü kullanım; atıf bile zorunlu değil | En serbest seçenek |
| **CC BY** | Ticari dahil her türlü kullanım | Kaynağa **atıf** yapmak zorunludur |
| **CC BY-SA** | Ticari dahil her türlü kullanım | Atıf + türettiğin veriyi **aynı lisansla** paylaşma zorunluluğu |
| **CC BY-NC** | Yalnızca **ticari olmayan** kullanım | Bir ürün veya şirket projesinde kullanılamaz |
| **Lisans belirtilmemiş** | Hiçbir şey | Lisans yoksa varsayılan olarak bütün haklar sahibindedir; izin almadan kullanma |

Kod için kullanılan MIT ve Apache lisansları da bazen veri setlerinde görülür; ikisi de ticari kullanıma izin verir. Bir veri setiyle eğittiğin modelin hangi koşullarda paylaşılabileceği de bu lisanslara bağlı olabilir; ticari bir projede bu konuda bir hukukçuya danışmak gerekir.

## 3. Kendin yaz

### 3.1 Veri kalitesini kontrol et

Bir veri setini indirdikten sonra ilk iş, ona model eğitmek değil, **içine bakmaktır**. Aşağıdaki kod dört yaygın sorunu arar:

- **Boş kayıtlar:** Temizlendikten sonra hiçbir şey kalmayan metinler.
- **Geçersiz etiketler:** Beklenen sınıflardan biri olmayan etiketler.
- **Tekrarlar:** Büyük-küçük harf veya noktalama dışında aynı olan metinler. Model bunları fazla önemser; eğitim ve teste dağılırsa sonuç şişer.
- **Sınıf dağılımı:** Her sınıftan kaç örnek var? (2.6 dersindeki dengesizlik sorunu.)

```python {.python-playground}
import unicodedata
from collections import Counter


def normallestir(metin):
    metin = unicodedata.normalize("NFC", metin)
    metin = metin.replace("İ", "i").replace("I", "ı").lower()
    metin = "".join(h if h.isalnum() else " " for h in metin)
    return " ".join(metin.split())


veri = [
    ("Ürün çok güzel", 1),
    ("ürün çok güzel!", 1),
    ("", 0),
    ("Kargo geç geldi", 0),
    ("Fiyatı uygun", 2),
    ("Harika bir film", 1),
]

bos = [i for i, (metin, _) in enumerate(veri) if not normallestir(metin)]
gecersiz = [i for i, (_, etiket) in enumerate(veri) if etiket not in (0, 1)]

gorulen = {}
tekrarlar = []
for i, (metin, _) in enumerate(veri):
    anahtar = normallestir(metin)
    if anahtar and anahtar in gorulen:
        tekrarlar.append((gorulen[anahtar], i))
    elif anahtar:
        gorulen[anahtar] = i

print("Boş metin:", bos)
print("Geçersiz etiket:", gecersiz)
print("Tekrar eden çiftler:", tekrarlar)
print("Sınıf dağılımı:", dict(Counter(etiket for _, etiket in veri)))
```
```text {.python-playground-expected}
Boş metin: [2]
Geçersiz etiket: [4]
Tekrar eden çiftler: [(0, 1)]
Sınıf dağılımı: {1: 3, 0: 2, 2: 1}
```
```text {.python-playground-help}
`def normallestir(metin):` | 4.3 dersindeki adımlar; sonucu sözcük listesi değil, tek boşluklu bir metin olarak döndürür. Karşılaştırma bu biçim üzerinden yapılır.
`enumerate(veri)` | Her kaydın konum numarasını (`i`) da verir; böylece sorunlu kaydın yerini bildirebiliriz.
`if not normallestir(metin)` | Temizlendikten sonra boş kalan metin. Yalnızca boşluk veya noktalamadan oluşan kayıtları da yakalar.
`etiket not in (0, 1)` | Bu veri setinde yalnızca `0` ve `1` geçerli; `2` büyük olasılıkla bir etiketleme hatası.
`gorulen = {}` | Daha önce gördüğümüz normalleştirilmiş metinleri ve ilk göründükleri konumu tutar.
`tekrarlar.append((gorulen[anahtar], i))` | Aynı metin ikinci kez görüldüyse, ilk ve şimdiki konumu çift olarak kaydederiz.
`Counter(etiket for _, etiket in veri)` | Her etiketten kaç tane olduğunu sayar.
```

`0` ve `1` numaralı kayıtlar ilk bakışta farklı görünür, ama normalleştirince aynı cümledir. Gerçek veri setlerinde, özellikle web'den toplananlarda, tekrar oranı şaşırtıcı derecede yüksek olabilir.

### 3.2 Eğitim-test sızıntısını yakala

2.4 dersinde test kümesinin model için "hiç görülmemiş" veri olması gerektiğini söylemiştik. Ama aynı cümle hem eğitimde hem testte varsa model onu ezberleyip testte doğru cevaplar ve başarı olduğundan yüksek görünür. Bu bir **veri sızıntısıdır**. Hazır bölünmüş veri setlerinde bile görülebilir.

```python {.python-playground}
import unicodedata


def normallestir(metin):
    metin = unicodedata.normalize("NFC", metin)
    metin = metin.replace("İ", "i").replace("I", "ı").lower()
    metin = "".join(h if h.isalnum() else " " for h in metin)
    return " ".join(metin.split())


egitim = [("Harika bir film", 1), ("Kargo geç geldi", 0), ("Çok beğendim", 1)]
test = [("harika bir film.", 1), ("Kötü bir ürün", 0), ("ÇOK BEĞENDİM", 1)]

egitim_metinleri = {normallestir(m) for m, _ in egitim}
ortak = [m for m, _ in test if normallestir(m) in egitim_metinleri]

print(f"Test kümesinin {len(ortak)}/{len(test)} örneği eğitimde de var:")
for metin in ortak:
    print(" -", metin)
```
```text {.python-playground-expected}
Test kümesinin 2/3 örneği eğitimde de var:
 - harika bir film.
 - ÇOK BEĞENDİM
```
```text {.python-playground-help}
`egitim_metinleri = {normallestir(m) for m, _ in egitim}` | Eğitimdeki metinlerin normalleştirilmiş hâllerinden bir küme kurarız. Kümede arama çok hızlıdır.
`if normallestir(m) in egitim_metinleri` | Test metnini de aynı biçimde normalleştirip kümede ararız. Normalleştirmeden karşılaştırsaydık büyük harf ve nokta farkı yüzünden sızıntıyı göremezdik.
`f"{len(ortak)}/{len(test)}"` | Sızan örnek sayısını toplam test örneğine oranla gösteririz.
```

Bu örnekte test kümesinin üçte ikisi aslında eğitimde var. Böyle bir testte %100 başarı hiçbir şey kanıtlamaz. Sızan örnekleri testten çıkarmak veya bölmeyi tekrarlardan arındırdıktan sonra yapmak gerekir.

### 3.3 Kişisel verileri maskele

Kullanıcı yorumları, destek kayıtları veya sohbet metinleri çoğu zaman **kişisel veri** içerir: ad, e-posta, telefon numarası, T.C. kimlik numarası, adres... Türkiye'de bu veriler **6698 sayılı Kişisel Verilerin Korunması Kanunu (KVKK)** kapsamındadır. Bir modeli bu verilerle eğitmek, model onları ezberleyip başkalarına gösterebileceği için ayrıca risklidir.

Basit ama yararlı bir önlem, belirli kalıpları **düzenli ifadelerle** (regular expression) bulup yerlerine etiket koymaktır:

```python {.python-playground}
import re

EPOSTA = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
TELEFON = re.compile(r"(?<!\d)(?:\+90\s?|0)?5\d{2}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}(?!\d)")
TC_KIMLIK = re.compile(r"(?<!\d)[1-9]\d{10}(?!\d)")


def maskele(metin):
    metin = EPOSTA.sub("[EPOSTA]", metin)
    metin = TELEFON.sub("[TELEFON]", metin)
    metin = TC_KIMLIK.sub("[TCKN]", metin)
    return metin


ornekler = [
    "Bana ali.veli@ornek.com adresinden yazın.",
    "Numaram 0532 123 45 67, akşam arayın.",
    "TC kimlik no: 12345678901",
    "2024 yılında 3 ürün aldım, fiyatı 150 TL.",
]
for ornek in ornekler:
    print(maskele(ornek))
```
```text {.python-playground-expected}
Bana [EPOSTA] adresinden yazın.
Numaram [TELEFON], akşam arayın.
TC kimlik no: [TCKN]
2024 yılında 3 ürün aldım, fiyatı 150 TL.
```
```text {.python-playground-help}
`import re` | Python'ın düzenli ifade modülü. Düzenli ifade, metinde aranacak bir kalıbı tarif eden küçük bir dildir.
`re.compile(r"...")` | Kalıbı bir kez hazırlarız; sonra birçok metinde kullanırız. `r"..."` ters eğik çizgilerin olduğu gibi okunmasını sağlar.
`[\w.+-]+@[\w-]+(?:\.[\w-]+)+` | E-posta: harf/rakam/nokta dizisi, `@`, alan adı ve en az bir `.uzantı`.
`(?:\+90\s?|0)?5\d{2}...` | Cep telefonu: isteğe bağlı `+90` veya `0`, ardından `5` ile başlayan 10 hane; araya boşluk veya tire girebilir. `\d{2}` "iki rakam" demektir.
`(?<!\d)` ve `(?!\d)` | "Öncesinde/sonrasında rakam yok" koşulları. Daha uzun bir sayının ortasından parça yakalamayı önler.
`[1-9]\d{10}` | Sıfırla başlamayan 11 haneli sayı; T.C. kimlik numarası biçimi.
`EPOSTA.sub("[EPOSTA]", metin)` | Kalıba uyan her parçayı verilen etiketle değiştirir.
```

Son örnekteki sıradan sayılar (`2024`, `3`, `150`) dokunulmadan kaldı. Bu yöntemin sınırları var: İsimleri ve adresleri bulamaz ("Ayşe Hanım'ın evi Kadıköy'de"), yazım biçimi farklı bir numarayı kaçırabilir, 11 haneli rastgele bir sayıyı yanlışlıkla kimlik sanabilir. Gerçek projelerde bu kalıplar, ad ve yer tanıyan modellerle ve elle yapılan örnek kontrolleriyle birlikte kullanılır.

### 3.4 Ders kodu

Bu üç kontrolün düzenli hâli [`kod/veri_kontrol.py`](kod/veri_kontrol.py) dosyasındadır. Testler, farklı telefon yazımlarının maskelendiğini ve sıradan sayıların korunduğunu da denetler.

```bash
cd docs/faz-04-metin-ve-turkce-nlp/07-veri-setleri
python kod/veri_kontrol.py
python -m unittest discover -s test -v
```

### 3.5 Veri kartı: veri setinin kimliği

İyi hazırlanmış bir veri seti, ne olduğunu anlatan bir belgeyle gelir. Gebru ve arkadaşlarının önerdiği **"veri setleri için bilgi formu"** (datasheet) fikri, Hugging Face'te **veri kartı** (dataset card) olarak yaygınlaştı. Kendi veri setini paylaşırken en az şunları yaz:

- **Amaç:** Bu veri seti neden ve kim tarafından oluşturuldu?
- **İçerik:** Kaç örnek var, hangi alanlar var, etiketler ne anlama geliyor?
- **Kaynak:** Metinler nereden ve hangi tarihlerde toplandı? Kim etiketledi?
- **Lisans:** Hangi koşullarla kullanılabilir?
- **Sınırlar ve riskler:** Hangi gruplar veya konular az temsil ediliyor? Kişisel veri temizlendi mi?

Başkasının veri setini kullanırken de önce veri kartını oku. Veri kartı yoksa veya çok kısaysa bunu bir uyarı işareti say.

### Şimdi sen yaz: boş ve tekrar eden kayıtları say

Veri kaydındaki boş metinleri ve tekrarları say. `# TODO` yazan yerlerdeki `___` boşluklarını tamamla, sonra çalıştır.

```python {.python-playground-task}
veri = [("Harika ürün", 1), ("harika ürün", 1), ("", 0), ("Kötü", 0)]

bos_sayisi = 0
# set: tekrarsız öğeler kümesi. .add() ile öğe eklenir, in ile var mı diye bakılır.
gorulen = set()
tekrar_sayisi = 0

for metin, etiket in veri:
    temiz = metin.lower().strip()
    # TODO: Temizlenince boş kalan metni say.
    if ___:
        bos_sayisi += 1
    # TODO: Daha önce görülen metni tekrar olarak say.
    elif temiz in ___:
        tekrar_sayisi += 1
    else:
        gorulen.add(temiz)

print("Boş:", bos_sayisi, "Tekrar:", tekrar_sayisi)
```
```text {.python-playground-expected}
Boş: 1 Tekrar: 1
```
```text {.python-playground-help}
`if ___:` | Temizlenince hiçbir şey kalmadıysa `temiz` boş metindir: `temiz == ""`.
`elif temiz in ___:` | Daha önce gördüğümüz metinleri `gorulen` kümesinde tutuyoruz; metin orada varsa tekrardır.
```
```python {.python-playground-solution}
veri = [("Harika ürün", 1), ("harika ürün", 1), ("", 0), ("Kötü", 0)]

bos_sayisi = 0
# set: tekrarsız öğeler kümesi. .add() ile öğe eklenir, in ile var mı diye bakılır.
gorulen = set()
tekrar_sayisi = 0

for metin, etiket in veri:
    temiz = metin.lower().strip()
    # Temizlenince boş kalan metni say.
    if temiz == "":
        bos_sayisi += 1
    # Daha önce görülen metni tekrar olarak say.
    elif temiz in gorulen:
        tekrar_sayisi += 1
    else:
        gorulen.add(temiz)

print("Boş:", bos_sayisi, "Tekrar:", tekrar_sayisi)
```

## 4. Kütüphaneyle yap

Hugging Face'in `datasets` kütüphanesi, Hub'daki veri setlerini tek satırla indirmeyi ve büyük verilerde filtreleme, dönüştürme ve bölme işlemlerini verimli yapmayı sağlar. Aynı araçlar kendi CSV dosyaların için de çalışır. Aşağıdaki örnek internet bağlantısı gerektirmez.

Kütüphaneyi kur:

```bash
python -m pip install datasets
```

Kodu ders klasöründe `hf_veri.py` adıyla kaydet ve `python hf_veri.py` ile çalıştır:

```python
import csv
import sys
from collections import Counter

from datasets import load_dataset

sys.path.insert(0, "kod")
from veri_kontrol import kisisel_veriyi_maskele

satirlar = [
    ("Ürün çok güzel, beğendim", 1),
    ("Kargo geç geldi, bilgi için 0532 123 45 67", 0),
    ("Harika bir film", 1),
    ("Berbat, hiç beğenmedim", 0),
    ("Fiyatı uygun ve kaliteli", 1),
    ("Çok sıkıcı bir dizi", 0),
    ("Herkese tavsiye ederim", 1),
    ("Rengi güzel değil", 0),
]
with open("yorumlar.csv", "w", newline="", encoding="utf-8") as dosya:
    yazici = csv.writer(dosya)
    yazici.writerow(["metin", "etiket"])
    yazici.writerows(satirlar)

veri = load_dataset("csv", data_files="yorumlar.csv", split="train")
print(veri)
print("Sınıf sayıları:", dict(Counter(veri["etiket"])))

veri = veri.map(lambda ornek: {"metin": kisisel_veriyi_maskele(ornek["metin"])})
print(veri[1])

bolunmus = veri.train_test_split(test_size=0.25, seed=42)
print("Eğitim:", len(bolunmus["train"]), "Test:", len(bolunmus["test"]))
```

Beklenen çıktı (kütüphane ayrıca ilerleme çubukları da gösterebilir):

```text
Dataset({
    features: ['metin', 'etiket'],
    num_rows: 8
})
Sınıf sayıları: {1: 4, 0: 4}
{'metin': 'Kargo geç geldi, bilgi için [TELEFON]', 'etiket': 0}
Eğitim: 6 Test: 2
```

- `load_dataset("csv", data_files=..., split="train")`: CSV dosyasını bir `Dataset` nesnesine çevirir. Hub'daki bir veri seti için `"csv"` yerine veri setinin adı yazılır.
- `veri["etiket"]`: Bir sütunun bütün değerleri.
- `veri.map(...)`: Her örneğe bir fonksiyon uygular ve sonucu yeni bir veri seti olarak döndürür. Burada 3.3'teki maskelemeyi kullandık.
- `train_test_split(test_size=0.25, seed=42)`: 2.4 dersindeki eğitim-test bölmesi. `seed` aynı bölmeyi tekrar elde etmeyi sağlar.

Hub'dan bir veri seti indirdiğinde, kullanmadan önce bu dersteki kontrolleri (tekrar, boş kayıt, sınıf dağılımı, sızıntı, kişisel veri) onun üzerinde de çalıştır.

## 5. Sık yapılan hatalar

- **Lisansa bakmadan veri kullanmak.** "İnternette herkese açık" olması, model eğitiminde veya ticari bir üründe kullanılabileceği anlamına gelmez.
- **CC BY-NC lisanslı veriyle ticari ürün geliştirmek.** "NC" ticari olmayan kullanım demektir.
- **Veri setine hiç bakmadan model eğitmek.** Tekrarlar, boş kayıtlar ve hatalı etiketler modeli sessizce bozar. Rastgele 20-30 örneği gözle okumak bile çok şey öğretir.
- **Tekrarları bölmeden sonra temizlemek.** Önce tekrarları temizle, sonra eğitim-test bölmesini yap; yoksa aynı cümle iki tarafa da düşebilir.
- **Kişisel veriyi "nasılsa model görecek" diye bırakmak.** Modeller eğitim verisindeki numaraları, adresleri ezberleyip tekrar üretebilir. KVKK açısından da sorumluluk veriyi işleyene aittir.
- **Maskelemeyi kusursuz sanmak.** Düzenli ifadeler isimleri ve alışılmadık biçimleri kaçırır; sonuçları örneklerle kontrol et.
- **Verinin herkesi temsil ettiğini varsaymak.** Yalnızca belirli bir siteden, bölgeden veya yaş grubundan toplanan veriyle eğitilen model, başka gruplarda kötü çalışabilir.

## 6. Pekiştir

**Quiz**

1. Bir veri setini kullanmadan önce cevaplaman gereken üç soru nedir?
2. CC BY ile CC BY-NC arasındaki fark nedir? Lisansı belirtilmemiş bir veri setini kullanabilir misin?
3. Tekrar eden kayıtlar neden zararlıdır? Kontrol ederken neden önce normalleştiriyoruz?
4. Eğitim-test sızıntısı test sonucunu nasıl etkiler?
5. KVKK nedir ve metin verisiyle çalışırken neden önemlidir?

**Alıştırmalar**

1. 3.1'deki veriye `("   ", 1)` ve `("HARİKA BİR FİLM!!!", 1)` ekle. Rapor nasıl değişti?
2. 3.2'deki sızıntıyı temizle: test kümesinden eğitimde bulunan örnekleri çıkaran bir satır yaz.
3. 3.3'teki maskeleme fonksiyonuna `"Ev: 0216 123 45 67"` gibi bir sabit hat numarası ver. Maskelendi mi? Kalıbı sabit hatları da kapsayacak şekilde genişlet.
4. Hugging Face Hub'da dil filtresiyle Türkçe bir veri seti bul. Veri kartını oku: lisansı ne, kaç örnek var, nereden toplanmış?
5. (İsteğe bağlı) 4.6 dersindeki duygu analizi verisine `kod/veri_kontrol.py` içindeki `kalite_raporu` ve `sizinti` fonksiyonlarını uygula.

??? success "Quiz cevapları"
    1. Kullanabilir miyim (lisans)? Güvenilir mi (kalite)? Zarar verir mi (kişisel veri, temsil)?
    2. CC BY ticari kullanıma izin verir, yalnızca atıf ister; CC BY-NC ticari kullanımı yasaklar. Lisans yoksa bütün haklar sahibindedir; izin almadan kullanmamalısın.
    3. Model tekrar eden örnekleri fazla önemser ve eğitim ile test kümelerine dağılırsa sonucu şişirir. Büyük harf ve noktalama farkları aynı cümleyi farklı gösterebileceği için önce normalleştiririz.
    4. Model test örneklerini eğitimde gördüğü için onları ezberleyerek doğru cevaplar; başarı olduğundan yüksek görünür ve yeni verideki gerçek başarıyı yansıtmaz.
    5. 6698 sayılı Kişisel Verilerin Korunması Kanunu. Metinler ad, telefon, kimlik numarası gibi kişisel veriler içerebilir; bunları işlemek yasal yükümlülükler doğurur ve modeller bu bilgileri ezberleyip açığa çıkarabilir.

## Özet

Türkçe veri; Hugging Face Hub, Universal Dependencies, OPUS ve Vikipedi gibi kaynaklardan bulunabilir. Her veri setinin lisansı, onunla neler yapılabileceğini belirler; "herkese açık" her zaman "serbestçe kullanılabilir" demek değildir. Kullanmadan önce boş kayıtları, geçersiz etiketleri, tekrarları ve sınıf dağılımını kontrol etmek; eğitim-test sızıntısını aramak ve kişisel verileri maskelemek gerekir. Kendi veri setini paylaşırken amacını, kaynağını, lisansını ve sınırlarını anlatan bir veri kartı yaz.

## Kaynaklar

- Timnit Gebru ve ark. (2021), *Datasheets for Datasets*, Communications of the ACM
- [Hugging Face: Veri kartları (dataset cards)](https://huggingface.co/docs/hub/datasets-cards)
- [Hugging Face `datasets` belgeleri](https://huggingface.co/docs/datasets)
- [Creative Commons lisansları hakkında](https://creativecommons.org/licenses/)
- [Kişisel Verileri Koruma Kurumu (KVKK)](https://www.kvkk.gov.tr/)
- [Python resmî belgesi: `re` modülü](https://docs.python.org/3/library/re.html)
