# Faz 0 – Ders 3: Git ve GitHub ile çalışmak

> ⏱️ Tahmini süre: 60-75 dk · 📚 Ön koşul: 0.1 Geliştirme ortamı · 💻 Gereksinim: Git, internet erişimi (GitHub adımları için)

## Bu derste ne öğreneceksin?

- Git ile dosyalardaki değişiklikleri kaydetmeyi
- `status`, `add`, `commit`, `diff` ve `log` komutlarını kullanmayı
- Yeni bir branch açıp değişiklikleri ayrı tutmayı
- GitHub'da fork ve pull request kavramlarını anlamayı
- Bir katkıyı küçük ve takip edilebilir adımlara bölmeyi

## 1. Problem

Bir Python dosyasını değiştirirken çalışan eski hâli kaybetmek kolaydır. Değişikliği ne zaman yaptığını, hangi satırı etkilediğini veya önceki hâle nasıl döneceğini hatırlamayabilirsin.

**Git**, dosyalardaki değişikliklerin geçmişini bilgisayarında tutar. **GitHub** ise Git depolarını internet üzerinde barındırır ve başkalarıyla birlikte çalışmayı kolaylaştırır. GitHub, Git'in kendisi değildir; Git olmadan da yerel geçmiş tutabilirsin.

Git'in temel akışını şöyle düşünebilirsin:

```text
Dosyaları düzenle → Değişikliği hazırlık alanına seç (stage) → Commit oluştur
```

Commit, seçtiğin dosyaların o andaki hâlini açıklayıcı bir mesajla geçmişe kaydeder. Tüm klasörü otomatik olarak commit etmezsin; önce hangi değişiklikleri ekleyeceğini seçersin.

## 2. Kendin yaz

### 2.1 Güvenli bir deneme deposu oluştur

Bu alıştırmayı ana projenin kopyasında değil, ayrı bir klasörde yap. Böylece deneme dosyaların ders deposuna karışmaz.

Önce ana proje klasörünün dışında olduğundan emin ol. 0.1'de proje klasörünü açtıysan PowerShell veya Git Bash'te `cd ~` ile ev dizinine geç; ardından `pwd` ile konumunu kontrol et. Proje deposunun içindeyken `mkdir git-alistirma` çalıştırırsan yeni bir Git deposunu yanlışlıkla projenin içine yerleştirebilirsin.

PowerShell, Terminal veya Git Bash'te aşağıdaki komutları sırayla çalıştır:

```bash
mkdir git-alistirma
cd git-alistirma
git init
git status
```

`git init`, mevcut klasörde yeni bir Git deposu başlatır. `git status`, henüz Git'in kaydetmediği dosya ve değişikliklerin durumunu gösterir. İlk kez commit oluştururken ad ve e-posta sorulursa 0.1 dersindeki `git config` adımlarını tamamla.

Şimdi klasörde `notlar.txt` adlı dosya oluştur ve içine şu satırı yaz:

```text
Git değişikliklerin geçmişini tutar.
```

Git'in dosyayı fark edip etmediğini kontrol et:

```bash
git status
```

Dosya **untracked** (izlenmeyen) olarak görünür. Bu, dosyanın klasörde bulunduğu ama henüz Git geçmişine eklenmediği anlamına gelir.

### 2.2 Değişikliği seç ve kaydet

```bash
git add notlar.txt
git status
git commit -m "İlk notu ekle"
git status
```

- `git add notlar.txt`, dosyanın o anki hâlini bir sonraki kayda seçer. Dosyayı silmez veya internete göndermez.
- `git commit -m "İlk notu ekle"`, seçilmiş değişikliği yerel geçmişe kaydeder. Tırnak içindeki mesaj, ne yaptığını kısa biçimde anlatır.
- Son `git status`, kaydedilmemiş başka değişiklik yoksa çalışma alanının temiz olduğunu söyler.

