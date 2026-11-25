# Sıfırdan Yapay Zeka Mühendisliği (Türkçe)

Yapay zekâ mühendisliğini **Türkçe**, **sıfırdan** ve **kendi ellerinle yazarak** öğrenmek için açık kaynak bir ders serisi.

🌐 **Site:** https://coshkax.github.io/Sifirdan_Ai_Muhendisligi/

> 🚧 Proje erken aşamada. Hangi derslerin hazır olduğunu görmek için [müfredata](docs/MUFREDAT.md) bak.

## Hızlı başlangıç

- Dersleri okumak için siteyi ya da [`docs/`](docs/) klasörünü kullan.
- `{.python-playground}` ile işaretlenmiş ders kodlarını sayfada düzenleyip çalıştır; ilk çalıştırmada Python çalışma zamanı tarayıcıya CDN üzerinden indirilir.
- Müfredat: [docs/MUFREDAT.md](docs/MUFREDAT.md)
- Katkı: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

Bir dersin kodunu çalıştırmak (örnek):

```bash
cd docs/faz-04-metin-ve-turkce-nlp/01-metni-sayilara-cevirmek
python kod/tokenizer_demo.py
python -m unittest discover -s test
```

## Siteyi kendi bilgisayarında görmek

```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdocs serve
```

Sonra tarayıcıda http://127.0.0.1:8000 adresini aç. Dosyaları değiştirdikçe sayfa kendiliğinden yenilenir.

## Lisans

Bu proje MIT lisansı ile paylaşılmaktadır. Ayrıntılar için [LICENSE](LICENSE) dosyasına bak.
