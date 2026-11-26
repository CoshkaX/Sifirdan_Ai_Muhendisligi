# Faz 4 – Ders 6: Duygu analizi

> ⏱️ Tahmini süre: 60-75 dk · 📚 Ön koşul: 2.3 Lojistik regresyon, 2.4 Eğitim, doğrulama ve test, 4.5 Benzerlik ve arama · 💻 Gereksinim: Python 3.11+, ek paket yok; scikit-learn örneği için scikit-learn kurulmalıdır

## Bu derste ne öğreneceksin?

- Bir yorumun olumlu mu olumsuz mu olduğunu tahmin etmeyi
- Elle yazılmış sözcük listesiyle yapılan analizin neden yetersiz kaldığını
- Metni özellik kümesine çevirip lojistik regresyonla sınıflandırmayı
- Türkçede olumsuzluğun (`-me` eki ve `değil`) neden ayrıca ele alınması gerektiğini
- Bir görev için doğru olan ön işlemenin başka bir görevde neden zararlı olabileceğini

## 1. Problem

Bir e-ticaret sitesinde binlerce ürün yorumu olduğunu düşün. Hangi ürünlerin şikâyet aldığını görmek için hepsini okuyamazsın. **Duygu analizi** (sentiment analysis), bir metnin olumlu mu olumsuz mu olduğunu otomatik tahmin etme görevidir.

Bu, 2.3 dersindeki iki sınıflı sınıflandırmanın metne uygulanmış hâlidir: `1` olumlu, `0` olumsuz. Fark şu: Girdimiz bir sayı değil, bir cümle. Önce cümleyi modelin kullanabileceği özelliklere çevirmemiz gerekiyor.

Bu derste bu ders için yazılmış 16 eğitim ve 8 test yorumu kullanacağız. Bu kadar az veriyle gerçek bir model kurulmaz; amaç adımları görünür kılmaktır.

## 2. Kendin yaz

### 2.1 İlk deneme: olumlu ve olumsuz sözcük listeleri

En akla yatkın yöntem şudur: Olumlu ve olumsuz sözcüklerin listesini yaz, yorumda hangisinden çok varsa ona karar ver. Buna **sözlük tabanlı** yaklaşım denir.

```python {.python-playground}
olumlu = {"güzel", "beğendim", "harika", "iyi", "hızlı", "memnun", "teşekkürler"}
olumsuz = {"kötü", "berbat", "sıkıcı", "pahalı", "geç", "beğenmedim"}


def sozluk_ile_tahmin(yorum):
    sozcukler = yorum.lower().replace(",", "").split()
    puan = sum(1 for s in sozcukler if s in olumlu) - sum(1 for s in sozcukler if s in olumsuz)
    return "olumlu" if puan > 0 else "olumsuz"


yorumlar = [
    "Ürün çok güzel, beğendim",
    "Berbat bir ürün, beğenmedim",
    "Rengi güzel değil",
    "Kargo hızlı ama memnun değilim",
]
for yorum in yorumlar:
    print(f"{sozluk_ile_tahmin(yorum):8} ← {yorum}")
```
```text {.python-playground-expected}
olumlu   ← Ürün çok güzel, beğendim
olumsuz  ← Berbat bir ürün, beğenmedim
olumlu   ← Rengi güzel değil
olumlu   ← Kargo hızlı ama memnun değilim
```
```text {.python-playground-help}
`olumlu = {...}` ve `olumsuz = {...}` | Elle yazılmış sözcük kümeleri. Küme, bir sözcüğün içinde olup olmadığını hızlıca kontrol etmeye yarar.
`yorum.lower().replace(",", "").split()` | Basit temizlik: küçük harf, virgülü sil, sözcüklere böl.
`sum(1 for s in sozcukler if s in olumlu)` | Yorumdaki olumlu sözcükleri sayar.
`puan = ... - ...` | Olumlu sayısından olumsuz sayısını çıkarırız; pozitifse yorum olumlu sayılır.
`f"{...:8}"` | Sonucu 8 karakter genişliğinde yazar; oklar hizalı görünür.
```

