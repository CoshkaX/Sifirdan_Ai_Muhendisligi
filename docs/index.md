# Sıfırdan Yapay Zeka Mühendisliği

**Yapay zekâ mühendisliğini Türkçe, sıfırdan ve kendi ellerinle yazarak öğren.**

Bu seri açık kaynaktır, ücretsizdir ve her dersin çalışan, test edilmiş kodu vardır. Amaç, bir kütüphanenin fonksiyonunu çağırmayı değil, o fonksiyonun **içinde ne olduğunu** anlamaktır.

!!! warning "Proje erken aşamada"
    Dersler yazıldıkça [müfredat](MUFREDAT.md) sayfasında ✅ ile işaretleniyor. Şu an hazır olan dersler: [0.1 Geliştirme ortamı](faz-00-hazirlik/01-gelistirme-ortami/README.md), [0.6 Yapay zekâ nedir?](faz-00-hazirlik/06-yapay-zeka-nedir/README.md) ve [4.1 Metni sayılara çevirmek](faz-04-metin-ve-turkce-nlp/01-metni-sayilara-cevirmek/README.md).

## Neden böyle bir seri?

Birçok kaynak sana hazır bir kütüphaneyi gösterir: üç satır kod yazarsın, model çalışır. Ama bir şey ters gittiğinde ne yapacağını bilmezsin. Kayıp neden düşmüyor? Model neden saçmalıyor? Arama neden yanlış belgeyi getiriyor?

Bu seride her konuyu önce **küçük ve sade bir sürümle kendin yazarsın**: tokenizer, attention, agent döngüsü. Sonra aynı işi gerçek araçlarla yaparsın. Kütüphaneye geldiğinde, onun senin yazdığının büyüğü olduğunu bilirsin.

İkinci neden: İngilizce kaynaklar Türkçe'nin kendine özgü problemlerini genellikle anlatmaz. Türkçe ekli bir dildir; bir kökten yüzlerce kelime biçimi türer. Bu, tokenizer'ı, arama kalitesini ve embedding'leri etkiler. Bu seri bu konuları ayrı dersler olarak işler.

## Bu seri kimin için?

- Python'a başlangıç düzeyinde aşinasın (ya da öğrenmeye hazırsın) ve yapay zekâ mühendisliğine girmek istiyorsun.
- Hazır kütüphaneleri kullanıyorsun ama altında ne olduğunu merak ediyorsun.
- Türkçe veriyle çalışan bir RAG, agent ya da NLP uygulaması geliştirmek istiyorsun.

!!! note "Ön koşullar"
    Başlamak için tek şart bir bilgisayar ve merak. Faz 0, kod yazmak için gereken ortamı sıfırdan kurdurur. Matematik Faz 1'de kod üzerinden anlatılır; lise düzeyi cebir yeterli bir başlangıçtır.

## Her ders aynı 4 adımı izler

| Adım | Ne yaparsın? | Neden? |
|---|---|---|
| **1. Problem** | Somut bir sorunla başlarsın | Neden bu konuyu öğrendiğini görürsün |
| **2. Kendin yaz** | Framework'süz, sade kod yazarsın | Mekanizmayı gerçekten anlarsın |
| **3. Kütüphaneyle yap** | Aynı işi gerçek araçlarla yaparsın | Üretimde nasıl kullanıldığını görürsün |
| **4. Pekiştir** | Quiz ve alıştırmalar çözersin | Öğrendiğini sınarsın |

Her dersin başında tahmini süre, ön koşul ve gereken araçlar yazar. Her dersin kodu `kod/` klasöründe, testi `test/` klasöründedir. Testler, kodun gerçekten çalıştığını kanıtlar.

## Müfredata genel bakış

| Bölüm | Fazlar | Ne öğrenirsin? |
|---|---|---|
| **Temeller** | 0-3 | Ortam kurulumu, matematik, klasik makine öğrenmesi, sinir ağları ve geri yayılım |
| **Dil modelleri** | 4-6 | Metin işleme, Türkçe NLP, transformer, sıfırdan küçük bir dil modeli |
| **Uygulama** | 7-10 | LLM API'leri, RAG, agent'lar, fine-tuning |
| **Mühendislik** | 11-13 | Değerlendirme, üretime alma, bitirme projeleri |

Ayrıntılı ders listesi için [müfredata](MUFREDAT.md) bak.

## Nereden başlamalıyım?

| Durumun | Önerilen yol |
|---|---|
| Hiç kod yazmadım | [Faz 0](faz-00-hazirlik/01-gelistirme-ortami/README.md) ile başla, sırayla ilerle |
| Python biliyorum, yapay zekâya yeniyim | Faz 1 (matematik) → 2 → 3 |
| Sadece LLM uygulamaları geliştirmek istiyorum | Faz 7 → 8 → 9 → 11 → 12 |
| Türkçe NLP ile ilgileniyorum | Faz 4 → 5 → 6 → 8 → 10 |

## Kodları çalıştırmak

Her dersin kodu ek kurulum gerektirmeden çalışacak şekilde yazılır. Gerekiyorsa dersin başında hangi paketin kurulacağı belirtilir. Örnek olarak 4.1 dersinin kodunu çalıştıralım:

```bash
cd faz-04-metin-ve-turkce-nlp/01-metni-sayilara-cevirmek
python kod/tokenizer_demo.py
python -m unittest discover -s test
```

GPU'n yoksa sorun değil. Dersler CPU'da ya da ücretsiz Colab/Kaggle ortamında çalışacak şekilde tasarlanır.

## Sık sorulan sorular

??? question "Matematik bilmiyorum, yapabilir miyim?"
    Evet. Faz 1 matematiği formülle değil, kodla ve örnekle anlatır. Lise düzeyi cebir yeterli bir başlangıçtır. Takıldığın yeri bir "anlamadım" issue'su olarak yaz, ders iyileştirilir.

??? question "GPU'm yok, sorun olur mu?"
    Hayır. Derslerin çoğu CPU'da çalışır. GPU gereken derslerde ücretsiz Colab veya Kaggle kullanacağız ve bunu dersin başında belirteceğiz.

??? question "İngilizce bilmem gerekir mi?"
    Dersler Türkçe. Ama makaleler ve resmî dokümanlar çoğunlukla İngilizce olduğundan, her dersin "Kaynaklar" bölümünde bunları da veriyoruz. Mesleki olarak ilerlerken İngilizce okumak sana yardımcı olacaktır.

??? question "Ücretli mi? Sertifika veriyor mu?"
    Tamamen ücretsiz ve açık kaynak. Sertifika vermiyoruz; amaç gerçek bir beceri kazandırmak.

??? question "Bir hata buldum ya da bir yeri anlamadım."
    GitHub'da bir issue aç. "Bunu anlamadım" issue'ları da değerli katkıdır, çünkü dersin yazarı çoğu zaman neyin anlaşılmaz olduğunu fark etmez.

## Katkı

Hata düzeltmek, ders yazmak ya da bir konu önermek istersen [katkı rehberine](CONTRIBUTING.md) bak.

## Lisans

Bu proje MIT lisansı ile paylaşılmaktadır. Kodları ve metinleri, lisans metnindeki şartlara uyarak kullanabilir ve dağıtabilirsin.
