# Faz 0 – Ders 6: Yapay zekâ nedir?

> ⏱️ Tahmini süre: 45-60 dk · 📚 Ön koşul: değişkenler, sözlükler ve fonksiyonlar · 💻 Gereksinim: Python 3.11+

## Bu derste ne öğreneceksin?

- Yapay zekâyı tek bir sihirli algoritma olarak değil, belirli görevleri yerine getiren sistemler olarak tanımlamayı
- Bir sistemde bilgi, bellek, çıkarım, öğrenme ve açıklama parçalarının nasıl ayrıldığını
- Bir yapay zekâ iddiasını algoritma sonuçlarından öte somut ölçütlerle sorgulamayı
- Roger C. Schank'ın 1987 tarihli *What Is AI, Anyway?* makalesinin günümüz mühendisliği açısından temel sorularını

## 1. Problem

“Yapay zekâ” ifadesi; satranç oynayan bir programa, konuşan bir modele, fotoğraf sınıflandırıcısına ve bir ajansın yayımladığı metinlere aynı başlık altında uygulanabiliyor. Bu durumda hangi sistemin yapay zekâ sayıldığına ilişkin açık bir sınır gerekir.

Bu ders için kullanacağımız tanım şudur:

!!! quote "Dersin tanımı"
    Bir yapay zekâ sistemi, belirsiz veya daha önce karşılaşılmamış durumlar için bilgi üretmek üzere girdiyi işler, geçmişten aldığı bilgisini temsil eder ve ürettiği sonuca göre bir karar veya açıklama verir.

Bu tanım tek başına yeterli değildir. Sistemin şu sorulara cevap verebilmesi gerekir:

1. Bilgi nasıl temsil ediliyor?
2. Geçmiş gözlem nerede saklanıyor?
3. Yeni bir durum eski bilgiyle nasıl ilişkilendiriliyor?
4. Sistem deneyimden nasıl öğreniyor?
5. Bir kararın neden verildiği nasıl açıklanıyor?

Bu sorular, 1987'de yazılmış bir makale için geçerli olmanın ötesinde; bugün kurduğumuz dil modeli uygulamaları ve agent sistemleri için de geçerlidir.

## 2. Yapay zekânın beş yapı taşı

Bir yapay zekâ sistemi tek bir fonksiyondan daha fazlasıdır. Aşağıdaki beş yapı, sistemi incelememizi kolaylaştırır.

| Yapı taşı | Sorduğu soru | Basit örnek |
|---|---|---|
| **Temsil** | Bilgi programa hangi biçimde aktarılıyor? | Bir hava durumu kaydı sözlükte tutulur |
| **Bellek** | Geçmiş bilgi nerede saklanıyor? | Önceki gözlem kayıtları listede tutulur |
| **Çıkarım** | Yeni veri mevcut bilgiyle nasıl ilişkilendiriliyor? | Yağmur kuralı yeni hava gözlemine uygulanır |
| **Öğrenme** | Sistem yeni deneyimden ne değiştiriyor? | Yeni örnekten çıkarılan kural belleğe eklenir |
| **Açıklama** | Neden bu sonuca ulaşıldı? | Kullanılan kural ve gözlem kullanıcıya gösterilir |

Bir sistem bu parçaların tamamını barındırmak zorunda değildir. Ancak her parçanın varlığını veya eksikliğini bilmek, sistemi doğru değerlendirmemizi sağlar.

## 3. Temsil: problemi bilgisayarın anlayacağı biçimde tanımlamak

Bir yapay zekâ sistemine gerçek dünyanın tüm ayrıntısını vermek mümkün değildir. Görev için gereken bilgi seçilir ve tutarlı bir biçimde saklanır.

Örneğin bir öneri sistemi yalnızca iki bilgi alanına odaklanabilir:

```python
gözlem = {
    "hava": "yağmurlu",
    "plan": "bahçede fidan dikmek",
}
```

Bu kayıt, hava, zaman, zemin sıcaklığı veya rüzgâr gibi başka ayrıntıları taşımaz. Ama verdiğimiz örnek için önemli olan iki bilgiyi açık tutar:

- mevcut hava durumu;
- kullanıcının gerçekleştirmek istediği plan.

İyi temsil, gereksiz ayrıntıyı silmekten daha fazlasını yapar. Karar vermek için gerekli ilişkileri kaybetmeden sadeleştirme yapar.

