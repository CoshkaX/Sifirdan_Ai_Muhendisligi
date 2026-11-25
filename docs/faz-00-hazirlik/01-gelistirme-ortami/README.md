# Faz 0 – Ders 1: Geliştirme ortamını kurmak

> ⏱️ Tahmini süre: 60-90 dk · 📚 Ön koşul: yok · 💻 Gereksinim: bir bilgisayar (Windows, macOS veya Linux) ve internet

## Bu derste ne öğreneceksin?

- Terminal nedir, nasıl açılır, hangi temel komutlar yeterlidir
- Python'u kurmayı ve doğru kurulduğunu kontrol etmeyi
- Bir kod editörü (VS Code) hazırlamayı
- Git ile bu projeyi bilgisayarına indirmeyi
- Sanal ortam (virtual environment) oluşturmayı ve neden gerektiğini
- İlk Python dosyanı yazıp çalıştırmayı ve bir hata mesajını okumayı

## 1. Problem

Yapay zekâ kodu yazmadan önce, kodu **çalıştıracak bir yere** ihtiyacın var. Yeni başlayanların çoğu ilk engeli algoritmada değil, kurulumda yaşar: "python bulunamadı", "komut tanınmıyor", "paket yüklü ama import edemiyorum".

Bu ders o engelleri baştan temizler. Dersin sonunda şunu yapabiliyor olacaksın: terminali açıp projenin klasörüne girmek, bir Python dosyasını çalıştırmak ve bir şey ters giderse hata mesajından nedenini bulmak.

