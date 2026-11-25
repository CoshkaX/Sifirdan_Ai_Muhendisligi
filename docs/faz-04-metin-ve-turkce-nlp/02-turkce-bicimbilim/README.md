# Faz 4 – Ders 2: Türkçe sözcüklerin içini açmak

> ⏱️ Tahmini süre: 45-60 dk · 📚 Ön koşul: 4.1 Metni sayılara dönüştürmek · 💻 Gereksinim: Python 3.11+, ek paket yok

## Bu derste ne öğreneceksin?

- Kök, ek ve biçimbilim kavramlarını
- Türkçede sözcüklerin eklerle nasıl yeni anlamlar ve görevler kazandığını
- Büyük ünlü uyumunun `-ler` / `-lar` ekini nasıl etkilediğini
- Ekleri sondan eşleştiren küçük bir Python örneğinin neyi yapıp neyi yapamadığını

## 1. Problem

`evlerimizden` sözcüğünü düşün. Bir tokenizer bunu tek parça olarak saklayabilir; ama sözcüğün içinde bir kök ve birkaç ek vardır:

```text
ev + ler + imiz + den
```

Burada `ev` temel anlamı taşır. `-ler` çoğul, `-imiz` birinci çoğul kişi iyelik, `-den` ise ayrılma anlamı katar. Ekleri tanımak, benzer sözcük biçimlerinin ortak parçalarını bulmaya yardım eder.

Bu sözcük yapısını inceleyen dilbilim alanına **biçimbilim** (morfoloji) denir. Sözcüğün en küçük anlamlı veya dilbilgisel parçalarına **biçimbirim** adı verilir. Bu derste dilin bütün kurallarını kodlamayacağız; yalnızca eklerin nasıl tekrar kullanılabildiğini göreceğiz.

## 2. Kendin yaz

### 2.1 Büyük ünlü uyumu: `-ler` mi, `-lar` mı?

Türkçedeki çoğul eki, sözcüğün son ünlüsüne göre iki biçimden birini alır. Son ünlü `a, ı, o, u` grubundaysa `-lar`; `e, i, ö, ü` grubundaysa `-ler` kullanılır.

```python {.python-playground}
def cogul_eki(kok):
    for harf in reversed(kok):
        if harf in "aıou":
            return "lar"
        if harf in "eiöü":
            return "ler"
    raise ValueError("Sözcükte Türkçe ünlü bulunamadı.")


for kok in ["kitap", "ev", "okul", "gül"]:
    ek = cogul_eki(kok)
    print(f"{kok} + {ek} -> {kok + ek}")
```
```text {.python-playground-expected}
kitap + lar -> kitaplar
ev + ler -> evler
okul + lar -> okullar
gül + ler -> güller
```
```text {.python-playground-help}
`def cogul_eki(kok):` | `def` bir işlev başlatır. Parantezdeki `kok`, birazdan vereceğimiz sözcüğü tutacak; işlev sonunda `lar` veya `ler` dönecek.
`for harf in reversed(kok):` | `reversed` sözcüğün harflerini sondan başa verir. `ev` için önce `v`, sonra `e` incelenir; böylece son ünlüyü bulabiliriz.
`if harf in "aıou":` | `in`, harfin tırnak içindeki ünlü grubunda olup olmadığını sorar. Örneğin `kitap` sözcüğünde sondan ilk bulunan ünlü `a` olduğu için bu koşul doğru olur.
`return "lar"` | Koşul doğruysa bu satır işlevi bitirir ve `"lar"` değerini çağrıldığı yere gönderir. Sonraki satırlar aynı sözcük için çalışmaz.
`if harf in "eiöü":` | İlk grup eşleşmezse bu grup denenir. `ev` sözcüğündeki son ünlü `e` bu grupta bulunduğu için `"ler"` seçilir.
`return "ler"` | İkinci koşul doğru olduğunda işlev bu eki geri verir; çağıran kod sonucu `ek` değişkenine koyar.
`raise ValueError("Sözcükte Türkçe ünlü bulunamadı.")` | Bu satıra gelindiyse sözcükte `a, ı, o, u, e, i, ö, ü` harflerinden hiçbiri bulunmamıştır; işlev bu yüzden `-lar` mı `-ler` mi seçeceğini bilemez. `ValueError`, verilen değerin bu işlevin kurallarına uymadığını söyleyen hatadır. `raise` çalışmayı burada durdurup bu açıklamayı gösterir.
`for kok in ["kitap", "ev", "okul", "gül"]:` | Döngü listedeki sözcükleri birer birer `kok` değişkenine koyar ve altındaki iki satırı her sözcük için çalıştırır.
`ek = cogul_eki(kok)` | O anki sözcüğü işlevimize veririz; dönen `"lar"` veya `"ler"` değeri `ek` değişkeninde saklanır.
`print(f"{kok} + {ek} -> {kok + ek}")` | `f` metni değişken değerlerini gösterir; `kok + ek` sözcükle eki birleştirip sonucu ekrana yazar.
```

