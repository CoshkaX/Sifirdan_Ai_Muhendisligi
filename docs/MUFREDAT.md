# Müfredat

**Durum:** ✅ yazıldı · 🚧 yazılıyor · ⬜ planlandı

Bu liste bir **taslaktır**. Ders başlıkları ve sırası ilerledikçe değişebilir. Her ders, [aynı 4 adımı](index.md) izler: problem, kendin yaz, kütüphaneyle yap, pekiştir.

!!! tip "Öğrenme yolları"
    Hangi hedefe ulaşmak istediğine göre dersleri sıralamak için [öğrenme yolları sayfasına](OGRENME-YOLLARI.md) bak.

    | Hedef | Yol |
    |---|---|
    | Yapay zekâ temelleri | Faz 0 → 1 → 2 → 3 → 4 |
    | LLM uygulamaları | Faz 0 → 7 → 8 → 9 → 11 → 12 |
    | Türkçe doğal dil işleme | Faz 0 → 4 → 5 → 6 → 8 |
    | Yapay zekâ mühendisliği | Faz 7 → 11 → 12 → 13 |

---

## Faz 0 – Hazırlık

Kod yazıp çalıştıracağın zemini hazırlar. **Ön koşul:** yok. **Çıktı:** çalışan bir Python ortamı, Git ile indirilmiş proje ve ilk testin.

- ✅ [0.1 Geliştirme ortamını kurmak](faz-00-hazirlik/01-gelistirme-ortami/README.md): terminal, Python, Git, sanal ortam, ilk betik
- ✅ [0.2 Python hızlı tekrar](faz-00-hazirlik/02-python-hizli-tekrar/README.md): değişkenler, listeler, sözlükler, fonksiyonlar, sınıflar
- ✅ [0.3 Git ve GitHub ile çalışmak](faz-00-hazirlik/03-git-ve-github/README.md): commit, branch, pull request, ilk katkını yapmak
- ✅ [0.4 Jupyter ve Colab](faz-00-hazirlik/04-jupyter-ve-colab/README.md): not defteri mantığı, ücretsiz bulut ortamı
- ✅ [0.5 Test yazmak ve hata ayıklamak](faz-00-hazirlik/05-test-ve-hata-ayiklama/README.md): `unittest`, `assert`, hata mesajı okumak
- ✅ [0.6 Yapay zekâ nedir?](faz-00-hazirlik/06-yapay-zeka-nedir/README.md): temsil, bellek, çıkarım, öğrenme ve açıklama

## Faz 1 – Matematik Temelleri

Yapay zekânın kullandığı matematiği formülle değil, kodla öğrenirsin. **Ön koşul:** Python temelleri. **Çıktı:** vektör, matris, olasılık ve istatistik ölçülerini kullanmak; türevle parametre güncellemek ve kaybın entropiyle ilişkisini anlamak.

- ✅ [1.1 Vektörler ve matrisler](faz-01-matematik/01-vektorler-ve-matrisler/README.md): veriyi sayı dizisi ve tablo olarak düşünmek
- ✅ [1.2 Matris çarpımı](faz-01-matematik/02-matris-carpimi/README.md): satır-sütun eşleşmesi ve noktasal çarpım
- ✅ [1.3 Türev ve gradyan](faz-01-matematik/03-turev-ve-gradyan/README.md): eğimi yaklaşık bulmak ve parametre güncellemek
- ✅ [1.4 Olasılık ve dağılımlar](faz-01-matematik/04-olasilik-ve-dagilimlar/README.md): eşit şanslı sonuçları saymak, dağılımı okumak ve gözlenen oranı ayırt etmek
- ✅ [1.5 İstatistik](faz-01-matematik/05-istatistik/README.md): ortalama, yayılımı gösteren varyans ve doğrusal ilişkiyi ölçen korelasyon
- ✅ [1.6 Entropi ve çapraz entropi](faz-01-matematik/06-entropi-ve-capraz-entropi/README.md): belirsizliği ölçmek ve sınıflandırma kaybını yorumlamak

