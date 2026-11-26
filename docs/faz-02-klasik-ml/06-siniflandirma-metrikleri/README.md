# Faz 2 – Ders 6: Sınıflandırma metrikleri

> ⏱️ Tahmini süre: 55-70 dk · 📚 Ön koşul: 0.2 Python hızlı tekrar, 2.3 Lojistik regresyon, 2.4 Eğitim, doğrulama ve test, 2.5 Karar ağaçları · 💻 Gereksinim: Python 3.11+; temel örnekler ek paketsiz, scikit-learn örneği için scikit-learn kurulmalıdır

## Bu derste ne öğreneceksin?

- Gerçek etiketlerle model tahminlerini karşılaştırmayı
- Doğru pozitif, yanlış pozitif, yanlış negatif ve doğru negatif sayılarını bulmayı
- Doğruluk, kesinlik, duyarlılık ve F1 skorunu hesaplamayı
- Dengesiz veride doğruluğun tek başına neden yanıltıcı olabildiğini görmeyi
- Hangi metriğin önemli olduğuna hatanın maliyetine göre karar vermeyi

## 1. Problem

Bir e-posta sınıflandırıcısının istenmeyen postaları bulduğunu düşün. `1` istenmeyen posta, `0` normal e-posta olsun. Model bazı istenmeyen postaları kaçırabilir; normal e-postaları da yanlışlıkla istenmeyen posta klasörüne atabilir. “Model yüzde kaç doğru?” sorusu bu hataların hangisinin yaşandığını tek başına söylemez.

Önce tahminleri gerçek etiketlerle karşılaştırıp dört sayıyı buluruz:

- **Doğru pozitif (TP):** İstenmeyen postaydı ve model doğru biçimde `1` dedi.
- **Yanlış pozitif (FP):** Normal e-postaydı ama model yanlışlıkla `1` dedi.
- **Yanlış negatif (FN):** İstenmeyen postaydı ama model onu kaçırıp `0` dedi.
- **Doğru negatif (TN):** Normal e-postaydı ve model doğru biçimde `0` dedi.

Bu sayılar **karmaşıklık matrisini** oluşturur. Hangi hatanın daha önemli olduğuna göre farklı metriklere bakarız:

- **Doğruluk (accuracy):** Bütün örneklerin ne kadarında doğru tahmin yaptık?
- **Kesinlik (precision):** Modelin `1` dediği e-postaların ne kadarı gerçekten istenmeyen postaydı?
- **Duyarlılık (recall veya sensitivity):** Gerçek istenmeyen postaların ne kadarını yakaladık?
- **F1 skoru:** Kesinlik ile duyarlılığı birlikte özetleyen ölçü nedir?

Kesinlik, duyarlılık ve F1; bu derste `1` olarak adlandırdığımız **pozitif sınıfa** göre hesaplanır. Başka bir problemde önemli sınıf farklıysa, pozitif sınıfı ona göre belirlemeliyiz. Doğruluk ise pozitif sınıf seçimine bağlı değildir; bütün örneklerdeki doğru tahminlerin oranını ölçer.

## 2. Kendin yaz

### 2.1 Hataları say ve metrikleri hesapla

On e-postanın dördü istenmeyen olsun. Gerçek etiketler ile tahminleri aynı sırada tutuyoruz: ilk gerçek etiket ilk tahminle eşleşir. Döngü her çifti inceleyip TP, FP, FN ve TN sayılarını artırır.