`reversed(kok)` harfleri sondan başa doğru dolaşır. İlk bulduğumuz ünlü, ekin biçimini seçmek için gereken son ünlüdür. Kodu değiştirip `kalem`, `bulut` veya `çiçek` sözcüklerini de dene.

Bu yalnızca çoğul ekinin iki biçimini seçen küçük bir örnektir. Türkçedeki bütün ekler bu tek kurala uymaz; ayrıca istisnalar ve ses değişimleri de vardır.

### 2.2 Sözcüğü eklerine ayırmak

Aşağıdaki örnek, bilinen ekleri sözcüğün sonundan arar. Bir ek bulduğunda onu ayırır ve kalan parçayı yeniden inceler:

```python {.python-playground}
EKLER = ("ler", "lar", "imiz", "ımız", "den", "dan")


def eklerine_ayir(sozcuk):
    kalan = sozcuk
    bulunan_ekler = []

    while True:
        for ek in sorted(EKLER, key=len, reverse=True):
            kok_uzunlugu = len(kalan) - len(ek)
            if kalan.endswith(ek) and kok_uzunlugu >= 2:
                kalan = kalan[:-len(ek)]
                bulunan_ekler.insert(0, ek)
                break
        else:
            return [kalan] + bulunan_ekler


for sozcuk in ["evlerimizden", "kitaplarımızdan"]:
    print(f"{sozcuk} -> {eklerine_ayir(sozcuk)}")
```
```text {.python-playground-expected}
evlerimizden -> ['ev', 'ler', 'imiz', 'den']
kitaplarımızdan -> ['kitap', 'lar', 'ımız', 'dan']
```
```text {.python-playground-help}
`EKLER = ("ler", "lar", "imiz", "ımız", "den", "dan")` | Parantez içindeki bu grup, örneğin tanıyacağı ek yazımlarını saklar. Listede olmayan bir eki bu basit program bulamaz.
`kalan = sozcuk` | Başta henüz hiçbir eki ayırmadığımız için kalan bölüm, sözcüğün tamamıdır.
`bulunan_ekler = []` | Boş bir liste açarız; sözcüğün sonundan bulduğumuz ekleri burada biriktireceğiz.
`while True:` | Bu döngü ek buldukça başa döner. Ek kalmadığında aşağıdaki `return` ile sonuç verip durur.
`for ek in sorted(EKLER, key=len, reverse=True):` | Ekleri uzun olandan kısa olana sırayla deneriz. Böylece uzun bir eki, onun içindeki kısa bir ek sanmayız.
`kok_uzunlugu = len(kalan) - len(ek)` | Sözcüğün ve denenmekte olan ekin harf sayılarını çıkarırız. Sonuç, eki çıkarırsak kökte kaç harf kalacağını söyler.
`if kalan.endswith(ek) and kok_uzunlugu >= 2:` | Önce sözcüğün bu ekle bitmesini, ayrıca kökte en az iki harf kalmasını isteriz. `and` iki koşulun da doğru olması gerektiği anlamına gelir.
`kalan = kalan[:-len(ek)]` | Ekin uzunluğu kadar harfi sondan siler. `evlerimizden` içinden `den` çıkınca `evlerimiz` kalır.
`bulunan_ekler.insert(0, ek)` | Eki listenin başına koyarız; çünkü ekleri sözcüğün sonundan buluyoruz ve sonuçta köke yakın olan ek önce gelmeli.
`break` | Bu turda bir ek bulduğumuz için aramayı durdurur. `while` döngüsü, kısalmış `kalan` sözcükte yeniden ek arar.
`else:` | Bu bölüm ancak `for` döngüsü hiçbir ek bulamadan biterse çalışır; yani artık ayıracak ek kalmamıştır.
`return [kalan] + bulunan_ekler` | Kalan bölümü kök kabul eder ve ek listesiyle birleştirip geri verir. Böylece parçalar kökten sona doğru sıralanır.
`print(f"{sozcuk} -> {eklerine_ayir(sozcuk)}")` | Her örnek sözcüğü işlevimize verir ve dönen parça listesini ekrana yazar.
```

Ekleri baştan sona değil, sondan başa buluyoruz: `evlerimizden` önce `den`, sonra `imiz`, ardından `ler` olarak ayrılıyor. Sonuçta bulduğumuz ekleri `insert(0, ek)` ile kökün önüne yerleştiriyoruz.

