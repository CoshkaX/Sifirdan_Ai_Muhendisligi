# Faz 3 – Ders 4: Çok katmanlı ağ

> ⏱️ Tahmini süre: 60-75 dk · 📚 Ön koşul: 3.1 Tek nöron, 3.3 Geri yayılım · 💻 Gereksinim: Python 3.11+, ek paket yok

## Bu derste ne öğreneceksin?

- Nöronları katmanlar hâlinde dizerek bir sinir ağı kurmayı
- Gizli katmanın neden "yeni özellikler" ürettiğini
- XOR problemini önce elle seçilmiş ağırlıklarla, sonra eğitimle çözmeyi
- Geri yayılımın birden fazla katmanda nasıl ilerlediğini
- Ağırlıkları neden hepsi aynı değil de farklı sayılarla başlattığımızı

## 1. Problem

3.1 dersinde tek bir nöronun **XOR** problemini çözemediğini gördük. XOR'da iki girdi farklıysa sonuç `1`, aynıysa `0`'dır:

| a | b | a XOR b |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

Bu dört noktayı bir kâğıda çizersen `1` olanların çaprazda durduğunu görürsün. Tek bir düz çizgi onları `0` olanlardan ayıramaz.

Çözüm, nöronları **katmanlar** hâlinde dizmektir. İlk katmandaki nöronlar girdilerden yeni ara bilgiler üretir; sonraki katman bu ara bilgilere bakarak karar verir. Girdi ile çıktı arasındaki katmana **gizli katman** denir; çünkü onun ürettiği değerleri veride doğrudan görmeyiz. Bu yapıya **çok katmanlı ağ** (multi-layer perceptron, MLP) denir.

```text
girdi katmanı      gizli katman        çıktı katmanı
   a  ───┬──────▶  h1  ───┐
         ╳                ├──────▶  tahmin
   b  ───┴──────▶  h2  ───┘
```

## 2. Kendin yaz

### 2.1 XOR'u elle kur: gizli katman yeni özellik üretir

XOR'u başka bir yolla da tanımlayabiliriz: "girdilerden **en az biri** `1`, ama **ikisi birden** değil." Bu cümlede iki ara soru var:

- `h1`: en az biri `1` mi? Bu bir **VEYA** kapısı.
- `h2`: ikisi birden `1` mi? Bu bir **VE** kapısı.

Çıktı nöronu da "`h1` doğru, `h2` yanlış" olduğunda `1` vermeli. 3.1 dersindeki VE/VEYA ağırlıklarını kullanarak bunu üç nöronla kurabiliriz:

```python {.python-playground}
def noron(girdiler, agirliklar, sabit):
    z = sum(g * a for g, a in zip(girdiler, agirliklar)) + sabit
    return 1 if z >= 0 else 0


def xor_agi(a, b):
    h1 = noron([a, b], [1, 1], -0.5)     # VEYA
    h2 = noron([a, b], [1, 1], -1.5)     # VE
    return noron([h1, h2], [1, -1], -0.5)  # h1 doğru ve h2 yanlış mı?


for a in [0, 1]:
    for b in [0, 1]:
        print(f"{a} XOR {b} = {xor_agi(a, b)}")
```
```text {.python-playground-expected}
0 XOR 0 = 0
0 XOR 1 = 1
1 XOR 0 = 1
1 XOR 1 = 0
```
```text {.python-playground-help}
`def noron(girdiler, agirliklar, sabit):` | 3.1 dersindeki basamak aktivasyonlu nöron.
`sum(g * a for g, a in zip(girdiler, agirliklar))` | `zip` her girdiyi kendi ağırlığıyla eşler; `sum` çarpımları toplar. Döngüyle yazdığımız ağırlıklı toplamın kısa hâli.
`h1 = noron([a, b], [1, 1], -0.5)` | Gizli katmanın ilk nöronu: girdilerden biri bile `1` ise `1` verir (VEYA).
`h2 = noron([a, b], [1, 1], -1.5)` | Gizli katmanın ikinci nöronu: yalnızca ikisi de `1` ise `1` verir (VE).
`noron([h1, h2], [1, -1], -0.5)` | Çıktı nöronu artık `a` ve `b`'ye değil, gizli katmanın ürettiği `h1` ve `h2`'ye bakar. `h2`'nin ağırlığı negatif: "ikisi birden" durumunu cezalandırır.
`for a in [0, 1]: for b in [0, 1]:` | Dört girdi çiftini sırayla dener.
```

