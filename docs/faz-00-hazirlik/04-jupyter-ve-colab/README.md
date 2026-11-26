# Faz 0 – Ders 4: Jupyter ve Colab ile çalışmak

> ⏱️ Tahmini süre: 45-60 dk · 📚 Ön koşul: 0.1 Geliştirme ortamı ve temel Python · 💻 Gereksinim: internet; Colab için Google hesabı, yerel Jupyter için Python

## Bu derste ne öğreneceksin?

- Jupyter defterinin kod ve açıklama hücrelerinden oluştuğunu
- Bir kod hücresini çalıştırıp sonucunu görmeyi
- Hücrelerin sırasının ve çalışma belleğinin neden önemli olduğunu
- Tarayıcıdaki Google Colab ile bilgisayarındaki Jupyter arasındaki temel farkı
- Küçük bir veri listesi üzerinde Python denemesi yapmayı

## 1. Problem

Bir Python dosyasını her değiştirdiğinde tüm programı baştan çalıştırman gerekebilir. Veriyi parça parça incelemek, sonucu hemen görmek ve araya açıklama yazmak istediğinde bu yöntem yavaşlayabilir.

Jupyter Notebook (Jupyter defteri), kodu küçük **hücrelere** bölüp her hücreyi ayrı ayrı çalıştırmaya yarar. Kodun yanına açıklama ve sonuç da ekleyebilirsin. Google Colab ise Jupyter defterlerini tarayıcıda çalıştıran bir hizmettir; bilgisayarına Python kurmadan deneme yapmana imkân verir.

## 2. Kendin yaz

### 2.1 İlk Colab defterini aç

