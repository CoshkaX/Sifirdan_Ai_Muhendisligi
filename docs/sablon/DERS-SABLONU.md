# Faz X – Ders Y: [Ders başlığı]

> ⏱️ Tahmini süre: __ dk · 📚 Ön koşul: [önceki ders] · 💻 Gereksinim: [Python 3.11+, ek paket yok]

## Bu derste ne öğreneceksin?

- Madde 1
- Madde 2
- Madde 3

## 1. Problem

Somut bir sorunla başla. Kısa bir örnek, bir hata, bir soru. Soyut tanımla başlama.

## 2. Kendin yaz

Önce fikri düz anlat, sonra kodu küçük ve denenebilir parçalara böl. Her parçanın ne yaptığını açıkla. Okur kodu sayfada düzenleyip çalıştırabilsin diye örnekleri aşağıdaki gibi yaz:

```python {.python-playground}
# Örneği değiştirip tekrar çalıştır.
mesaj = "Merhaba, yapay zekâ!"
print(mesaj)
```
```text {.python-playground-expected}
Merhaba, yapay zekâ!
```
```text {.python-playground-help}
`mesaj = "Merhaba, yapay zekâ!"` | `=` sağdaki metni `mesaj` adlı değişkene kaydeder; tırnaklar bunun bir metin olduğunu gösterir.
`print(mesaj)` | `print` değişkende saklanan değeri ekranda gösterir. Değişkenin adını verdiğimiz için tırnaklar çıktıda görünmez.
`mesaj = "Bugün Python öğreniyorum."` | Tırnak içindeki yazıyı değiştirip tekrar çalıştır; aynı `print` satırı yeni değeri gösterecektir.
```

Python kod bloğunun sonuna `{.python-playground}` eklemek onu tarayıcıda düzenlenebilir bir Python penceresine dönüştürür. Hemen arkasına gelen `{.python-playground-expected}` metin bloğu beklenen çıktıyı belirtir. Beklenen çıktı başlangıçta kapalıdır; sonuç eşleşmezse karşılaştırma için açılır. Çıktı eşleşirse pencere yeşile döner ve düğme başarı işaretini gösterir.

Öğrencinin değiştirmesi ve çalıştırması yararlı olan, kendi başına çalışabilen saf Python örneklerini etkileşimli pencereye dönüştür. Terminal komutlarını, işletim sistemine özgü kurulum adımlarını, yalnızca bir sınıfın içinde anlam kazanan eksik kod parçalarını ve bilgisayardaki dosya ya da özel paket gerektiren örnekleri normal kod bloğu olarak bırak; neden tarayıcıda çalışmadığını açıkla.

Örnek çözüme takılabilecek öğrenciler için `{.python-playground-help}` bloğunu da beklenen çıktı bloğunun arkasına ekle. Her boş olmayan satır açılır **“Yapamazsan buna bas”** yardımında ayrı bir adım olarak görünür. Her satırda önce açıklanan kod parçasını ters tırnak içinde, sonra `|` ayıracıyla açıklamasını yaz. Şunları anlat: bu kod ne alıyor, ne yapıyor, neden gerekiyor ve sonraki satırda hangi değeri kullanacağız. Terimi tanımlamadan kullanma; görevi tekrar etmekle yetinme ve bütün çözümü bir anda verme. Önce küçük bir parçayı açıkla.

Her pencere ve görev, açıklanan tek bir fikri gösterecek kadar küçük olsun. Öğrenciye hangi satırı değiştireceğini ve çalıştırınca ne görmesini beklediğini söyle. `Ctrl+Enter` kısayolu da çalıştırır.

Beklenen çıktılı pencerelerde yalnızca sabit metinleri `print()` ile yazdırmak başarı sayılmaz; çalışma alanı bu bariz kestirmeyi algılayıp öğrenciyi göreve yönlendirir. Bu kontrol tüm hileleri önleyemez. Görevi birden fazla girdiyle denetle, öğrenciden kodun ne yaptığını açıklamasını iste ve mesajları suçlayıcı değil destekleyici tut.

Örnekleri ders deposundaki dosyadan bağımsız, kendi başına çalışabilir tut. Bir alıştırma başlangıç koduysa, okurun yazacağı yeri açıkça belirt:

```python {.python-playground}
metin = "Türkçe"
# Görev: metnin UTF-8 bayt sayısını hesaplayıp yazdır.
```

Tarayıcıdaki çalışma alanı ders dosyalarını değiştirmez ve kodu siteye göndermez; ilk çalıştırmada Python çalışma zamanı CDN'den indirilir. Ders dosyasını bilgisayarında ayrıca çalıştırmak gerekiyorsa bunu da belirt:

```bash
python kod/dosya.py
```

## 3. Kütüphaneyle yap

Aynı işi gerçek bir araçla nasıl yaparız? Kendi yazdığınla farkı nedir?
Çalışma alanının saf Python örnekleri için olduğunu; yerel dosyaların, özel paketlerin veya internet servislerinin tarayıcıda kendiliğinden hazır olmayacağını açıkla.

## 4. Sık yapılan hatalar

- Hata 1: ne olur, nasıl anlaşılır, nasıl düzeltilir?
- Hata adını tek başına bırakma. Python'ın hangi adı/değeri aradığını, neyi bulamadığını veya hangi değerlerin uyuşmadığını ve hatayı nasıl düzelteceğini yeni başlayan birine anlat. Örneğin `NameError: name 'renk' is not defined`, Python'ın `renk` adlı değişkeni bulamadığı anlamına gelir; bu değişkeni kullanmadan önce tanımlayıp ilgili hücreyi çalıştırmak gerekir.

## 5. Pekiştir

**Quiz** (3-5 soru, cevaplar dosyanın sonunda)

**Alıştırmalar**
1. Kolay
2. Orta
3. Zor (isteğe bağlı)

## Özet

3-4 cümle.

## Kaynaklar

- Birincil kaynaklar (makale, resmî doküman, kitap)

## Quiz cevapları

1. ...
