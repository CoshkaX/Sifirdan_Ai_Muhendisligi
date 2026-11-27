# Sıfırdan Yapay Zeka Mühendisliği (Türkçe)

Yapay zekâ mühendisliğini **Türkçe**, **sıfırdan** ve **kendi ellerinle yazarak** öğrenmek için açık kaynak bir ders serisi. Hazır bir kütüphanenin fonksiyonunu çağırmak yerine, o fonksiyonun **içinde ne olduğunu** küçük ve anlaşılır kodlarla kurarsın; sonra aynı işi gerçek araçlarla yaparsın.

🌐 **Siteyi aç:** https://coshkax.github.io/Sifirdan_Ai_Muhendisligi/

> Dersler yazıldıkça [müfredat](docs/MUFREDAT.md) sayfasında ✅ ile işaretleniyor. Şu an **Faz 0–5 (37 ders)** hazır.

## Kimler için?

- Python'a yeni başladıysan ya da öğrenmeye hazırsan ve yapay zekâya girmek istiyorsan.
- Hazır kütüphaneleri kullanıyorsun ama altında ne olduğunu merak ediyorsan.
- Türkçe metinle çalışan bir arama, RAG ya da NLP uygulaması geliştirmek istiyorsan.

Başlamak için bir bilgisayar ve merak yeter. Matematik formülle değil kodla anlatılır; lise düzeyi cebir yeterlidir. GPU gerekmez.

## Neler var?

| Faz | Konu | Durum |
|---|---|---|
| 0 | Hazırlık: terminal, Python, Git, Jupyter, test, "yapay zekâ nedir?" | ✅ 6 ders |
| 1 | Matematik: vektör, matris, türev, olasılık, istatistik, entropi | ✅ 6 ders |
| 2 | Klasik makine öğrenmesi: regresyon, sınıflandırma, ölçme | ✅ 6 ders |
| 3 | Sinir ağları: nöron, otomatik türev, geri yayılım, PyTorch'a geçiş | ✅ 6 ders |
| 4 | Metin ve Türkçe NLP: tokenizer, biçimbilim, gömme, arama, duygu analizi | ✅ 7 ders |
| 5 | Transformer: dizi modelleme, attention, çok başlı attention, konum bilgisi, transformer bloğu, mini transformer | ✅ 6 ders |
| 6–13 | Küçük dil modeli, LLM API'leri, RAG, agent'lar, fine-tuning, değerlendirme, üretim, bitirme projeleri | ⬜ planlandı |

Ayrıntılı liste için [müfredata](docs/MUFREDAT.md), hedefine göre ders sırası için [öğrenme yollarına](docs/OGRENME-YOLLARI.md) bak.

## Her ders nasıl işlenir?

Her ders aynı dört adımı izler:

1. **Problem:** Somut bir sorunla başlarsın; neden bu konuyu öğrendiğini görürsün.
2. **Kendin yaz:** Sade kodla mekanizmayı kurarsın.
3. **Kütüphaneyle yap:** Aynı işi gerçek bir araçla (NumPy, scikit-learn, PyTorch...) yaparsın.
4. **Pekiştir:** Quiz ve alıştırmalarla öğrendiğini sınarsın.

### Sayfadaki kod pencereleri

Kodu kurulum yapmadan, sayfanın içinde çalıştırabilirsin (kod tarayıcında çalışır, hiçbir yere gönderilmez). İki tür pencere vardır:

- **Örnek:** Hazır kodu çalıştır, sonra bir değeri değiştirip çıktının nasıl değiştiğine bak. Anlamadığın satır için **Anlamadıysan bas** düğmesi kodu satır satır açıklar.
- **Kendin yaz:** Kod hazır gelir, eksik yerler kodun içinde boş kutu olarak durur. Kutulara yaz ve çalıştır; kodun geri kalanını değiştiremezsin. Çıktı doğruysa "✓ Başarılı" görürsün. Takılırsan **Yapamazsan buna bas** çözümün tamamını yeşil kodla ve açıklamasıyla gösterir.

Ayrıca metni seçip vurgulayabilir ve not alabilirsin; notların yalnızca kendi tarayıcında saklanır.

## Derslerin kodunu kendi bilgisayarında çalıştırmak

Bazı dersler tam bir kod dosyası ve test içerir (`kod/` ve `test/` klasörleri). Python 3.11 veya üstü gerekir:

```bash
git clone https://github.com/CoshkaX/Sifirdan_Ai_Muhendisligi.git
cd Sifirdan_Ai_Muhendisligi
```

Bir dersin kodunu ve testlerini çalıştırmak için (örnek):

```bash
cd docs/faz-04-metin-ve-turkce-nlp/01-metni-sayilara-cevirmek
python kod/tokenizer_demo.py
python -m unittest discover -s test
```

Bazı dersler NumPy, scikit-learn ya da PyTorch gibi paketler kullanır; hangisi gerektiği dersin başında yazar. Ayrıntılı kurulum için [0.1 dersine](docs/faz-00-hazirlik/01-gelistirme-ortami/README.md) bak.

## Siteyi kendi bilgisayarında görmek

```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdocs serve
```

Sonra tarayıcıda http://127.0.0.1:8000 adresini aç. Dosyaları değiştirdikçe sayfa kendiliğinden yenilenir.

## Proje yapısı

```text
docs/                         Siteye giren her şey
  faz-XX-faz-adi/
    NN-ders-adi/
      README.md               Ders metni
      kod/                    (varsa) bilgisayarda çalıştırılan tam kod
      test/                   (varsa) kodu doğrulayan testler
  MUFREDAT.md                 Ders listesi ve durumu
  SOZLUK.md                   Terim sözlüğü
  CONTRIBUTING.md             Katkı rehberi
  sablon/DERS-SABLONU.md      Yeni ders yazma şablonu
scripts/ornekleri_dogrula.py  Örnek ve görev çözümlerini denetler
mkdocs.yml                    Site yapılandırması ve menü
.github/workflows/            Testler ve siteyi yayınlama
```

## Katkı

Hata düzeltmek, yeni ders yazmak ya da "bunu anlamadım" demek bile değerli bir katkıdır. Nasıl yapılacağı için [katkı rehberine](docs/CONTRIBUTING.md), yeni ders için [ders şablonuna](docs/sablon/DERS-SABLONU.md) bak. Değişikliklerini göndermeden önce örneklerin hâlâ doğru çalıştığını denetle:

```bash
python scripts/ornekleri_dogrula.py
```

## Lisans

Bu proje MIT lisansı ile paylaşılmaktadır. Ayrıntılar için [LICENSE](LICENSE) dosyasına bak.