İlk iki yorum doğru, son ikisi yanlış. "Rengi **güzel değil**" içinde `güzel` sözcüğü var ama anlam olumsuz. "Memnun **değilim**" de öyle. Ayrıca bu listeleri her konu için elle yazmak zordur: "pil çabuk bitiyor" olumsuzdur, ama `çabuk` kendi başına olumsuz bir sözcük değildir.

### 2.2 Özellikler: hangi sözcükler var?

Sözcüklerin olumlu mu olumsuz mu olduğunu bize söylemesi yerine, modelin **örneklerden öğrenmesini** istiyoruz. Önce her yorumu, içindeki sözcüklerin kümesine çeviririz (4.5'teki sözcük torbası; burada yalnızca var/yok bilgisine bakıyoruz).

Türkçede iki ayrıntı önemli:

- **4.5'teki "ilk 5 harf" yöntemi burada zararlı.** `beğendim` ve `beğenmedim` ikisi de `beğen` olur; olumsuzluk eki `-me` kaybolur. Arama için iyi olan bir adım, duygu analizi için anlamı tersine çeviren bir hataya dönüşür.
- **`değil` sözcüğü kendinden önceki sözcüğü olumsuzlar.** `güzel değil` ifadesini tek bir özellik yaparız: `güzel_değil`. Böylece model `güzel` ile `güzel_değil`'e ayrı ağırlıklar öğrenebilir.

```python {.python-playground}
import unicodedata


def normallestir(metin):
    metin = unicodedata.normalize("NFC", metin)
    metin = metin.replace("İ", "i").replace("I", "ı").lower()
    metin = "".join(h if h.isalnum() else " " for h in metin)
    return metin.split()


def ozellikler(metin):
    birlesik = []
    for sozcuk in normallestir(metin):
        if sozcuk.startswith("değil") and birlesik:
            birlesik[-1] = birlesik[-1] + "_değil"
        else:
            birlesik.append(sozcuk)
    return set(birlesik)


print("İlk 5 harf:", "beğendim"[:5], "beğenmedim"[:5])
print(sorted(ozellikler("Rengi güzel değil")))
print(sorted(ozellikler("Kargo hızlı ama memnun değilim")))
```
```text {.python-playground-expected}
İlk 5 harf: beğen beğen
['güzel_değil', 'rengi']
['ama', 'hızlı', 'kargo', 'memnun_değil']
```
```text {.python-playground-help}
`def normallestir(metin):` | 4.3 ve 4.5 derslerindeki Türkçe temizlik adımları. Bu kez sözcükleri kesmiyoruz.
`"beğendim"[:5], "beğenmedim"[:5]` | İki zıt anlamlı sözcüğün ilk 5 harfinin aynı olduğunu gösterir.
`if sozcuk.startswith("değil") and birlesik:` | `değil`, `değilim`, `değildi` gibi biçimleri yakalar. `birlesik` boş değilse (öncesinde bir sözcük varsa) birleştiririz.
`birlesik[-1] = birlesik[-1] + "_değil"` | Listenin son öğesi, yani önceki sözcük, `güzel` → `güzel_değil` olur. `değil` ayrıca eklenmez.
`return set(birlesik)` | Küme, tekrar eden sözcükleri bir kez tutar; yalnızca "var mı?" sorusuyla ilgileniyoruz.
`sorted(...)` | Küme sırasız olduğu için çıktıyı her seferinde aynı görmek amacıyla alfabetik sıralarız.
```

Bu küçük kural `-me` ekli fiilleri de korur: `beğenmedim`, `beğendim`'den ayrı bir sözcük olarak kalır ve model ona kendi ağırlığını verir.

### 2.3 Lojistik regresyonla öğrenmek

Şimdi 2.3 dersindeki lojistik regresyonu, her sözcüğe bir ağırlık verecek şekilde genişletiyoruz:

`ham puan = sabit + (yorumdaki her sözcüğün ağırlıklarının toplamı)`

Sigmoid bu puanı olumlu olma olasılığına çevirir. Eğitimde, çapraz entropinin türevi olan `olasılık - etiket` farkıyla ağırlıkları güncelleriz. Bir sözcük çoğunlukla olumlu yorumlarda geçiyorsa ağırlığı pozitif, olumsuz yorumlarda geçiyorsa negatif olur.

```python {.python-playground}
import math
import unicodedata

egitim = [
    ("Ürün çok güzel, çok beğendim", 1), ("Kargo hızlı geldi, teşekkürler", 1),
    ("Kalitesi harika, herkese tavsiye ederim", 1), ("Fiyatına göre gayet iyi", 1),
    ("Film çok güzeldi, bayıldım", 1), ("Oyunculuk harika, tekrar izlerim", 1),
    ("Kumaşı yumuşak ve kaliteli, memnun kaldım", 1), ("Beklediğimden iyi çıktı, beğendim", 1),
    ("Ürün kötü, hiç beğenmedim", 0), ("Kargo çok geç geldi, memnun değilim", 0),
    ("Kalitesi berbat, tavsiye etmem", 0), ("Fiyatına göre çok pahalı ve kötü", 0),
    ("Film çok sıkıcıydı, beğenmedim", 0), ("Oyunculuk kötü, bir daha izlemem", 0),
    ("Kumaşı ince, iki yıkamada yırtıldı", 0), ("Hiç güzel değil, para çöpe gitti", 0),
]
test = [
    ("Telefon çok güzel, beğendim", 1), ("Hızlı kargo için teşekkürler", 1),
    ("Harika bir film, tavsiye ederim", 1), ("Kaliteli ve iyi bir ürün", 1),
    ("Berbat bir ürün, beğenmedim", 0), ("Çok sıkıcı bir dizi", 0),
    ("Kargo geç geldi, kötü", 0), ("Rengi güzel değil", 0),
]


def ozellikler(metin):
    metin = unicodedata.normalize("NFC", metin).replace("İ", "i").replace("I", "ı").lower()
    sozcukler = "".join(h if h.isalnum() else " " for h in metin).split()
    birlesik = []
    for sozcuk in sozcukler:
        if sozcuk.startswith("değil") and birlesik:
            birlesik[-1] += "_değil"
        else:
            birlesik.append(sozcuk)
    return set(birlesik)


agirliklar = {}
sabit = 0.0


def olasilik(metin):
    z = sabit + sum(agirliklar.get(s, 0.0) for s in ozellikler(metin))
    return 1 / (1 + math.exp(-z))


for tur in range(300):
    gradyanlar = {}
    sabit_gradyani = 0.0
    for metin, etiket in egitim:
        hata = olasilik(metin) - etiket
        for s in ozellikler(metin):
            gradyanlar[s] = gradyanlar.get(s, 0.0) + hata
        sabit_gradyani += hata
    for s, g in gradyanlar.items():
        agirliklar[s] = agirliklar.get(s, 0.0) - 0.5 * g / len(egitim)
    sabit -= 0.5 * sabit_gradyani / len(egitim)

dogru = sum(int(olasilik(m) >= 0.5) == e for m, e in test)
print(f"Test doğruluğu: {dogru}/{len(test)}")
print(f"'Rengi güzel değil' olumlu olasılığı: {olasilik('Rengi güzel değil'):.2f}")
sirali = sorted(agirliklar.items(), key=lambda cift: (round(cift[1], 6), cift[0]))
print("En olumsuz:", [s for s, _ in sirali[:3]])
print("En olumlu:", [s for s, _ in sirali[-3:]])
```
```text {.python-playground-expected}
Test doğruluğu: 8/8
'Rengi güzel değil' olumlu olasılığı: 0.42
En olumsuz: ['kötü', 'beğenmedim', 'berbat']
En olumlu: ['iyi', 'beğendim', 'harika']
```
```text {.python-playground-help}
`egitim` ve `test` | 2.4 dersindeki gibi ayrı tutulmuş iki küme. Model test yorumlarını eğitimde hiç görmez.
`def ozellikler(metin):` | 2.2'deki temizlik ve `değil` birleştirmesi, kısaltılmış biçimde.
`agirliklar = {}` | Her sözcüğün ağırlığını tutan sözlük. Henüz görülmemiş bir sözcüğün ağırlığı `0` kabul edilir.
`agirliklar.get(s, 0.0)` | Sözcük sözlükte yoksa `0` döndürür; test yorumlarındaki yeni sözcükler (`telefon`, `dizi`) böylece hata vermez.
`hata = olasilik(metin) - etiket` | 2.3 dersindeki gradyan: tahmin olasılığı ile gerçek etiket arasındaki fark.
`gradyanlar[s] = gradyanlar.get(s, 0.0) + hata` | Yorumdaki her sözcük bu hatadan pay alır. Bir sözcüğün girdisi `1` olduğu için türev doğrudan `hata`dır.
`agirliklar[s] = ... - 0.5 * g / len(egitim)` | Öğrenme hızı `0.5` ile ortalama gradyanın tersi yönünde güncelleriz.
`int(olasilik(m) >= 0.5) == e` | Tahmini sınıfa çevirip gerçek etiketle karşılaştırırız; `True` toplamda `1` sayılır.
`sorted(agirliklar.items(), key=lambda cift: (round(cift[1], 6), cift[0]))` | Sözcükleri ağırlıklarına göre küçükten büyüğe sıralarız. `berbat` ile `etmem` aynı tek yorumda geçtiği için ağırlıkları eşittir; eşitlikte alfabetik sıraya bakarız ki sonuç her çalıştırmada aynı olsun.
```

Model 8 test yorumunun hepsini doğru sınıflandırdı. Öğrendiği ağırlıklar da mantıklı: `kötü`, `beğenmedim`, `berbat` en olumsuz; `harika`, `beğendim`, `iyi` en olumlu. Bu listeleri biz yazmadık; model örneklerden çıkardı.

`"Rengi güzel değil"` için olasılık `0.42`, yani olumsuz tarafta ama sınırın çok yakınında. Eğitim verisinde `güzel_değil` yalnızca bir kez geçiyor; model bu konuda çok emin olamıyor. Daha çok veri bu tür ince durumları düzeltir.

### 2.4 Ders kodu

[`kod/duygu_analizi.py`](kod/duygu_analizi.py) dosyası aynı modeli bir sınıf olarak içerir ve `değil` birleştirmesini açıp kapatarak iki sonucu karşılaştırır. Birleştirme kapalıyken `"Rengi güzel değil"` yanlışlıkla olumlu sınıflandırılır ve test doğruluğu `0.88`'e düşer.

```bash
cd docs/faz-04-metin-ve-turkce-nlp/06-duygu-analizi
python kod/duygu_analizi.py
python -m unittest discover -s test -v
```

### Şimdi sen yaz: olumsuzluğu birleştir

`güzel değil` ifadesini tek bir özelliğe çeviren fonksiyonu tamamla. Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur, sonra çalıştır.

```python {.python-playground-task}
def ozellikler(metin):
    sozcukler = metin.lower().replace(",", "").split()
    birlesik = []
    for sozcuk in sozcukler:
        # TODO: Sözcük "değil" ise ve öncesinde bir sözcük varsa öncekine "_değil" ekle.
        if sozcuk == "değil" and ___:
            birlesik[-1] = birlesik[-1] + ___
        else:
            birlesik.append(sozcuk)
    return birlesik


print(ozellikler("Rengi güzel değil"))
print(ozellikler("Çok güzel, beğendim"))
```
```text {.python-playground-expected}
['rengi', 'güzel_değil']
['çok', 'güzel', 'beğendim']
```
```text {.python-playground-help}
`if sozcuk == "değil" and ___:` | Boş bir liste `False` sayılır. `birlesik` doluysa önceki sözcük var demektir.
`birlesik[-1] + ___` | `birlesik[-1]` son sözcüktür. Sonuna `"_değil"` metnini ekle.
```
```python {.python-playground-solution}
def ozellikler(metin):
    sozcukler = metin.lower().replace(",", "").split()
    birlesik = []
    for sozcuk in sozcukler:
        # Sözcük "değil" ise ve öncesinde bir sözcük varsa öncekine "_değil" ekle.
        if sozcuk == "değil" and birlesik:
            birlesik[-1] = birlesik[-1] + "_değil"
        else:
            birlesik.append(sozcuk)
    return birlesik


print(ozellikler("Rengi güzel değil"))
print(ozellikler("Çok güzel, beğendim"))
```

## 3. Kütüphaneyle yap

Scikit-learn'de `CountVectorizer` metinleri özellik vektörlerine, `LogisticRegression` de sınıflandırıcıya karşılık gelir. Kendi `ozellikler` fonksiyonumuzu kullanmak için kodu ders klasöründe `duygu_sklearn.py` adıyla kaydet ve `python duygu_sklearn.py` ile çalıştır:

```python
import sys

sys.path.insert(0, "kod")
from duygu_analizi import EGITIM, TEST, ozellikler

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

vektorlestirici = CountVectorizer(
    tokenizer=lambda metin: sorted(ozellikler(metin)),
    lowercase=False,
    token_pattern=None,
    binary=True,
)
X_egitim = vektorlestirici.fit_transform([m for m, _ in EGITIM])
X_test = vektorlestirici.transform([m for m, _ in TEST])

model = LogisticRegression()
model.fit(X_egitim, [e for _, e in EGITIM])
tahminler = model.predict(X_test)

print(classification_report([e for _, e in TEST], tahminler, target_names=["olumsuz", "olumlu"]))
print(model.predict(vektorlestirici.transform(["Ürün güzel değil", "Ürün çok güzel"])))
```

Beklenen çıktı:

```text
              precision    recall  f1-score   support

     olumsuz       1.00      1.00      1.00         4
      olumlu       1.00      1.00      1.00         4

    accuracy                           1.00         8
   macro avg       1.00      1.00      1.00         8
weighted avg       1.00      1.00      1.00         8

[1 1]
```

- `binary=True`: Sözcüğün kaç kez geçtiğine değil, geçip geçmediğine bakar; bizim kümemizle aynı.
- `classification_report`: 2.6 dersindeki kesinlik (precision), duyarlılık (recall) ve F1 değerlerini her sınıf için tek tabloda verir.
- Son satır iki yeni cümleyi sınıflandırır.

Son satıra dikkat: Model `"Ürün güzel değil"` cümlesini de **olumlu** (`1`) buldu. Test setinde kusursuz görünen model, 16 örnekten öğrenebileceğinden fazlasını bilmiyor. scikit-learn'ün lojistik regresyonu ağırlıkları aşırı büyümesin diye küçültür (düzenlileştirme); tek bir örnekte geçen `güzel_değil` özelliği bu yüzden zayıf kalıyor, `ürün` ve diğer sözcükler kararı belirliyor. 8 örneklik bir test setinde %100 başarı, 2.4 dersinde söylediğimiz gibi, güvenilir bir kanıt değildir.

!!! note "Gerçek uygulamalarda"
    Bu dersteki yöntem, sözcük sırasını ve bağlamı büyük ölçüde görmez. "Hiç beklemediğim kadar iyi" gibi cümleleri doğru anlamak için sırayı ve bağlamı işleyen modeller gerekir. Bugün Türkçe duygu analizi genellikle önceden eğitilmiş bir dil modeline (Faz 5-6'da yapısını öğreneceğin transformer'lar) etiketli örneklerle ince ayar yapılarak (Faz 10) yapılır. Ama sözcük torbası + lojistik regresyon hâlâ hızlı, anlaşılır ve güçlü bir başlangıç noktasıdır.

## 4. Sık yapılan hatalar

- **Her görevde aynı ön işlemeyi kullanmak.** İlk 5 harfi almak aramada işe yarar, ama `beğendim`/`beğenmedim` ayrımını sildiği için duygu analizini bozar. Ön işlemeyi göreve göre seç.
- **Olumsuzluğu görmezden gelmek.** Türkçede olumsuzluk `-me` ekiyle sözcüğün içinde veya `değil` ile ayrı bir sözcük olarak gelir. İkisi de ele alınmalıdır.
- **Durak sözcüklerini düşünmeden silmek.** `değil` ve `hiç` bazı listelerde "anlamsız sözcük" sayılır; duygu analizinde ise en önemli sözcükler arasındadır.
- **Küçük test setindeki başarıya güvenmek.** 8 örnekte %100, yeni yorumlarda da %100 demek değildir.
- **Sınıf dengesini kontrol etmemek.** Yorumların %90'ı olumluysa, her şeye "olumlu" diyen model %90 doğruluk alır (2.6 dersi). Kesinlik ve duyarlılığa da bak.
- **İroni ve bağlamı beklemek.** "Harika, ikinci günde bozuldu" gibi alaycı cümleleri sözcük torbası modelleri genellikle yanlış anlar.

## 5. Pekiştir

**Quiz**

1. Sözlük tabanlı yaklaşımın iki zayıflığı nedir?
2. 4.5'teki ilk 5 harf yöntemi duygu analizinde neden zararlı?
3. `güzel değil` ifadesini neden `güzel_değil` diye tek bir özelliğe çeviriyoruz?
4. Lojistik regresyon modelinde bir sözcüğün ağırlığı pozitif çıkarsa bu ne anlama gelir?
5. scikit-learn modeli test setinde %100 başarılı olduğu hâlde `"Ürün güzel değil"` cümlesini neden yanlış sınıflandırdı?

**Alıştırmalar**

1. 2.1'deki listelere `değilim` ekleyip olumsuz say. Hangi yorumlar düzeldi, hangileri hâlâ yanlış?
2. 2.2'deki `ozellikler` fonksiyonuna `"Hiç beğenmedim, hiç güzel değil"` ver. Çıktıyı açıkla.
3. 2.3'te `değil` birleştirmesini kapat (`birlesik[-1] += "_değil"` yerine `değil`'i de normal sözcük gibi ekle). Test doğruluğu ve `"Rengi güzel değil"` olasılığı nasıl değişti?
4. 2.3'teki eğitim verisine üç olumlu, üç olumsuz yorum ekle; bunlardan biri `"Ürün güzel değil"` gibi olsun. Model şimdi bu cümleyi doğru sınıflandırıyor mu?
5. (İsteğe bağlı) `kod/duygu_analizi.py` dosyasına 2.6 dersindeki kesinlik ve duyarlılık hesabını ekle.

