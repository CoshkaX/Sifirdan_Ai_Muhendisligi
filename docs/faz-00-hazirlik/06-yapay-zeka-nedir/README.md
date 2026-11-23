# Faz 0 – Ders 6: Yapay zekâ nedir?

> ⏱️ Tahmini süre: 50-70 dk · 📚 Ön koşul: değişkenler, sözlükler ve fonksiyonlar · 💻 Gereksinim: Python 3.11+

## Bu derste ne öğreneceksin?

- Yapay zekâyı tek bir sihirli algoritma olarak değil, belli görevleri çözmek için tasarlanmış sistemler bütünü olarak
- Bilgiyi temsil etmek, bellekte tutmak, çıkarım yapmak, deneyimden öğrenmek ve kararını açıklamak
- Bir yapay zekâ iddiasını çalıştırılabilir kriterlerle sınamak
- 1987 yılında Roger C. Schank’ın *What Is AI, Anyway?* makalesindeki temel soruların günümüzde neden hâlâ önemli olduğunu

## 1. Problem

“Yapay zekâ” sözcüğü bugün farklı şeyler için kullanılıyor: satranç oynayan bir program, düğmeye basınca cevap veren bir chatbot, yönlendiğinde resim üreten bir model veya evdeki sesi izleyen bir sistem. Peki hangi özelliklere sahip olduğunda bir sistemi yapay zekâ saymalıyız?

Bu sorunun güçlü bir yanıtı tek bir dilin, tek bir yazılım kütüphanesinin veya tek bir başarı ölçütünün adı olamaz. Yapay zekâ, bir hedefe ulaşmak için **girdi alabilen, bilgiyi anlamlı biçimde saklayabilen, eski bilgiyle yeni durumu ilişkilendirebilen ve çıkardığı sonucu açıklayabilen** sistemler alanıdır.

Bu ders 1987 tarihli [Roger C. Schank’ın makalesindeki](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/623) çerçeveden ilham alır. Makalenin terimlerini aynen aktarmaz; onları günümüzün yazılım problemlerine dönüştürür.

## 2. Yapay zekâyı ayıran sorular

Makale “akıllı” bir programın yalnızca doğru cevap vermekle yetmediğini, nasıl bildiğini de göstermesi gerektiğini tartışır. Aşağıdaki beş soru bu fikri somutlaştırır.

| Soru | Programın yapması gereken |
|---|---|
| Görevi neyi temsil eder? | Girdileri ve hedefleri açık veri biçiminde tutar |
| Bilgiyi nerede saklar? | Geçmiş gözlemleri ve kuralları bellekte tutar |
| Nasıl çıkarım yapar? | Yeni durumu kayıtlı bilgiyle ilişkilendirir |
| Deneyimden nasıl öğrenir? | Yeni örnekten bir sonuç çıkarır ve gelecekte kullanır |
| Kararını nasıl açıklar? | Kullanıcıya hangi bilgi ve kuralın etkili olduğunu bildirir |

Bu soruların yalnızca büyük dil modellerine değil, satranç motoruna, tavsiye sistemine, trafik tahmin programına ve biçimden etkili şekilde yararlanan küçük bir kural sistemine de uygulanabilir.

## 3. Temsil: dünyayı programa uygun biçimde yazmak

Bir durumun tüm ayrıntısını bilgisayara aktarmak zorunda değiliz. Görev için gerekli bilgiyi seçmek gerekir.

```python
gözlem = {
    "hava": "yağmurlu",
    "plan": "bahçede fidan dikmek",
}
```

Bu sözlük doğada olan her şeyi temsil etmiyor. Ancak sorunumuza doğrudan bağlı iki özelliği gösteriyor: hava durumu ve yapılacak iş. İyi temsil, gereksiz ayrıntıyı çıkarıp karar için gerekli ilişkiyi korur.

## 4. Bellek: gözlemi saklamak

Bir sistemin sadece o an gördüğüyle karar vermesiyle, geçmişi hatırlayarak karar vermesi aynı değildir. Burada belleği basitçe geçen gözlem listesi olarak tutuyoruz:

```python
self.bellek: list[Gözlem] = []
```

Yeni bir veri geldiğinde:

```python
gözlem = Gözlem(özellikler)
self.bellek.append(gözlem)
```

Bu örnek kalıcı bir veri tabanı değildir. Ama belleğin neyi sakladığını, saklanan verinin hangi sınıftan geldiğini ve belleğe erişimle kararın nasıl değiştiğini anlamak için yeterlidir.

## 5. Çıkarım: yeni durumu eski kuralla ilişkilendirmek

Çıkarım, bilinen bir kuralı yeni gözleme uygulamaktır:

```python
for anahtar, (beklenen, açıklama) in kurallar.items():
    if gözlem.özellikler.get(anahtar) == beklenen:
        return anahtar, açıklama
```

Örnekte hava `yağmurlu` olduğunda sistem, yağmuru beklemenin daha güvenli olabileceğini söyleyen kuralı seçiyor. Bu, meteorolojik gerçeğin kanıtı değil; yalnızca programın içindeki kurala göre üretilmiş bir öneridir.

