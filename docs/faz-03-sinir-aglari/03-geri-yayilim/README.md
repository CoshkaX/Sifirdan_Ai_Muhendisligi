# Faz 3 – Ders 3: Geri yayılım

> ⏱️ Tahmini süre: 55-70 dk · 📚 Ön koşul: 1.3 Türev ve gradyan, 3.1 Tek nöron, 3.2 Mini autograd · 💻 Gereksinim: Python 3.11+, ek paket yok; PyTorch örneği isteğe bağlı

## Bu derste ne öğreneceksin?

- Bir nöronun **ileri geçişini** ve **geri geçişini** adım adım hesaplamayı
- Kaybın her ağırlığa göre türevini zincir kuralıyla bulmayı
- Bulduğun türevleri **gradyan kontrolüyle** doğrulamayı
- Geri yayılım ve gradyan inişini birleştirerek bir nöronu eğitmeyi
- Sigmoid kullanan derin ağlarda türevlerin neden küçülebildiğini

## 1. Problem

3.1 dersinde perceptron kuralıyla bir nöron eğittik; ama bu kural yalnızca basamak aktivasyonlu tek nöron için işe yarar. 3.2 dersinde ise türevleri otomatik hesaplayan bir motor yazdık. Şimdi ikisini birleştiriyoruz.

**Geri yayılım** (backpropagation), kaybın ağdaki her ağırlığa göre türevini zincir kuralıyla, sondan başa doğru hesaplama yöntemidir. Bir eğitim adımı iki geçişten oluşur:

1. **İleri geçiş:** Girdiden başlayıp tahmini ve kaybı hesaplarız. Ara sonuçları saklarız.
2. **Geri geçiş:** Kayıptan başlayıp her adımın yerel türevini gelen türevle çarparak ağırlıkların türevlerine ulaşırız.

Sonra 1.3 dersindeki gradyan inişiyle ağırlıkları türevin ters yönünde güncelleriz. Bu derste her şeyi tek bir nöron üzerinde, sayıları görebileceğin kadar küçük tutarak yapacağız.

## 2. Kendin yaz

### 2.1 Tek nöronda ileri ve geri geçiş

Nöronumuzun iki girdisi var. Sigmoid aktivasyonu kullanıyor ve kayıp olarak kare hata alıyoruz:

```text
z     = w1 × x1 + w2 × x2 + b
p     = sigmoid(z)
kayıp = (p - y)²
```

Değerler: `x = [1.0, 2.0]`, `w = [0.5, -0.3]`, `b = 0.1`, hedef `y = 1`. Geri geçişte üç yerel türev kullanacağız:

- `kayıp = (p - y)²` için `p`'ye göre türev: `2 × (p - y)`
- `p = sigmoid(z)` için `z`'ye göre türev: `p × (1 - p)`
- `z = w1 × x1 + ...` için `w1`'e göre türev `x1`, `w2`'ye göre `x2`, `b`'ye göre `1`

```python {.python-playground}
import math

x1, x2 = 1.0, 2.0
w1, w2, b = 0.5, -0.3, 0.1
y = 1

# İleri geçiş
z = w1 * x1 + w2 * x2 + b
p = 1 / (1 + math.exp(-z))
kayip = (p - y) ** 2
print("z =", round(z, 4), " p =", round(p, 4), " kayıp =", round(kayip, 4))

# Geri geçiş
d_p = 2 * (p - y)
d_z = d_p * p * (1 - p)
d_w1 = d_z * x1
d_w2 = d_z * x2
d_b = d_z * 1
print("d_p =", d_p, " d_z =", d_z)
print("d_w1 =", d_w1, " d_w2 =", d_w2, " d_b =", d_b)
```
```text {.python-playground-expected}
z = 0.0  p = 0.5  kayıp = 0.25
d_p = -1.0  d_z = -0.25
d_w1 = -0.25  d_w2 = -0.5  d_b = -0.25
```
```text {.python-playground-help}
`z = w1 * x1 + w2 * x2 + b` | Ağırlıklı toplam: `0.5 × 1 + (-0.3) × 2 + 0.1 = 0`.
`p = 1 / (1 + math.exp(-z))` | Sigmoid; `z = 0` iken tam `0.5` verir.
`kayip = (p - y) ** 2` | Tahmin `0.5`, hedef `1`; farkın karesi `0.25`.
`d_p = 2 * (p - y)` | Kaybın `p`'ye göre türevi. Negatif çıkması, `p` artarsa kaybın azalacağını söyler.
`d_z = d_p * p * (1 - p)` | Zincir kuralı: gelen türev (`d_p`) × sigmoidin yerel türevi (`p × (1 - p)`).
`d_w1 = d_z * x1` | `z`'nin `w1`'e göre yerel türevi `x1`'dir. Gelen türevle çarparız.
`d_w2 = d_z * x2` | `x2 = 2` olduğu için `w2`'nin türevi iki kat büyüktür: bu girdi daha büyük olduğundan ağırlığı sonucu daha çok etkiler.
`d_b = d_z * 1` | Sabitin yerel türevi `1`'dir.
```

