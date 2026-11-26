# Faz 2 – Ders 5: Karar ağaçları

> ⏱️ Tahmini süre: 65-80 dk · 📚 Ön koşul: 0.2 Python hızlı tekrar, 1.6 Entropi ve çapraz entropi, 2.1 NumPy ile veri, 2.3 Lojistik regresyon, 2.4 Eğitim, doğrulama ve test · 💻 Gereksinim: Python 3.11+; temel örnekler ek paketsiz, scikit-learn örneği için scikit-learn kurulmalıdır

## Bu derste ne öğreneceksin?

- Karar ağacının sorularla veriyi gruplara ayırmasını
- Düğüm, dal ve yaprak kavramlarını
- Gini safsızlığını kullanarak basit bir bölme kuralı seçmeyi
- Ağacın derinliğini sınırlamanın aşırı öğrenmeye karşı nasıl yardımcı olduğunu
- Elle yazdığımız küçük bir ağacı scikit-learn ile eğitilmiş ağaçla karşılaştırmayı

## 1. Problem

Bir öğrencinin çalışma saatine bakarak sınavı geçip geçemeyeceğini tahmin edelim. Doğrusal regresyonda bir çizgiyle sayısal sonuç tahmin etmiştik; lojistik regresyonda olasılık hesaplayıp sınıf seçmiştik. **Karar ağacı** ise sırayla sorular sorar. Örneğin “Çalışma saati `3.5`'ten fazla mı?” sorusunun cevabına göre bir sonraki adıma gider.

Ağacın her soru sorduğu yere **düğüm**, sorudan çıkan yollara **dal**, artık yeni soru sormadan tahmin veren son noktalara **yaprak** denir. Bu derste yalnızca iki sınıfı (`0`: başarısız, `1`: başarılı) ve tek bir sayısal girdiyi kullanacağız. Gerçek ağaçlar birden fazla özellik üzerinde tekrar tekrar bölme yapabilir.

## 2. Kendin yaz

### 2.1 Bir karar sorusu yaz

Önce ağacı elle tek soruluk bir kurala indirgeyelim. Burada eşiği biz seçiyoruz; bu kod henüz veriden öğrenmiyor.

```python {.python-playground}
calisma_saati = 4

if calisma_saati <= 3.5:
    tahmin = "Başarısız"
else:
    tahmin = "Başarılı"

print(f"{calisma_saati} saat çalışma: {tahmin}")
```
```text {.python-playground-expected}
4 saat çalışma: Başarılı
```
```text {.python-playground-help}
`calisma_saati = 4` | Tahmin yapacağımız öğrencinin çalışma saatini belirleriz.
`if calisma_saati <= 3.5:` | Ağacın kök düğümündeki soruyu yazarız. `<=`, “küçük veya eşit” demektir.
`tahmin = "Başarısız"` | Saat `3.5` veya daha azsa ilk dala gidip bu sınıfı seçeriz.
`else:` | Önceki koşul yanlışsa, yani saat `3.5`'ten büyükse diğer dala geçeriz.
`tahmin = "Başarılı"` | İkinci dala ait sınıf tahminini belirleriz.
`print(...)` | Girdiyle birlikte seçilen sınıfı gösteririz.
```

`calisma_saati` değerini `2` yaparsan ilk dal, `5` yaparsan ikinci dal çalışır. `3.5` eşiğini şimdilik elle seçtik. Bir sonraki örnekte benzer bir eşiği eğitim verisinden nasıl seçebileceğimizi göreceğiz.

### 2.2 Veriden en iyi bölmeyi bul

Karar ağacı, her sorudan sonra oluşan grupların olabildiğince **tek bir sınıftan** oluşmasını ister. Bu karışıklığı ölçmek için **Gini safsızlığı** kullanacağız:

`Gini = 1 - (başarısız oranı² + başarılı oranı²)`