!!! info "Hiçbir şey kurmak istemiyorsan"
    [Google Colab](https://colab.research.google.com) ile tarayıcıda da başlayabilirsin (Ders 0.4'te anlatacağız). Ama uzun vadede kendi bilgisayarında çalışmak daha öğreticidir ve internet olmadan da çalışabilirsin.

## 2. Terminal

Terminal, bilgisayara **yazıyla** komut verdiğin penceredir. Fare yerine klavye kullanırsın. İlk başta tuhaf gelir ama programcılığın temel aracıdır.

### 2.1 Terminali aç

| Sistem | Nasıl açılır? |
|---|---|
| **Windows** | Başlat menüsüne "PowerShell" veya "Terminal" yaz ve aç |
| **macOS** | Spotlight'ta (`Cmd + Boşluk`) "Terminal" yaz |
| **Linux** | `Ctrl + Alt + T` (dağıtıma göre değişebilir) |

### 2.2 Temel komutlar

Terminal her zaman bir **klasörde** çalışır. Aşağıdaki komutlar, o klasörde gezinmeni sağlar:

| Komut | Ne yapar? | Örnek |
|---|---|---|
| `pwd` | Şu an hangi klasördesin? | `pwd` |
| `ls` | Klasördeki dosyaları listeler (Windows CMD'de `dir`) | `ls` |
| `cd klasor` | Klasöre girer | `cd Masaüstü` |
| `cd ..` | Bir üst klasöre çıkar | `cd ..` |
| `mkdir klasor` | Yeni klasör oluşturur | `mkdir yz-calisma` |

İki ipucu hayatını kolaylaştırır:

- **Tab tuşu** yazdığın adı tamamlar. `cd Mas` yazıp `Tab`'a bas.
- **Yukarı ok** önceki komutu geri getirir.

!!! warning "Boşluk ve Türkçe karakter içeren klasör adları"
    Klasör adında boşluk varsa tırnak içine al: `cd "Benim Projelerim"`. Kurulumla uğraşırken ilk başta Türkçe karakter içermeyen kısa klasör adları (`yz-calisma` gibi) kullanmak sorunları azaltır.

**Küçük deneme:** Terminalde şunları sırayla çalıştır.

```bash
mkdir yz-calisma
cd yz-calisma
pwd
```

`pwd` çıktısı, yeni klasörünün tam yolunu göstermelidir.

## 3. Python kurulumu

Bu seri için **Python 3.11 veya daha yenisi** gerekiyor.

=== "Windows"

    1. [python.org/downloads](https://www.python.org/downloads/) adresinden son sürümü indir.
    2. Kurulum ekranının **ilk sayfasında** "Add python.exe to PATH" kutusunu **mutlaka işaretle**.
    3. "Install Now" de.
    4. Yeni bir PowerShell aç (eski pencereler değişikliği görmez) ve kontrol et:

    ```powershell
    python --version
    ```

    `python` çalışmazsa `py --version` dene.

=== "macOS"

    1. [python.org/downloads](https://www.python.org/downloads/) adresinden macOS yükleyicisini indir ve kur. (Homebrew kullanıyorsan `brew install python` de olur.)
    2. Terminalde kontrol et:

    ```bash
    python3 --version
    ```

=== "Linux (Ubuntu/Debian)"

    ```bash
    sudo apt update
    sudo apt install python3 python3-venv python3-pip
    python3 --version
    ```

Windows ve macOS'ta seçtiğin güncel kurulum bu şartı karşılamalıdır. Ubuntu/Debian'da `apt` ile gelen Python sürümü dağıtımın sürümüne göre değişebilir. `python3 --version` sonucu 3.11'den eskiyse dersler için henüz uygun sürüm yok demektir; sistemin kullandığı Python'u silip değiştirme. Bilgisayarına kurulum yapmak istemiyorsan 0.4 dersindeki Colab ile devam edebilirsin. Yerel kurulum gerekiyorsa dağıtımına uygun adımlar için [Python'ın Unix kurulum belgesine](https://docs.python.org/3/using/unix.html) bak ve en son `python3 --version` ile sürümü yeniden kontrol et.

!!! note "PATH nedir?"
    PATH, işletim sisteminin programları aradığı klasörlerin listesidir. Python PATH'te değilse terminale `python` yazdığında "bulunamadı" der. Windows'ta kurulumda PATH kutusunu işaretlemek bu yüzden önemli.

## 4. Kod editörü

Python dosyalarını Not Defteri ile de yazabilirsin ama bir editör renklendirme, hata uyarısı ve otomatik tamamlama sağlar. Başlangıç için [Visual Studio Code](https://code.visualstudio.com/) iyi bir seçimdir.

1. VS Code'u kur.
2. Soldaki "Extensions" (eklentiler) bölümünden **Python** eklentisini (Microsoft) kur.
3. `Dosya → Klasör Aç` ile `yz-calisma` klasörünü aç.

Dosyaları **UTF-8** olarak kaydetmen önemlidir, aksi halde Türkçe karakterler bozulabilir. VS Code'da varsayılan zaten UTF-8'dir; sağ alttaki durum çubuğunda "UTF-8" yazdığını kontrol edebilirsin.

## 5. Git ve projeyi indirmek

Git, kodun sürümlerini takip eden bir araçtır. Bu dersteki tek amacımız projeyi indirmek; Git'i ayrıntılı olarak Ders 0.3'te öğreneceğiz.

1. [git-scm.com/downloads](https://git-scm.com/downloads) adresinden kur.
2. Terminali **kapatıp yeniden aç**, sonra kontrol et:

    ```bash
    git --version
    ```

3. Kimliğini tanıt (commit'lerde adın görünür). Bunu bir kez yapman yeter:

    ```bash
    git config --global user.name "Adın Soyadın"
    git config --global user.email "mail@ornek.com"
    ```

4. Projeyi indir:

    ```bash
    git clone https://github.com/CoshkaX/Sifirdan_Ai_Muhendisligi.git
    cd Sifirdan_Ai_Muhendisligi
    ```

    İlk komut projeyi bilgisayarına kopyalar, ikincisi proje klasörüne girer.

## 6. Sanal ortam (virtual environment)

### Neden gerekli?

Her Python projesi farklı paketlere (ve farklı paket sürümlerine) ihtiyaç duyar. Hepsini tek bir yere kurarsan bir proje diğerini bozabilir. **Sanal ortam**, her proje için ayrı ve izole bir paket alanı oluşturur.

### Oluştur ve etkinleştir

Proje klasöründeyken:

```bash
python -m venv .venv
```

(macOS/Linux'ta `python3 -m venv .venv`.) Bu komut `.venv` adlı bir klasör oluşturur. Sonra ortamı **etkinleştir**:

| Sistem | Komut |
|---|---|
| macOS / Linux | `source .venv/bin/activate` |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows CMD | `.venv\Scripts\activate.bat` |

Etkinleşince satırın başında `(.venv)` yazar. Kapatmak için `deactivate` yaz.

!!! warning "Windows PowerShell'de 'betik çalıştırma devre dışı' hatası"
    Bu hatayı alırsan PowerShell'de şu komutu bir kez çalıştırıp tekrar dene:

    ```powershell
    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
    ```

    Bu, yalnızca senin kullanıcın için yerel betiklere izin verir. Komut istemi (CMD) kullanmak da bir alternatiftir.

### Paket kurmak

Sanal ortam **etkinken** `pip` ile paket kurulur. İlk fazlarda ek paket gerekmiyor, ama nasıl yapıldığını görelim:

```bash
pip install requests   # örnek bir paket
pip list               # kurulu paketleri göster
```

Ortamı kapatıp başka bir ortamda `pip list` yaparsan `requests`'i görmezsin; işte izolasyon budur.

## 7. İlk Python dosyan ve ilk hatan

Önce kodu aşağıdaki pencerede dene. Bu pencere tarayıcıda çalışır ve bilgisayarında dosya oluşturmaz. Sonra aynı kodu VS Code'da `yz-calisma` klasörüne `merhaba.py` adıyla kaydet.

```python {.python-playground}
isim = "dünya"
print(f"Merhaba, {isim}!")
print("Türkçe karakterler: ç ğ ı ö ş ü İ")
```
```text {.python-playground-expected}
Merhaba, dünya!
Türkçe karakterler: ç ğ ı ö ş ü İ
```
```text {.python-playground-help}
`isim = "dünya"` | Tırnak içindeki `"dünya"` metnini `isim` adlı değişkene kaydederiz; aşağıdaki satır bu değeri kullanacak.
`print(f"Merhaba, {isim}!")` | `f` metni, süslü parantez içindeki `isim` değerini cümleye ekler; `print` cümleyi ekranda gösterir.
`print("Türkçe karakterler: ç ğ ı ö ş ü İ")` | Tırnak içindeki yazıyı aynen gösterir. Türkçe harfler düzgün görünüyorsa Python dosyan UTF-8 metni doğru okuyordur.
`isim = "dünya"` | `"dünya"` yerine kendi adını yazıp yeniden çalıştır; ilk `print` satırındaki selam da değişmelidir.
```

Terminalde o klasördeyken çalıştır (macOS/Linux'ta `python` yerine `python3` yaz):

```bash
python merhaba.py
```

Beklenen çıktı:

```
Merhaba, dünya!
Türkçe karakterler: ç ğ ı ö ş ü İ
```

### Hata mesajını okumak

Şimdi bilerek bir hata yapalım. `hata.py` adlı bir dosya oluşturup aşağıdaki kodu yaz. Kod, hiç tanımlanmamış `isim` adını kullandığı için hata verecek; bu beklenen bir durum.

```python
ad = "Ayşe"
print(f"Merhaba, {isim}!")
```

Çalıştırınca şuna benzer bir çıktı alırsın:

```
Traceback (most recent call last):
  File "hata.py", line 2, in <module>
    print(f"Merhaba, {isim}!")
NameError: name 'isim' is not defined
```

Hata mesajını **aşağıdan yukarıya** oku:

1. **Son satır:** hatanın türü ve nedeni. `NameError: name 'isim' is not defined` demek "isim diye bir değişken tanımlamamışsın".
2. **Üstündeki satırlar:** hatanın hangi dosyada ve hangi satırda olduğu (`line 2`).

Burada değişkeni `ad` diye tanımlayıp `isim` diye kullandık. Hata mesajını okumak, programcılığın en değerli alışkanlığıdır: mesaj genellikle sorunun nerede olduğunu doğrudan söyler.

## 8. Kurulumun tam olduğunu kontrol et

Aşağıdakilerin hepsini yapabiliyorsan hazırsın:

- [ ] Terminali açıp `pwd`, `ls`, `cd` kullanabiliyorum
- [ ] `python --version` (veya `python3 --version`) 3.11+ gösteriyor
- [ ] `git --version` bir sürüm gösteriyor
- [ ] Projeyi `git clone` ile indirdim
- [ ] Sanal ortam oluşturup etkinleştirebiliyorum (`(.venv)` görünüyor)
- [ ] `merhaba.py` dosyasını çalıştırıp Türkçe karakterleri doğru gördüm
- [ ] `hata.py` çıktısındaki hata türünü ve satır numarasını söyleyebiliyorum

## 9. Sık yapılan hatalar

| Belirti | Olası neden | Çözüm |
|---|---|---|
| `python: command not found` / "Python bulunamadı" | Windows'ta PATH işaretlenmedi ya da macOS/Linux'ta komut `python3` | Python'u yeniden kurup PATH kutusunu işaretle; `python3` dene; `py` dene |
| Windows'ta `python` yazınca Microsoft Store açılıyor | Uygulama yürütme takma adı komutu Store'a yönlendiriyor olabilir | Ayarlar → Uygulamalar → Gelişmiş uygulama ayarları → Uygulama yürütme takma adları bölümünde `python.exe` ve `python3.exe` takma adlarını kapat. Yeni bir PowerShell açıp `py --version` ile Python'u kontrol et. |
| Kurulumdan sonra komut hâlâ tanınmıyor | Terminal eski ortamı kullanıyor | Terminali kapatıp yeniden aç |
| `(.venv)` görünmüyor | Ortam etkinleştirilmemiş | Etkinleştirme komutunu çalıştır (bölüm 6) |
| Paketi kurdum ama `import` hata veriyor | Paket başka bir Python'a kurulmuş | Sanal ortamın etkin olduğundan emin ol, `pip` yerine `python -m pip install ...` dene |
| Türkçe karakterler `?` veya garip işaretler | Dosya UTF-8 kaydedilmemiş ya da terminal kodlaması farklı | Dosyayı UTF-8 kaydet; Windows'ta Windows Terminal kullanmayı dene |
| `git clone` hata veriyor | Git kurulu değil ya da internet yok | `git --version` ile kontrol et |

## 10. Pekiştir

**Quiz**

1. `cd ..` komutu ne yapar?
2. Sanal ortam neden kullanılır?
3. Python hata mesajında önce hangi satıra bakmalısın?
4. Windows'ta Python kurulumunda "Add python.exe to PATH" kutusu neden önemlidir?
5. `(.venv)` yazısının satır başında görünmesi ne anlama gelir?

**Alıştırmalar**

1. Masaüstünde `yz-calisma` adlı bir klasör oluştur, içine gir ve `pwd` ile konumunu doğrula.
2. İkinci bir sanal ortam (`.venv2`) oluşturup etkinleştir. `pip list` çıktısında yalnızca `pip` (Python sürümüne göre `setuptools` da) bulunduğunu, `requests` paketinin ise bu ortama kurulmadığını kontrol et; sonra `deactivate` ile ortamı kapat.
3. `merhaba.py` dosyasını kendi adını ve doğum yılından hesapladığın yaşını yazdıracak şekilde değiştir.
4. (İsteğe bağlı) `hata.py` dosyasında hatayı düzelt. Sonra bilerek farklı bir hata yap (örn. `print("merhaba"` — parantezi kapatma) ve Python'un bu sefer hangi hata türünü verdiğini oku.

## Özet

Bu derste terminali, Python'u, bir editörü, Git'i ve sanal ortamı kurdun; ilk betiğini çalıştırdın ve bir hata mesajını nasıl okuyacağını öğrendin. Bundan sonraki her dersin ortak zemini bu araçlar. Takıldığın bir adım olursa bir "anlamadım" issue'su aç: bu ders onunla iyileşecek.

## Kaynaklar

- Python resmî dokümanı: "Virtual Environments and Packages" öğreticisi (docs.python.org)
- Python resmî dokümanı: "Using Python on Windows / Unix / macOS" bölümleri
- Pro Git kitabı (ücretsiz, Türkçe çevirisi de mevcut): git-scm.com/book
- Visual Studio Code: "Python in Visual Studio Code" dokümanı (code.visualstudio.com)

??? success "Quiz cevapları"
    1. Bir üst klasöre çıkar.
    2. Her projenin paketlerini birbirinden ayırmak ve sürüm çakışmalarını önlemek için.
    3. Önce son satıra (hatanın türü ve nedeni), sonra hangi dosyada ve hangi satırda olduğuna.
    4. PATH'te olmazsa terminal `python` komutunu bulamaz.
    5. Sanal ortamın o terminal oturumunda etkin olduğu anlamına gelir; kurduğun paketler o ortama gider.