Önemli fikir şu: Çıktı nöronu XOR'u `a` ve `b` üzerinden ayıramıyordu; ama `h1` ve `h2` üzerinden ayırabiliyor. Gizli katman, problemi çözülebilir hâle getiren **yeni özellikler** üretti. Sinir ağlarının gücü buradan gelir.

### 2.2 Ağırlıkları eğitimle bulmak

Elle ağırlık seçmek bu küçük problemde mümkün, ama gerçek problemlerde neyin "ara özellik" olacağını bilemeyiz. Bunun yerine ağın ağırlıklarını küçük ve birbirinden farklı sayılarla başlatıp geri yayılımla eğitiriz. Ağımız şöyle:

- 2 girdi → **3 nöronlu gizli katman** (sigmoid) → 1 çıktı nöronu (sigmoid)
- Kayıp: ortalama kare hata

Geri geçiş, 3.3 dersindeki tek nöronun aynısı; yalnızca bir halka uzun. Çıktı nöronunun türevi `d_z2`'yi bulduktan sonra bunu gizli nöronlara geri taşırız: her gizli nöron, çıktıya bağlandığı ağırlık oranında sorumluluk alır (`d_z2 × W2[j]`), sonra kendi sigmoid türeviyle çarpılır.

```python {.python-playground}
import math


def sigmoid(z):
    return 1 / (1 + math.exp(-z))


veri = [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]
W1 = [[0.5, -0.4], [-0.3, 0.8], [0.9, 0.2]]   # her satır bir gizli nöron
b1 = [0.0, 0.0, 0.0]
W2 = [0.3, -0.5, 0.4]                          # gizli nöronlardan çıktıya
b2 = 0.0
ogrenme_hizi = 2.0


def ileri(x):
    h = [sigmoid(W1[j][0] * x[0] + W1[j][1] * x[1] + b1[j]) for j in range(3)]
    p = sigmoid(sum(W2[j] * h[j] for j in range(3)) + b2)
    return h, p


for tur in range(2001):
    g_W1 = [[0, 0], [0, 0], [0, 0]]
    g_b1 = [0, 0, 0]
    g_W2 = [0, 0, 0]
    g_b2 = 0
    kayip = 0
    for x, y in veri:
        h, p = ileri(x)
        kayip += (p - y) ** 2 / 4
        d_z2 = 2 * (p - y) * p * (1 - p)
        g_b2 += d_z2
        for j in range(3):
            g_W2[j] += d_z2 * h[j]
            d_z1 = d_z2 * W2[j] * h[j] * (1 - h[j])
            g_W1[j][0] += d_z1 * x[0]
            g_W1[j][1] += d_z1 * x[1]
            g_b1[j] += d_z1
    if tur % 500 == 0:
        print(f"Tur {tur}: kayıp {kayip:.4f}")
    for j in range(3):
        W1[j][0] -= ogrenme_hizi * g_W1[j][0] / 4
        W1[j][1] -= ogrenme_hizi * g_W1[j][1] / 4
        b1[j] -= ogrenme_hizi * g_b1[j] / 4
        W2[j] -= ogrenme_hizi * g_W2[j] / 4
    b2 -= ogrenme_hizi * g_b2 / 4

for x, y in veri:
    print(f"{x[0]} XOR {x[1]}: hedef {y}, tahmin {ileri(x)[1]:.2f}")
```
```text {.python-playground-expected}
Tur 0: kayıp 0.2511
Tur 500: kayıp 0.0215
Tur 1000: kayıp 0.0036
Tur 1500: kayıp 0.0018
Tur 2000: kayıp 0.0012
0 XOR 0: hedef 0, tahmin 0.01
0 XOR 1: hedef 1, tahmin 0.96
1 XOR 0: hedef 1, tahmin 0.96
1 XOR 1: hedef 0, tahmin 0.05
```
```text {.python-playground-help}
`W1 = [[0.5, -0.4], ...]` | Girdiden gizli katmana giden ağırlıklar. Üç satır, üç gizli nöron; her satırda iki girdinin ağırlığı var.
`W2 = [0.3, -0.5, 0.4]` | Gizli nöronlardan çıktı nöronuna giden üç ağırlık.
`def ileri(x):` | İleri geçiş: önce gizli katmanın üç çıktısı `h`, sonra bunlardan çıktı `p` hesaplanır.
`g_W1 = [[0, 0], ...]` | Her turda türev toplamlarını sıfırdan başlatırız.
`d_z2 = 2 * (p - y) * p * (1 - p)` | Çıktı nöronunun türevi; 3.3 dersindeki tek nöronla aynı.
`g_W2[j] += d_z2 * h[j]` | Çıktı nöronunun girdileri artık gizli çıktılar (`h`); yerel türev `h[j]`.
`d_z1 = d_z2 * W2[j] * h[j] * (1 - h[j])` | Türevi gizli katmana taşırız: çıktının türevi × bağlantı ağırlığı × gizli nöronun sigmoid türevi.
`g_W1[j][0] += d_z1 * x[0]` | Gizli nöronun girdileri gerçek girdilerdir; yerel türev `x[0]`.
`if tur % 500 == 0:` | Her 500 turda kaybı yazdırırız. Kayıp, güncellemeden önceki ağırlıklarla hesaplanır.
`W1[j][0] -= ogrenme_hizi * g_W1[j][0] / 4` | Dört örneğin ortalama türevinin tersi yönünde adım atarız.
`ileri(x)[1]` | `ileri` iki değer döndürür; `[1]` ile ikincisini, yani tahmini alırız.
```