## 4. Bellek: gözlem ve kuralları saklamak

Bellek, sistemin önceki çalışmalardan aldığı bilgiyi sonraki kararlara taşıyan yapıdır.

Bu dersin örneğinde bellek iki katmandan oluşur:

```python
self.bellek = []                 # Geçmiş gözlem kayıtları
self.kurallar = {}               # Anahtar ve açıklama çiftleri
```

Yeni bir gözlem geldiğinde önce kaydedilir:

```python
gözlem = Gözlem(özellikler)
self.bellek.append(gözlem)
```

Bu yapı kalıcı bir veri tabanı değildir. Ama bir sistemin belleği olmadığında geçmişi hatırlayamayacağını göstermek için yeterlidir.

Belleği olan bir sistemin iki temel davranışı vardır:

- daha önce gördüğü kayıtları geri çağırabilir;
- yeni durumlarla bu kayıtları ilişkilendirebilir.

Gerçek uygulamalarda belleği bir veri tabanı, dosya, sohbet geçmişi veya belgeleme arama sistemi olarak kurabiliriz. Temel fikir değişmez: sistemin geçmiş bilgiyi saklayabilmesi gerekir.

## 5. Çıkarım: kuralı yeni duruma uygulamak

Çıkarım, temsil edilmiş bir durumu mevcut kurallarla karşılaştırma işlemidir.

```python
for anahtar, (beklenen, açıklama) in self.kurallar.items():
    if gözlem.özellikler.get(anahtar) == beklenen:
        return anahtar, açıklama

return "belirsiz", "Hiçbir tanımlı kural bu gözlemle eşleşmedi."
```

Bu örnekte hava `"yağmurlu"` olduğunda sistem, kayıtlı açıklamayı döndürebilir. Bu karar gerçek dünyada kesin bir sonuç sunmak için değil, kural tabanlı çıkarımın mekanizmasını göstermek için kullanılır.

!!! warning "Çıkarım ile gerçeklik aynı şey değildir"
    Bir kuralın sonuç vermesi, önerinin doğrulanmış olduğu anlamına gelmez. Örneğin `"yağmurlu"` olunca şemsiye öneren bir sistem güvenli karar verme garantisi vermez; onu yalnızca kendi kuralına göre açıklar.

## 6. Kendin yaz

Kodun tamamı [`kod/yapay_zeka_durumu.py`](kod/yapay_zeka_durumu.py) dosyasındadır.

Kod, aşağıdaki görevleri sırayla gerçekleştirir:

1. Bir gözlem nesnesi oluşturur.
2. Gözlemi belleğe ekler.
3. Kural eşleşmesi arar.
4. Bulunan anahtarı ve açıklamayı ekrana yazdırır.

Çalıştır:

```bash
python kod/yapay_zeka_durumu.py
```

Beklenen sonuç:

```text
hava: Islak zeminde kayma riski artabilir.
plan: Bu görev için yağmuru beklemek daha güvenli olabilir.
Bellek özeti: {'hava': 2, 'plan': 2}
```

Bu örnek bir sohbet sistemi değildir. Ama yapay zekâ sistemlerinde aradığımız parçaları açık biçimde gösterir: veri temsil edilir, gözlem saklanır, çıkarım yapılır ve kararın nedeni açıklanır.

## 7. Öğrenme: sabit kuraldan deneyimle değişen sisteme

Bu örnekte kurallar doğrudan programa yazılmıştır. Bu, öğrenme değil, programlama anlamına gelir.

Bir sistemin öğrenmesi için en azından yeni örneklerden gelen bilgiyi kullanarak gelecekteki davranışı değiştirmesi gerekir. Örneğin:

- yanlış bir tahmin için beklenen sonuç düzeltilir;
- benzer hatalar tekrar etmesin diye kural güncellenir;
- modelin ağırlıkları yeni veriyle değişir;
- arama sistemi yeni belgeleri belleğe ekler.

!!! note "Öğrenme örneği"
    Bir telefon öneri sistemini ele alalım. Kullanıcıların dönüşüm verilerini toplayan sistem, daha iyi tahmin yapmak için satış örüntülerini kullanır. Bu sistemin modeli verilerden öğrenir. Ama telefon hakkında sahip olduğu bilgiler zamanla değişebilir.

