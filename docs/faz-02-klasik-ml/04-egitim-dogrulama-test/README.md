# Faz 2 – Ders 4: Eğitim, doğrulama ve test

> ⏱️ Tahmini süre: 50-65 dk · 📚 Ön koşul: 0.2 Python hızlı tekrar, 2.1 NumPy ile veri, 2.2 Doğrusal regresyon, 2.3 Lojistik regresyon · 💻 Gereksinim: Python 3.11+; temel örnekler ek paketsiz, scikit-learn örneği için scikit-learn kurulmalıdır

## Bu derste ne öğreneceksin?

- Bir veri kümesini eğitim, doğrulama ve test parçalarına ayırmayı
- Her parçanın farklı bir amacı olduğunu açıklamayı
- Eğitim verisini tekrar tekrar değerlendirmekten kaçınmayı
- Aşırı öğrenmenin eğitim başarısı yüksekken yeni örneklerde neden başarısız olabildiğini görmeyi
- Test verisini model seçimi bittikten sonra kullanmayı

## 1. Problem

Bir modele öğrencilerin çalışma saatlerini ve sınav sonuçlarını verdiğimizi düşün. Modelin bu örnekleri ezberlemesi değil, daha önce görmediği öğrenciler için de işe yarayan bir örüntü öğrenmesi gerekir. Bunu anlayabilmek için elimizdeki veriyi üç ayrı parçaya ayırırız:

- **Eğitim kümesi:** Modelin ağırlıklarını ve diğer öğrenilen değerlerini ayarlamak için kullanılır.
- **Doğrulama kümesi:** Farklı modelleri veya ayarları karşılaştırırken kullanılır. Bu kümeye bakarak model seçebiliriz; modelin ağırlıkları doğrudan bu veriden öğrenilmez.
- **Test kümesi:** Modeli ve ayarları seçtikten sonra, daha önce kullanılmamış verideki başarısını son kez ölçmek için ayrılır.

Bir öğrenci soruların cevaplarını ezberleyip aynı soruları yeniden doğru yanıtlayabilir. Ancak bu, yeni soruları çözebildiğini kanıtlamaz. Modeli eğitim verisinde değerlendirmek de buna benzer: model bu veriyi zaten gördüğü için sonucu olduğundan iyi görünebilir.

Model eğitim örneklerini çok iyi öğrenip yeni örneklerde kötü sonuç veriyorsa **aşırı öğrenme** (overfitting) vardır. Model, genel örüntü yerine eğitim verisindeki ayrıntıları veya gürültüyü ezberlemiş olabilir. Doğrulama kümesi bu durumu fark etmemize, test kümesi ise son değerlendirmeyi daha adil yapmamıza yardım eder.

## 2. Kendin yaz

### 2.1 Veriyi üç parçaya ayır

Her kayıt bir `(çalışma saati, gerçek sonuç)` çiftidir. Çifti tek bir öğe olarak sakladığımız için saat ile ona ait sonuç ayrılmaz. Önce kayıtları karıştırır, sonra yaklaşık yüzde 60'ını eğitim, yüzde 20'sini doğrulama ve kalanını test için ayırırız.

