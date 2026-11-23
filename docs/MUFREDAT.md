# Müfredat

**Durum:** ✅ yazıldı · 🚧 yazılıyor · ⬜ planlandı

Bu liste bir **taslaktır**. Ders başlıkları ve sırası ilerledikçe değişebilir. Her ders, [aynı 4 adımı](index.md) izler: problem, kendin yaz, kütüphaneyle yap, pekiştir.

!!! tip "Öğrenme yolları"
    | Hedef | Yol |
    |---|---|
    | Sıfırdan temel | Faz 0 → 1 → 2 → 3 → 4 → 5 → 6 |
    | LLM uygulama geliştirici | Faz 0 → 7 → 8 → 9 → 11 → 12 |
    | Türkçe NLP | Faz 0 → 4 → 5 → 6 → 8 → 10 |

---

## Faz 0 – Hazırlık

Kod yazıp çalıştıracağın zemini hazırlar. **Ön koşul:** yok. **Çıktı:** çalışan bir Python ortamı, Git ile indirilmiş proje ve ilk testin.

- ✅ [0.1 Geliştirme ortamını kurmak](faz-00-hazirlik/01-gelistirme-ortami/README.md): terminal, Python, Git, sanal ortam, ilk betik
- ⬜ 0.2 Python hızlı tekrar: değişkenler, listeler, sözlükler, fonksiyonlar, sınıflar
- ⬜ 0.3 Git ve GitHub ile çalışmak: commit, branch, pull request, ilk katkını yapmak
- ⬜ 0.4 Jupyter ve Colab: not defteri mantığı, ücretsiz bulut ortamı
- ⬜ 0.5 Test yazmak ve hata ayıklamak: `unittest`, `assert`, hata mesajı okumak

## Faz 1 – Matematik Temelleri

Yapay zekânın kullandığı matematiği formülle değil, kodla öğrenirsin. **Ön koşul:** Python temelleri. **Çıktı:** vektör, matris ve türev işlemlerini kodla yapabilmek.

- ⬜ 1.1 Vektörler ve matrisler: veriyi sayı dizisi olarak düşünmek
- ⬜ 1.2 Matris çarpımı: sinir ağlarının temel işlemi
- ⬜ 1.3 Türev ve gradyan: bir fonksiyonun hangi yöne değiştiğini bulmak
- ⬜ 1.4 Olasılık ve dağılımlar: belirsizliği sayıyla ifade etmek
- ⬜ 1.5 İstatistik: ortalama, varyans, korelasyon
- ⬜ 1.6 Entropi ve çapraz entropi: kayıp fonksiyonunun kaynağı

## Faz 2 – Klasik Makine Öğrenmesi

Verinden öğrenen ilk modellerini yazarsın. **Ön koşul:** Faz 1. **Çıktı:** sıfırdan yazılmış regresyon ve sınıflandırıcı, bir modelin iyi olup olmadığını ölçebilme becerisi.

- ⬜ 2.1 NumPy ile veri: diziler, dilimleme, yayın (broadcasting)
- ⬜ 2.2 Doğrusal regresyon: gradyan inişi ile sıfırdan
- ⬜ 2.3 Lojistik regresyon: sınıflandırma ve olasılık
- ⬜ 2.4 Eğitim, doğrulama, test: aşırı öğrenmeyi yakalamak
- ⬜ 2.5 Karar ağaçları: kuralları veriden öğrenmek
- ⬜ 2.6 Metrikler: doğruluk, kesinlik, duyarlılık, F1

## Faz 3 – Sinir Ağları

Sinir ağlarının nasıl öğrendiğini, geri yayılımı elle yazarak görürsün. **Ön koşul:** Faz 1-2. **Çıktı:** kendi yazdığın bir mini autograd motoru ve onunla eğitilmiş bir ağ.

- ⬜ 3.1 Tek nöron: girdi, ağırlık, aktivasyon
- ⬜ 3.2 Mini autograd: türevi otomatik hesaplayan küçük bir motor
- ⬜ 3.3 Geri yayılım: hatanın katmanlara dağıtılması
- ⬜ 3.4 Çok katmanlı ağ: XOR ve basit sınıflandırma
- ⬜ 3.5 Optimizasyon: SGD, momentum, Adam
- ⬜ 3.6 PyTorch'a geçiş: aynı ağ, çok daha az kod

## Faz 4 – Metin ve Türkçe NLP

Metni sayılara çevirmenin yollarını ve Türkçe'ye özgü zorlukları öğrenirsin. **Ön koşul:** Faz 0 (Faz 1-3 sonraki derslerde gerekir). **Çıktı:** Türkçe metinle çalışan bir sınıflandırıcı ve arama.

- ✅ [4.1 Metni sayılara çevirmek (ve Türkçe neden zor?)](faz-04-metin-ve-turkce-nlp/01-metni-sayilara-cevirmek/README.md): tokenizer, UTF-8, `lower()` tuzağı
- ⬜ 4.2 Türkçe biçimbilim: kök, ek, ünlü uyumu ve kurala dayalı ek ayırma
- ⬜ 4.3 Metin temizleme: normalleştirme ve Türkçe karakter tuzakları
- ⬜ 4.4 Gömme (embedding): kelimeyi vektöre çevirmek
- ⬜ 4.5 Benzerlik ve arama: kosinüs benzerliği
- ⬜ 4.6 Duygu analizi: Türkçe yorumlarla basit sınıflandırıcı
- ⬜ 4.7 Veri setleri: nereden bulunur, lisans ve etik

## Faz 5 – Transformer'ı Anlamak

Modern dil modellerinin temelindeki mimariyi parça parça kurarsın. **Ön koşul:** Faz 3-4. **Çıktı:** PyTorch ile yazılmış çalışan küçük bir transformer.

- ⬜ 5.1 Dizi modelleme: sırada anlam taşıyan veri
- ⬜ 5.2 Attention: "hangi kelimeye bakmalı?" sorusunun matematiği
- ⬜ 5.3 Çok başlı attention: aynı anda birden fazla ilişkiyi yakalamak
- ⬜ 5.4 Konum bilgisi: sıra bilgisini modele vermek
- ⬜ 5.5 Transformer bloğu: attention, ileri besleme, normalizasyon
- ⬜ 5.6 Mini transformer: PyTorch ile küçük bir model

## Faz 6 – Küçük Bir Dil Modeli (LLM) Sıfırdan

Küçük ölçekte de olsa, bir dil modelini baştan sona kendin eğitirsin. **Ön koşul:** Faz 5. **Çıktı:** kendi eğittiğin mini bir GPT ve Türkçe'de tokenizer verimliliği ölçümü.

- ⬜ 6.1 Sonraki token tahmini: dil modelinin tek işi
- ⬜ 6.2 BPE tokenizer: alt-kelime sözlüğünü veriden öğrenmek
- ⬜ 6.3 Türkçe'de tokenizer verimliliği: aynı anlam kaç token tutuyor?
- ⬜ 6.4 Mini GPT eğitimi: eğitim döngüsü ve kayıp eğrisi
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