Kayıp hızla düşüyor ve ağ XOR'u öğreniyor. Tek nörondan tek farkı, aradaki gizli katman.

### 2.3 Neden ağırlıkları farklı sayılarla başlatıyoruz?

Bütün gizli nöronların ağırlıklarını aynı sayıyla başlattığını düşün. O zaman her gizli nöron aynı girdiyi alıp aynı çıktıyı üretir ve geri geçişte aynı türevi alır. Güncellemeden sonra da birbirinin aynısı kalırlar. Üç nöron, tek bir nöron gibi davranır. Buna **simetri sorunu** denir.

Bu yüzden ağırlıklar genellikle küçük **rastgele** sayılarla başlatılır; her nöron farklı bir yerden başlar ve farklı bir özellik öğrenebilir. Bu derste sonuçlar her çalıştırmada aynı çıksın diye rastgele görünen ama sabit sayılar yazdık. Alıştırma 3'te simetri sorununu kendin göreceksin.

### 2.4 Ders kodu

Aynı ağın düzenli hâli [`kod/xor_agi.py`](kod/xor_agi.py) dosyasında, `IkiKatmanliAg` sınıfı olarak duruyor. Gizli nöron sayısını değiştirebilir, ağırlıkları rastgele başlatabilirsin. Testler, ağın XOR'u öğrendiğini ve geri yayılım türevlerinin sonlu farkla aynı olduğunu (gradyan kontrolü) denetler.

```bash
cd docs/faz-03-sinir-aglari/04-cok-katmanli-ag
python kod/xor_agi.py
python -m unittest discover -s test -v
```

## 3. Kütüphaneyle yap

Bu ağı PyTorch ile yazmak birkaç satır sürer; bunu 3.6 dersinde yapacağız. O derste aynı başlangıç ağırlıklarını kullanıp burada bulduğumuz sonuçların aynısını elde edeceğiz. Önce 3.5 dersinde ağırlık güncellemesini hızlandıran yöntemleri göreceğiz.

Burada şunu aklında tut: Kütüphaneler katmanları matris işlemi olarak yazar. Gizli katmanın üç nöronunu tek tek döngüyle hesaplamak yerine `h = sigmoid(X @ W1ᵀ + b1)` gibi tek bir satırla, bütün örnekler için birden hesaplarlar. 1.2 dersindeki matris çarpımı burada işe yarar.

## 4. Sık yapılan hatalar

