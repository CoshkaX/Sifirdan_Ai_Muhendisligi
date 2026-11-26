# Faz 0 – Ders 6: Yapay zekâ nedir?

> ⏱️ Tahmini süre: 45-60 dk · 📚 Ön koşul: değişkenler, sözlükler ve fonksiyonlar · 💻 Gereksinim: Python 3.11+

## Bu derste ne öğreneceksin?

- Yapay zekâ sistemlerinin hangi işleri yaptığını örneklerle tanımayı
- Bilginin nasıl saklandığını, kuralların nasıl uygulandığını ve öğrenmenin ne anlama geldiğini ayırt etmeyi
- Bir sistemin başarılı olduğunu nasıl kontrol edebileceğimizi görmeyi

## 1. Problem

Bir program veri alır, işlem yapar ve sonuç üretir. Örneğin hava durumuna göre şemsiye öneren program, yazdığımız bir kurala uyabilir. Fotoğrafları sınıflandıran başka bir program ise çok sayıda örnekten öğrendiği örüntülerden yararlanabilir.

Yapay zekânın sınırları konusunda herkesin kullandığı tek bir tanım yoktur. Bu derste **yapay zekâ sistemi** derken, sınıflandırma, tahmin ya da metin üretme gibi belirli bir işi veri veya kurallardan yararlanarak yapan sistemleri pratik bir örnek olarak ele alıyoruz. Bir sistemin yalnızca `if` kuralı kullanması, onun öğrendiği anlamına gelmez; öğrenme ile kural uygulama arasındaki farkı ayrıca inceleyeceğiz. Bu sistemlerin hiçbiri yalnızca adına bakarak başarılı sayılmaz; başarısını yaptığı işi ne kadar doğru yerine getirdiğini ölçerek kontrol ederiz.

!!! quote "Dersin tanımı"
    Bir yapay zekâ sistemi, verilen bilgileri işleyerek bir görev için tahmin, sınıflandırma veya içerik üretme gibi sonuçlar veren yazılımdır.

Bir sistemi anlamak için şu basit soruları sorabiliriz. Her sistemin bu parçaların tümüne sahip olması gerekmez:

1. Sisteme hangi bilgiler veriliyor?
2. Önceki bilgiler saklanıyor mu?
3. Sistem elindeki bilgiyle nasıl karar veriyor?
4. Yeni örnekler sistemin sonraki sonuçlarını değiştiriyor mu?
5. Sonucun nedenini kontrol edebiliyor muyuz?

Bu sorular basit kurallarla çalışan programlar için de günümüzün büyük modelleri için de sorulabilir.

## 2. Bir sistemin beş parçası

Yukarıdaki beş soru, bir sistemin beş parçasına karşılık gelir:

| Parça | Basitçe ne anlama gelir? | Örnek |
|---|---|---|
| **Temsil** | Bilgiyi programın kullanabileceği biçimde yazmak | Hava durumunu `"yağmurlu"` metni olarak saklamak |
| **Bellek** | Bilgiyi daha sonra kullanmak için saklamak | Önceki hava gözlemlerini bir listede tutmak |
| **Çıkarım** | Bilgiye veya kurala bakıp sonuç çıkarmak | Yağmur varsa şemsiye önermek |
| **Öğrenme** | Örneklerden yararlanıp sonraki sonuçları değiştirmek | Eski örnekleri kullanarak yeni bir tahmini iyileştirmek |
| **Açıklama** | Sonucun hangi bilgiye dayandığını göstermek | “Yağmur var, bu yüzden şemsiye önerdim” demek |

Bir sistem bu parçaların tamamını barındırmak zorunda değildir. Ancak her parçanın varlığını veya eksikliğini bilmek, sistemi doğru değerlendirmemizi sağlar.

## 3. Temsil: bilgiyi programın kullanacağı biçimde saklamak

Bir programa dünyanın bütün ayrıntılarını veremeyiz. Yaptırmak istediğimiz işe yarayan bilgileri seçip düzenli biçimde saklarız. Bu işlem, bilgiyi program için **temsil etmek** demektir.

Örneğin bir öneri sistemi yalnızca iki bilgi alanına odaklanabilir:

```python {.python-playground}
gözlem = {
    "hava": "yağmurlu",
    "plan": "bahçede fidan dikmek",
}

print(f"Hava: {gözlem['hava']}")
print(f"Plan: {gözlem['plan']}")
```
```text {.python-playground-expected}
Hava: yağmurlu
Plan: bahçede fidan dikmek
```
```text {.python-playground-help}
`gözlem = {` | Süslü ayraçlar bir sözlük başlatır. Sözlükte her anahtarın yanında ona ait bir değer bulunur.
`"hava": "yağmurlu"` | `"hava"` anahtarı mevcut hava bilgisini, `"yağmurlu"` ise bu bilginin değerini tutar.
`"plan": "bahçede fidan dikmek"` | İkinci anahtar planı saklar. Yeni bir alan eklemek için bu satıra benzer bir anahtar-değer çifti yazabilirsin.
`}` | Süslü ayraçla sözlüğü kapatırız; iki bilgi artık `gözlem` değişkenindedir.
`print(f"Hava: {gözlem['hava']}")` | `gözlem['hava']` sözlükten hava değerini alır; `print` bunu açıklama metniyle birlikte gösterir.
`print(f"Plan: {gözlem['plan']}")` | Aynı yöntemle plan değerini alıp ekrana yazar. Sözlükteki `"plan"` değerini değiştirerek sonucu dene.
```

Bu kayıt; saat, sıcaklık veya rüzgâr gibi başka ayrıntıları taşımaz. Ama verdiğimiz örnek için önemli olan iki bilgiyi açık tutar:

- mevcut hava durumu;
- kullanıcının gerçekleştirmek istediği plan.

Bu örnekte yalnızca hava ve plan bilgileri var; kişinin yaşı veya bulunduğu şehir gibi bilgiler yok. Çünkü örneğin kuralı için şimdilik bu iki alan yeterli. Başka bir görevde gereken bilgiler farklı olabilir.

## 4. Bellek: bilgiyi daha sonra kullanmak için saklamak

Bellek, programın daha sonra kullanmak üzere sakladığı bilgidir. Aşağıdaki kısa örnekte bir gözlemi listeye ekliyoruz:

```python {.python-playground}
bellek = []
gözlem = {"hava": "yağmurlu", "plan": "fidan dikmek"}
bellek.append(gözlem)

print("Saklanan kayıt sayısı:", len(bellek))
print("İlk kayıttaki hava:", bellek[0]["hava"])
```
```text {.python-playground-expected}
Saklanan kayıt sayısı: 1
İlk kayıttaki hava: yağmurlu
```
```text {.python-playground-help}
`bellek = []` | Boş bir liste oluştururuz. Bu örnekte önceki gözlemleri bu listede tutacağız.
`gözlem = {"hava": "yağmurlu", "plan": "fidan dikmek"}` | Bir sözlükte iki bilgiyi saklarız: hava durumu ve kişinin planı. Her bilginin adı ve değeri birlikte bulunur.
`bellek.append(gözlem)` | `append` gözlemi listenin sonuna ekler. Böylece program bu çalışması sırasında kaydı bellekte tutar.
`print("Saklanan kayıt sayısı:", len(bellek))` | `len` listedeki kayıtların sayısını bulur; az önce bir gözlem eklediğimiz için ekranda `1` görürüz.
`print("İlk kayıttaki hava:", bellek[0]["hava"])` | Listelerde ilk kayıt `0` konumundadır. Bu kaydın içindeki `"hava"` bilgisini seçip ekrana yazarız.
```

Bu liste yalnızca program çalışırken bellekte kalır. Program kapanınca bu örnekteki kayıt da kaybolur. Bilgiyi sonraki çalıştırmada da saklamak istersek dosya veya veri tabanı gibi kalıcı bir yere yazmamız gerekir.

## 5. Çıkarım: kuralı yeni duruma uygulamak

**Çıkarım**, verilen bilgiyi bir kuralla karşılaştırıp sonuç üretmektir. Aşağıdaki programda kuralı biz açıkça yazıyoruz:

```python {.python-playground}
hava = "yağmurlu"

if hava == "yağmurlu":
    karar = "Şemsiye al."
else:
    karar = "Bu hava için kayıtlı bir önerim yok."

print("Gözlem:", hava)
print("Karar:", karar)
```
```text {.python-playground-expected}
Gözlem: yağmurlu
Karar: Şemsiye al.
```
```text {.python-playground-help}
`hava = "yağmurlu"` | O anki hava bilgisini `hava` değişkenine kaydederiz. `"güneşli"` yazarak da deneyebilirsin.
`if hava == "yağmurlu":` | `if`, bir koşulu kontrol eder. `==` iki değerin aynı olup olmadığını sorar; `=` ise değer atamak için kullanılır.
`karar = "Şemsiye al."` | Koşul doğruysa bu öneriyi `karar` değişkenine kaydederiz. Girintili satır, `if` koşulu doğru olduğunda çalışır.
`else:` | Önceki koşul yanlışsa çalışacak bölümü başlatır.
`karar = "Bu hava için kayıtlı bir önerim yok."` | Hava yağmurlu değilse bu kez bu metni karar olarak saklarız.
`print("Gözlem:", hava)` | Sisteme verdiğimiz hava bilgisini gösterir.
`print("Karar:", karar)` | Kuralın seçtiği sonucu ekrana yazar. Bu örnek yalnızca yazdığımız açık kuralı uygular.
```

`hava` değerini `"güneşli"` yapıp tekrar çalıştır. Sonuç değişir; çünkü program iki durumu karşılaştırır. Program yağmurun ne olduğunu anlamaz, yalnızca yazdığımız koşulu uygular.

!!! warning "Çıkarım ile gerçeklik aynı şey değildir"
    Bir kuralın sonuç vermesi, önerinin doğrulanmış olduğu anlamına gelmez. Örneğin `"yağmurlu"` olunca şemsiye öneren bir sistem güvenli karar verme garantisi vermez; onu yalnızca kendi kuralına göre açıklar.

## 6. Kendin yaz

Kodun tamamı [`kod/yapay_zeka_durumu.py`](kod/yapay_zeka_durumu.py) dosyasındadır. Dosyada sınıf kullanımı gibi daha önce öğrendiğin Python konuları bulunur; aşağıdaki küçük pencere ise aynı kural fikrini daha kısa biçimde gösterir.

Önce bu küçük kural örneğini pencerede çalıştır. Gözlemdeki hava durumunu değiştirerek hangi önerinin seçildiğini gör:

```python {.python-playground}
kurallar = {
    "yağmurlu": "Şemsiye al.",
    "güneşli": "Güneş kremi al.",
}

gözlem = "yağmurlu"
öneri = kurallar.get(gözlem, "Bu durum için bir kuralım yok.")
print(f"{gözlem}: {öneri}")
```
```text {.python-playground-expected}
yağmurlu: Şemsiye al.
```
```text {.python-playground-help}
`kurallar = {` | Bu satır süslü ayraçlarla bir sözlük başlatır. Sözlükte bir anahtarın yanında ona ait değer bulunur.
`"yağmurlu": "Şemsiye al."` | Sol taraftaki `"yağmurlu"` aranacak hava durumudur; sağ taraftaki `"Şemsiye al."` o durum için saklanan öneridir.
`"güneşli": "Güneş kremi al."` | İkinci kuralı ekleriz. Gözlem `"güneşli"` olduğunda program bu öneriyi bulabilir.
`}` | Süslü ayraçla kural sözlüğünü kapatırız; artık iki hava durumu için öneri vardır.
`gözlem = "yağmurlu"` | Sisteme gelen mevcut durumu `gözlem` değişkenine kaydederiz. Buradaki değer, sözlükte arayacağımız anahtarla aynı olmalı.
`öneri = kurallar.get(gözlem, "Bu durum için bir kuralım yok.")` | `.get(...)` sözlükte `gözlem` değerini arar; bulursa öneriyi, bulamazsa ikinci metni verir. Bulunan metni `öneri` değişkenine kaydederiz.
`print(f"{gözlem}: {öneri}")` | `f` metnindeki süslü parantezler değişkenlerin değerlerini yerleştirir. `print` oluşan cümleyi ekrana yazar.
```

Şimdi yeni bir kural ekle ve `gözlem` değerini değiştir. Kod penceresi tarayıcıda çalışır; bilgisayarındaki ders dosyasını değiştirmez.

Kod, aşağıdaki görevleri sırayla gerçekleştirir:

1. Bir gözlem nesnesi oluşturur.
2. Gözlemi belleğe ekler.
3. Kural eşleşmesi arar.
4. Bulunan anahtarı ve açıklamayı ekrana yazdırır.

Projeyi 0.1 dersinde indirdiysen, proje klasöründeyken şu komutlarla çalıştır:

```bash
cd docs/faz-00-hazirlik/06-yapay-zeka-nedir
python kod/yapay_zeka_durumu.py
```

Beklenen sonuç:

```text
hava: Islak zeminde kayma riski artabilir.
plan: Fidanı dikmeden önce toprağın nemini kontrol et.
Bellek özeti: {'hava': 2, 'plan': 2}
```

İlk gözlemde hava yağmurlu olduğu için ilk kural eşleşir. İkinci gözlemde hava güneşli; bu kez hava kuralı eşleşmez ve sıradaki plan kuralı seçilir.

Bu örnek bir sohbet sistemi değildir. Ama yapay zekâ sistemlerinde aradığımız parçaları açık biçimde gösterir: veri temsil edilir, gözlem saklanır, çıkarım yapılır ve kararın nedeni açıklanır.

### Şimdi sen yaz: kural ekle

Kural sözcüğüne yeni bir durum ekle ve kuralı olmayan durumda ne olacağını belirle. `# TODO` yazan yerlerdeki `___` boşluklarını tamamla, sonra çalıştır.

```python {.python-playground-task}
kurallar = {
    "yağmurlu": "Şemsiye al.",
    "güneşli": "Güneş kremi al.",
    # TODO: "karlı" hava için "Bot giy." önerisini ekle.
    "___": "___",
}

for hava in ["karlı", "rüzgârlı"]:
    # TODO: Kuralı bul; kural yoksa "Kuralım yok." döndür (.get metodu).
    oneri = kurallar.___(hava, "Kuralım yok.")
    print(f"{hava}: {oneri}")
```
```text {.python-playground-expected}
karlı: Bot giy.
rüzgârlı: Kuralım yok.
```
```text {.python-playground-help}
`"___": "___",` | Tırnaklar hazır, yalnızca metinleri yaz. Sözlükte `anahtar: değer` biçiminde yazılır: anahtar hava durumu, değer öneridir.
`kurallar.___(hava, "Kuralım yok.")` | `get` anahtar varsa değerini, yoksa ikinci değeri verir.
```
```python {.python-playground-solution}
kurallar = {
    "yağmurlu": "Şemsiye al.",
    "güneşli": "Güneş kremi al.",
    # "karlı" hava için "Bot giy." önerisini ekle.
    "karlı": "Bot giy.",
}

for hava in ["karlı", "rüzgârlı"]:
    # Kuralı bul; kural yoksa "Kuralım yok." döndür (.get metodu).
    oneri = kurallar.get(hava, "Kuralım yok.")
    print(f"{hava}: {oneri}")
```

## 7. Öğrenme: örnekler sonraki sonucu değiştiriyor mu?

Yukarıdaki şemsiye örneğinde kuralı biz yazdık: hava yağmurluysa şemsiye öner. Program bu kuralı uyguluyor; **öğrenmiyor**. Yeni bir gözlemi listeye eklemek de tek başına öğrenme sayılmaz, çünkü karar kuralı değişmemiştir.

Bir sistemin öğrenmesinden söz etmek için, örneklerden gelen bilginin gelecekteki tahminlerini değiştirmesi gerekir. Örneğin sınav sonuçları ve çalışma süreleri içeren çok sayıda örneği inceleyen bir program, daha önce görmediği bir çalışma süresi için sonuç tahmini yapmayı öğrenebilir. Bu tahminin ne kadar doğru olduğunu ayrıca ölçmek gerekir.

!!! note "Öğrenme örneği"
    Bir telefon öneri sistemi, insanların hangi telefonları seçtiğine dair örneklerden yararlanabilir. Ancak yalnızca bu örnekleri saklamak yeterli değildir: yeni örneklerin sonraki önerileri gerçekten değiştirip değiştirmediğini kontrol etmeliyiz.

Bu derste gerçek bir model eğitmiyoruz. İlerleyen derslerde örneklerden öğrenmenin nasıl kurulduğunu ve başarısının nasıl ölçüldüğünü adım adım göreceğiz.

## 8. Açıklama ve güven

Bir sistem açıklama üretebilir ama bu açıklama mutlaka doğru değildir.

Sağlam bir değerlendirmede beş soru sorulur:

1. Sistem hangi kaynağa dayanıyor?
2. Cevabı hangi bilgilerden türetildi?
3. Bilgiler güncel mi?
4. Kesinlik ile olasılık arasında fark gösteriliyor mu?
5. Hata oluştuğunda kullanıcıya ne anlatılıyor?