## 6. Kendin yaz

Tam kod [`kod/yapay_zeka_durumu.py`](kod/yapay_zeka_durumu.py) dosyasındadır. Kodu çalıştır:

```bash
python kod/yapay_zeka_durumu.py
```

Beklenen çıktının ana hatları şöyledir:

```text
hava: Islak zeminde kayma riski artabilir.
plan: Bu görev için yağmuru beklemek daha güvenli olabilir.
Bellek özeti: {'hava': 2, 'plan': 2}
```

Ekranda gördüğün şey tek başına “akıllı” bir sistem değildir. Ama yapay zekâ sisteminde aradığımız parçaları açık biçimde gösterir:

1. Girdi bir sözlük olarak temsil edildi.
2. Gözlem belleğe eklandı.
3. Yeni durum bir kuralla eşleştirildi.
4. Kararın nedeni metin olarak açıklandı.

## 7. Öğrenme ve sınırlar

Bu dersin ilk sürümü veriyi bellekte tutup sabit kurallarla çıkarım yapar. Yeni bir kural eklenirse sistemi geliştirebiliriz. Ama bu haliyle deneyimden otomatik öğrenmez.

Daha gelişmiş sistemlerde:

- kurallar veriden öğrenilir;
- eskiden olan benzer örnekler aranır;
- belirsizlik olasılıkla ifade edilir;
- modelden gelen cevap doğruluk, güvenilirlik ve açıklama açısından ölçülür;
- sistemin hangi bilginin üzerine konuştuğu denetlenir.

Faz 2’de veriyle öğrenen ilk modelleri; Faz 7’de hazır dil modeli çağrılarını; Faz 11’de ise bu tür sistemleri nasıl değerlendireceğimizi öğreneceğiz.

## 8. Makaleden günümüze

Schank’ın makalesindeki “yapay zekânın amacı” sorusu güncel modallerle daha görünür hale geldi. Yine de sorular değişmedi:

- Sistem hangi düşünceyi temsil ediyor?
- Bilgiyi nasıl organize ediyor?
- Yanlış bilgiyle karşılaşınca ne yapıyor?
- Cevabı yalnızca ezberliyor, yoksa örnekler arasında genelleme yapabiliyor mu?
- Başarısını ve hatalarını nasıl kanıtlıyor?

Bu sorular, güzel görünen bir çıkıştan daha sağlam bir mühendislik temelidir.

!!! warning "Dil modeliyle karıştırma"
    Bir dil modeli metin üretebilir, kurallara benzeyen örüntüler seçebilir ve açıklama yazabilir. Ancak çıktısı otomatik olarak doğru, güvende veya gerçeğe dayalı değildir. Sonuçların kaynak ve davranış bakımından doğrulanması gerekir.

## 9. Kütüphaneyle karşılaştırma

Bu küçük örnek, kütüphane yerine açık Python nesneleri kullanır. Gerçek bir uygulamada çok benzer parçaları kütüphanelerden alırız:

- veri için `pandas` veya veri sınıfları
- metin araması için embedding modelleri
- çıkarım için makine öğrenmesi modeli
- açıklama için yapılandırılmış çıktılar ve kaynak kayıtları
- test için `unittest`, `pytest` veya benzeri araçlar

Fark, kütüphaneyi ilk çağırmadan önce temsil, bellek, çıkarım ve sınama sorularını anlamış olmamızdır.

## 10. Pekiştir

**Quiz**

1. Bir sistemde temsil neden önemlidir?
2. Bellek, sadece önceki gözlemleri saklayan bir liste olarak hangi sınırı taşır?
3. Kurala dayalı çıkarım ile öğrenilmiş çıkarım arasındaki fark nedir?
4. Bir programın açıklama üretebilmesi neden doğru olduğunu kanıtlamaz?
5. Bir dil modelinin çıktısını güvenilir kabul etmek için hangi kontroller gerekir?

**Alıştırmalar**

1. Sisteme `"ses": ("yüksek", "Kulaklık sesini azaltmayı öner")` kuralını ekle.
2. Eşleşmeyen gözlem için bellek özeti değişimini incele.
3. En az üç gözlemden oluşan bir deneme senaryosu yaz.
4. Kural sisteminin çözüm üretemeyeceği bir örnek oluştur.
5. Bu örneğin hangi bölümünün “öğrenme” yerine “programlama” olduğunu yazılı açıkla.

## Özet

Yapay zekâya tek bir araç gözüyle bakmak yerine, temsil, bellek, çıkarım, öğrenme ve açıklama gibi sınanabilir parçalar olarak bakmak daha yararlı olur. 1987’deki tartışmaların çekirdeği bu parçalar üzerinedir; günümüzün dil modelleri ve agent sistemleri de aynı soruların yeni yüzleridir.

## Kaynaklar

- Roger C. Schank, “What Is AI, Anyway?”, *AI Magazine*, 1987, cilt 8, sayı 4, DOI: `10.1609/aimag.v8i4.623`
- [AAAI AI Magazine makalesi](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/623)
- Python resmi belgesi: veri sınıfları, sözlükler ve tip işaretleri