Bütün türevler negatif. Gradyan inişinde türevin **tersi** yönünde gittiğimiz için üç parametre de artacak; bu, `z`'yi ve dolayısıyla `p`'yi büyütür. Hedef `1` olduğuna göre doğru yön budur.

### 2.2 Gradyan kontrolü: türevler doğru mu?

Geri geçişi elle yazarken bir işaret veya çarpanı unutmak kolaydır. Hata yaptığımızı anlamanın güvenilir yolu, aynı türevi 1.3 dersindeki **sonlu fark** yöntemiyle de hesaplayıp karşılaştırmaktır. Buna **gradyan kontrolü** denir.

Burada parametreyi hem biraz artırıp hem biraz azaltıyoruz; bu **merkezi fark** tek yönlü farktan daha doğru sonuç verir:

`türev ≈ (kayıp(w + h) - kayıp(w - h)) / (2 × h)`

```python {.python-playground}
import math


def kayip_hesapla(w1, w2, b):
    x1, x2, y = 1.0, 2.0, 1
    z = w1 * x1 + w2 * x2 + b
    p = 1 / (1 + math.exp(-z))
    return (p - y) ** 2


w1, w2, b = 0.5, -0.3, 0.1
h = 0.0001

sayisal_w1 = (kayip_hesapla(w1 + h, w2, b) - kayip_hesapla(w1 - h, w2, b)) / (2 * h)
sayisal_w2 = (kayip_hesapla(w1, w2 + h, b) - kayip_hesapla(w1, w2 - h, b)) / (2 * h)
sayisal_b = (kayip_hesapla(w1, w2, b + h) - kayip_hesapla(w1, w2, b - h)) / (2 * h)

print("Geri yayılım : -0.25  -0.5  -0.25")
print("Sonlu fark   :", round(sayisal_w1, 4), "", round(sayisal_w2, 4), "", round(sayisal_b, 4))
```
```text {.python-playground-expected}
Geri yayılım : -0.25  -0.5  -0.25
Sonlu fark   : -0.25  -0.5  -0.25
```
```text {.python-playground-help}
`def kayip_hesapla(w1, w2, b):` | İleri geçişi bir fonksiyona koyarız; böylece farklı parametrelerle tekrar tekrar çağırabiliriz.
`h = 0.0001` | Parametreyi ne kadar oynatacağımız. Çok büyükse yaklaşım kabalaşır, çok küçükse bilgisayarın yuvarlama hataları büyür.
`kayip_hesapla(w1 + h, w2, b) - kayip_hesapla(w1 - h, w2, b)` | Yalnızca `w1`'i biraz artırıp biraz azaltırız; diğer parametreler sabit kalır.
`/ (2 * h)` | İki nokta arasındaki uzaklık `2h` olduğu için farkı buna böleriz.
`round(..., 4)` | Sonlu fark yaklaşık bir hesaptır; dört basamağa yuvarlayınca geri yayılımla aynı çıkar.
```

İki yöntem aynı sonucu veriyor; geri geçişimiz doğru. Peki neden her zaman sonlu fark kullanmıyoruz? Çünkü sonlu fark her parametre için kaybı iki kez yeniden hesaplar. Milyonlarca ağırlığı olan bir ağda bu çok yavaştır. Geri yayılım ise **tek bir geri geçişte** bütün türevleri birden bulur. Sonlu farkı yalnızca kontrol amaçlı, küçük örneklerde kullanırız.