!!! warning "Bu bir dilbilim çözümleyicisi değil"
    Kod, listedeki yazımları sözcüğün sonundan eşleştirir. Sözcüğün gerçekten o köke ait olup olmadığını, eklerin o sırada kullanılabilir olup olmadığını veya ses değişimlerini denetlemez. Örneğin listedeki bir ek rastlantıyla başka bir sözcüğün sonunda geçerse yanlış bölme yapabilir. Bu örneği gerçek metni çözümlemek için değil, ek eşleştirme fikrini görmek için kullan.

## 3. Kütüphaneyle yap

Gerçek bir Türkçe biçimbilim çözümleyicisi yalnızca sondaki harflere bakmaz. Olası kökleri ve ek dizilerini sözlükle karşılaştırır; ses değişimlerini ve dilbilgisel kuralları hesaba katar. Aynı sözcüğün birden fazla çözümlemesi de olabileceği için bağlam önem kazanabilir.

Zemberek gibi Türkçe doğal dil işleme araçları, kök bulma ve biçimbilim çözümleme gibi daha kapsamlı işler yapar. Buradaki örnek, bu araçların yerine geçmez; yalnızca bir ekin nasıl tanınabileceğini gösterir. Gerçek uygulamada bir kütüphane seçerken desteklenen dil sürümünü, lisansını ve çözümleme başarısını kendi verin üzerinde kontrol et.

## 4. Sık yapılan hatalar

- **Ekleri kökle karıştırmak.** `evlerimizden` tek bir kökten oluşmaz; ekler sözcüğün sayısını, sahipliğini ve cümledeki görevini değiştirir.
- **Her ekin tek biçimi olduğunu sanmak.** Büyük ünlü uyumu nedeniyle çoğul eki `-ler` veya `-lar` olabilir.
- **Sondan eşleştirmeyi gerçek çözümleme sanmak.** Bir harf dizisinin sözcük sonunda bulunması, onun her zaman ek olduğu anlamına gelmez.
- **Kökü her zaman sözlükteki yalın biçimle aynı kabul etmek.** Bazı ekler sözcüğün seslerini değiştirebilir; bu derste o durumları işlemiyoruz.

## 5. Pekiştir

**Quiz**

1. `evlerimizden` sözcüğünde kök ve ekler nelerdir?
2. `kitap` sözcüğüne neden `-lar`, `ev` sözcüğüne neden `-ler` gelir?
3. Örnekteki `sorted(..., key=len, reverse=True)` ne sağlar?
4. Sondan ek eşleştiren örnek hangi durumda yanlış sonuç verebilir?

**Alıştırmalar**

1. İlk çalışma alanına `araba`, `gözlük` ve `çocuk` sözcüklerini ekle. Seçilen çoğul ekini kontrol et.
2. İkinci çalışma alanındaki ek listesine `"de"` ve `"da"` ekle. `evlerimizde` ve `okullarda` sözcüklerini dene.
3. `"beden"` sözcüğünü ikinci çalışma alanında dene. Programın bulduğu parçanın neden gerçek bir çözümleme garantisi vermediğini açıkla.
4. (Zor) `cogul_eki` fonksiyonunu büyük harfli sözcüklerde de çalışacak şekilde genişlet. Türkçe `I/İ` harflerini düşün ve önceki derste öğrendiğin küçük harfe çevirme yöntemini uygula.

??? success "Quiz cevapları"
    1. `ev` kök; `-ler`, `-imiz` ve `-den` ektir.
    2. `kitap` sözcüğünün son ünlüsü `a`, `ev` sözcüğünün son ünlüsü `e` olduğu için büyük ünlü uyumuna göre ek biçimi seçilir.
    3. Ekleri uzunluklarına göre uzun olandan kısa olana sıralar. Bu, daha uzun bir ek eşleşirken onun daha kısa bir parçasının önce seçilmesini önlemeye yardımcı olur.
    4. Bir ek yazımı başka bir sözcüğün sonunda tesadüfen bulunabilir; örnek, sözlük ve dilbilgisi denetimi yapmadığı için onu yanlışlıkla ayırabilir.

## Özet

Türkçede ekler, köklere eklenerek yeni sözcük biçimleri ve dilbilgisel görevler oluşturur. Büyük ünlü uyumu `-ler` ve `-lar` gibi ek biçimlerini seçmeye yardım eder. Sondan eşleştirme fikri basit bir örneği anlamak için yararlıdır; ancak güvenilir biçimbilim çözümlemesi sözlük, ses kuralları ve bağlam gerektirir.

## Kaynaklar

- Türk Dil Kurumu, *Türkçe Dil Bilgisi* ve ses bilgisi kaynakları: [tdk.gov.tr](https://www.tdk.gov.tr/)
- Zemberek-NLP, Türkçe doğal dil işleme araçları: [github.com/ahmetaa/zemberek-nlp](https://github.com/ahmetaa/zemberek-nlp)
- Python resmî belgesi: `str.endswith`, `sorted` ve `reversed`