Commit mesajını dosya adı gibi değil, yapılan işi anlatan kısa bir not gibi yaz: `Ders 0.2 örneğini ekle` veya `Türkçe açıklamayı düzelt` gibi.

### 2.3 Farkı gör ve ikinci bir kayıt oluştur

`notlar.txt` dosyasına şu cümleyi ekle:

```text
Commit, seçtiğim değişikliği geçmişe kaydeder.
```

Kaydetmeden önce farkı incele:

```bash
git diff
```

`git diff`, son commit'ten beri çalışma klasöründeki değişikliği gösterir. Çıktıda `+` ile başlayan satırlar eklenen, `-` ile başlayan satırlar silinen içeriktir. Sonra değişikliği seçip kaydet:

```bash
git add notlar.txt
git diff --staged
git commit -m "Commit açıklamasını ekle"
git log --oneline
```

`git diff --staged`, bir sonraki commit'e girecek değişikliği gösterir. `git log --oneline` ise geçmiş kayıtlarını kısa biçimde listeler.

### 2.4 Dal (branch) ile ayrı bir çalışma alanı aç

Dal (branch), ana geçmişten ayrılan bağımsız bir çalışma çizgisidir. Yeni bir fikir üzerinde çalışırken ana dalı doğrudan değiştirmek yerine kendi dalını açabilirsin:

```bash
git switch -c notlara-ornek-ekle
git branch
```

`git switch -c` yeni dalı oluşturup ona geçer. `git branch` dalları listeler; yıldız (`*`) o anda çalıştığın dalı gösterir.

`notlar.txt` dosyasına yeni bir satır ekleyip kaydet. Sonra:

```bash
git status
git add notlar.txt
git commit -m "Notlara örnek ekle"
git log --oneline
```

Bu commit yeni dalın geçmişindedir. Ana dalın adı projeye göre `main` veya `master` olabilir. Hangi dalda olduğunu görmek için `git branch --show-current` çalıştır; geri dönmek istersen listede gördüğün ana dal adını `git switch` komutuna ver.

### 2.5 GitHub'da pull request aç

Değişiklik önerisi (pull request, PR), bir daldaki değişikliklerin ana projeye eklenmesi için incelemeye sunulur. Katkı süreci çoğunlukla şöyle ilerler:

1. GitHub'da katkı yapacağın projeyi **fork** et. Fork, deponun kendi hesabındaki kopyasıdır.
2. Kendi fork'unu bilgisayarına `git clone` ile indir.
3. Yeni bir branch aç: `git switch -c ders-aciklamasini-duzelt`.
4. Dosyada küçük bir değişiklik yap; `git diff` ile yalnızca beklediğin satırların değiştiğini kontrol et.
5. Değişikliği `git add` ve `git commit` ile kaydet, sonra `git push -u origin ders-aciklamasini-duzelt` ile fork'una gönder. `origin`, GitHub'daki deponun bilgisayarındaki kısa adıdır; `-u`, bu dalı GitHub'daki aynı adlı dalla eşleştirir. Böylece sonraki gönderimlerde yalnızca `git push` yazabilirsin. HTTPS ile gönderirken GitHub hesap parolan çalışmaz; kimlik doğrulama için Git Credential Manager'ın tarayıcı girişini kullan veya istendiğinde kişisel erişim belirteci (token) gir. Token'ı koda ya da commit'e koyma.
6. GitHub sayfasında **Compare & pull request** düğmesini kullan. Başlıkta neyi değiştirdiğini söyle; açıklamada nedenini ve varsa kontrol ettiğin sonucu yaz.

PR açmak değişikliği otomatik olarak ana projeye eklemez. Proje sorumluları önerini inceler, soru sorabilir veya düzenleme isteyebilir.

## 3. Kütüphaneyle yap

Git bir Python kütüphanesi değil, sürüm kontrol aracıdır. Bu nedenle bu dersin komutları tarayıcıdaki Python penceresinde çalıştırılamaz; onları bilgisayarındaki terminalde, `git-alistirma` klasöründe dene.

