# Katkı Rehberi

Bu proje öğrenenler için, öğrenenlerle birlikte yazılıyor. Her katkı değerli: tek bir yazım hatası düzeltmesi de, yeni bir ders de.

## Katkı türleri

| Katkı | Nasıl? | Zorluk |
|---|---|---|
| **"Anlamadım" bildirimi** | GitHub'da issue aç; hangi dersin hangi kısmında takıldığını yaz | Kolay |
| **Yazım ve dil düzeltmesi** | Sayfanın sağ üstündeki kalem simgesine tıkla, düzelt, pull request aç | Kolay |
| **Teknik hata düzeltmesi** | Hatayı, doğrusunu ve kaynağını yaz | Orta |
| **Çalışmayan kod bildirimi** | İşletim sistemini, Python sürümünü ve hata mesajını issue'ya yaz | Kolay |
| **Yeni ders** | [Müfredattaki](MUFREDAT.md) ⬜ olan bir dersi seç, önce issue aç | Zor |
| **Çeviri/sözlük önerisi** | [Sözlüğe](SOZLUK.md) eksik terim ya da daha iyi karşılık öner | Kolay |

!!! tip "Hiç Git bilmiyorsan"
    GitHub'da sayfanın sağ üstündeki kalem simgesi, dosyayı tarayıcıdan düzenlemeni ve "Propose changes" ile öneri göndermeni sağlar. Terminal gerekmez.

## Yeni ders yazma adımları

1. **Issue aç.** Hangi dersi yazmak istediğini söyle; iki kişi aynı şeyi yazmasın.
2. **Şablonu kopyala.** [Ders şablonundaki](sablon/DERS-SABLONU.md) bölümleri doldur.
3. **Klasör yapısını kur.**

    ```
    faz-XX-faz-adi/
      NN-ders-adi/
        README.md      # ders metni
        kod/           # çalışan kod
        test/          # kodu doğrulayan testler
    ```

4. **Kodu yaz ve test et.** Test olmadan ders birleştirilmez.
5. **Siteye ekle.** `mkdocs.yml` içindeki `nav:` bölümüne dersi ekle.
6. **Müfredatı güncelle.** [MUFREDAT.md](MUFREDAT.md) içinde dersin durumunu ✅ yap ve bağlantı ver.
7. **Pull request aç.** Kontrol listesini doldur.

## Yazım kuralları

**Dil ve üslup**

- Okuyucuya "sen" diye hitap et. Kısa cümleler ve somut örnekler kullan.
- Bir terimi ilk kullandığın yerde açıkla. Terimleri [sözlükle](SOZLUK.md) uyumlu kullan.
- Karşılığı yerleşmemiş terimleri İngilizce bırak (token, prompt gibi). İlk geçtiği yerde Türkçe karşılığı varsa parantez içinde ver.
- Soyut tanımla başlama. Önce bir problem veya örnek göster.

**İçerik**

- **Özgün yaz.** Başka bir kursun metnini veya kodunu çevirme. Birincil kaynaklardan (makaleler, resmî dokümanlar, kitaplar) öğren, kendi sözlerinle anlat ve "Kaynaklar" bölümünde belirt.
- **Sayısal iddiaları doğrula.** "X, Y'den şu kadar hızlı" diyorsan ölçümü veya kaynağı ver.
- **Neden olduğunu anlat.** "Şunu yap" demek yerine "şunu yap, çünkü..." de.
- **Yaygın hataları ekle.** Her dersin "Sık yapılan hatalar" bölümü, öğrencinin en çok vakit kazandığı yerdir.

**Kod**

- Mümkünse yalnızca standart kütüphane kullan. Ek paket gerekiyorsa dersin başında belirt.
- Fonksiyonlara kısa bir açıklama (docstring) ekle. Değişken ve fonksiyon adları Türkçe olabilir, ama tek bir derste tutarlı ol.
- Dersin içindeki kod parçaları `kod/` klasöründeki dosyayla birebir aynı olmalı.
- Testler `unittest` ile yazılır ve `python -m unittest discover -s test` ile çalışır.

## Siteyi kendi bilgisayarında görmek

Değişikliğin nasıl göründüğüne yayınlamadan önce bakmak istersen:

```bash
pip install -r requirements.txt
mkdocs serve
```

Sonra tarayıcıda `http://127.0.0.1:8000` adresini aç. Bu adım isteğe bağlıdır; GitHub her yüklemede siteyi otomatik derler.

## Pull request kontrol listesi

- [ ] [Ders şablonundaki](sablon/DERS-SABLONU.md) bölümlerin hepsi var
- [ ] Kod temiz bir ortamda çalışıyor
- [ ] Testler geçiyor
- [ ] Terimler sözlükle tutarlı, yeni terimler sözlüğe eklendi
- [ ] Kaynaklar listelenmiş
- [ ] `mkdocs.yml` ve `MUFREDAT.md` güncellendi

## İnceleme süreci

Gönderdiğin her katkı şunlara bakılarak değerlendirilir: Doğru mu? Açık mı? Kod çalışıyor mu? Geri bildirim, katkıyı reddetmek için değil, iyileştirmek içindir. Fikir ayrılığı olursa issue üzerinden konuşuruz.

## Davranış

Burada herkes öğreniyor. Soru sormaktan çekinme, başkasının sorusuna küçümsemeden cevap ver. Saygısız ya da aşağılayıcı bir dil kabul edilmez.