```python {.python-playground}
import random

veriler = [
    (1, 0), (2, 0), (3, 1), (4, 1), (5, 1),
    (0, 0), (6, 1), (2, 0), (4, 1), (1, 0)
]

karisik_veriler = veriler.copy()
rastgele = random.Random(42)
rastgele.shuffle(karisik_veriler)

egitim_sonu = int(len(karisik_veriler) * 0.6)
dogrulama_sonu = int(len(karisik_veriler) * 0.8)

egitim = karisik_veriler[:egitim_sonu]
dogrulama = karisik_veriler[egitim_sonu:dogrulama_sonu]
test = karisik_veriler[dogrulama_sonu:]

print("Toplam örnek:", len(karisik_veriler))
print("Eğitim kümesi:", len(egitim))
print("Doğrulama kümesi:", len(dogrulama))
print("Test kümesi:", len(test))
```
```text {.python-playground-expected}
Toplam örnek: 10
Eğitim kümesi: 6
Doğrulama kümesi: 2
Test kümesi: 2
```
```text {.python-playground-help}
`import random` | Python'la birlikte gelen rastgele seçim araçlarını kullanıma açar; paket kurmamız gerekmez.
`veriler = [...]` | Her öğrenciyi `(çalışma saati, sonuç)` biçiminde yazarız. `0` başarısız, `1` başarılı anlamına gelir.
`karisik_veriler = veriler.copy()` | Verilerin bir kopyasını alırız; karıştırma özgün listedeki sırayı bozmaz.
`rastgele = random.Random(42)` | Aynı başlangıç sayısını kullanarak yeniden çalıştırdığımızda aynı karışıklığı elde ederiz. `42` özel bir sayı değildir; sabit seçilmesi örneği tekrarlanabilir yapar.
`rastgele.shuffle(karisik_veriler)` | Kopyadaki kayıtların sırasını karıştırırız. Saat ve sonuç aynı çiftte kaldığından yanlış kişiye ait etiketle eşleşmez.
`egitim_sonu = int(len(karisik_veriler) * 0.6)` | Toplam örnek sayısının yüzde 60'ını eğitim için ayıracağımız son konumu buluruz.
`dogrulama_sonu = int(len(karisik_veriler) * 0.8)` | Toplamın yüzde 80'ine kadar olan konumu buluruz; eğitimden sonraki bölüm doğrulama kümesi olacaktır.
`egitim = karisik_veriler[:egitim_sonu]` | Listenin başından yüzde 60 sınırına kadar olan kayıtları eğitim kümesine alırız.
`dogrulama = karisik_veriler[egitim_sonu:dogrulama_sonu]` | Eğitim sınırından yüzde 80 sınırına kadar olan kayıtları doğrulama kümesine alırız.
`test = karisik_veriler[dogrulama_sonu:]` | Geriye kalan kayıtları test kümesine ayırırız. Bu örnekte toplamın yüzde 20'sidir.
`print(...)` satırları | Her parçaya kaç örnek düştüğünü kontrol ederiz; bu örnekte sayılar `6`, `2` ve `2` olur.
```

Yüzdeler küçük veri kümelerinde tam tutmayabilir; bu örnekte sayıların tam bölünmesi sonucu 6, 2 ve 2 kayıt elde ettik. Gerçek veride her sınıftan yeterli sayıda örnek bulunduğunu da kontrol et. Zaman sıralı verilerde (örneğin geçmiş satışlardan gelecek ayı tahmin ederken) rastgele karıştırmak geleceğe ait bilgiyi geçmişe sızdırabilir; bu durumda eski kayıtları eğitim, daha yeni kayıtları doğrulama ve test için ayırmak gerekir.

### 2.2 Ezberlemeyi doğrulama verisinde yakala

Aşağıdaki örnekte iki basit tahmin yöntemini karşılaştırıyoruz. **Ezberci** yöntem eğitimde gördüğü saatleri ve sonuçları bir sözlükte tutar; yeni bir saat görünce her zaman `0` der. **Eşik kuralı** ise saat `3` veya daha fazlaysa `1` tahmin eder. Bunlar gerçek bir eğitim algoritması değil, ezber ile genel bir kural arasındaki farkı görünür kılmak için hazırlanmış örneklerdir.

