# Faz X – Ders Y: [Ders başlığı]

> ⏱️ Tahmini süre: __ dk · 📚 Ön koşul: [önceki ders] · 💻 Gereksinim: [Python 3.11+, ek paket yok]

## Bu derste ne öğreneceksin?

- Madde 1
- Madde 2
- Madde 3

## 1. Problem

Somut bir sorunla başla. Kısa bir örnek, bir hata, bir soru. Soyut tanımla başlama.

## 2. Kendin yaz

Önce fikri düz anlat, sonra kodu küçük ve denenebilir parçalara böl. Her ders bölümü iki tür kod kutusu kullanır:

| | **Örnek** | **Kendin yaz** |
|---|---|---|
| Amaç | Çalışan kodu görmek, değiştirip ne olduğunu denemek | Eksik kodu kendin tamamlamak |
| Kod nasıl gelir? | Eksiksiz | İskelet: yazılacak yerler `___`, notlar `# TODO` |
| Başarı rozeti | Yok | Çıktı beklenenle eşleşirse "✓ Başarılı" |
| Yardım düğmesi | **Anlamadıysan bas**: kodu satır satır açıklar | **Yapamazsan buna bas**: çözümün tamamını yeşil kodla ve satır satır açıklamasını gösterir |
| Markdown işareti | `{.python-playground}` | `{.python-playground-task}` |

### Örnek kutusu

Her fikir için bir **Örnek** kutusu yaz. Kutu, öğrenciye kodu değiştirmesini söyleyen bir uyarıyla kendiliğinden gelir; ayrıca altına neyi değiştirebileceğini bir cümleyle yaz. Kutunun arkasına sırayla `{.python-playground-expected}` (başlangıç koduyla çıkan çıktı) ve `{.python-playground-help}` (satır satır açıklama) blokları gelir:

```python {.python-playground}
mesaj = "Merhaba, yapay zekâ!"
print(mesaj)
```
```text {.python-playground-expected}
Merhaba, yapay zekâ!
```
```text {.python-playground-help}
`mesaj = "Merhaba, yapay zekâ!"` | `=` sağdaki metni `mesaj` adlı değişkene kaydeder; tırnaklar bunun bir metin olduğunu gösterir.
`print(mesaj)` | `print` değişkende saklanan değeri ekranda gösterir. Değişkenin adını verdiğimiz için tırnaklar çıktıda görünmez.
```

Kutunun altına şöyle bir cümle ekle: "`mesaj` değişkenindeki yazıyı değiştirip tekrar çalıştır; aynı `print` satırı yeni değeri gösterecek."

### Kendin yaz görevi

Her dersin "Kendin yaz" bölümünün sonuna, `### Şimdi sen yaz: [konu]` başlığıyla en az bir görev ekle. Görev kutusunun arkasına **dört** blok gelir ve sırası değişmez: görev, beklenen çıktı, yardım, çözüm.

```python {.python-playground-task}
fiyat = 40
adet = 3

# TODO: Toplam tutarı hesapla (fiyat çarpı adet).
toplam = ___

print(f"Toplam: {toplam} TL")
```
```text {.python-playground-expected}
Toplam: 120 TL
```
```text {.python-playground-help}
`toplam = ___` | Fiyatı adetle çarpmak için `*` işaretini kullan: `fiyat * adet`.
```
```python {.python-playground-solution}
fiyat = 40
adet = 3

# Toplam tutarı hesapla (fiyat çarpı adet).
toplam = fiyat * adet

print(f"Toplam: {toplam} TL")
```

Görev yazarken şu kurallara uy. Hepsi, yeni başlayan bir öğrencinin takıldığı yerlerden çıkarıldı:

1. **Sıfırdan yazdırma, iskelet ver.** Öğrencinin yazacağı yeri `___` ile boş bırak, üstüne `# TODO: ...` notu yaz. `___` doluyken kutu çalışmaz; öğrenci önce boşluğu doldurur.
2. **Cevabı yorumda söyleme.** `# TODO` notu *ne* yapılacağını söylesin, cevabı değil. Cevaba yardım düğmesi götürür.
3. **Yalnızca derste öğretilen sözdizimini kullan.** Öğrencinin görmediği bir şey varsa (tek satırlık `if ... else`, `set`, iç içe döngü, `a = b = 0` gibi) iskelete bir açıklama satırı ekle.
4. **Çarpma `*`, üs alma `**`.** Yorumlarda matematik yazımı (×) kullanırsan, öğrenci bunu koda yazmasın diye kutunun üstündeki yönerge zaten hatırlatır; yine de yardımda `*` yaz.
5. **Boşluğu tırnağın içine koyma.** Koyman gerekiyorsa yardımda "tırnaklar hazır, yalnızca metni yaz" de.
6. **Çıktı, yanlış kodu yakalasın.** Yalnızca `print("başarılı")` yazdıran bir görevde yanlış çözüm de geçer. Fonksiyonların sonuçlarını yazdır; yanlış çözümlerin aynı çıktıyı vermemesi için simetrik veri seçme (örneğin yanlış pozitif ile yanlış negatif sayısı aynı olmasın).
7. **Farklı ama doğru cevaplar da geçsin.** Kontrol çıktıya bakar. Sabit bir sayının tek doğru cevap olmadığı durumlarda (ör. bir eşik, bir ağırlık) beklenen çıktı bütün geçerli cevaplarda aynı olmalı.
8. **Yardım adımları kısa olsun.** Boşluk içeren her satır için bir adım yaz; her adım en fazla iki kısa cümle. Önce açıklanan kod parçasını ters tırnak içinde, sonra `|` ayıracıyla açıklamasını yaz. Terimi tanımlamadan kullanma.
9. **Çözüm bloğu çalışan tam koddur.** `___` ve `TODO` içermez. Beklenen çıktıyı çözümü çalıştırarak al; elle yazma.
10. **Görev küçük kalsın.** Tek bir fikri sınasın ve birkaç dakikada çözülsün. Birden fazla boşluk varsa her biri ayrı bir adım olsun.

Beklenen çıktılı görevlerde yalnızca sabit metinleri `print()` ile yazdırmak başarı sayılmaz; çalışma alanı bu bariz kestirmeyi algılar. Bu kontrol tüm hileleri önlemez ve zaten bu bir sınav değil, öğrenme aracıdır; mesajları suçlayıcı değil destekleyici tut.

### Hangi kodlar kutuya girmez?

Terminal komutlarını, işletim sistemine özgü kurulum adımlarını, yalnızca bir sınıfın içinde anlam kazanan eksik kod parçalarını ve bilgisayardaki dosya ya da özel paket gerektiren örnekleri normal kod bloğu olarak bırak; neden tarayıcıda çalışmadığını açıkla. Tarayıcıdaki çalışma alanı ders dosyalarını değiştirmez ve kodu siteye göndermez; ilk çalıştırmada Python çalışma zamanı CDN'den indirilir. Ders dosyasını bilgisayarında ayrıca çalıştırmak gerekiyorsa bunu da belirt:

```bash
python kod/dosya.py
```

### Doğrula

Ders eklemeden önce proje klasöründe çalıştır:

```bash
python scripts/ornekleri_dogrula.py
```

Betik bütün Örnek kutularının ve Kendin yaz çözümlerinin beklenen çıktıyı verdiğini, görevlerde `___` bulunduğunu ve çözümlerde `___` ya da `TODO` kalmadığını denetler. GitHub'da her gönderimde de otomatik çalışır.

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