### 2.3 Geri yayılım + gradyan inişi = öğrenme

Şimdi ileri geçiş, geri geçiş ve güncellemeyi bir döngüye koyalım. Nörona VEYA kapısını öğretiyoruz; bu kez basamak yerine sigmoid kullandığımız için perceptron kuralına değil, türevlere dayanıyoruz. Her turda dört örneğin türevlerini toplayıp ortalamasını alır, sonra ağırlıkları güncelleriz.

```python {.python-playground}
import math

veri = [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 1)]
w1, w2, b = 0.0, 0.0, 0.0
ogrenme_hizi = 2.0

for tur in range(301):
    toplam_kayip = 0
    g_w1 = g_w2 = g_b = 0
    for (x1, x2), y in veri:
        z = w1 * x1 + w2 * x2 + b
        p = 1 / (1 + math.exp(-z))
        toplam_kayip += (p - y) ** 2
        d_z = 2 * (p - y) * p * (1 - p)
        g_w1 += d_z * x1
        g_w2 += d_z * x2
        g_b += d_z
    w1 -= ogrenme_hizi * g_w1 / len(veri)
    w2 -= ogrenme_hizi * g_w2 / len(veri)
    b -= ogrenme_hizi * g_b / len(veri)
    if tur % 100 == 0:
        print(f"Tur {tur}: ortalama kayıp {toplam_kayip / len(veri):.4f}")

for (x1, x2), y in veri:
    p = 1 / (1 + math.exp(-(w1 * x1 + w2 * x2 + b)))
    print(f"{x1} VEYA {x2}: hedef {y}, tahmin {p:.2f}")
```
```text {.python-playground-expected}
Tur 0: ortalama kayıp 0.2500
Tur 100: ortalama kayıp 0.0181
Tur 200: ortalama kayıp 0.0082
Tur 300: ortalama kayıp 0.0052
0 VEYA 0: hedef 0, tahmin 0.11
0 VEYA 1: hedef 1, tahmin 0.93
1 VEYA 0: hedef 1, tahmin 0.93
1 VEYA 1: hedef 1, tahmin 1.00
```
```text {.python-playground-help}
`w1, w2, b = 0.0, 0.0, 0.0` | Nöron sıfır ağırlıklarla başlar; ilk tahminlerin hepsi `0.5` olur.
`ogrenme_hizi = 2.0` | Sigmoidin türevi küçük olduğu için (en fazla `0.25`) bu örnekte görece büyük bir adım seçtik.
`g_w1 = g_w2 = g_b = 0` | Bu turda dört örnekten gelen türevleri biriktireceğimiz değişkenler.
`for (x1, x2), y in veri:` | Her örneği ve hedefini açarız. İç parantez, girdi listesini doğrudan iki değişkene ayırır.
`d_z = 2 * (p - y) * p * (1 - p)` | 2.1'deki geri geçiş: kaybın türevi × sigmoidin türevi.
`g_w1 += d_z * x1` | Bu örneğin `w1` türevini toplama ekleriz.
`w1 -= ogrenme_hizi * g_w1 / len(veri)` | Dört örneğin ortalama türevinin ters yönünde adım atarız.
`if tur % 100 == 0:` | `%` bölümden kalanı verir; her 100 turda bir kaybı yazdırırız.
`f"{... :.4f}"` | Sayıyı virgülden sonra dört basamakla gösterir.
```

Kayıp her yüz turda küçülüyor ve tahminler hedeflere yaklaşıyor. Tahminler hiçbir zaman tam `0` veya `1` olmaz, çünkü sigmoid bu değerlere yalnızca yaklaşır. İstersen 3.1 dersindeki gibi `0.5` eşiğiyle sınıfa çevirebilirsin.