Dil modelleri metin üretebilir ve sürece benzeyen açıklamalar yazabilir. Ancak üretilen metinleri doğru, güvenli veya kaynağa dayalı kabul etmek için ayrıca doğrulama gerekir.

## 9. 1987'den günümüze

Roger C. Schank'ın 1987 tarihli *What Is AI, Anyway?* makalesi yapay zekânın ne olduğuna ilişkin temel sorular sorar. Bugünkü sistemleri incelerken de şunları sorabiliriz:

- Bir sisteme hangi bilgiler veriliyor?
- Önceki bilgilerini saklayabiliyor mu?
- Yeni bir bilgi geldiğinde hangi kurala göre karar veriyor?
- Yeni örnekler sonraki tahminlerini değiştiriyor mu?
- Ürettiği sonucu test edip hata yaptığında gösterebiliyor mu?

Teknoloji değişse de bir sistemin ne bildiğini, nasıl karar verdiğini ve başarısını nasıl ölçtüğümüzü sormak bugün de yararlıdır. Makalenin kaynak bağlantısı konuyu daha ileri okumak isteyenler içindir; bu dersi anlamak için makaleyi önceden bilmek gerekmez.

## 10. Kütüphanelerle bağlantı

Bu derste dışarıdan bir paket kurmuyoruz; örnekleri Python'ın temel özellikleriyle yazıyoruz. Gerçek projelerde dosya ve veri tabanları bilgiyi saklamaya, makine öğrenmesi araçları örneklerden tahmin üretmeye, test araçları da sonuçların beklediğimiz gibi olup olmadığını kontrol etmeye yardım eder. Bu araçların adlarını şimdilik ezberlemene gerek yok; sonraki derslerde ihtiyaç oldukça tanıtacağız.

## 11. Pekiştir

**Quiz**

1. Temsil ile bellek arasındaki fark nedir?
2. Bir kurala dayalı çıkarım ile deneyimden öğrenme arasındaki temel fark nedir?
3. Bir açıklamanın doğru olduğundan nasıl emin olursun?
4. Belleği olan fakat çıkarım yapamayan bir sistemin hangi sınırı vardır?
5. Bir dil modelinin başarılı görünmesinden daha güçlü kanıtlar hangileridir?

**Alıştırmalar**

1. Sisteme `"ses": ("yüksek", "Kulaklık sesini azaltmayı öner")` kuralını ekle.
2. Hiçbir kuralla eşleşmeyen bir gözlem oluştur.
3. Üç gözlemden oluşan bir senaryo yaz ve bellek özetini incele.
4. Sistemin yanlış veya eksik karar verebileceği bir durum bul.
5. Bu örnekte hangi bölümler temsil, bellek, çıkarım ve öğrenme olarak ayrılabilir?

??? success "Quiz cevapları"
    1. **Temsil**, tek bir durumu veya bilgiyi programın kullanabileceği biçimde ifade eder. **Bellek** ise bu bilgiyi sonradan kullanmak üzere saklar.
    2. Kural tabanlı sistemde davranışı programcı belirler; öğrenen sistemde yeni örnekler, modelin ya da karar kuralının gelecekteki çıktısını değiştirir.
    3. Açıklamanın dayandığı veri ve kuralları inceleyip sonucu bağımsız örneklerle doğrularız. Açıklamanın akıcı olması tek başına doğruluk kanıtı değildir.
    4. Gözlemleri saklayabilir ama onlardan yeni bir sonuç çıkaramaz; belleği tek başına akıllı davranış sağlamaz.
    5. Temsil edici testlerde ölçülen başarı, hata analizi, kaynak doğrulaması ve farklı koşullarda tekrarlanabilir sonuçlar daha güçlü kanıttır.

## 12. Özet

Bir sistemi anlamak için hangi bilgiyi kullandığına, bunu saklayıp saklamadığına, nasıl karar verdiğine ve yeni örneklerden öğrenip öğrenmediğine bakarız. Yazdığımız sabit bir kuralı uygulamak tek başına öğrenme değildir. Sonraki derslerde bu fikirleri matematik, veri ve model eğitimi örnekleriyle somutlaştıracağız.

## Kaynaklar

- Roger C. Schank, “What Is AI, Anyway?”, *AI Magazine*, 1987, cilt 8, sayı 4, DOI: `10.1609/aimag.v8i4.623`
- [AAAI AI Magazine makale sayfası](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/623)
- Python resmî belgesi: veri sınıfları, sözlükler ve tip işaretleri