## Faz 2 – Klasik Makine Öğrenmesi

Veriden öğrenen ilk modellerini yazarsın. **Ön koşul:** Faz 1. **Çıktı:** NumPy ile sayısal veriyi düzenlemek; sıfırdan yazılmış regresyon ve sınıflandırıcıyla model eğitmek ve başarısını ölçmek.

- ✅ [2.1 NumPy ile veri](faz-02-klasik-ml/01-numpy-ile-veri/README.md): dizileri, dilimlemeyi ve yayınlamayı öğrenmek
- ✅ [2.2 Doğrusal regresyon](faz-02-klasik-ml/02-dogrusal-regresyon/README.md): MSE ve gradyan inişiyle sayısal tahmin yapmak
- ✅ [2.3 Lojistik regresyon](faz-02-klasik-ml/03-lojistik-regresyon/README.md): sigmoid, sınıf olasılığı ve çapraz entropiyle öğrenme
- ✅ [2.4 Eğitim, doğrulama ve test](faz-02-klasik-ml/04-egitim-dogrulama-test/README.md): aşırı öğrenmeyi fark etmek ve adil ölçüm yapmak
- ✅ [2.5 Karar ağaçları](faz-02-klasik-ml/05-karar-agaclari/README.md): Gini safsızlığı ve bölme kurallarıyla sınıflandırma
- ✅ [2.6 Sınıflandırma metrikleri](faz-02-klasik-ml/06-siniflandirma-metrikleri/README.md): doğruluk, kesinlik, duyarlılık ve F1

## Faz 3 – Sinir Ağları

Sinir ağlarının nasıl öğrendiğini, geri yayılımı elle yazarak görürsün. **Ön koşul:** Faz 1-2. **Çıktı:** kendi yazdığın bir mini autograd motoru ve onunla eğitilmiş bir ağ.