İki sınıfın oranı eşitse Gini `0.5` olur; grup tek bir sınıftan oluşuyorsa Gini `0` olur. Her olası eşiği dener, bölünmeden sonraki Gini değerlerinin örnek sayısına göre ağırlıklı ortalamasını hesaplar ve en küçük değeri seçeriz.

1.6 dersinde gördüğün entropi de sınıfların dağılımını ölçmek için kullanılabilir. Entropi ile Gini aynı formül değildir; ikisi de olası bölünmeleri karşılaştırmaya yarar. Bu derste hesabı daha kısa olan Gini'yi kullanacağız.

```python {.python-playground}
egitim_verisi = [
    (1, 0), (2, 0), (3, 0),
    (4, 1), (5, 1), (6, 1)
]


def gini(veriler):
    basarili_sayisi = 0
    for saat, etiket in veriler:
        if etiket == 1:
            basarili_sayisi += 1

    basarili_orani = basarili_sayisi / len(veriler)
    basarisiz_orani = 1 - basarili_orani
    return 1 - basarili_orani ** 2 - basarisiz_orani ** 2


sirali_veri = sorted(egitim_verisi)
esik_adaylari = []
for i in range(len(sirali_veri) - 1):
    saat = sirali_veri[i][0]
    sonraki_saat = sirali_veri[i + 1][0]
    if saat != sonraki_saat:
        esik_adaylari.append((saat + sonraki_saat) / 2)

en_iyi_esik = esik_adaylari[0]
en_dusuk_gini = float("inf")

for esik in esik_adaylari:
    sol_grup = []
    sag_grup = []

    for saat, etiket in sirali_veri:
        if saat <= esik:
            sol_grup.append((saat, etiket))
        else:
            sag_grup.append((saat, etiket))

    bolunme_ginisi = (
        len(sol_grup) / len(sirali_veri) * gini(sol_grup)
        + len(sag_grup) / len(sirali_veri) * gini(sag_grup)
    )

    if bolunme_ginisi < en_dusuk_gini:
        en_dusuk_gini = bolunme_ginisi
        en_iyi_esik = esik

print("Bölmeden önce Gini:", round(gini(sirali_veri), 2))
print("Seçilen eşik:", en_iyi_esik)
print("Bölünmeden sonra ağırlıklı Gini:", round(en_dusuk_gini, 2))

for saat in [2, 4, 6]:
    if saat <= en_iyi_esik:
        sinif = "Başarısız"
    else:
        sinif = "Başarılı"
    print(f"{saat} saat çalışma: {sinif}")
```
```text {.python-playground-expected}
Bölmeden önce Gini: 0.5
Seçilen eşik: 3.5
Bölünmeden sonra ağırlıklı Gini: 0.0
2 saat çalışma: Başarısız
4 saat çalışma: Başarılı
6 saat çalışma: Başarılı
```
```text {.python-playground-help}
`egitim_verisi` | Her öğrencinin saatini ve gerçek sınıfını aynı çiftte tutarız; bu örnekte ilk üç etiket `0`, son üç etiket `1`'dir.
`def gini(veriler):` | Verilen grupta iki sınıfın ne kadar karışık olduğunu hesaplayan işlevi tanımlarız.
`basarili_sayisi = 0` | Başarılı etiketlerin sayısını sıfırdan başlatırız.
`for saat, etiket in veriler:` | Gruptaki her örneğin etiketini sırayla inceleriz.
`if etiket == 1:` ve `basarili_sayisi += 1` | Etiket başarılıysa başarılı sayısını bir artırırız.
`basarili_orani = basarili_sayisi / len(veriler)` | Gruptaki başarılı örneklerin oranını buluruz.
`basarisiz_orani = 1 - basarili_orani` | İki sınıf olduğundan başarısızların oranı, başarılıların oranının `1`'den çıkarılmasıyla bulunur.
`return 1 - ...` | Oranların karelerini kullanarak Gini safsızlığını hesaplarız; tüm örnekler aynı sınıftaysa sonuç `0` çıkar. Bu örnekte işlevi yalnızca boş olmayan gruplara uygularız.
`sirali_veri = sorted(egitim_verisi)` | Örnekleri çalışma saatine göre sıralarız; eşik adaylarını komşu saatlerden çıkaracağız.
`for i in range(len(sirali_veri) - 1):` | Son örnek dışında her örnekle bir sonrakini karşılaştırırız.
`saat` ve `sonraki_saat` | Sıralı listedeki yan yana iki çalışma saatini alırız.
`if saat != sonraki_saat:` | Aynı saatteki örneklerin arasına bölme koymayız; onları birbirinden ayırmak doğru olmaz.
`esik_adaylari.append((saat + sonraki_saat) / 2)` | Farklı iki saatin tam ortasını olası eşik olarak saklarız. Örneğin `3` ile `4` arasındaki eşik `3.5` olur.
`en_iyi_esik = esik_adaylari[0]` | İlk eşiği başlangıçtaki en iyi aday kabul ederiz; daha iyi eşik bulursak değiştireceğiz.
`en_dusuk_gini = float("inf")` | Şimdiye kadarki en düşük bölünme değerini başlangıçta sonsuz seçeriz; denenen ilk gerçek değer bundan küçük olur.
`for esik in esik_adaylari:` | Her olası eşiği sırayla deneyip grupların ne kadar karışık kaldığını ölçeriz.
`sol_grup = []` ve `sag_grup = []` | Eşiğin soluna ve sağına düşen örnekleri ayrı listelerde toplarız.
`for saat, etiket in sirali_veri:` | Her eşik için bütün eğitim örneklerini yeniden inceleriz.
`if saat <= esik:` | Örneğin çalışma saatinin eşiğin solunda olup olmadığını kontrol ederiz.
`sol_grup.append(...)` ve `sag_grup.append(...)` | Örneği koşulun sonucuna göre ilgili gruba ekleriz.
`bolunme_ginisi = ...` | İki grubun Gini değerlerini grup büyüklükleriyle ağırlıklandırıp ortalarız. Büyük gruplar sonuca daha fazla etki eder.
`if bolunme_ginisi < en_dusuk_gini:` | Denediğimiz eşik şimdiye kadarki en temiz bölünmeyi sağlıyor mu diye kontrol ederiz.
`en_dusuk_gini = bolunme_ginisi` ve `en_iyi_esik = esik` | Daha iyi bölünme bulduysak en iyi değerleri güncelleriz.
İlk üç `print(...)` çağrısı | Başlangıçtaki karışıklığı, seçilen eşiği ve bölünme sonrası ağırlıklı karışıklığı gösteririz.
`for saat in [2, 4, 6]:` | Öğrenilmiş soruyu üç çalışma saati üzerinde deneriz.
`if saat <= en_iyi_esik:` ve `else:` | Saatin hangi dala gideceğini belirleyip o dalın sınıfını seçeriz.
`print(f"{saat} saat çalışma: {sinif}")` | Her deneme girdisi için ağacın verdiği sınıf tahminini gösteririz.
```

