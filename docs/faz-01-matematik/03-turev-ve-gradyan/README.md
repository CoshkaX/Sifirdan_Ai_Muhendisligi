# Faz 1 – Ders 3: Türev ve gradyan

> ⏱️ Tahmini süre: 50-65 dk · 📚 Ön koşul: 0.2 Python hızlı tekrar ve temel cebir · 💻 Gereksinim: Python 3.11+; temel örnekler için ek paket gerekmez, PyTorch örneği için PyTorch kurulmalıdır

## Bu derste ne öğreneceksin?

- Bir fonksiyonun belirli bir noktadaki eğimini yaklaşık hesaplamayı
- Türevin fonksiyonun nasıl değiştiğini anlattığını
- Gradyan inişinin parametreleri kaybı azaltacak yönde güncellediğini
- Öğrenme hızının adım büyüklüğünü nasıl etkilediğini

## 1. Problem

Bir model tahmin yapar, tahmini gerçek değerle karşılaştırır ve ne kadar yanıldığını bir sayıyla ölçer. Bu hata ölçüsüne **kayıp** denir: kayıp ne kadar küçükse modelin tahmini o kadar iyidir. Eğitim sırasında modelin ayarlanabilir sayılarını, yani parametrelerini, değiştirip kaybı azaltmaya çalışırız.

Peki hangi yönde değişiklik yapacağımızı nasıl anlarız? Bir yokuşun eğimi, yukarı mı aşağı mı gittiğini ve ne kadar dik olduğunu anlatır. Bir fonksiyonun eğimi de girişteki küçük bir değişikliğin çıktıyı hangi yönde ve ne kadar değiştirdiğini söyler. Tek değişkenli durumda bu eğime **türev** deriz. Birden fazla parametre varsa her parametreye göre alınan türevleri birlikte **gradyan** olarak düşünürüz.

Bu derste önce türevi yaklaşık hesaplayacağız. Ardından, bir modelin ayarlanabilir sayısını kaybı azaltacak yönde nasıl değiştirdiğimizi küçük bir örnekle göreceğiz.

## 2. Kendin yaz

### 2.1 Eğimi küçük bir adımla tahmin et

Türevi önce yaklaşık olarak hesaplayalım. `f(x)`, `x` girdisi verildiğinde fonksiyonun ürettiği sonuç demektir. Örneğimizde `f(x)`, `kare(x)` fonksiyonudur. `x` değerini `h` kadar artırıp yeni ve eski sonuç arasındaki farkı bulur, bu farkı girişteki artış olan `h` değerine böleriz:

`eğim ≈ (f(x + h) - f(x)) / h`

Burada `h`, girişte yaptığımız küçük artıştır. `f(x) = x²` demek, `x` sayısını kendisiyle çarpmak demektir. `x = 3` ve `h = 0.001` seçersek eski sonuç `3 × 3 = 9`, yeni sonuç ise `3.001 × 3.001 = 9.006001` olur. Bu iki sonuç arasındaki farkı `0.001`'e böldüğümüzde yaklaşık `6.001` buluruz; iki basamağa yuvarlayınca `6.0` görünür.

```python {.python-playground}
def kare(x):
    return x * x


x = 3
h = 0.001
egim = (kare(x + h) - kare(x)) / h
print("Yaklaşık eğim:", round(egim, 2))
```
```text {.python-playground-expected}
Yaklaşık eğim: 6.0
```
```text {.python-playground-help}
`def kare(x):` | `x` sayısını alıp karesini hesaplayan bir fonksiyon tanımlarız; `x` bu fonksiyonun girdisidir.
`return x * x` | Sayıyı kendisiyle çarpıp sonucu geri verir; `kare(3)` çağrısının sonucu `9` olur.
`x = 3` | Eğimi inceleyeceğimiz noktayı seçeriz; burada fonksiyonun `3` çevresindeki değişimiyle ilgileniyoruz.
`h = 0.001` | Giriş değerine ekleyeceğimiz küçük miktarı belirleriz. Bu örnekte `x + h`, `3.001` olur.
`egim = (kare(x + h) - kare(x)) / h` | Yeni sonuçtan eski sonucu çıkarır, farkı `h`'ye böleriz. Bu değer `x = 3` çevresindeki yaklaşık eğimdir.
`print("Yaklaşık eğim:", round(egim, 2))` | `round(egim, 2)` sonucu iki ondalık basamağa yuvarlar; `print` hem açıklamayı hem de `6.0` değerini gösterir.
```