```python {.python-playground}
egitim = [(1, 0), (2, 0), (4, 1), (5, 1)]
dogrulama = [(3, 1), (6, 1)]
test = [(0, 0), (7, 1)]

ezber_sozlugu = {}
for saat, gercek_sonuc in egitim:
    ezber_sozlugu[saat] = gercek_sonuc


def tahmin_et(saat, yontem):
    if yontem == "ezberci":
        return ezber_sozlugu.get(saat, 0)
    return int(saat >= 3)


def dogruluk(veriler, yontem):
    dogru_sayisi = 0
    for saat, gercek_sonuc in veriler:
        tahmin = tahmin_et(saat, yontem)
        if tahmin == gercek_sonuc:
            dogru_sayisi += 1
    return round(dogru_sayisi / len(veriler) * 100)


print(
    "Ezberci - eğitim:",
    f"{dogruluk(egitim, 'ezberci')}%",
    "| doğrulama:",
    f"{dogruluk(dogrulama, 'ezberci')}%"
)
print(
    "Eşik kuralı - eğitim:",
    f"{dogruluk(egitim, 'esik')}%",
    "| doğrulama:",
    f"{dogruluk(dogrulama, 'esik')}%"
)
print("Seçilen eşik kuralı - test:", f"{dogruluk(test, 'esik')}%")
```
```text {.python-playground-expected}
Ezberci - eğitim: 100% | doğrulama: 0%
Eşik kuralı - eğitim: 100% | doğrulama: 100%
Seçilen eşik kuralı - test: 100%
```
```text {.python-playground-help}
`egitim`, `dogrulama` ve `test` listeleri | Önceki bölümde öğrendiğimiz gibi, her kayıt bir girdi ve ona ait doğru cevaptır. Burada örnekleri farkı daha net göstermek için elle ayırdık.
`ezber_sozlugu = {}` | Ezberci yöntemin eğitimde gördüğü saatleri ve cevapları saklayacağı boş sözlüğü oluştururuz.
`for saat, gercek_sonuc in egitim:` | Eğitim kayıtlarını sırayla açarız; her çiftin ilk değeri saat, ikincisi doğru sonuçtur.
`ezber_sozlugu[saat] = gercek_sonuc` | Gördüğümüz saatin cevabını sözlüğe yazarız. Yeni bir örüntü öğrenmek yerine kayıtları hatırlıyoruz.
`def tahmin_et(saat, yontem):` | Verilen saat ve yöntem adına göre tahmin yapan işlevi tanımlarız.
`if yontem == "ezberci":` | Ezberci yöntemi kullanmamız istenmiş mi diye kontrol ederiz.
`ezber_sozlugu.get(saat, 0)` | Saat sözlükte varsa ezberlenen cevabı verir; yoksa bu örnekte seçtiğimiz varsayılan cevap `0`'ı verir.
`return int(saat >= 3)` | Eşik kuralında saat en az `3` ise `1`, daha azsa `0` döndürürüz. Python'da doğru/yanlış koşulu `int` ile `1`/`0` olur.
`def dogruluk(veriler, yontem):` | Seçilen yöntemin verilen kayıtların yüzde kaçında doğru cevap verdiğini hesaplayan işlevi tanımlarız.
`dogru_sayisi = 0` | Doğru tahminleri saymaya sıfırdan başlarız.
`for saat, gercek_sonuc in veriler:` | Ölçmek istediğimiz kümedeki her kaydı sırayla inceleriz.
`tahmin = tahmin_et(saat, yontem)` | O kaydın tahminini seçilen yöntemle hesaplarız.
`if tahmin == gercek_sonuc:` | Tahminin doğru cevapla aynı olup olmadığını kontrol ederiz.
`dogru_sayisi += 1` | Tahmin doğruysa doğru sayısını bir artırırız.
`round(dogru_sayisi / len(veriler) * 100)` | Doğru tahmin oranını yüzdeye çevirip tam sayıya yuvarlarız.
İlk iki `print(...)` çağrısı | İki yöntemin hem eğitim hem doğrulama kümelerindeki doğruluk oranını karşılaştırırız.
Son `print(...)` çağrısı | Doğrulama sonucunda seçtiğimiz eşik kuralını, model seçimi için kullanmadığımız test kümesinde son kez ölçeriz.
```

Ezberci yöntem eğitim kümesinde yüzde 100 doğru görünür; çünkü cevapları zaten saklamıştır. Ancak yeni saatleri görünce işe yaramaz ve doğrulama sonucu bunu ortaya çıkarır. Eşik kuralının bu küçük örneklerde daha iyi sonuç vermesi, gerçek hayattaki her problemde doğru model olacağını kanıtlamaz. Buradaki kümeler çok küçüktür; amaç ölçüm düzenini öğrenmektir, güvenilir bir başarı iddiası üretmek değil.

Doğrulama kümesine bakarak model veya ayar seçtikten sonra test kümesini bu seçimi değiştirmek için tekrar tekrar kullanma. Test sonucuna göre modeli yeniden ayarlarsan test verisi de karar sürecine katılmış olur; artık tarafsız bir son ölçüm sayılmaz. Test (veya doğrulama) verisinden gelen bilgi yanlışlıkla modelin eğitimine ya da seçimine karışırsa buna **veri sızıntısı** denir.