Bu örnek tek bir soru bulduğu için **tek seviyeli ağaç** veya **karar kütüğü** olarak düşünülebilir. Gerçek bir ağaç aynı bölme fikrini alt gruplarda da tekrarlayarak birden çok düğüm oluşturabilir. Gini `0` çıktığında, bu örnekteki her yaprak tek bir sınıftan oluşmuştur; bu küçük ve düzenli veri, gerçek verilerin her zaman bu kadar kolay ayrılacağı anlamına gelmez.

### Şimdi sen yaz: Gini safsızlığı

Gini fonksiyonunu tamamla ve bir bölmenin ağırlıklı Gini değerini hesapla. `# TODO` yazan yerlerdeki `___` boşluklarını tamamla, sonra çalıştır.

```python {.python-playground-task}
def gini(etiketler):
    basarili_orani = sum(etiketler) / len(etiketler)
    basarisiz_orani = 1 - basarili_orani
    # TODO: Gini = 1 - (başarılı oranı² + başarısız oranı²)
    return ___


print("Karışık grup:", gini([0, 1, 0, 1]))
print("Saf grup:", gini([1, 1, 1, 1]))

sol = [0, 0, 0]
sag = [1, 1, 0]
# TODO: Ağırlıklı Gini = sol_oran × gini(sol) + sağ_oran × gini(sag). Toplam 6 örnek var.
bolunme = ___
print("Bölünme sonrası:", round(bolunme, 2))
```
```text {.python-playground-expected}
Karışık grup: 0.5
Saf grup: 0.0
Bölünme sonrası: 0.22
```
```text {.python-playground-help}
`return ___` | Formül yorumda yazıyor. Oranların karelerini `** 2` ile al, topla ve `1`'den çıkar.
`bolunme = ___` | Her grubun Gini değerini, o grubun örnek sayısının toplama oranıyla çarp: `len(sol) / 6 * gini(sol)`. Sağ grup için de aynısını yap ve topla.
```