Bu yaklaşıma **sonlu fark** denir: fonksiyonun gerçek türevini cebirle çıkarmak yerine, iki yakın noktadaki sonuçları karşılaştırırız. Örneğin `h` değerini `0.1` yaparsan yaklaşık eğim `6.1` olur; adım büyüdüğü için yerel eğim daha kabaca tahmin edilir. Çalışma penceresindeki beklenen `6.0`, başlangıçtaki `h = 0.001` içindir. `h`'yi değiştirdiğinde çıktı farklı olur; pencerenin beklenen sonuç işaretinin değişmesi kodun çalışmadığı anlamına gelmez.

### 2.2 Gradyan inişiyle bir parametreyi güncelle

Şimdi tek bir ayarlanabilir sayı düşünelim: modelin **ağırlığı**. Bu örnekte hedefimiz ağırlığı `4` yapmak. Hedefe ne kadar uzak olduğumuzu ölçmek için şu kaybı kullanacağız:

`kayıp = (ağırlık - 4)²`

`²`, parantez içindeki sayıyı kendisiyle çarpmak demektir. Bu yüzden kayıp negatif olmaz: ağırlık `4` ise kayıp `0`; ağırlık `3` veya `5` ise kayıp `1` olur. Yani bu örnekte ağırlık `4`'e yaklaştıkça kayıp küçülür.

Bu kayıp fonksiyonunun türevi `2 × (ağırlık - 4)` olur. Önce bildiğimiz kare örneğine bakalım: `x` değerini `h` kadar artırırsak karedeki değişim oranı `((x + h)² - x²) / h = 2x + h` olur. `h` sıfıra yaklaşırken `2x + h`, `2x`'e yaklaşır; bu nedenle `x²` ifadesinin türevi `2x`'tir. Bizim kaybımızda `x` yerine `(ağırlık - 4)` bulunur. Ağırlık bir birim değiştiğinde bu parantezin içi de bir birim değiştiği için türev `2 × (ağırlık - 4)` olur. Bu türev, ağırlık azıcık değiştiğinde kaybın hangi yönde değişeceğini gösterir.

Gradyan inişinde her adımda türevi hesaplar ve ağırlığı ters yönde güncelleriz:

`yeni ağırlık = eski ağırlık - öğrenme hızı × türev`

Başlangıçta ağırlık `0` olduğundan türev `2 × (0 - 4) = -8` çıkar. Güncelleme `0 - 0.1 × (-8) = 0.8` olur. Eksi bir sayıyı çıkardığımız için ağırlık artar ve hedef olan `4`'e yaklaşır. Bir sonraki adım, eski `0` değerini değil yeni `0.8` değerini kullanır.

```python {.python-playground}
agirlik = 0.0
ogrenme_hizi = 0.1

for adim in range(5):
    gradyan = 2 * (agirlik - 4)
    agirlik = agirlik - ogrenme_hizi * gradyan

print("5 adım sonraki ağırlık:", round(agirlik, 2))
```
```text {.python-playground-expected}
5 adım sonraki ağırlık: 2.69
```
```text {.python-playground-help}
`agirlik = 0.0` | Modelin ayarlayacağımız parametresini başlangıçta sıfır seçeriz; başlangıç değeri hedef olan `4`ten uzaktır.
`ogrenme_hizi = 0.1` | Her güncellemede ne kadar büyük adım atılacağını belirler. Bu değer türevi çarpacağımız katsayıdır.
`for adim in range(5):` | `range(5)` döngüyü beş kez çalıştırır. `adim`, kaçıncı tekrarda olduğumuzu gösterir; bu örnekte ayrıca hesaplamada kullanılmaz.
`gradyan = 2 * (agirlik - 4)` | Bu örnekte kaybın türevini hesaplarız. Ağırlık `0` iken sonuç `-8` olur; eksi işaret ağırlığı artırmamız gerektiğini gösterir.
`agirlik = agirlik - ogrenme_hizi * gradyan` | Öğrenme hızı ile türevi çarpıp mevcut ağırlıktan çıkarırız. Sonucu aynı değişkene kaydettiğimiz için sonraki tekrar güncel ağırlıkla başlar.
`print("5 adım sonraki ağırlık:", round(agirlik, 2))` | Beş güncellemeden sonra ağırlığı iki ondalık basamakla gösteririz; sonuç `2.69` olur ve hedef olan `4`'e yaklaşır.
```