!!! note "Kaybolan gradyan"
    Sigmoidin türevi `p × (1 - p)` en fazla `0.25` olur. Çok katmanlı bir ağda geri geçiş her sigmoid katmanında bu sayıyla çarpılır; on katmandan sonra türev `0.25¹⁰ ≈ 0.000001` kadar küçülebilir. İlk katmanlar neredeyse hiç öğrenemez. Buna **kaybolan gradyan** (vanishing gradient) denir. Modern ağların gizli katmanlarda genellikle ReLU kullanmasının bir nedeni budur: ReLU'nun türevi pozitif bölgede `1`'dir.

### Şimdi sen yaz: bir nöronu eğit

**Görev:** Tek bir nöron üç adım eğitiliyor. Her adımda geri geçişin türevlerini sen yazacaksın. Ekranda her adımın tahmini ve kaybı görünür; kayıp adım adım küçülmeli.

Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur ve çalıştır. Çıktın aşağıdaki **Hedef çıktı** ile aynıysa başardın.

```python {.python-playground-task}
import math

x, y = 2.0, 1
w, b = 0.0, 0.0
ogrenme_hizi = 1.0

for adim in range(3):
    z = w * x + b
    p = 1 / (1 + math.exp(-z))
    # TODO: Kayıp (p - y)² için d_p = 2 × (p - y).
    d_p = ___
    # TODO: Sigmoidin türevi p × (1 - p). Gelen d_p ile çarp.
    d_z = d_p * ___
    # TODO: w'nin türevi d_z × x, b'nin türevi d_z.
    w -= ogrenme_hizi * ___
    b -= ogrenme_hizi * ___
    print(f"Adım {adim + 1}: tahmin {p:.3f}, kayıp {(p - y) ** 2:.3f}")
```
```text {.python-playground-expected}
Adım 1: tahmin 0.500, kayıp 0.250
Adım 2: tahmin 0.777, kayıp 0.050
Adım 3: tahmin 0.837, kayıp 0.027
```
```text {.python-playground-help}
`d_p = ___` | Kaybın `p`'ye göre türevi `2 × (p - y)`.
`d_z = d_p * ___` | Sigmoidin yerel türevi `p * (1 - p)`.
`w -= ogrenme_hizi * ___` | `z = w × x + b` olduğundan `w`'nin türevi `d_z * x`.
`b -= ogrenme_hizi * ___` | Sabitin yerel türevi `1`'dir; yani `b`'nin türevi `d_z`.
```
```python {.python-playground-solution}
import math

x, y = 2.0, 1
w, b = 0.0, 0.0
ogrenme_hizi = 1.0

for adim in range(3):
    z = w * x + b
    p = 1 / (1 + math.exp(-z))
    # Kayıp (p - y)² için d_p = 2 × (p - y).
    d_p = 2 * (p - y)
    # Sigmoidin türevi p × (1 - p). Gelen d_p ile çarp.
    d_z = d_p * p * (1 - p)
    # w'nin türevi d_z × x, b'nin türevi d_z.
    w -= ogrenme_hizi * d_z * x
    b -= ogrenme_hizi * d_z
    print(f"Adım {adim + 1}: tahmin {p:.3f}, kayıp {(p - y) ** 2:.3f}")
```

## 3. Kütüphaneyle yap

PyTorch, 2.1'deki geri geçişi kendisi yapar. Aynı nöronu yazıp türevlerin bizimkilerle aynı olduğunu görebilirsin:

```python
import torch

x = torch.tensor([1.0, 2.0])
w = torch.tensor([0.5, -0.3], requires_grad=True)
b = torch.tensor(0.1, requires_grad=True)
y = torch.tensor(1.0)

p = torch.sigmoid(w @ x + b)
kayip = (p - y) ** 2
kayip.backward()

print("w türevleri:", [round(t, 4) for t in w.grad.tolist()])
print("b türevi:", round(b.grad.item(), 4))
```

Beklenen çıktı:

```text
w türevleri: [-0.25, -0.5]
b türevi: -0.25
```

`w @ x` iki girdinin ağırlıklı toplamını tek işlemde bulur. `kayip.backward()` geri geçişi yapar ve türevleri `w.grad` ile `b.grad` içine yazar. Bu kodu 3.2 dersindeki gibi bilgisayarında, PyTorch kurulu bir ortamda çalıştır.

## 4. Sık yapılan hatalar