- **Bütün ağırlıkları sıfır veya aynı sayıyla başlatmak.** Gizli nöronlar birbirinin kopyası olur ve ağ katmanlı olmanın avantajını kaybeder.
- **Gizli katmanda aktivasyonu unutmak.** Aktivasyonsuz iki katman, tek bir katmana denktir; XOR yine çözülemez.
- **Gizli katmanın türevinde bağlantı ağırlığını unutmak.** Gizli nöronun sorumluluğu, çıktıya bağlandığı ağırlıkla orantılıdır: `d_z2 × W2[j]`.
- **Ağırlıkları türevleri hesaplarken güncellemek.** Bütün türevler eski ağırlıklarla hesaplanmalı, güncelleme sonra yapılmalıdır. Döngü ortasında `W2[j]`'yi değiştirirsen sonraki hesaplar yanlış ağırlıkla yapılır.
- **Daha çok nöronun her zaman daha iyi olduğunu sanmak.** Daha büyük ağ daha karmaşık örüntü öğrenebilir, ama 2.4 dersindeki aşırı öğrenme riski de artar.

## 5. Pekiştir

**Quiz**

1. Gizli katman ne demektir ve neden "gizli" denir?
2. 2.1'deki elle kurulan ağda `h1` ve `h2` hangi soruları cevaplıyor?
3. Gizli nöronun türevi hesaplanırken neden `W2[j]` ile çarpılır?
4. Simetri sorunu nedir?
5. Aktivasyonu olmayan iki katmanlı bir ağ XOR'u neden öğrenemez?

**Alıştırmalar**

1. 2.1'deki ağı değiştirerek **XNOR** (girdiler aynıysa `1`) kapısı kur. İpucu: yalnızca çıktı nöronunu değiştirmen yeterli.
2. 2.2'de öğrenme hızını `0.5` yap. 2000 turun sonunda tahminler ne kadar iyi?
3. 2.2'de `W1` satırlarının hepsini `[0.5, 0.5]`, `W2`'yi `[0.5, 0.5, 0.5]` yap. Ağ XOR'u öğrenebiliyor mu? `1 XOR 1` tahminine bak ve nedenini açıkla.
4. (İsteğe bağlı) `kod/xor_agi.py` dosyasında `gizli_noron_sayisi=1` ile bir ağ eğit. Sonra `2` ve `5` dene. En az kaç gizli nöron gerekiyor?
5. (Zor) 2.2'deki ağda gizli katmanın aktivasyonunu ReLU yap. Türevde `h[j] * (1 - h[j])` yerine ne yazman gerekir?

??? success "Quiz cevapları"
    1. Girdi ile çıktı arasındaki katmandır. Ürettiği değerler veride bulunmaz; ağ onları kendisi oluşturur, dışarıdan görmeyiz.
    2. `h1`: "en az biri `1` mi?" (VEYA). `h2`: "ikisi birden `1` mi?" (VE).
    3. Gizli nöronun çıktısı, sonuca `W2[j]` ağırlığıyla katılır. Zincir kuralına göre yerel türev bu ağırlıktır; etkisi büyük olan nöron daha çok düzeltilir.
    4. Aynı başlatılan nöronlar aynı türevleri alır ve hep aynı kalır; birden çok nöron tek nöron gibi davranır.
    5. Aktivasyonsuz katmanlar yalnızca çarpıp toplar; art arda iki doğrusal işlem yine tek bir doğrusal işlemdir, yani yine düz bir çizgi çizer.

## Özet

Tek nöronun çözemediği XOR gibi problemler, nöronları katmanlar hâlinde dizerek çözülür. Gizli katman girdilerden yeni özellikler üretir; çıktı katmanı bu özelliklere bakarak karar verir. Ağırlıkları geri yayılımla öğrenirken türev çıktıdan gizli katmana, bağlantı ağırlıklarıyla çarpılarak taşınır. Ağırlıkları farklı sayılarla başlatmak, gizli nöronların farklı şeyler öğrenebilmesi için şarttır.

## Kaynaklar

- Rumelhart, Hinton ve Williams (1986), *Learning representations by back-propagating errors*, Nature
- Ian Goodfellow, Yoshua Bengio ve Aaron Courville (2016), *Deep Learning*, 6. bölüm (XOR örneği): [deeplearningbook.org](https://www.deeplearningbook.org/)
- [TensorFlow Playground](https://playground.tensorflow.org/): katman ve nöron sayısını tarayıcıda deneyerek görmek için