Bir parametre varsa onun için tek bir türev hesaplarız. Birden fazla parametre varsa her biri için ayrı türev bulunur; bu türevlerin oluşturduğu vektöre **gradyan** denir. Bu küçük örnekte tek parametre olduğu için gradyan tek bir sayıdır. Gerçek bir modelde çok sayıda parametre bulunabilir. Buradaki amaç, güncelleme fikrini küçük bir örnekte görmektir; üretim ölçeğinde model eğitmek değildir.

`ogrenme_hizi` değerini `0.01` yapıp beş adım sonra ne olduğunu dene: ağırlık yaklaşık `0.38` olur, yani hedefe daha yavaş yaklaşır. Bu özel örnekte `0.5` seçilirse ilk adım ağırlığı doğrudan `4`'e taşır; bu, `0.5` değerinin başka bir model veya kayıp için de uygun olacağı anlamına gelmez. Çok büyük bir adım hedefin ötesine sıçrayabilir ve kaybı azaltmak yerine artırabilir; bu yüzden öğrenme hızını dikkatli seçeriz. Değiştirdiğin değer için ekrandaki sonuç başlangıçtaki beklenen değerle aynı olmayabilir.

### Şimdi sen yaz: gradyan inişi adımları

Ağırlığı hedef olan `2`'ye yaklaştıran üç gradyan inişi adımı yaz. Sitede `___` yazan her yer yazılabilir bir kutu olur; `# TODO` notlarına bakarak kutuları doldur, sonra çalıştır.

```python {.python-playground-task}
agirlik = 10.0
ogrenme_hizi = 0.25

for adim in range(3):
    # TODO: Kayıp (agirlik - 2) ** 2 ise türevi 2 × (agirlik - 2)'dir.
    gradyan = ___
    # TODO: Ağırlığı gradyanın ters yönünde güncelle.
    agirlik = agirlik - ___ * gradyan
    print(f"Adım {adim + 1}: ağırlık = {agirlik}")
```
```text {.python-playground-expected}
Adım 1: ağırlık = 6.0
Adım 2: ağırlık = 4.0
Adım 3: ağırlık = 3.0
```
```text {.python-playground-help}
`gradyan = ___` | Türev formülü yorumda yazıyor: `2 × (agirlik - 2)`. Python'da `2 * (agirlik - 2)` yaz.
`agirlik = agirlik - ___ * gradyan` | Gradyan inişi: eski ağırlıktan öğrenme hızı × gradyan çıkarılır.
```
```python {.python-playground-solution}
agirlik = 10.0
ogrenme_hizi = 0.25

for adim in range(3):
    # Kayıp (agirlik - 2) ** 2 ise türevi 2 × (agirlik - 2)'dir.
    gradyan = 2 * (agirlik - 2)
    # Ağırlığı gradyanın ters yönünde güncelle.
    agirlik = agirlik - ogrenme_hizi * gradyan
    print(f"Adım {adim + 1}: ağırlık = {agirlik}")
```

## 3. Kütüphaneyle yap

Elle yazdığımız örnek, tek parametrenin gradyanını kendimiz hesapladı. PyTorch gibi kütüphaneler, daha karmaşık hesaplamalarda türevleri otomatik bulabilir. Bu özelliğe **otomatik türev alma** denir.