??? success "Quiz cevapları"
    1. Olumsuzluk gibi bağlamı görmez ("güzel değil"), ve her alan için elle uzun listeler yazmak gerekir; bir sözcüğün duygusu konuya göre değişebilir.
    2. Olumsuzluk eki `-me` sözcüğün ortasındadır; ilk 5 harf `beğendim` ile `beğenmedim`'i aynı terime çevirir ve anlam farkı kaybolur.
    3. Böylece model `güzel` ve `güzel_değil` için ayrı ağırlıklar öğrenir; olumsuzlanmış bir sözcük artık olumlu puan kazandırmaz.
    4. O sözcük daha çok olumlu yorumlarda geçmiştir; yorumda bulunması olumlu olma olasılığını artırır.
    5. Eğitim verisi çok küçük. `güzel_değil` yalnızca bir kez geçtiği ve scikit-learn ağırlıkları küçülttüğü için bu özelliğin etkisi zayıf kaldı. Test seti de çok küçük olduğundan bu zayıflığı ortaya çıkaramadı.

## Özet

Duygu analizi, metinler için iki sınıflı bir sınıflandırma problemidir. Elle yazılmış sözcük listeleri olumsuzluk ve bağlam karşısında yetersiz kalır. Metni sözcük kümesine çevirip lojistik regresyonla eğitmek, her sözcüğün olumlu ya da olumsuz etkisini örneklerden öğrenmemizi sağlar. Türkçede olumsuzluk hem `-me` ekiyle hem `değil` sözcüğüyle gelir; ön işleme bunları korumalıdır. Aynı ön işleme adımı bir görevde yararlıyken başka bir görevde anlamı bozabilir. Küçük veriyle elde edilen yüksek test başarısı güvenilir bir kanıt değildir.

## Kaynaklar

- Bo Pang ve Lillian Lee (2008), *Opinion Mining and Sentiment Analysis*, Foundations and Trends in Information Retrieval
- Dan Jurafsky ve James H. Martin, *Speech and Language Processing* (3. baskı taslağı), 4. bölüm ("Naive Bayes, Text Classification, and Sentiment") ve 5. bölüm ("Logistic Regression"): [web.stanford.edu/~jurafsky/slp3](https://web.stanford.edu/~jurafsky/slp3/)
- [scikit-learn resmî belgesi: Metinden özellik çıkarma](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