```python {.python-playground}
gercek_etiketler = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
tahminler = [1, 1, 0, 0, 1, 0, 0, 0, 0, 0]

tp = 0
fp = 0
fn = 0
tn = 0

for gercek, tahmin in zip(gercek_etiketler, tahminler):
    if gercek == 1 and tahmin == 1:
        tp += 1
    elif gercek == 0 and tahmin == 1:
        fp += 1
    elif gercek == 1 and tahmin == 0:
        fn += 1
    else:
        tn += 1

matris = [[tn, fp], [fn, tp]]
dogruluk = (tp + tn) / len(gercek_etiketler)
kesinlik = tp / (tp + fp)
duyarlilik = tp / (tp + fn)
f1 = 2 * kesinlik * duyarlilik / (kesinlik + duyarlilik)

print("TP, FP, FN, TN:", tp, fp, fn, tn)
print("Karmaşıklık matrisi (satırlar gerçek 0/1, sütunlar tahmin 0/1):")
for satir in matris:
    print(satir)
print("Doğruluk:", round(dogruluk, 2))
print("Kesinlik:", round(kesinlik, 2))
print("Duyarlılık:", round(duyarlilik, 2))
print("F1 skoru:", round(f1, 2))
```
```text {.python-playground-expected}
TP, FP, FN, TN: 2 1 2 5
Karmaşıklık matrisi (satırlar gerçek 0/1, sütunlar tahmin 0/1):
[5, 1]
[2, 2]
Doğruluk: 0.7
Kesinlik: 0.67
Duyarlılık: 0.5
F1 skoru: 0.57
```
```text {.python-playground-help}
`gercek_etiketler` | Her e-postanın gerçek sınıfını yazarız. `1` istenmeyen, `0` normal e-posta demektir.
`tahminler` | Modelin aynı e-postalar için verdiği sınıfları aynı sırada tutarız; iki listenin uzunluğu ve sırası eşleşmelidir.
`tp = 0`, `fp = 0`, `fn = 0`, `tn = 0` | Dört hata/doğru tahmin sayacını sıfırdan başlatırız.
`for gercek, tahmin in zip(gercek_etiketler, tahminler):` | `zip`, iki listedeki aynı konumları bir çift olarak verir; böylece her gerçek etiketi modelin tahminiyle karşılaştırırız.
`if gercek == 1 and tahmin == 1:` | Gerçek etiket de tahmin de `1` ise istenmeyen postayı doğru yakalamışızdır.
`tp += 1` | Doğru pozitif sayısını bir artırırız.
`elif gercek == 0 and tahmin == 1:` | Gerçek e-posta normalken model `1` dediyse yanlış alarm vermiştir.
`fp += 1` | Yanlış pozitif sayısını artırırız.
`elif gercek == 1 and tahmin == 0:` | E-posta istenmeyen olduğu hâlde model `0` dediyse onu kaçırmıştır.
`fn += 1` | Yanlış negatif sayısını artırırız.
`else:` ve `tn += 1` | Bu ikililerden hiçbiri değilse gerçek etiket ve tahmin `0`'dır; normal e-postayı doğru tanımışızdır.
`matris = [[tn, fp], [fn, tp]]` | Dört sayıyı iki satırlı ve iki sütunlu bir listeye koyarız. İlk satır gerçek sınıfı `0`, ikinci satır `1` olan örnekleri; her satırdaki ilk ve ikinci değer de tahmin `0` ve `1` sayılarını gösterir.
`for satir in matris:` ve `print(satir)` | Her satırı ayrı ayrı yazdırıp karmaşıklık matrisini ekranda 2×2 tablo olarak görürüz.
`dogruluk = (tp + tn) / len(gercek_etiketler)` | Doğru tahminleri (TP ve TN) bütün örnek sayısına bölerek genel doğru oranını buluruz.
`kesinlik = tp / (tp + fp)` | Modelin `1` dediği örneklerden ne kadarının gerçekten `1` olduğunu hesaplarız. Yanlış alarm sayısı artarsa kesinlik düşer.
`duyarlilik = tp / (tp + fn)` | Gerçekte `1` olan örneklerden ne kadarını yakaladığımızı hesaplarız. Kaçırılan örnek sayısı artarsa duyarlılık düşer.
`f1 = 2 * kesinlik * duyarlilik / (kesinlik + duyarlilik)` | Kesinlik ve duyarlılığı birlikte özetleyen F1 değerini hesaplarız; ikisinden biri çok düşükse F1 de düşük kalır.
`print(...)` satırları | Önce saydığımız dört değeri ve karmaşıklık matrisini, sonra dört metriği iki ondalık basamakla gösteririz.
```

Bu örnekte iki istenmeyen e-postayı yakaladık (**TP=2**), bir normal e-postayı yanlışlıkla işaretledik (**FP=1**) ve iki istenmeyen e-postayı kaçırdık (**FN=2**). Kalan beş normal e-postayı doğru tanıdık (**TN=5**). Böylece doğruluk `0.7`, yani yüzde `70` olur; duyarlılık `0.5` olduğundan istenmeyen postaların yalnızca yarısını yakaladık.

Kesinlik ile duyarlılığın ikisi de önemliyse F1'e bakabiliriz. F1, ikisinin harmonik ortalamasıdır; basitçe söylemek gerekirse birinin yüksek, diğerinin çok düşük olduğu durumda yüksek görünmez. F1, doğru negatifleri doğrudan hesaba katmaz; bu nedenle her problemi tek başına açıklayan bir sayı değildir.