1. [Google Colab](https://colab.research.google.com/) sayfasını aç. Google hesabınla oturum açman istenebilir.
2. **Yeni defter** oluştur ve üstteki başlığı `ilk-python-denemem` olarak değiştir.
3. Kod hücresine `print("Merhaba, Python!")` yaz.
4. Hücrenin solundaki çalıştır düğmesine bas veya `Shift+Enter` kullan.
5. Çıktıda `Merhaba, Python!` görmelisin. `Shift+Enter` hücreyi çalıştırır ve çoğu durumda bir sonraki hücreye geçirir.

Bu dersin sayfasındaki pencere kısa bir kod denemek içindir; bir Jupyter defteri değildir ve dosya kaydetmez. Gerçek hücreleri, aralarındaki durumu ve defterin kaydedilmesini Colab'da dene.

### 2.2 Kod hücresi ve Markdown hücresi

Kod hücresi Python çalıştırır. Markdown hücresi ise başlık, açıklama veya liste gibi biçimlendirilmiş metin gösterir. Colab'da hücre eklemek için araç çubuğundaki **+ Code** veya **+ Text** düğmesini kullan.

Bir defterde kodun sırasını şu küçük örnekle görebilirsin. Bunu tek bir kod hücresine yazıp çalıştır:

```python {.python-playground}
sayilar = [2, 3, 5]
toplam = 0
for sayi in sayilar:
    toplam += sayi
print(f"Sayı adedi: {len(sayilar)}")
print(f"Toplam: {toplam}")
```
```text {.python-playground-expected}
Sayı adedi: 3
Toplam: 10
```
```text {.python-playground-help}
`sayilar = [2, 3, 5]` | Köşeli ayraçlar bir liste oluşturur; üç sayıyı bu listede sırayla saklarız.
`toplam = 0` | Toplama başlamadan önce sonucu sıfırdan başlatırız; döngü bu değerin üzerine ekleme yapacak.
`for sayi in sayilar:` | Döngü listedeki sayıları birer birer `sayi` değişkenine koyar ve girintili satırı her sayı için çalıştırır.
`toplam += sayi` | Bu kısaltma, `toplam = toplam + sayi` ile aynıdır. Her turda o anki sayıyı toplamın üzerine ekler.
`print(f"Sayı adedi: {len(sayilar)}")` | `len` listedeki öğe sayısını bulur; `print` bunu açıklama metniyle birlikte gösterir.
`print(f"Toplam: {toplam}")` | Döngü bittikten sonra biriken toplamı ekrana yazar.
```

`sayilar` listesini değiştirip tekrar çalıştır. Listeyi değiştirdiğinde hem öğe sayısının hem toplamın güncellendiğini gözlemle.

### 2.3 Hücre sırası ve çalışma belleği

Python, çalıştırdığın tek bir kod hücresindeki satırları yukarıdan aşağıya işler. Örneğin aynı hücrede `renk = "mavi"` satırı `print(renk)` satırından önceyse Python önce değişkeni oluşturur, sonra değerini ekrana yazar. Jupyter defterinde kod farklı hücrelere bölünebilir; hücreleri ise istediğin sırada çalıştırabilirsin. Bu yüzden ekranda üstte duran bir hücre, mutlaka önce çalıştırılmış demek değildir. Jupyter'de kod hücrelerini çalıştıran Python sürecine **kernel** denir. Bir hücrede oluşturduğun değişken, bu süreç açık kaldığı sürece sonraki hücrelerde kullanılabilir.

Colab'da ilk hücreye `renk = "mavi"` yazıp çalıştır. Bu satır `"mavi"` metnini `renk` adlı değişkene kaydeder. Altındaki hücreye `print(renk)` yazıp çalıştır; `print`, değişkende saklanan değeri ekranda gösterir.

İkinci hücreyi ilk hücreden önce çalıştırırsan `NameError: name 'renk' is not defined` hatası alırsın. Python, `print(renk)` satırında `renk` adlı değişkeni bulamaz; çünkü değişkeni oluşturan ilk hücre henüz çalıştırılmamıştır. Önce ilk hücreyi çalıştır, sonra `print(renk)` hücresini.

Bir hücreyi tekrar tekrar çalıştırmak bazı işlemleri iki kez yapabilir. Örneğin `konular.append("Python")`, `"Python"` öğesini listenin sonuna ekler. Hücreyi iki kez çalıştırırsan öğe de iki kez eklenir; önceki çalıştırmanın yaptığı işlem kendiliğinden geri alınmaz.

Sonuçların karıştığını düşünüyorsan **Runtime → Restart session** ile Colab'ın çalışan Python sürecini yeniden başlatabilirsin. Bu işlem bellekteki değişkenleri siler. Ardından değişkenleri kullanan hücrelerden önce onları oluşturan hücreleri çalıştır; yoksa yine `NameError` alırsın.

### 2.4 Defteri kaydet ve paylaş

Colab defterini Google Drive'a kaydedebilir ve bağlantıyla paylaşabilirsin. Paylaşım iznini göndermeden önce kontrol et. Gizli anahtar, parola veya kişisel veri içeren dosyaları herkese açık bir deftere koyma. Yerel Jupyter'de defter `.ipynb` dosyası olarak bilgisayarında saklanır.

### Şimdi sen yaz: listeyle çalış

Colab'daki bir hücrede yazacağın türden kısa bir kod: listeye öğe ekle ve say. Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur, sonra çalıştır.

```python {.python-playground-task}
konular = ["Python"]

# TODO 1: Listeye "Colab" öğesini ekle (append metodu).
konular.___("Colab")

# TODO 2: Listedeki öğe sayısını bul (len fonksiyonu).
sayi = ___(konular)

print("Konular:", konular)
print("Öğe sayısı:", sayi)
```
```text {.python-playground-expected}
Konular: ['Python', 'Colab']
Öğe sayısı: 2
```
```text {.python-playground-help}
`konular.___("Colab")` | Bir listenin sonuna öğe eklemek için `append` kullanılır.
`sayi = ___(konular)` | Listedeki öğe sayısını `len` verir.
```
```python {.python-playground-solution}
konular = ["Python"]

# Listeye "Colab" öğesini ekle (append metodu).
konular.append("Colab")

# Listedeki öğe sayısını bul (len fonksiyonu).
sayi = len(konular)

print("Konular:", konular)
print("Öğe sayısı:", sayi)
```

## 3. Kütüphaneyle yap

Jupyter ve Colab, Python kütüphanesi değil; kodu hücreler halinde çalıştırıp açıklamalarla birlikte tutmaya yarayan araçlardır.

Bilgisayarında yerel Jupyter kullanmak istersen önce 0.1 dersinde anlattığımız sanal ortamı etkinleştir, sonra:

```bash
python -m pip install notebook
python -m notebook
```

Tarayıcıda açılan yerel sayfada yeni bir Python defteri oluşturabilirsin. Colab'da ise hesap ve internet bağlantısı gerekir; hücreler uzaktaki çalışma ortamında çalışır.

## 4. Sık yapılan hatalar

- **Hücreleri sırayla çalıştırdığını varsaymak.** `renk = "mavi"` hücresi çalışmadan `print(renk)` çalışırsa Python `renk` değerini bulamaz ve `NameError` verir. Değişkeni oluşturan hücreyi önce çalıştır.
- **Hücreyi çok kez çalıştırmak.** `append` gibi ekleme yapan işlemler her çalıştırmada yeniden uygulanır; aynı öğe listeye birden fazla kez eklenebilir.
- **Çıktıyı kodun bir parçası sanmak.** Kod hücresi talimattır; altında görünen çıktı o çalıştırmanın sonucudur.
- **Kernel'i yeniden başlatınca değişkenlerin kalacağını düşünmek.** Yeniden başlatma çalışma belleğini temizler; hücreleri baştan çalıştır.
- **Colab'ı yerel bilgisayarınmış gibi kullanmak.** Colab kodu uzaktaki bir ortamda çalıştırır; bilgisayardaki dosyalar kendiliğinden görünmez.
- **Gizli bilgiyi deftere koymak.** Paylaşılan veya herkese açık bir notebook'a parola ve API anahtarı ekleme.

## 5. Pekiştir

**Quiz**

1. Jupyter defterindeki kod hücresi ne yapar?
2. Markdown hücresi ne için kullanılır?
3. `renk = "mavi"` hücresinden önce `print(renk)` çalıştırılırsa `NameError` neden oluşur?
4. Kernel'i yeniden başlatınca değişkenlere ne olur?
5. Colab ve yerel Jupyter arasındaki bir fark nedir?

**Alıştırmalar**

1. Colab'da bir kod hücresine üç sevdiğin konuyu liste olarak yazdır.
2. Listenin öğe sayısını `len` ile bul ve bir Markdown hücresinde sonucu açıkla.
3. Bir değişkeni tanımlayan hücreyi ikinci hücreden sonra çalıştır; oluşan hatayı gözlemle, sonra sırasını düzelt.
4. Listeye `append` ile bir öğe ekle ve hücreyi iki kez çalıştır. Neden iki kopya oluştuğunu açıkla.
5. (İsteğe bağlı) Yerel Jupyter kurup aynı iki hücrelik örneği `.ipynb` dosyası olarak kaydet.

??? success "Quiz cevapları"
    1. Python kodunu çalıştırır ve oluşan çıktıyı hücrenin altında gösterir.
    2. Başlık ve açıklama gibi biçimlendirilmiş metin yazmak için.
    3. `renk` adlı değişkeni oluşturan hücre henüz çalışmadığı için Python bu adı bulamaz; önce tanım hücresini çalıştırmak gerekir.
    4. Çalışma belleği silinir; hücreleri yeniden çalıştırarak değişkenleri tekrar oluşturmak gerekir.
    5. Colab tarayıcıda, uzak bir ortamda çalışır; yerel Jupyter bilgisayara kurulur ve yerel kaynakları kullanır.

## Özet

Jupyter defteri kod, açıklama ve çıktıyı hücreler halinde bir araya getirir. Colab, bu defterleri tarayıcıda çalıştırmanın bir yoludur. Hücreleri doğru sırada çalıştırmak ve kernel belleğini anlamak, tekrar üretilebilir sonuçlar için önemlidir. Bu dersteki pencere kısa Python denemesi içindir; gerçek notebook deneyimini Colab'da veya yerel Jupyter'de yap.

## Kaynaklar

- [Jupyter Notebook belgeleri](https://docs.jupyter.org/en/latest/)
- [Google Colab SSS](https://research.google.com/colaboratory/faq.html)
- [Python öğreticisi: `for` döngüsü ve listeler](https://docs.python.org/3/tutorial/controlflow.html)
