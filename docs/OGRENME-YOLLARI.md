# Öğrenme yolları

**Bir hedef seç, müfredattan bu hedefe çıkan yolu izle.**

Yollardaki dersleri verilen sırayla oku; her ders bir öncekinin üstüne kurulur. Derslerin çoğunda önce mekanizmayı sade kodla kendin kurar, sonra gerçek araçlarla aynı problemi tekrar çözersin.

<div class="learning-grid learning-grid--page">
  <article class="learning-card learning-card--wide">
    <span class="learning-card__number">01</span>
    <span class="learning-card__title" id="yapay-zeka-temelleri">Yapay zekâ temelleri</span>
    <span class="learning-card__text">Veriden öğrenmenin ilkelerini, sinir ağlarını ve eğitimin mekanizmasını anlamak isteyenler için.</span>
    <span class="learning-card__route">Faz 0 → 1 → 2 → 3</span>
  </article>
  <article class="learning-card learning-card--wide">
    <span class="learning-card__number">02</span>
    <span class="learning-card__title" id="llm-uygulamalari">LLM uygulamaları</span>
    <span class="learning-card__text">Modeli API, RAG, araç çağrısı ve agent döngüsüyle çalışan bir ürüne dönüştürmek isteyenler için.</span>
    <span class="learning-card__route">Faz 0 → 7 → 8 → 9 → 11 → 12</span>
  </article>
  <article class="learning-card learning-card--wide">
    <span class="learning-card__number">03</span>
    <span class="learning-card__title" id="turkce-dogal-dil-isleme">Türkçe doğal dil işleme</span>
    <span class="learning-card__text">Türkçe metni temsil eden, arayan ve üreten sistemlerde dilin özel yapısını öğrenmek isteyenler için.</span>
    <span class="learning-card__route">Faz 0 → 4 → 5 → 6 → 8</span>
  </article>
  <article class="learning-card learning-card--wide">
    <span class="learning-card__number">04</span>
    <span class="learning-card__title" id="yapay-zeka-muhendisligi">Yapay zekâ mühendisliği</span>
    <span class="learning-card__text">Bir prototipi ölçülen, gözlemlenen, güvenli ve maliyeti kontrol edilen bir hizmete dönüştürmek isteyenler için.</span>
    <span class="learning-card__route">Faz 7 → 11 → 12 → 13</span>
  </article>
</div>

## 1. Yapay zekâ temelleri

Bu yol, hazır bir model çağrısına geçmeden önce verinin, matematiğin ve öğrenme mekanizmasının temelini kurar.

| Sıra | Ders | Kazanım |
|---:|---|---|
| 1 | [Faz 0 — Hazırlık](faz-00-hazirlik/01-gelistirme-ortami/README.md) | Python, Git, Jupyter ve test temellerini kurar |
| 2 | [Faz 1 — Matematik](faz-01-matematik/01-vektorler-ve-matrisler/README.md) | Vektör, matris, olasılık, istatistik, gradyan ve kayıp fikirlerini kodla öğrenir |
| 3 | [Faz 2 — Klasik öğrenme](faz-02-klasik-ml/01-numpy-ile-veri/README.md) | Veriyi temsil eder, model eğitir ve hatayı ölçer |
| 4 | **Faz 3 — Sinir ağları** | Geri yayılımı ve optimizasyonu kendi koduyla izler |
| 5 | [Faz 4 — Metin](faz-04-metin-ve-turkce-nlp/01-metni-sayilara-cevirmek/README.md) | Metni temsil etmeyi ve Türkçe'nin özel durumlarını kavrar |

Bu yolun çıkış projesi, veriyi alıp eğitilmiş bir model üreten ve sonuçlarını testlerle doğrulayan küçük bir deney hattıdır.

## 2. LLM uygulamaları

Bu yol, bir dil modelini ürün koduna bağlamayı; bağlamı, araçları, aramayı ve hataları sistemli biçimde ele almayı öğretir.

| Sıra | Ders | Kazanım |
|---:|---|---|
| 1 | [Faz 0 — Hazırlık](faz-00-hazirlik/01-gelistirme-ortami/README.md) | Çalışan Python ortamı ve test alışkanlığı |
| 2 | **Faz 7 — LLM'ler** | İstek, yanıt, biçimli çıktı ve hata yönetimi |
| 3 | **Faz 8 — RAG** | Dokümanı parçalara ayırır, getirir ve kaynağa bağlar |
| 4 | **Faz 9 — Agent'lar** | Araç çağıran, bellekli ve güvenlik sınırı olan döngü kurar |
| 5 | **Faz 11 — Değerlendirme** | Deneme seti ve otomatik regresyon testi hazırlar |
| 6 | **Faz 12 — Üretim** | İzleme, maliyet, dağıtım ve geri alma uygular |

Bu yolun çıkış projesi, kaynaklı cevap veren, araç çağırabilen ve başarısı ölçülen bir Türkçe uygulamadır.

## 3. Türkçe doğal dil işleme

Bu yol Türkçe'nin ekli yapısını, Unicode ayrıntılarını, alt kelime ayrımını ve anlam aramayı dersler boyunca ele alır.

| Sıra | Ders | Kazanım |
|---:|---|---|
| 1 | [Faz 0 — Hazırlık](faz-00-hazirlik/01-gelistirme-ortami/README.md) | Çalışan Python ortamı |
| 2 | [Faz 4 — Türkçe NLP](faz-04-metin-ve-turkce-nlp/01-metni-sayilara-cevirmek/README.md) | UTF-8, küçük harf, ekler, temizleme, embedding ve benzerlik |
| 3 | **Faz 5 — Transformer** | Attention ve pozisyon bilgisini parça parça kurar |
| 4 | **Faz 6 — Küçük dil modeli** | BPE ve mini bir GPT eğitimi yapar |
| 5 | **Faz 8 — Türkçe RAG** | Ek yapısı ve normalleştirmeyi arama hattına dahil eder |

Bu yolun çıkış projesi, Türkçe belgeleri etkili biçimde dizinleyen ve sorgulayan bir arama sistemi olabilir.

## 4. Yapay zekâ mühendisliği

Bu yol bir modelin başarısından önce sistem davranışını, güvenilirliği, maliyeti ve üretim sınırlarını ele alır.

| Sıra | Ders | Kazanım |
|---:|---|---|
| 1 | **Faz 7 — Model kullanımı** | API, prompt, yapılandırılmış çıktı ve hata durumları |
| 2 | **Faz 11 — Değerlendirme** | Metrik, test seti, hakem modeli ve regresyon |
| 3 | **Faz 12 — Üretim** | Servisleme, izleme, güvenlik ve dağıtım |
| 4 | **Faz 13 — Bitirme projesi** | Birden fazla beceriyi tek portföy üründe birleştirir |

Bu yolun çıkış projesi, kullanıma hazır bir hizmetin yanında test raporu, gözlem panosu ve geri alma planı içeren bir sistemdir.
