# Faz 0 – Ders 5: Test yazmak ve hata ayıklamak

> ⏱️ Tahmini süre: 60-75 dk · 📚 Ön koşul: 0.1 Geliştirme ortamı ve 0.2 Python hızlı tekrar · 💻 Gereksinim: Python 3.11+, ek paket yok

## Bu derste ne öğreneceksin?

- Testin neyi doğruladığını ve neden koddan ayrı tutulduğunu
- `assert` ile bir koşulu sınamayı
- Hata mesajını okuyup sorunu küçük adımlarla bulmayı
- `unittest` ile testleri dosyaya koyup tekrar çalıştırmayı
- Başarılı ve başarısız test sonucunu ayırt etmeyi

## 1. Problem

Bir fonksiyon ekranda doğru görünen tek bir sonuç üretebilir ama başka girdilerde bozulabilir. Her değişiklikten sonra her örneği elle denemek hem zaman alır hem de bir durumu unutmayı kolaylaştırır.

**Test**, programın belirli bir girdi için beklenen davranışı gösterip göstermediğini sınar. Hata ayıklama (debugging) ise beklenmeyen sonucu bulup nedenini anlamaya çalışmaktır. Test sorar: “Bu davranış doğru mu?” Hata ayıklama sorar: “Doğru değilse nerede ve neden bozuldu?”

## 2. Kendin yaz

### 2.1 Önce beklenen davranışı belirle

Bir dikdörtgenin alanını hesaplayacağız. Kenarlar 3 ve 4 ise beklenen sonuç 12'dir. Aşağıdaki pencerede fonksiyonu çalıştır, sonra `*` işaretini geçici olarak `+` yapıp testin hatayı yakaladığını gör:

```python {.python-playground}
def dikdortgen_alani(en, boy):
    return en * boy


assert dikdortgen_alani(3, 4) == 12
assert dikdortgen_alani(5, 2) == 10
print("İki test de başarılı.")
```
```text {.python-playground-expected}
İki test de başarılı.
```
```text {.python-playground-help}
`def dikdortgen_alani(en, boy):` | Fonksiyon iki kenar uzunluğunu alır; amacı bu değerlerden alanı hesaplamaktır.
`return en * boy` | Dikdörtgen alanı iki kenarın çarpımıdır; `return` sonucu fonksiyonu çağıran koda verir.
`assert dikdortgen_alani(3, 4) == 12` | `assert`, soldaki sonuç 12 değilse testi durdurup `AssertionError` üretir. Bu örnek 3 × 4 işlemini sınar.
`assert dikdortgen_alani(5, 2) == 10` | İkinci girdi çifti, fonksiyonun tek bir örneğe özel çalışmadığını kontrol eder.
`print("İki test de başarılı.")` | Buraya yalnızca iki koşul da doğruysa ulaşılır; mesaj bütün testlerin geçtiğini gösterir.
```

`assert` satırlarından birindeki beklenen sayıyı bilerek yanlış yap. Programın testte durduğunu gör; sonra beklenen değeri düzeltip yeniden çalıştır.

### 2.2 Hata mesajını adım adım oku

Bir test başarısız olduğunda ilk iş tahmin yürütmek değil, son satırdaki hata türünü ve hatanın gösterdiği satırı okumaktır:

- `AssertionError`: `assert` koşulu yanlış çıktı. Örneğin alanı `12` olan dikdörtgen için test `10` bekliyorsa Python testi durdurur; beklenen sayı ile fonksiyonun hesabını karşılaştır.
- `NameError`: Python, kodda kullandığın adı bulamadı. Değişkeni hiç tanımlamamış, adını farklı yazmış veya onu oluşturan Colab hücresini henüz çalıştırmamış olabilirsin. Örneğin `renk = "mavi"` çalışmadan `print(renk)` yazarsan `renk` mevcut değildir.
- `TypeError`: yaptığın işlem, değerlerin türleriyle uyuşmuyor. Örneğin `"3" + 2` satırında Python metin ile sayıyı toplayamaz. Sayısal toplama istiyorsan `int("3") + 2` yaz; `int` metni sayıya çevirir ve sonuç `5` olur. Metinleri birleştirmek istiyorsan `"3" + str(2)` yaz; `str` sayıyı metne çevirir ve sonuç `"32"` olur.
- `IndexError`: listede bulunmayan bir sıradaki öğeyi istedin. Örneğin iki öğeli `[7, 9]` listesinde `liste[2]` üçüncü öğeyi arar, ama yalnızca `liste[0]` ve `liste[1]` vardır.