### Şimdi sen yaz: veriyi üçe böl

On örneği yüzde 60 eğitim, yüzde 20 doğrulama, yüzde 20 test olarak dilimle. `# TODO` yazan yerlerdeki `___` boşluklarını tamamla, sonra çalıştır.

```python {.python-playground-task}
veriler = list(range(1, 11))   # 10 örnek: 1, 2, ..., 10

# TODO: İlk 6 örnek eğitim, sonraki 2 doğrulama, kalan test olsun.
egitim = veriler[:___]
dogrulama = veriler[___:___]
test = veriler[___:]

print("Eğitim:", egitim)
print("Doğrulama:", dogrulama)
print("Test:", test)
```
```text {.python-playground-expected}
Eğitim: [1, 2, 3, 4, 5, 6]
Doğrulama: [7, 8]
Test: [9, 10]
```
```text {.python-playground-help}
`veriler[:___]` | Eğitim kümesi ilk 6 örnektir; dilimin bitişi `6`.
`veriler[___:___]` | Doğrulama, eğitimin bittiği yerden (`6`) başlar ve 2 örnek sürer, yani `8`'e kadar gider.
`veriler[___:]` | Test, doğrulamanın bittiği yerden (`8`) sona kadar olan örneklerdir.
```

## 3. Kütüphaneyle yap

Scikit-learn, veri ayırma işini `train_test_split` ile yapabilir. Burada önce verinin yüzde 60'ını eğitim, yüzde 40'ını geçici bölüm olarak ayırırız. Geçici bölümü yarıya böldüğümüzde doğrulama ve test kümelerinin her biri toplam verinin yüzde 20'si olur.

```python
from sklearn.model_selection import train_test_split

girdiler = [[1], [2], [3], [4], [5], [0], [6], [2], [4], [1]]
etiketler = [0, 0, 1, 1, 1, 0, 1, 0, 1, 0]

egitim_girdileri, gecici_girdiler, egitim_etiketleri, gecici_etiketler = (
    train_test_split(
        girdiler,
        etiketler,
        test_size=0.4,
        random_state=42,
        stratify=etiketler
    )
)

dogrulama_girdileri, test_girdileri, dogrulama_etiketleri, test_etiketleri = (
    train_test_split(
        gecici_girdiler,
        gecici_etiketler,
        test_size=0.5,
        random_state=42,
        stratify=gecici_etiketler
    )
)

print("Eğitim:", len(egitim_girdileri))
print("Doğrulama:", len(dogrulama_girdileri))
print("Test:", len(test_girdileri))
```

Beklenen çıktı:

```text
Eğitim: 6
Doğrulama: 2
Test: 2
```

Bu kod tarayıcıdaki Python penceresinde çalışmaz; scikit-learn bu çalışma alanında kurulu değildir. Python'ın kurulu olduğu bilgisayarda gerekirse `python -m pip install scikit-learn` komutuyla paketi kur, kodu `veri_bolme.py` adıyla kaydet ve `python veri_bolme.py` komutuyla çalıştır.

- `girdiler`: Her öğrencinin çalışma saatini bir elemanlı listede tutarız; scikit-learn girdi tablosunu satır ve sütunlardan oluşan bir yapı olarak bekler.
- `etiketler`: Her girdiye karşılık gelen doğru sınıfı aynı sırada tutarız. Girdilerle etiketler aynı sırada verilmelidir.
- `test_size=0.4`: İlk ayırmada verinin yüzde 40'ını geçici bölüme bırakırız.
- `random_state=42`: Aynı veride aynı bölmeyi yeniden elde etmek için sabit başlangıç değeri kullanırız.
- `stratify=etiketler`: Sınıfların oranını parçalar arasında olabildiğince korur. Her sınıfta yeterli örnek yoksa bu seçenek bölme hatası verebilir.
- İkinci çağrıda `test_size=0.5`: Geçici bölümün yarısını doğrulama, yarısını test olarak ayırırız.

## 4. Sık yapılan hatalar