## 3. Kütüphaneyle yap

Scikit-learn, karar ağacını veriden eğitmeye yarar. `max_depth=1` diyerek ağacın tek bir soru sormasına izin veriyoruz; böylece az önce elle bulduğumuz basit ağaçla karşılaştırabiliriz.

```python
from sklearn.tree import DecisionTreeClassifier

egitim_girdileri = [[1], [2], [3], [4], [5], [6]]
egitim_etiketleri = [0, 0, 0, 1, 1, 1]

model = DecisionTreeClassifier(max_depth=1, random_state=42)
model.fit(egitim_girdileri, egitim_etiketleri)

yeni_girdiler = [[2], [4], [6]]
tahminler = model.predict(yeni_girdiler)

print("Öğrenilen eşik:", round(model.tree_.threshold[0], 1))
print("Tahmin edilen sınıflar:", tahminler.tolist())
```

Beklenen çıktı:

```text
Öğrenilen eşik: 3.5
Tahmin edilen sınıflar: [0, 1, 1]
```

Bu kod tarayıcıdaki Python penceresinde çalışmaz; scikit-learn bu çalışma alanında kurulu değildir. Python'ın kurulu olduğu bilgisayarda gerekirse `python -m pip install scikit-learn` komutuyla paketi kur, kodu `karar_agaci.py` adıyla kaydet ve `python karar_agaci.py` komutuyla çalıştır.

- `DecisionTreeClassifier(...)`: Sınıf tahmini yapacak karar ağacını oluşturur.
- `max_depth=1`: Ağacın en fazla bir karar sorusu sormasına izin verir. Daha derin ağaçlar daha karmaşık örüntüler yakalayabilir, fakat eğitim verisini ezberleme riski de artar.
- `random_state=42`: Aynı ayarlarla yeniden çalıştırdığımızda tekrarlanabilir sonuç almamıza yardım eder.
- `model.fit(...)`: Eğitim girdilerini ve doğru etiketleri kullanarak ağacı kurar.
- `model.predict(...)`: Daha önce vermediğimiz saatler için tahmin edilen sınıfları döndürür.
- `model.tree_.threshold[0]`: Kök düğümde öğrenilen ilk eşiği gösterir. Buradaki `0` indeksli düğüm ağacın köküdür.
- `tahminler.tolist()`: NumPy dizisi olan tahminleri, ekranda daha kolay okunması için Python listesine çevirir.

Gerçek bir çalışmada `max_depth` gibi ayarları doğrulama kümesinde karşılaştır; test kümesini seçimi bitirene kadar kullanma. Bir ağacı gereğinden fazla büyütmek aşırı öğrenmeye yol açabilir. Çok sığ bir ağaç ise önemli örüntüleri yakalayamayabilir.

## 4. Sık yapılan hatalar