GitHub, Git depolarını barındırmanın yanı sıra issue, pull request ve kod inceleme araçları sunar. GitHub'a dosya göndermeden önce `git status` ve `git diff` ile ne göndereceğini kontrol et.

## 4. Sık yapılan hatalar

- **`git add` ile dosyayı GitHub'a göndereceğini sanmak.** `add` yalnızca bir sonraki yerel commit için değişikliği seçer.
- **Her değişikliği tek commit'te toplamak.** Küçük, tek konulu commit'leri incelemek ve geri almak daha kolaydır.
- **`git status` çıktısını okumadan devam etmek.** Bu komut hangi dalda olduğunu ve hangi dosyaların değiştiğini gösterir.
- **`.venv` klasörünü depoya eklemek.** Sanal ortam bilgisayara özeldir. Proje kökündeki `.gitignore` dosyası, Git'in hangi dosya ve klasörleri yok sayacağını söyler; içine `.venv/` ve `__pycache__/` ekleyerek bunların depoya gönderilmesini önle.
- **Ana dalda doğrudan çalışmak.** Deneme veya katkı için ayrı branch aç; PR'da neyin değiştiği daha net olur.
- **Commit mesajına belirsiz söz yazmak.** `değişiklik` yerine `UTF-8 örneğini düzelt` gibi somut bir mesaj kullan.
- **PR'ı değişiklikler kaydedilmeden açmak.** Önce commit oluştur, kendi branch'ine push et, sonra PR aç.

## 5. Pekiştir

**Quiz**

1. Git ile GitHub arasındaki fark nedir?
2. `git add` ve `git commit` hangi farklı işleri yapar?
3. `git diff` ve `git diff --staged` neyi gösterir?
4. Branch açmanın katkı sürecindeki yararı nedir?
5. Pull request açınca değişiklik ana projeye hemen eklenir mi?

**Alıştırmalar**

1. `git-alistirma` deposunda iki ayrı commit oluştur. `git log --oneline` ile ikisini de gör.
2. Dosyada bir satırı değiştir; önce `git diff`, sonra `git add` sonrasında `git diff --staged` çalıştır. Aradaki farkı açıkla.
3. Yeni bir branch açıp dosyaya bir satır ekle. `git branch --show-current` ile dal adını doğrula.
4. (İsteğe bağlı) GitHub'da kendi fork'unda bir branch açıp küçük bir yazım düzeltmesi için PR oluştur.

??? success "Quiz cevapları"
    1. Git değişiklik geçmişini yöneten araçtır; GitHub Git depolarını çevrimiçi barındırıp iş birliği sağlar.
    2. `add` değişikliği bir sonraki kayıt için seçer; `commit` seçilmiş değişikliği yerel geçmişe kaydeder.
    3. `diff` henüz seçilmemiş çalışma değişikliklerini; `diff --staged` seçilmiş, commit'e girecek değişiklikleri gösterir.
    4. Yeni çalışmayı ana daldan ayırır; böylece değişiklikler ayrı incelenip PR ile önerilebilir.
    5. Hayır. PR incelenir; proje sorumluları kabul ederse ana dala eklenir.

## Özet

Git, dosyaların yerel değişiklik geçmişini tutar; GitHub ise bu depolar üzerinde çevrimiçi iş birliğini sağlar. `status` ve `diff` ile neyin değiştiğini görür, `add` ile kayda alınacak kısmı seçer, `commit` ile geçmişe eklersin. Branch ayrı bir çalışma çizgisi açar; pull request bu çalışmayı incelemeye sunar. Küçük ve açıklayıcı değişiklikler, ekip çalışmasını kolaylaştırır.

## Kaynaklar

- [Git resmî kitabı: Git temelleri](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Docs: Fork kullanarak katkı yapma](https://docs.github.com/en/get-started/quickstart/contributing-to-projects)
- [GitHub Docs: Pull request oluşturma](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