Öğrenmenin gerçekleştiğini yalnızca kodun bir sözlüğe yeni veri eklemesinden anlamıyoruz. Ayrıca sistemin gelecekteki çıktısının deneyimden sonra gerçekten değişmesini ölçmemiz gerekiyor.

## 8. Açıklama ve güven

Bir sistem açıklama üretebilir ama bu açıklama mutlaka doğru değildir.

Güvenli bir değerlendirmede beş soru sorulur:

1. Sistem hangi kaynağa dayanıyor?
2. Cevabı hangi bilgilerden türetildi?
3. Bilgiler güncel mi?
4. Kesinlik ile olasılık arasında fark gösteriliyor mu?
5. Hata oluştuğunda kullanıcıya ne anlatılıyor?

Dil modelleri metin üretebilir ve sürece benzeyen açıklamalar yazabilir. Ancak üretilen metinleri doğru, güvenli veya kaynağa dayalı kabul etmek için ayrıca doğrulama gerekir.

## 9. 1987'den günümüze

Roger C. Schank'ın makalesi yapay zekânın sınırlarını tek bir programlama dili üzerinden tanımlamaya çalışmaz. Makalenin soruları şunlardır:

- Bir sistem dünyayı nasıl temsil ediyor?
- Hafızaya sahip olup bilgilerini düzenli tutabiliyor mı?
- Yeni durumları eski bilgilerle ilişkilendiriyor mı?
- Deneyimden genelleme çıkarabiliyor mı?
- Sonucunu açıklayıp kendini sınayabiliyor mu?

Bu soruların yazıldığı 1987 yılıyla bugün arasında teknoloji değişmiştir. Ancak iyi mühendislik soruları değişmemiştir. Modern bir dil modeli çağrısı, bir RAG hattı veya bir agent döngüsü de aynı temel parçalarla değerlendirilmelidir.

## 10. Kütüphanelerle bağlantı

Bu dersin örneğinde kütüphane kullanılmıyor. Ama gerçek bir uygulamada aşağıdaki araçları benzer parçalara bağlayabiliriz:

- veri sınıfları: `dataclass`, `pydantic`
- bellek: dosya, veri tabanı veya sohbet geçmişi
- arama: embedding modelleri ve vektör veritabanı
- çıkarım: makine öğrenmesi modelleri
- açıklama: yapılandırılmış çıktı ve kaynak kayıtları
- test: `unittest`, `pytest` ve örnek veri setleri

Amaç kütüphanenin adını ezberlemek değildir. Amaç, kütüphane kullanıldığında hangi temel parçanın çözüldüğünü görmek ve hatayı hangi katmanda arayacağını bilmektir.

## 11. Pekiştir

**Quiz**

1. Temsil ile bellek arasındaki fark nedir?
2. Bir kurala dayalı çıkarım ile deneyimden öğrenme arasındaki temel fark nedir?
3. Bir açıklamanın doğru olduğuna nasıl emin olursunuz?
4. Belleği olan fakat çıkarım yapamayan bir sistemin hangi sınırı vardır?
5. Bir dil modelinin başarılı görünmesinden daha güçlü kanıtlar hangileridir?

**Alıştırmalar**

1. Sisteme `"ses": ("yüksek", "Kulaklık sesini azaltmayı öner")` kuralını ekleyin.
2. Hiçbir kuralla eşleşmeyen bir gözlem oluşturun.
3. Üç gözlemden oluşan bir senaryo yazın ve bellek özetini inceleyin.
4. Sistemin yanlış veya eksik karar verebileceği bir durum bulun.
5. Bu örnekte hangi bölümler temsil, bellek, çıkarım ve öğrenme olarak ayrılabilir?

## 12. Özet

Yapay zekâyı tek bir araç olarak tanımlamak yerine, bilgi temsilini, belleği, çıkarımı, öğrenmeyi ve açıklamayı ayrı parçalar olarak incelemek daha işlevseldir. Bu bölüm, 1987'deki temel soruların güncel sistemlere nasıl taşındığını gösterir. Sonraki derslerde bu kavramları matematik, veri, model eğitimi ve araç kullanımına bağlı olarak daha somut biçimde ele alacağız.

## Kaynaklar

- Roger C. Schank, “What Is AI, Anyway?”, *AI Magazine*, 1987, cilt 8, sayı 4, DOI: `10.1609/aimag.v8i4.623`
- [AAAI AI Magazine makale sayfası](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/623)
- Python resmî belgesi: veri sınıfları, sözlükler ve tip işaretleri