Sorunu bulmak için şu sırayı izle:

1. Hata mesajının son satırını oku; ne tür bir hata olduğunu öğren.
2. Üstte belirtilen dosya ve satıra git.
3. O satırdaki değişkenlerin değerlerini ve türlerini kontrol et.
4. En küçük düzeltmeyi yapıp aynı testi tekrar çalıştır.

0.1 dersindeki `isim`/`ad` hatası da bu yöntemi gösterir: Python, tanımlanmamış `isim` adını kullanan satırı belirtir.

### 2.3 Testleri dosyada sakla

Tekrar tekrar kullanacağın testleri ayrı bir dosyada tutabilirsin. Örneğin klasör yapısı şöyle olsun:

```text
calisma/
  hesaplama.py
  test/
    test_hesaplama.py
```

`hesaplama.py` dosyasına işlevi yaz:

```python
def dikdortgen_alani(en, boy):
    return en * boy
```

`test/test_hesaplama.py` dosyasına testleri yaz:

```python
import unittest

from hesaplama import dikdortgen_alani


class DikdortgenTesti(unittest.TestCase):
    def test_alani_hesaplar(self):
        self.assertEqual(dikdortgen_alani(3, 4), 12)

    def test_sifir_kenar_sifir_alan_verir(self):
        self.assertEqual(dikdortgen_alani(0, 5), 0)


if __name__ == "__main__":
    unittest.main()
```

Terminalde `calisma` klasörüne girip testleri çalıştır:

```bash
python -m unittest discover -s test -v
```

`unittest` Python ile birlikte gelen test aracıdır. `TestCase` sınıfı testleri toplar; adı `test_` ile başlayan yöntemler ayrı test olarak çalıştırılır. `assertEqual(gerçek, beklenen)` iki değerin eşit olup olmadığını sınar. Testler geçtiğinde `OK`, tek bir test başarısız olduğunda özet satırında `FAILED (failures=1)` görürsün.

### Şimdi sen yaz: kendi testini yaz

Fonksiyonu yaz, sonra testlerin beklenen değerlerini kâğıtta hesaplayıp doldur. `# TODO` yazan yerlerdeki `___` boşluklarını tamamla, sonra çalıştır.

```python {.python-playground-task}
def dikdortgen_cevresi(en, boy):
    # TODO: Çevre = 2 × (en + boy). Sonucu geri ver.
    return ___


# TODO: Beklenen değerleri kendin hesapla ve yaz.
assert dikdortgen_cevresi(3, 4) == ___
assert dikdortgen_cevresi(5, 5) == ___
print("İki test de başarılı.")
print("Çevreler:", dikdortgen_cevresi(3, 4), dikdortgen_cevresi(5, 5))
```
```text {.python-playground-expected}
İki test de başarılı.
Çevreler: 14 20
```
```text {.python-playground-help}
`return ___` | Dikdörtgenin çevresi iki kısa ve iki uzun kenarın toplamıdır: `2 × (en + boy)`.
`assert dikdortgen_cevresi(3, 4) == ___` | Beklenen sonucu önce kendin hesapla: `2 × (3 + 4)`. Kodun çıktısından kopyalama.
`assert dikdortgen_cevresi(5, 5) == ___` | Aynı işlemi `5` ve `5` için yap.
```
```python {.python-playground-solution}
def dikdortgen_cevresi(en, boy):
    # Çevre = 2 × (en + boy). Sonucu geri ver.
    return 2 * (en + boy)


# Beklenen değerleri kendin hesapla ve yaz.
assert dikdortgen_cevresi(3, 4) == 14
assert dikdortgen_cevresi(5, 5) == 20
print("İki test de başarılı.")
print("Çevreler:", dikdortgen_cevresi(3, 4), dikdortgen_cevresi(5, 5))
```

## 3. Kütüphaneyle yap

`assert` hızlı bir deneme için yararlıdır; ancak kalıcı testleri `unittest` gibi test araçlarıyla yazmak daha uygundur. Test aracı testleri bulur, çalıştırır ve sonuçları toplu gösterir.