Bu örnek, tarayıcıdaki Python penceresinde çalışmaz; çünkü PyTorch ayrı kurulması gereken bir pakettir. Bilgisayarında denemek için resmî [PyTorch kurulum sayfasında](https://pytorch.org/get-started/locally/) işletim sistemine ve donanımına uygun komutu seçip çalıştır. Sanal ortam kullanıyorsan önce onu etkinleştir; böylece PyTorch kodu çalıştıracağın aynı Python ortamına kurulur. Sonra aşağıdaki kodu `turev_pytorch.py` adlı dosyaya kaydet, dosyanın bulunduğu klasörde terminal aç ve `python turev_pytorch.py` komutunu çalıştır. Bilgisayarında `python` komutu yoksa `python3 turev_pytorch.py` komutunu dene.

```python
import torch

agirlik = torch.tensor(0.0, requires_grad=True)
kayip = (agirlik - 4) ** 2
kayip.backward()

print(agirlik.grad.item())
```

Beklenen çıktı:

```text
-8.0
```

`torch.tensor(...)`, PyTorch'un sayılar üzerinde işlem yapabilen değerini oluşturur. Python'da `** 2`, sayının karesini alır. `requires_grad=True`, ağırlığın türevini izlememizi sağlar. `kayip.backward()` türevi hesaplar ve `agirlik.grad` içinde saklar; **ağırlığı kendiliğinden güncellemez**. `agirlik.grad.item()` hesaplanan türevi alır ve ekrana yazılabilecek normal bir sayıya çevirir. Bu örnekte `-8.0`, ağırlık `0` iken kaybın türevidir. Elle yazdığımız güncelleme fikri, sonraki derslerde küçük bir sinir ağı kurarken tekrar kullanılacak.

## 4. Sık yapılan hatalar

- **Türevi her noktada aynı sanmak.** Tek değişkenli bir fonksiyonun belirli bir noktadaki türevi bir sayıdır, ancak başka noktada bu sayı değişebilir. Örneğin `x²` fonksiyonunun `x = 2` noktasındaki eğimi `4`, `x = 3` noktasındaki eğimi `6`'dır.
- **Gradyanın yönünü ters kullanmak.** Kayıp azaltmak için küçük adımlarla gradyanın ters yönüne gideriz. Bu örnekte gradyan `-8` olduğu için onu çıkarmak ağırlığı artırır.
- **Öğrenme hızını türevle karıştırmak.** Türev yön ve yerel değişim hakkında bilgi verir; öğrenme hızı bu yönde atılan adımın büyüklüğünü belirler.
- **Öğrenme hızını sıfır veya aşırı büyük seçmek.** Sıfır seçilirse ağırlık hiç değişmez; aşırı büyük seçilirse hedefin ötesine geçip kaybı artırabilir.
- **Her adımda eski ağırlığı kullanmak.** Yeni ağırlık değişkene yazılmazsa döngü aynı değeri tekrar tekrar hesaplar.
- **Yaklaşık türevi tam sonuç sanmak.** Sonlu fark hesabı seçilen `h` değerine bağlı bir yaklaşımdır; burada yuvarlama da gösterilen basamakları etkiler.
- **`h` değerini sıfır yapmak.** Formülde değişimi `h`'ye böldüğümüz için `h = 0` olamaz; sıfıra bölme işlemi yapılamaz.
- **Her fonksiyonun kolayca en küçük değere ulaşacağını varsaymak.** Bu örnek basit bir kayba sahiptir. Gerçek modellerde adım çok büyükse kayıp artabilir; daha karmaşık kayıplarda gradyan inişi hedeflenen en iyi sonuca ulaşmayı da garanti etmez.

## 5. Pekiştir

**Quiz**

1. Türev, bir fonksiyon hakkında hangi tür bilgiyi verir?
2. Gradyan inişinde türevi neden ağırlıktan çıkarıyoruz?
3. Öğrenme hızı çok küçük seçilirse ne olabilir?
4. Sonlu fark yaklaşımında `h` neyi temsil eder?

**Alıştırmalar**

1. İlk örnekte `x` değerini `2` yap ve yaklaşık eğimin nasıl değiştiğini gözlemle; yaklaşık sonuç `4.0` olmalıdır.
2. Gradyan inişi örneğinde tur sayısını `10` yap. Ağırlık `4`e yaklaşıyor mu?
3. Öğrenme hızını `0.01` ve `0.5` yapıp sonuçları karşılaştır. Hangisi daha yavaş ilerliyor?
4. (İsteğe bağlı) Kayıp fonksiyonunu `(agirlik - 2) ** 2` olarak değiştir. Türev formülünü de buna uygun düzenleyip ağırlığın `2`ye yaklaştığını doğrula.

??? success "Quiz cevapları"
    1. Fonksiyonun seçilen noktada ne yönde ve ne hızla değiştiğini.
    2. Gradyan, küçük bir değişikliğin kaybı hangi yönde artıracağını gösterir. Ters yönde ve uygun büyüklükte adım atmak kaybı azaltmaya çalışır.
    3. Güncellemeler hedefe doğru ilerler ama daha fazla adım gerekebilir.
    4. Giriş değerinde yaptığımız küçük artışı temsil eder.

## Özet

Türev, bir fonksiyonun belirli bir noktadaki değişim hızını anlatır. Sonlu fark yaklaşımı, küçük bir giriş değişikliğinin çıktıyı nasıl etkilediğine bakarak türevi yaklaşık hesaplar. Gradyan inişi, parametreleri türevin gösterdiği yönün tersine ve öğrenme hızının belirlediği büyüklükte günceller. Bu fikir, bir modelin kaybını azaltarak öğrenmesinin temel parçalarından biridir.

## Kaynaklar

- [Khan Academy: Türevlere giriş](https://www.khanacademy.org/math/differential-calculus/dc-diff-intro)
- [PyTorch: Otomatik türev alma](https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)