- **Ağacın bütün veriyi tek seferde ezberlediğini sanmak.** Ağaç, düğümlerdeki sorularla veriyi adım adım gruplara ayırır.
- **Gini safsızlığını doğruluk yüzdesi sanmak.** Gini, bir gruptaki sınıfların ne kadar karışık olduğunu ölçer; tahminlerin yüzde kaçının doğru olduğunu söylemez.
- **İki grubun Gini değerini ağırlıksız ortalamak.** Grupların örnek sayıları farklı olabilir; büyük gruba daha fazla ağırlık vermeliyiz.
- **Bir düğümün Gini değeri `0` ise modelin her yerde doğru olduğunu düşünmek.** Bu yalnızca incelenen gruptaki eğitim etiketlerinin aynı olduğunu söyler; yeni verideki sonucu garanti etmez.
- **Derin ağacın her zaman daha iyi olduğunu sanmak.** Derin ağaç eğitim verisindeki küçük ayrıntıları ezberleyebilir; derinliği doğrulama verisiyle seç.
- **Tek eşikli örneğin bütün ağaçları anlattığını sanmak.** Bu dersin saf Python kodu yalnızca bir bölme yapar; gerçek ağaçlar birden fazla özellik ve ardışık bölmeler kullanabilir.
- **Test verisini ayar seçmek için kullanmak.** Son değerlendirmeyi tarafsız tutmak için 2.4 dersindeki eğitim-doğrulama-test ayrımını koru.

## 5. Pekiştir

**Quiz**

1. Karar ağacındaki düğüm, dal ve yaprak ne anlama gelir?
2. Bu örnekte Gini değeri `0` olan bir grup bize ne söyler?
3. Eşik seçerken neden iki grubun Gini değerini ağırlıklandırıyoruz?
4. `max_depth` neyi sınırlar ve neden yararlı olabilir?
5. Ağacın derinliğini seçmek için hangi veri kümesine, son değerlendirme için hangisine bakmalıyız?

**Alıştırmalar**

1. İlk penceredeki çalışma saatini `2` ve `5` yap. Her biri neden farklı dala gider?
2. İkinci pencerede `(3, 1)` örneğini eğitim verisine ekle. En iyi eşik ve Gini değeri değişiyor mu?
3. İkinci pencerede etiketlerden birini ters çevir. Biraz gürültü eklendiğinde en iyi bölünmenin neden artık `0` Gini vermeyebileceğini açıkla.
4. (İsteğe bağlı) Scikit-learn örneğinde `max_depth=1` değerini `2` yap. Eğitim tahminleri değişiyor mu? Bir sonraki derste metriklerle nasıl değerlendirebileceğimizi öğreneceksin.
5. (İsteğe bağlı) Birden fazla karar sorusu içeren günlük bir örnek düşün ve soruları kök, dallar ve yapraklar olarak yaz.

??? success "Quiz cevapları"
    1. Düğüm soru sorulan noktadır; dal cevaba göre izlenen yoldur; yaprak son sınıf tahminini verir.
    2. O gruptaki eğitim örneklerinin hepsi aynı sınıftadır.
    3. Çünkü grupların büyüklükleri farklı olabilir; çok küçük bir grubun saflığı tüm bölünmeyi tek başına belirlememelidir.
    4. Ağacın en fazla kaç karar katmanı oluşturabileceğini sınırlar; gereksiz karmaşıklığı ve aşırı öğrenme riskini azaltmaya yardım eder.
    5. Ayar seçimi için doğrulama, son değerlendirme için test kümesine bakarız.

## Özet

Karar ağacı, veriyi art arda sorularla gruplara ayırır ve yapraklarda sınıf tahmini üretir. Bu derste Gini safsızlığıyla tek bir eşik seçtik; scikit-learn ile aynı fikri bir karar ağacına uygulatıp derinliğini sınırladık. Ağacın eğitim verisini ezberleyip ezberlemediğini anlamak için ayarları doğrulama kümesinde seçmeli, test kümesini ise son değerlendirmeye saklamalıyız.

## Kaynaklar

- [scikit-learn resmî belgesi: Karar ağaçları](https://scikit-learn.org/stable/modules/tree.html)
- [scikit-learn resmî belgesi: `DecisionTreeClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)