`assert` ifadeleri Python `-O` (optimize) seçeneğiyle çalıştırıldığında kaldırılabilir. Bu nedenle programın çalışması için gerekli denetimleri `assert` ile yapma; kullanıcı girdilerini ayrıca doğrula.

## 4. Sık yapılan hatalar

- **Yalnızca kodu elle denemek.** Aynı örnekleri tekrar tekrar kontrol etmek yerine önemli durumlar için test yaz.
- **Beklenen değeri koddan kopyalamak.** Beklenen sonucu fonksiyonu çalıştırıp çıktısından alırsan, kod yanlışsa test de yanlışı “doğru” kabul eder. Beklenen değeri elle veya bağımsız bir yolla hesapla.
- **Hata mesajının ilk satırında takılı kalmak.** Önce son satırdaki hata adını ve satır numarasını bul.
- **Tüm kodu birden değiştirmek.** Bir küçük değişiklik yapıp testleri tekrar çalıştır; böylece hangi değişikliğin etkili olduğunu anlarsın.
- **`assert` ile kullanıcı girdisi denetlemek.** `assert` test içindir; gerekli çalışma kontrolleri normal `if` koşulları ve anlaşılır hata mesajlarıyla yapılmalıdır.
- **Bir testin geçmesini bütün programın kusursuz olduğuna kanıt saymak.** Test yalnızca sınadığı durumlar hakkında bilgi verir; yeni durumlar ekledikçe testleri de genişlet.

## 5. Pekiştir

**Quiz**

1. `assert` koşulu doğru değilse ne olur?
2. `NameError` genellikle neyi anlatır ve `print(renk)` satırı neden bu hatayı verebilir?
3. Bir testte beklenen sonucu kim belirlemelidir?
4. Neden iki farklı girdiyle aynı fonksiyonu sınarız?
5. `assert` ifadelerini kullanıcı girdilerini denetlemek için kullanmalı mıyız?

**Alıştırmalar**

1. Penceredeki alan fonksiyonuna `2` ve `8` girdilerini sınayan bir `assert` ekle.
2. Fonksiyonda `*` yerine `+` yaz; hangi testin başarısız olduğunu gözlemle ve düzelt.
3. `hesaplama.py` ve `test/test_hesaplama.py` dosyalarını oluşturup yerel test komutunu çalıştır.
4. `dikdortgen_alani` için negatif kenar uzunluğunda ne olmasını istediğini belirle; bu davranışı önce test olarak yaz, sonra uygula.
5. (İsteğe bağlı) Kendi fonksiyonlarından biri için sıfır, normal ve beklenmeyen giriş durumlarını sınayan testler ekle.

??? success "Quiz cevapları"
    1. Program `AssertionError` üretir ve o noktada durur.
    2. Python kullanılan adı bulamamıştır. `renk` değişkeni hiç tanımlanmadıysa, farklı yazıldıysa veya onu oluşturan hücre çalışmadıysa `print(renk)` bu hatayı verir.
    3. Programın gereksinimini ve doğru davranışı bilen kişi; beklenen değer tahmin edilmemelidir.
    4. Tek bir örnek, fonksiyonun yalnızca o girdide doğru çalıştığını gösterebilir.
    5. Hayır. Python `-O` seçeneğiyle çalıştırılınca `assert` satırları atlanır; kullanıcı girdileri için normal `if` koşulu ve hata yönetimi gerekir.

## Özet

Test, programın belirli girdilerde beklenen sonucu verip vermediğini kontrol eder; hata ayıklama ise sorun çıktığında nedenini bulmaya yardım eder. `assert` ile küçük bir koşulu sınayabilir, `unittest` ile testleri dosyada saklayıp tekrar çalıştırabilirsin. Test başarısız olduğunda hata türünü, satır numarasını ve o satırdaki değerleri incele. Testleri küçük ve anlamlı tut, her değişiklikten sonra yeniden çalıştır.

## Kaynaklar

- [Python öğreticisi: Hatalar ve istisnalar](https://docs.python.org/3/tutorial/errors.html)
- [Python `unittest` belgeleri](https://docs.python.org/3/library/unittest.html)
- [Python `assert` deyimi](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)