### 2.2 Doğruluğun yanıltıcı olduğu durumu gör

Şimdi on e-postadan yalnızca birinin istenmeyen olduğunu ve modelin hepsine “normal” dediğini düşün. Model dokuz örneği doğru bildiği için doğruluğu yüzde `90` çıkar; ama istenmeyen postaların hiçbirini yakalayamamıştır.

```python {.python-playground}
gercek_etiketler = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
tahminler = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

dogru_sayisi = 0
istenmeyen_sayisi = 0
yakaladigimiz_istenmeyen = 0

for gercek, tahmin in zip(gercek_etiketler, tahminler):
    if gercek == tahmin:
        dogru_sayisi += 1
    if gercek == 1:
        istenmeyen_sayisi += 1
        if tahmin == 1:
            yakaladigimiz_istenmeyen += 1

dogruluk = dogru_sayisi / len(gercek_etiketler)
duyarlilik = yakaladigimiz_istenmeyen / istenmeyen_sayisi

print("Doğruluk:", round(dogruluk, 2))
print("Yakalanan istenmeyen posta:", yakaladigimiz_istenmeyen)
print("İstenmeyen postaları yakalama oranı:", round(duyarlilik, 2))
```
```text {.python-playground-expected}
Doğruluk: 0.9
Yakalanan istenmeyen posta: 0
İstenmeyen postaları yakalama oranı: 0.0
```
```text {.python-playground-help}
`gercek_etiketler` | Dokuz normal e-posta (`0`) ve bir istenmeyen e-posta (`1`) olduğunu belirtiriz.
`tahminler` | Modelin her e-postaya normal dediğini gösteririz; bu basit model hiçbir istenmeyen postayı yakalamaya çalışmıyor.
`dogru_sayisi = 0` | Doğru sınıflandırılan e-postaları sayacağımız değişkeni başlatırız.
`istenmeyen_sayisi = 0` | Gerçekte kaç istenmeyen e-posta olduğunu saymak için sayaç açarız.
`yakaladigimiz_istenmeyen = 0` | Modelin doğru yakaladığı istenmeyen e-postaları sayacağımız değişkeni başlatırız.
`for gercek, tahmin in zip(...):` | Gerçek etiketlerle tahminleri aynı konumda eşleştirip sırayla inceleriz.
`if gercek == tahmin:` | Tahmin gerçekle aynıysa örnek doğru sınıflandırılmıştır.
`dogru_sayisi += 1` | Doğru tahmin sayısını artırırız.
`if gercek == 1:` | Bu örneğin gerçekten istenmeyen posta olup olmadığını kontrol ederiz.
`istenmeyen_sayisi += 1` | Gerçek istenmeyen posta sayısını artırırız.
`if tahmin == 1:` | Model bu istenmeyen postayı yakalamış mı diye bakarız.
`yakaladigimiz_istenmeyen += 1` | Yakalamışsa bulunan istenmeyen posta sayısını artırırız.
`dogru_sayisi / len(gercek_etiketler)` | Tüm e-postalar içindeki doğru tahmin oranını buluruz.
`yakaladigimiz_istenmeyen / istenmeyen_sayisi` | Gerçek istenmeyen e-postalardan yakalananların oranını, yani duyarlılığı hesaplarız.
`print(...)` satırları | Genel doğruluğu, yakalanan istenmeyen posta sayısını ve duyarlılığı gösteririz.
```

Yüzde `90` doğruluk kulağa iyi gelse de modelin duyarlılığı `0`'dır. İstenmeyen postaları kaçırmak bizim için önemliyse doğruluğa tek başına güvenemeyiz. Benzer biçimde, yanlışlıkla normal e-postaları spam klasörüne atmak daha maliyetliyse kesinliğe özellikle bakmalıyız.

### Şimdi sen yaz: kesinlik ve duyarlılık

Hata sayaçlarını tamamla, sonra kesinlik ve duyarlılığı hesapla. Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur, sonra çalıştır.

