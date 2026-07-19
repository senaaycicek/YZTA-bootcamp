# Product Backlog

## Story 1: Ürün Bilgi Girişi Akışı (8 puan)
Satıcının ürün temel özelliklerini (materyal, tarz, renk, kullanım amacı) girebileceği basit bir giriş formu/akışı tasarlanır.

- [x] Task: Girdi alanlarının belirlenmesi (materyal, tarz, renk, kategori vb.) — 2 puan
- [x] Task: Form/giriş arayüzünün taslak (wireframe) çizimi — 3 puan
- [x] Task: Girilen verinin JSON/veri modeli olarak tanımlanması — 3 puan

## Story 2: Tasarımcı Agent — Prompt Üretim Mantığı (13 puan)
Kullanıcı girdisini alıp Midjourney/DALL-E için görsel üretim promptu üreten agent mantığı kurulur.

- [x] Task: Prompt şablonunun tasarlanması (ürün özelliği → prompt eşlemesi) — 5 puan
- [x] Task: Örnek 5 ürün için prompt üretiminin test edilmesi — 5 puan
- [x] Task: Üretilen promptların kalite kontrolü ve iyileştirilmesi — 3 puan

## Story 3: Tasarımcı Agent — Görsel Üretim Entegrasyonu (8 puan)
Üretilen promptun görsel üretim API'sine (Midjourney/DALL-E) gönderilip görselin alınması.

- [x] Task: API/araç seçiminin yapılması — 2 puan
- [ ] Task: Basit bir API çağrısı ile örnek görsel üretiminin denenmesi — 5 puan
- [ ] Task: Üretilen görselin kaydedilmesi/gösterilmesi — 1 puan

## Story 4: Metin Yazarı Agent — Taslak Akış (8 puan)
Görsel ve ürün özelliklerini temel alarak SEO uyumlu ürün açıklaması üreten agent'ın ilk mantığının kurulması.

- [x] Task: SEO uyumlu ürün açıklaması için prompt şablonunun yazılması — 5 puan
- [x] Task: Örnek bir ürün için açıklama metni üretiminin test edilmesi — 3 puan

## Story 5: Takım & Süreç Kurulumu (5 puan)
- [x] Task: GitHub reposunun kurulması ve README'nin oluşturulması — 1 puan
- [x] Task: Backlog'un Miro/Trello'ya işlenmesi — 1 puan
- [x] Task: Sprint board'un kurulması (To Do / In Progress / Done) — 1 puan
- [x] Task: Daily Scrum kanalının/rutininin belirlenmesi — 1 puan
- [x] Task: Roller ve sorumlulukların netleştirilmesi (PO, SM, Developer) — 1 puan

---
**Sprint 1 için hedeflenen toplam puan:** ~35 puan (Story 5 tamamlandı, Story 1 ve 2 başlandı)
**Sprint 2 için hedeflenen toplam puan:** ~34 puan (Story 1, Story 2, Story 4 tamamlandı, Story 3 üzerinde çalışıldı)

---

# Sprint 3 Hazırlık Backlog (Aday Hikayeler ve Görevler)

Sprint 2 retrospektif çıktıları ve takım içi (Slack/Daily Scrum) konuşmalar doğrultusunda Sprint 3 kapsamında ele alınması planlanan aday işler aşağıda listelenmiştir. Bu işler veritabanı yapılandırması, alternatif AI modelleri ve API limit/kredi kısıtları gibi engelleri aşmaya yöneliktir.

## Story 6: Veri Tabanı Yapılandırması ve Ortam Değişkenleri (3 puan)
SQLite dışındaki veri tabanlarının (PostgreSQL vb.) ve ortam değişkenlerinin (env) sunucu ortamında dinamik olarak tanımlanabilmesi.
- [ ] **Task:** Veri tabanı bağlantı adresinin `.env` üzerinden dinamik olarak okunmasının test edilmesi ve Railway/PostgreSQL altyapısına uyumlu hale getirilmesi — 2 puan
- [ ] **Task:** Ortam değişkenlerinin dokümante edilmesi ve `.env.example` dosyasının güncellenmesi — 1 puan

## Story 7: Bütçe Dostu/Ücretsiz Görsel Üretim Alternatifleri ve API Entegrasyonu (8 puan)
DALL-E/Midjourney dışındaki alternatif ve bütçe dostu (veya ücretsiz API anahtarı sunan) görsel üretim modellerinin entegre edilmesi.
- [ ] **Task:** Ücretsiz/bütçe dostu görsel üretim API'lerinin (örn. Pollinations AI, Hugging Face, Stable Diffusion API) araştırılması ve test edilmesi — 3 puan
- [ ] **Task:** Seçilen alternatif görsel üretim modelinin `image_adapter.py` dosyasına entegre edilerek mock servisin gerçeğe dönüştürülmesi — 3 puan
- [ ] **Task:** Üretilen görsellerin kullanıcı arayüzünde (Frontend - Result ekranı) gösterilmesi — 2 puan

## Story 8: API Anahtarı, Hata Yönetimi ve Alternatif LLM Seçenekleri (5 puan)
OpenAI API kredi yetersizliği durumunda uygulamanın çökmesini önlemek ve yedek model desteği sağlamak.
- [ ] **Task:** API anahtarı geçersizliği veya limit/kredi yetersizliği hatalarının yakalanarak kullanıcıya arayüzde anlamlı hata mesajlarının gösterilmesi — 2 puan
- [ ] **Task:** `llm_client.py` yapısına alternatif/ücretsiz modellerin (örn. Gemini API, Claude API veya Hugging Face LLM'leri) yedek (fallback) olarak eklenmesi — 3 puan

## Story 9: Bulut Depolama Entegrasyonu (5 puan)
Üretilen görsellerin kalıcı olarak depolanması.
- [ ] **Task:** Üretilen görsellerin AWS S3 veya benzeri bir bulut depolama servisine yüklenmesi ve URL'lerin veri tabanında saklanması — 5 puan

---
**Sprint 3 için hedeflenen toplam puan (Tahmini):** ~21 puan (Kalan Story 3 görevleri dahil edildiğinde ~27 puan)