- ✅ [3.1 Tek nöron](faz-03-sinir-aglari/01-tek-noron/README.md): girdi, ağırlık, aktivasyon
- ✅ [3.2 Mini autograd](faz-03-sinir-aglari/02-mini-autograd/README.md): türevi otomatik hesaplayan küçük bir motor
- ✅ [3.3 Geri yayılım](faz-03-sinir-aglari/03-geri-yayilim/README.md): hatanın katmanlara dağıtılması
- ✅ [3.4 Çok katmanlı ağ](faz-03-sinir-aglari/04-cok-katmanli-ag/README.md): XOR ve basit sınıflandırma
- ✅ [3.5 Optimizasyon](faz-03-sinir-aglari/05-optimizasyon/README.md): SGD, momentum, Adam
- ✅ [3.6 PyTorch'a geçiş](faz-03-sinir-aglari/06-pytorcha-gecis/README.md): aynı ağ, çok daha az kod

## Faz 4 – Metin ve Türkçe NLP

Metni sayılara çevirmenin yollarını ve Türkçe'ye özgü zorlukları öğrenirsin. **Ön koşul:** Faz 0 (Faz 1-3 sonraki derslerde gerekir). **Çıktı:** Türkçe metinle çalışan bir sınıflandırıcı ve arama.

- ✅ [4.1 Metni sayılara dönüştürmek: Türkçe neden zor?](faz-04-metin-ve-turkce-nlp/01-metni-sayilara-cevirmek/README.md): tokenizer, UTF-8, `lower()` tuzağı
- ✅ [4.2 Türkçe sözcüklerin içini açmak](faz-04-metin-ve-turkce-nlp/02-turkce-bicimbilim/README.md): kök, ek, ünlü uyumu ve basit ek ayırma
- ✅ [4.3 Türkçe metni temizlemek ve normalleştirmek](faz-04-metin-ve-turkce-nlp/03-metin-temizleme/README.md): Unicode NFC, Türkçe harfler ve boşluklar
- ✅ [4.4 Gömme (embedding)](faz-04-metin-ve-turkce-nlp/04-gomme/README.md): kelimeyi vektöre çevirmek
- ✅ [4.5 Benzerlik ve arama](faz-04-metin-ve-turkce-nlp/05-benzerlik-ve-arama/README.md): kosinüs benzerliği, TF-IDF ve Türkçe için kök yaklaşımı
- ✅ [4.6 Duygu analizi](faz-04-metin-ve-turkce-nlp/06-duygu-analizi/README.md): Türkçe yorumlarla basit sınıflandırıcı
- ✅ [4.7 Veri setleri](faz-04-metin-ve-turkce-nlp/07-veri-setleri/README.md): nereden bulunur, lisans ve etik

## Faz 5 – Transformer'ı Anlamak

Modern dil modellerinin temelindeki mimariyi parça parça kurarsın. **Ön koşul:** Faz 3-4. **Çıktı:** PyTorch ile yazılmış çalışan küçük bir transformer.

- ✅ [5.1 Dizi modelleme](faz-05-transformer/01-dizi-modelleme/README.md): sırada anlam taşıyan veri
- ✅ [5.2 Attention](faz-05-transformer/02-attention/README.md): "hangi kelimeye bakmalı?" sorusunun matematiği
- ✅ [5.3 Çok başlı attention](faz-05-transformer/03-cok-basli-attention/README.md): aynı anda birden fazla ilişkiyi yakalamak
- ✅ [5.4 Konum bilgisi](faz-05-transformer/04-konum-bilgisi/README.md): sıra bilgisini modele vermek
- ✅ [5.5 Transformer bloğu](faz-05-transformer/05-transformer-blogu/README.md): attention, ileri besleme, normalizasyon
- ✅ [5.6 Mini transformer](faz-05-transformer/06-mini-transformer/README.md): PyTorch ile küçük bir model

## Faz 6 – Küçük Bir Dil Modeli (LLM) Sıfırdan

Küçük ölçekte de olsa, bir dil modelini baştan sona kendin eğitirsin. **Ön koşul:** Faz 5. **Çıktı:** kendi eğittiğin mini bir GPT ve Türkçe'de tokenizer verimliliği ölçümü.

- ✅ [6.1 Sonraki token tahmini](faz-06-kucuk-dil-modeli/01-sonraki-token-tahmini/README.md): dil modelinin tek işi
- ✅ [6.2 BPE tokenizer](faz-06-kucuk-dil-modeli/02-bpe-tokenizer/README.md): alt-kelime sözlüğünü veriden öğrenmek
- ✅ [6.3 Türkçe tokenizer verimliliği](faz-06-kucuk-dil-modeli/03-turkce-tokenizer-verimliligi/README.md): aynı anlam kaç token tutuyor?
- ✅ [6.4 Mini GPT eğitimi](faz-06-kucuk-dil-modeli/04-mini-gpt-egitimi/README.md): eğitim döngüsü ve kayıp eğrisi
- ⬜ 6.5 Metin üretimi: sıcaklık, top-k, top-p
- ⬜ 6.6 Küçük Türkçe veriyle deney: sonuçları yorumlamak

## Faz 7 – LLM'leri Kullanmak

Hazır modelleri uygulamalarında güvenle kullanmayı öğrenirsin. **Ön koşul:** Faz 0. **Çıktı:** hata yönetimi olan, maliyetini bilen bir LLM istemcisi.

- ⬜ 7.1 API ile model çağırmak: istek, yanıt, anahtar yönetimi
- ⬜ 7.2 Etkili prompt: açık talimat, örnek, format
- ⬜ 7.3 Yapılandırılmış çıktı: JSON alıp doğrulamak
- ⬜ 7.4 Bağlam, maliyet, gecikme: token hesabı
- ⬜ 7.5 Hata yönetimi: zaman aşımı, yeniden deneme, hız sınırları

## Faz 8 – Arama ve RAG

Modele kendi dokümanlarını okutan sistemi baştan sona kurarsın. **Ön koşul:** Faz 4, Faz 7. **Çıktı:** Türkçe dokümanlar üzerinde çalışan ve değerlendirilmiş bir RAG hattı.

- ⬜ 8.1 Anlamsal arama: embedding ile benzer metni bulmak
- ⬜ 8.2 Parçalama (chunking): dokümanı doğru boyutta bölmek
- ⬜ 8.3 Vektör veritabanı: saklamak ve sorgulamak
- ⬜ 8.4 Sıfırdan RAG hattı: getir, bağlama koy, cevapla
- ⬜ 8.5 Türkçe RAG: ek yapısı, normalleştirme, tuzaklar
- ⬜ 8.6 RAG'i değerlendirmek: doğru parça getirildi mi, cevap dayanaklı mı?

## Faz 9 – Agent'lar

Modelin araç kullanarak iş yapmasını sağlayan döngüyü kurarsın. **Ön koşul:** Faz 7. **Çıktı:** araç kullanan, hatalarını yönetebilen bir agent.

- ⬜ 9.1 Agent döngüsü: düşün, araç çağır, gözlemle
- ⬜ 9.2 Araç tanımlamak: fonksiyonu modele tanıtmak
- ⬜ 9.3 Bellek ve durum: konuşma ve görev geçmişi
- ⬜ 9.4 MCP'ye giriş: araçları standart bir protokolle sunmak
- ⬜ 9.5 Agent'lar neden başarısız olur? Döngüye girme, yanlış araç, bağlam taşması
- ⬜ 9.6 Güvenlik: prompt injection ve yetki sınırı

## Faz 10 – Fine-tuning

Bir modeli kendi verinle uyarlamayı ve bunun ne zaman gerektiğini öğrenirsin. **Ön koşul:** Faz 3, 6. **Çıktı:** küçük bir Türkçe model üzerinde ölçülmüş bir fine-tuning deneyi.

- ⬜ 10.1 Ne zaman fine-tuning? Prompt, RAG ve fine-tuning karşılaştırması
- ⬜ 10.2 Veri hazırlama: Türkçe talimat verisi
- ⬜ 10.3 LoRA: az parametreyle uyarlama
- ⬜ 10.4 Küçük bir modeli fine-tune etmek: uçtan uca
- ⬜ 10.5 Sonucu ölçmek: öncesi ve sonrası karşılaştırma

## Faz 11 – Değerlendirme (Eval)

Bir sistemin "iyi" olduğunu nasıl kanıtlarsın? **Ön koşul:** Faz 7-8. **Çıktı:** kendi projen için bir test seti ve otomatik değerlendirme hattı.

- ⬜ 11.1 "İyi" ne demek? Metrik seçimi
- ⬜ 11.2 Test seti hazırlamak: temsil edici örnekler
- ⬜ 11.3 Otomatik ve insan değerlendirmesi
- ⬜ 11.4 LLM'i hakem olarak kullanmak: avantajları ve önyargıları
- ⬜ 11.5 Regresyon testleri: sistemi bozmadan geliştirmek

## Faz 12 – Üretime Almak

Çalışan bir prototipi, güvenilir bir servise dönüştürürsün. **Ön koşul:** Faz 7-11. **Çıktı:** izlenen, güvenli ve maliyeti kontrol altındaki bir servis.

- ⬜ 12.1 Modeli servis etmek: API sunucusu
- ⬜ 12.2 Maliyet ve gecikme: önbellek, toplu istek, küçük model
- ⬜ 12.3 İzleme ve loglama: ne olduğunu görebilmek
- ⬜ 12.4 Güvenlik ve gizlilik: kişisel veri ve KVKK farkındalığı
- ⬜ 12.5 Dağıtım: sürümleme ve geri alma

## Faz 13 – Bitirme Projeleri

Öğrendiklerini portföyüne dönüşecek projelerde birleştirirsin.

- ⬜ 13.1 Türkçe doküman sohbet botu (RAG)
- ⬜ 13.2 Araç kullanan agent
- ⬜ 13.3 Kendi mini dil modelin
- ⬜ 13.4 Proje sunumu ve portföy