```python {.python-playground-task}
gercek = [1, 1, 0, 0, 1, 0, 1]
tahmin = [1, 0, 0, 1, 1, 0, 0]

# tp = fp = fn = 0, üç değişkene de aynı anda 0 verir.
tp = fp = fn = 0
for g, t in zip(gercek, tahmin):
    if g == 1 and t == 1:
        tp += 1
    # TODO: Gerçek 0 iken tahmin 1 ise yanlış pozitiftir.
    elif ___:
        fp += 1
    # TODO: Gerçek 1 iken tahmin 0 ise yanlış negatiftir.
    elif ___:
        fn += 1

# TODO: Kesinlik = tp / (tp + fp), duyarlılık = tp / (tp + fn).
kesinlik = ___
duyarlilik = ___
print("TP, FP, FN:", tp, fp, fn)
print("Kesinlik:", round(kesinlik, 2), "Duyarlılık:", round(duyarlilik, 2))
```
```text {.python-playground-expected}
TP, FP, FN: 2 1 2
Kesinlik: 0.67 Duyarlılık: 0.5
```
```text {.python-playground-help}
`elif ___:` (ilki) | Yanlış pozitif: gerçek `0` ama model `1` demiş. `g == 0 and t == 1`.
`elif ___:` (ikincisi) | Yanlış negatif: gerçek `1` ama model `0` demiş. `g == 1 and t == 0`.
`kesinlik = ___` | Modelin `1` dediklerinin kaçı gerçekten `1`: `tp / (tp + fp)`.
`duyarlilik = ___` | Gerçek `1`'lerin kaçını yakaladık: `tp / (tp + fn)`.
```
```python {.python-playground-solution}
gercek = [1, 1, 0, 0, 1, 0, 1]
tahmin = [1, 0, 0, 1, 1, 0, 0]

# tp = fp = fn = 0, üç değişkene de aynı anda 0 verir.
tp = fp = fn = 0
for g, t in zip(gercek, tahmin):
    if g == 1 and t == 1:
        tp += 1
    # Gerçek 0 iken tahmin 1 ise yanlış pozitiftir.
    elif g == 0 and t == 1:
        fp += 1
    # Gerçek 1 iken tahmin 0 ise yanlış negatiftir.
    elif g == 1 and t == 0:
        fn += 1

# Kesinlik = tp / (tp + fp), duyarlılık = tp / (tp + fn).
kesinlik = tp / (tp + fp)
duyarlilik = tp / (tp + fn)
print("TP, FP, FN:", tp, fp, fn)
print("Kesinlik:", round(kesinlik, 2), "Duyarlılık:", round(duyarlilik, 2))
```

## 3. Kütüphaneyle yap

Scikit-learn, bu metrikleri hazır işlevlerle hesaplar. Karmaşıklık matrisinde satırlar gerçek sınıfı, sütunlar tahmin edilen sınıfı gösterir; `labels=[0, 1]` sırası kullanıldığında matris `[[TN, FP], [FN, TP]]` biçimindedir.

```python
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score
)

gercek_etiketler = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
tahminler = [1, 1, 0, 0, 1, 0, 0, 0, 0, 0]

matris = confusion_matrix(gercek_etiketler, tahminler, labels=[0, 1])
dogruluk = accuracy_score(gercek_etiketler, tahminler)
kesinlik = precision_score(gercek_etiketler, tahminler, pos_label=1)
duyarlilik = recall_score(gercek_etiketler, tahminler, pos_label=1)
f1 = f1_score(gercek_etiketler, tahminler, pos_label=1)

print("Karmaşıklık matrisi:")
print(matris)
print("Doğruluk:", round(dogruluk, 2))
print("Kesinlik:", round(kesinlik, 2))
print("Duyarlılık:", round(duyarlilik, 2))
print("F1 skoru:", round(f1, 2))
```

Beklenen çıktı:

```text
Karmaşıklık matrisi:
[[5 1]
 [2 2]]
Doğruluk: 0.7
Kesinlik: 0.67
Duyarlılık: 0.5
F1 skoru: 0.57
```

Bu kod tarayıcıdaki Python penceresinde çalışmaz; scikit-learn bu çalışma alanında kurulu değildir. Python'ın kurulu olduğu bilgisayarda gerekirse `python -m pip install scikit-learn` komutuyla paketi kur, kodu `metrikler.py` adıyla kaydet ve `python metrikler.py` komutuyla çalıştır.

`pos_label=1`, kesinlik, duyarlılık ve F1'in hangi sınıfa göre hesaplanacağını açıkça belirtir. Bu örnekte pozitif sınıf istenmeyen postadır. Başka bir problemde önemli sınıf `0` ise pozitif sınıf ayarını ve yorumunu ona göre değiştirmek gerekir.

## 4. Sık yapılan hatalar

