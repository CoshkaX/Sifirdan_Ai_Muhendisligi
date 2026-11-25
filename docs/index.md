# Sıfırdan Yapay Zeka Mühendisliği

**Yapay zekâ mühendisliğini Türkçe, sıfırdan ve kendi ellerinle yazarak öğren.**

Bu seri açık kaynaktır, ücretsizdir ve her dersin çalışan, test edilmiş kodu vardır. Amaç, bir kütüphanenin fonksiyonunu çağırmayı değil, o fonksiyonun **içinde ne olduğunu** anlamaktır.

!!! warning "Proje erken aşamada"
    Dersler yazıldıkça [müfredat](MUFREDAT.md) sayfasında ✅ ile işaretleniyor. Şu an **Faz 0** (hazırlık), **Faz 1** (matematik) ve **Faz 2** (klasik makine öğrenmesi) tamamlandı; **Faz 4**\'ün ilk üç dersi hazır. İlk kez geliyorsan [0.1 Geliştirme ortamı](faz-00-hazirlik/01-gelistirme-ortami/README.md) dersinden başla.

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

Her dersin başında tahmini süre, ön koşul ve gereken araçlar yazar. Uygun örnekler sayfada düzenlenip çalıştırılabilir; yerel dosya veya test gerektiren dersler bunları ayrıca belirtir. Testler, sınadıkları davranışın beklendiği gibi çalışıp çalışmadığını kontrol eder.

## Müfredata genel bakış

| Bölüm | Fazlar | Ne öğrenirsin? |
|---|---|---|
| **Temeller** | 0-3 | Ortam kurulumu, matematik, klasik makine öğrenmesi, sinir ağları ve geri yayılım |
| **Dil modelleri** | 4-6 | Metin işleme, Türkçe NLP, transformer, sıfırdan küçük bir dil modeli |
| **Uygulama** | 7-10 | LLM API'leri, RAG, agent'lar, fine-tuning |
| **Mühendislik** | 11-13 | Değerlendirme, üretime alma, bitirme projeleri |

Ayrıntılı ders listesi için [müfredata](MUFREDAT.md) bak.

## Nereden başlamalıyım?

<div class="learning-intro">
  <p><strong>Bir hedef seç.</strong> Her yol, aynı çekirdek müfredattan hedefine uygun dersleri bir araya getirir.</p>
</div>

<div class="learning-grid">
  <div class="learning-card">
    <span class="learning-card__number">01</span>
    <span class="learning-card__title">Yapay zekâ temelleri</span>
    <span class="learning-card__text">Python, matematik, klasik öğrenme ve sinir ağlarını sıfırdan kur.</span>
    <span class="learning-card__route">Faz 0 → 1 → 2 → 3 → 4</span>
  </div>
  <div class="learning-card">
    <span class="learning-card__number">02</span>
    <span class="learning-card__title">LLM uygulamaları</span>
    <span class="learning-card__text">API'leri, aramayı, agent'ları ve üretim sınırlarını öğren.</span>
    <span class="learning-card__route">Faz 0 → 7 → 8 → 9 → 11 → 12</span>
  </div>
  <div class="learning-card">
    <span class="learning-card__number">03</span>
    <span class="learning-card__title">Türkçe doğal dil işleme</span>
    <span class="learning-card__text">Tokenization, ekler, embedding'ler ve Türkçe RAG'i uygulamalı öğren.</span>
    <span class="learning-card__route">Faz 0 → 4 → 5 → 6 → 8</span>
  </div>
  <div class="learning-card">
    <span class="learning-card__number">04</span>
    <span class="learning-card__title">Yapay zekâ mühendisliği</span>
    <span class="learning-card__text">Ölç, güvenilir hale getir, maliyeti hesapla ve sistemi hizmet olarak sun.</span>
    <span class="learning-card__route">Faz 7 → 11 → 12 → 13</span>
  </div>
</div>

## Kodları çalıştırmak

Temel örnekler ek kurulum gerektirmez; çoğunu doğrudan sayfadaki pencerede çalıştırabilirsin. NumPy gibi bir paket gereken yerlerde dersin başında yazar. Projeyi [0.1 dersindeki](faz-00-hazirlik/01-gelistirme-ortami/README.md) gibi indirdiysen, örneğin 4.1 dersinin kodunu proje klasöründeyken şöyle çalıştırırsın:

```bash
cd docs/faz-04-metin-ve-turkce-nlp/01-metni-sayilara-cevirmek
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
