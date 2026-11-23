# Faz 2 – Ders 7: Soyağacı ve akrabalık katsayısı

> ⏱️ Tahmini süre: 45-60 dk · 📚 Ön koşul: Python, sözlükler ve fonksiyonlar · 💻 Gereksinim: Python 3.11+, ek paket yok

## Bu derste ne öğreneceksin?

- Bir aile ilişkisinin neden **ağaç** olarak temsil edilebileceğini
- Tüm eşleşmeleri tek tek denemeden iki birey arasında ortak ataları nasıl bulacağını
- Bir hesaplamanın özyinelemeli fonksiyonlarla nasıl parçalara ayrılacağını
- 1987'lerin popüler yapay zekâ dili ve mantığıyla geliştirilen döngülere doğrudan bağlı olmayan, güncel ve özgün bir yaklaşımı

!!! note "Tarihsel ilham"
    Bu dersin fikri, 1987 yılında akrabalık hesapları için yapay zekâ dilleri ve özyineleme kullanan çalışmaların teknik zemininden ilham alır. Ancak kod, açıklamalar ve örnekler bu projeye özgüdür; eski makalelerin aynısı değildir.

## 1. Problem

Bir biyoloji laboratuvarının kayıt defterinde yüzlerce bireyin ebeveynleri vardır. Soru şudur: iki bireyin ortak atalardan ne ölçüde kaynaklandığını sayısal olarak hesaplayabilir miyiz?

Basitçe tüm aileleri yazdırmak yetmez. Her atanın ata mı, kardeş mi veya farklı bir koldan mı geldiğini hesaplamamız gerekir.

Bu dersin modelinde her bireyin:

- kayıtlı ebeveyni yoksa bulunduğu yerde biten bir kök vardır;
- kaydı varsa iki ebeveyni vardır;
- her bağlantı döngüsüzdür.

## 2. Soyağacını veri olarak yaz

Python sözlüğünde bireyi, ebeveynlerinin isminden oluşan ikiliyle eşleştiririz:

```python
soya = {
    "Ayşe": None,
    "Bora": None,
    "Cem": ("Ayşe", "Bora"),
    "Derya": None,
    "Emre": ("Cem", "Derya"),
}
```

`None`, o bireyin ebeveyn kaydı bulunmadığı kökü temsil eder.

!!! tip "Tasarım seçimi"
    Gerçek veri daha fazla alan içerebilir: ad, doğum yılı, cinsiyet, kayıt kaynağı gibi. Ancak bu ders hesaplamayı öğrenmek için yalnızca ebeveyn ilişkisini tutar. Ayrıntı ekledikçe temel ağaç algoritması bozulmaz.

## 3. Ağaçları özyinelemeyle dolaş

Bir bireyin atalarını bulmak için onun ebeveynlerini, sonra ebeveynlerinin ebeveynlerini dolaşırız:

```python
def atalar(soya, kisi):
    ebeveynler = soya[kisi]
    if ebeveynler is None:
        return {kisi}

    p1, p2 = ebeveynler
    return {kisi} | atalar(soya, p1) | atalar(soya, p2)
```

Bu fonksiyon önce küçük problemi çözer: kökte bireyin kendisinden başka ata yoktur. Aksi halde kendi adını ve ebeveynlerinin tüm atalarını birleştirir.

## 4. Kendin yaz

Tam kod [`kod/soyagaci.py`](kod/soyagaci.py) dosyasındadır.

Akrabalık katsayısı için aşağıdaki özyinelemeli ilişkiyi kullanıyoruz:

- İki birey birbirinin aynısı ve kökse katsayı `0.5`
- İki farklı kök birey ortak ata içermezse katsayı `0`
- Bireylerden biri kök değilse hesabı ebeveynlerin her biri üzerinden ortalıyoruz

```python
if x == y:
    ebeveynler = soya[x]
    if ebeveynler is None:
        return 0.5
    p1, p2 = ebeveynler
    return 0.5 * (1.0 + phi(p1, p2))
```

Bu yaklaşım modern akrabalık katsayısının temel özyinelemeli hesaplamasını sadelik ve doğruluk açısından açıklar.

## 5. Çalıştır

```bash
python kod/soyagaci.py
python -m unittest discover -s test -v
```

Kodun doğrudan çalışan betik kısmı testler üzerinden kullanılır. Soyağacı döngü içerebiliyorsa kayıt işlemi hesaplama başlamadan önce hata üretmelidir.

## 6. 1987 ile bugünün farkı

1987'deki bir çok deneysel sistem, veriyi kurallar ve özyinelemeli ağaçlar olarak temsil ediyordu. Bugün aynı problemi:

- açık veri yapıları,
- otomatik test,
- bellekli özyineleme,
- daha güvenli hata kontrolleri

ile daha anlaşılır hale getirebiliriz.

Bu ders "yapay zekâ" etiketiyle sihirli bir tahmin yapmaz. Belli bir ağaç üzerinde **ölçülebilir ve denetlenebilir** bir hesap yapar.

## 7. Pekiştir

**Quiz**

1. Soyağacında `None` neyi temsil eder?
2. Bir ağacı sözlük yerine listeyle temsil etseydin hangi bilgi kaybolurdu?
3. Özyineleme bitmeden önce hangi temel durum gerekir?
4. Aynı ebeveynlere sahip iki bireyin katsayısı neden 0.5 değil başka bir hesap verebilir?

**Alıştırmalar**

1. Yeni bireyler ekle: üç nesil, bir dış evlilik kolu.
2. İki birey arasında beklediğin katsayıyı elle hesapla, sonra fonksiyonla karşılaştır.
3. Döngü oluşturan kötü bir veri ekle ve doğrulayıcının hata vermesini izle.
4. Fonksiyon çıktısını canlı bir HTML tabloya dönüştür.

## Özet

Soyağacı bir aileyi değil, **ebeveyn bilgisine sahip yönlendirilmiş bir ağacı** temsil eder. Doğru temel durum ve döngü kontrolüyle özyineleme, eski dönem bilgisayar bilimindeki ağaç problemlerini modern Python'da anlaşılır ve test edilebilir biçimde çözebilir.