- **Doğruluğu tek başına yeterli görmek.** Sınıflar dengesizse model çoğunluk sınıfını hep seçerek yüksek doğruluk alabilir ama önemli sınıfı hiç bulamayabilir.
- **Kesinlikle duyarlılığı karıştırmak.** Kesinlik, modelin pozitif dediği örneklerin ne kadarının doğru olduğunu sorar; duyarlılık, gerçek pozitiflerin ne kadarını bulduğunu sorar.
- **Yanlış pozitif ve yanlış negatifi ters anlamak.** Yanlış pozitif, normal e-postaya spam demektir; yanlış negatif, spam'i kaçırıp normal saymaktır.
- **F1'i bütün başarıyı gösteren tek puan sanmak.** F1 kesinlik ve duyarlılığı özetler; doğru negatifleri doğrudan hesaba katmaz.
- **Önemli sınıfı belirtmemek.** Kesinlik, duyarlılık ve F1'in ne ifade ettiği pozitif sınıfın ne olduğuna bağlıdır.
- **Sıraları eşleşmeyen listeleri karşılaştırmak.** Her tahmin aynı konumdaki gerçek etikete ait olmalıdır; listelerin uzunluğu ve sırası uyuşmalıdır.
- **Bir payda sıfır olduğunda metrik tanımlıymış gibi davranmak.** Hiç pozitif tahmin yoksa kesinlik hesabının paydası sıfır olur; hiç gerçek pozitif yoksa duyarlılık tanımsızdır. Gerçek projede bu durumu açıkça ele al ve hangi kuralı kullandığını belirt.
- **Test kümesine tekrar tekrar bakarak model ayarlamak.** Metrikleri model seçmek için doğrulama verisinde karşılaştır; 2.4'teki gibi test verisini en son değerlendirmeye sakla.

## 5. Pekiştir

**Quiz**

1. İstenmeyen bir postayı normal diye sınıflandırmak hangi hata türüdür?
2. Modelin `1` dediği e-postaların ne kadarının gerçekten spam olduğunu hangi metrik ölçer?
3. Gerçek spam e-postaların ne kadarını yakaladığımızı hangi metrik ölçer?
4. Model her e-postaya `0` dediğinde doğruluk neden yanıltıcı olabilir?
5. F1 hangi iki metriği birlikte özetler?

**Alıştırmalar**

1. İlk pencerede ilk tahmini `0` yap. Hangi sayaç değişir ve metrikler nasıl etkilenir?
2. İkinci pencerede son tahmini `1` yap. Doğruluk `0.9`'dan `0.8`'e nasıl değişir? Başta pozitif tahmin olmadığı için kesinlik neden tanımsızdır; son tahmini `1` yapınca neden `0` olur? Duyarlılık neden hâlâ `0` kalır?
3. (İsteğe bağlı) Bir hastalık tarama modelinde hastalığı kaçırmak maliyetliyse duyarlılık mı, kesinlik mi daha önemli olabilir? Yanlış alarmın da maliyetini düşün.
4. (İsteğe bağlı) Scikit-learn örneğinde `pos_label=1` değerini `0` yap. Kesinlik ve duyarlılık artık hangi sınıfı anlatır?

??? success "Quiz cevapları"
    1. Yanlış negatif (FN): gerçek etiket `1` iken model `0` tahmin etmiştir.
    2. Kesinlik (precision).
    3. Duyarlılık (recall veya sensitivity).
    4. Çoğunluk sınıfı `0` ise model hiçbir `1` örneğini bulmasa bile çok sayıda `0` örneğini doğru tahmin edebilir.
    5. Kesinlik ve duyarlılığı.

## Özet

Sınıflandırma başarısını anlamak için gerçek etiketlerle tahminleri karşılaştırıp doğru pozitif, yanlış pozitif, yanlış negatif ve doğru negatif sayılarını buluruz. Doğruluk genel doğru oranını; kesinlik pozitif tahminlerin güvenilirliğini; duyarlılık gerçek pozitifleri yakalama oranını anlatır. F1, kesinlikle duyarlılığı birlikte özetler ama her hata türünü tek başına açıklamaz. Kullanılacak metriği, problemde hangi hatanın daha maliyetli olduğuna göre seçmeliyiz.

## Kaynaklar

- [scikit-learn resmî belgesi: Sınıflandırma metrikleri](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)
- [scikit-learn resmî belgesi: `confusion_matrix`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)