- **İleri geçişteki ara sonuçları saklamamak.** Geri geçişte `p`, `z` gibi ara değerlere ihtiyaç vardır; her biri ileri geçişte hesaplanıp tutulmalıdır.
- **Zincirde bir halkayı atlamak.** `d_w1 = 2 × (p - y) × x1` yazıp sigmoidin türevini unutmak sık yapılan bir hatadır. Gradyan kontrolü bu tür hataları yakalar.
- **Gradyan kontrolünde çok büyük veya çok küçük `h` seçmek.** `0.1` kaba sonuç verir; `1e-12` ise yuvarlama hatası yüzünden saçma sonuç verebilir. `1e-4` ile `1e-6` arası genellikle iyidir.
- **Türevleri turlar arasında sıfırlamamak.** Her turda türev toplamları sıfırdan başlamalıdır; yoksa eski turların türevleri yeni güncellemeye karışır.
- **Kaybın hiç sıfır olmamasını hata sanmak.** Sigmoid çıktısı `0` veya `1`'e ancak yaklaşır; kayıp küçülmeye devam ediyorsa öğrenme sürüyor demektir.

## 5. Pekiştir

**Quiz**

1. İleri geçiş ve geri geçiş sırasında neler hesaplanır?
2. 2.1'deki örnekte `d_w2` neden `d_w1`'in iki katı?
3. Gradyan kontrolü nedir ve neden eğitimde değil, yalnızca doğrulamada kullanılır?
4. Türevler negatifse gradyan inişi parametreleri hangi yönde değiştirir?
5. Kaybolan gradyan sorunu neden sigmoid kullanan derin ağlarda ortaya çıkar?

**Alıştırmalar**

1. 2.1'deki hedefi `y = 0` yap. Türevlerin işareti nasıl değişti? Bunu açıkla.
2. 2.1'deki geri geçişte `d_z = d_p * p * (1 - p)` satırını bilerek `d_z = d_p` yap. Sonra 2.2'deki gradyan kontrolüyle hatayı yakala.
3. 2.3'te öğrenme hızını `0.5` yap. 300 turun sonunda kayıp ne olur? Neden daha yavaş öğrendi?
4. 2.3'teki veriyi VE kapısına göre değiştir (`[0, 0, 0, 1]`). Nöron bunu da öğreniyor mu?
5. (İsteğe bağlı) 2.3'teki veriyi XOR'a göre değiştir (`[0, 1, 1, 0]`) ve 1000 tur çalıştır. Tahminler neden `0.5` civarında takılıyor?

??? success "Quiz cevapları"
    1. İleri geçişte tahmin ve kayıp (ve aradaki değerler); geri geçişte kaybın her ara değere ve parametreye göre türevi.
    2. `z`'nin `w2`'ye göre yerel türevi `x2 = 2`, `w1`'e göre ise `x1 = 1`'dir. İkisi de aynı `d_z` ile çarpılır.
    3. Türevleri sonlu farkla da hesaplayıp geri yayılımla karşılaştırmaktır. Her parametre için kaybı iki kez hesapladığı için çok yavaştır.
    4. Türevin tersi yönünde, yani parametreleri artırarak.
    5. Geri geçiş her sigmoid katmanında en fazla `0.25` olan bir sayıyla çarpılır; çok katmandan sonra türev neredeyse sıfıra iner.

## Özet

Geri yayılım, ileri geçişte hesaplanan ara değerleri kullanarak kaybın her parametreye göre türevini zincir kuralıyla sondan başa doğru bulur. Elle yazılan geri geçişi gradyan kontrolüyle, yani sonlu fark sonucuyla karşılaştırarak doğrularız. Geri yayılım ile gradyan inişi birleşince bir nöron örneklerden öğrenebilir. Sigmoid gibi türevi küçük aktivasyonlar derin ağlarda kaybolan gradyan sorununa yol açabilir.

## Kaynaklar

- Rumelhart, Hinton ve Williams (1986), *Learning representations by back-propagating errors*, Nature
- [Stanford CS231n ders notları: Backpropagation, Intuitions](https://cs231n.github.io/optimization-2/)
- [PyTorch: Otomatik türev alma öğreticisi](https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)