- **Modeli test kümesinde seçmek.** Test sonuçlarına bakarak model veya ayar değiştirirsen test verisini de karar sürecinde kullanmış olursun.
- **Eğitim başarısını yeni verideki başarı sanmak.** Model eğitim örneklerini görmüştür; ezberleyip ezberlemediğini bu örneklerden tek başına anlayamayız.
- **Kayıtları ayırırken girdiyle etiketi koparmak.** Çalışma saati ile o öğrencinin gerçek sonucu aynı kayıtta kalmalıdır.
- **Veriyi her zaman rastgele bölmek.** Zaman sıralı verilerde rastgele bölme, gelecekten geçmişe bilgi sızdırabilir. Aynı kişiye ait tekrar kayıtlar varsa bunları farklı kümelere dağıtmak da modelin o kişiyi ezberlemesine yol açabilir.
- **Küçük test kümesindeki sonucu kesin kanıt saymak.** İki örnekte yüzde 100 başarı, gerçek kullanımda yüzde 100 başarı demek değildir; değerlendirme için yeterli ve uygun veri gerekir.
- **Doğrulama ve test kümelerini birbirinin yerine kullanmak.** Doğrulama model seçimine yardım eder; test, seçim tamamlandıktan sonra son ölçüm içindir.
- **Veri sızıntısını gözden kaçırmak.** Test kümesinden gelen bilgiyle ön işleme, özellik seçimi veya ayar yaparsan son ölçüm artık bağımsız değildir. Bu adımları yalnızca eğitim verisinden öğrenmek gerekir.

## 5. Pekiştir

**Quiz**

1. Eğitim kümesi model için ne yapar?
2. Doğrulama kümesini hangi amaçla kullanırız?
3. Test kümesine ne zaman bakmalıyız?
4. Eğitim başarısı yüksek, doğrulama başarısı düşükse ne olmuş olabilir?
5. Test sonucuna bakıp modeli değiştirirsek test kümesi neden artık tarafsız ölçüm olmaz?

**Alıştırmalar**

1. İlk penceredeki toplam kayıt sayısını `20` yap. Eğitim, doğrulama ve test kümelerindeki kayıt sayıları nasıl değişiyor?
2. İkinci pencerede eşik kuralını `saat >= 5` yap. Eğitim ve doğrulama sonuçları nasıl değişiyor? Bu ayarı seçmek için hangi kümeye bakmalısın?
3. Ezberci yöntemin sözlüğünde bulunmayan bir saati doğrulama verisine ekle. Ezberci yöntem neden varsayılan `0` tahminini verir?
4. (İsteğe bağlı) Bir kaydın etiketini değiştirip sadece test listesini uzat. Bu küçük örnekte doğruluk yüzdesi neden bir anda çok değişebilir?
5. (İsteğe bağlı) Aynı öğrencinin birden fazla kaydı varsa, bu kayıtların neden farklı kümelere dağılmaması gerektiğini kendi sözlerinle açıkla.

??? success "Quiz cevapları"
    1. Modelin ağırlıklarını ve öğrenilen diğer değerlerini ayarlamak için kullanılır.
    2. Modelleri veya ayarları karşılaştırıp seçim yapmak için kullanılır.
    3. Model ve ayarlar seçildikten sonra, son ve bağımsız bir değerlendirme yapmak için.
    4. Model eğitim örneklerini ezberlemiş olabilir; yani aşırı öğrenme vardır.
    5. Çünkü test sonucu artık model seçimini etkiler; model bu bilgiden dolaylı olarak yararlanmış olur.

## Özet

Eğitim kümesi modeli öğretir, doğrulama kümesi model veya ayar seçimine yardım eder, test kümesi ise seçim tamamlandıktan sonra son değerlendirme için kullanılır. Eğitim başarısının yüksek olması tek başına yeterli değildir; model yeni örneklerde başarısızsa aşırı öğrenmiş olabilir. Test verisini karar sürecinden ayrı tutmak ve verinin nasıl bölündüğünü probleme uygun seçmek adil değerlendirme için önemlidir.

## Kaynaklar

- [Google Machine Learning Crash Course: Training and test sets](https://developers.google.com/machine-learning/crash-course/training-and-test-sets)
- [scikit-learn resmî belgesi: `train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)
