# OrkestrAI

## Takım Üyeleri

| İsim | Rol |
|---|---|
| Rabia Sena UYSAL | Product Owner |
| Kadir Zeybekoğlu | Scrum Master |
| Bengisu Sarıkaya | Developer |
| Kutay Çalış | Developer |
| Sena Nur Ayçiçek | Developer |

## Ürün İsmi

**OrkestrAI** - Ürünün, kişiselleştirilmiş e-ticaret ürünleri için görsel ve pazarlama metni üreten yapay zeka ajanlarını bir orkestra gibi bir araya getirmesinden gelir.

## Ürün Açıklaması

**3. Fikir: E-Ticaret İçin Uçtan Uca Ürün Görselleştirme ve Pazarlama Ağı**

Kişiselleştirilmiş ürünler veya butik tasarımlar yapan satıcılar için görsel üretim ve pazarlama süreçlerini otomatikleştiren, çoklu yapay zeka ajanının birlikte çalıştığı bir orkestrasyon sistemidir. Satıcı yalnızca ürünün temel özelliklerini girer; sistem geri kalan tasarım ve metin üretim sürecini uçtan uca yönetir.

**Nasıl Çalışır:**
1. Satıcı, ürünün temel özelliklerini (materyal, tarz, renk, kullanım amacı vb.) sisteme girer.
2. **Tasarımcı Agent**, bu bilgiyi alarak Midjourney/DALL-E gibi görsel üretim modellerine uygun yüksek kaliteli promptlar oluşturur ve ürün infografikleri/görsellerini üretir.
3. **Metin Yazarı Agent**, Tasarımcı Agent'ın ürettiği görseli ve ürün özelliklerini temel alarak e-ticaret siteleri için SEO uyumlu ürün açıklamaları ve pazarlama metinleri yazar.
4. Üretilen görsel + metin çıktısı satıcıya sunulur ve doğrudan e-ticaret platformunda yayına hazır hale gelir.

## Ürün Özellikleri

- Ürün temel bilgisinden otomatik görsel üretim (Tasarımcı Agent)
- Görsele dayalı SEO uyumlu ürün açıklaması ve pazarlama metni üretimi (Metin Yazarı Agent)
- Çoklu ajan orkestrasyonu ile uçtan uca otomasyon
- Kişiselleştirilmiş / butik ürünlere özel çalışma mantığı
- E-ticaret sitelerine entegrasyona uygun çıktı formatı

## Hedef Kitle

Kişiselleştirilmiş ürünler veya butik tasarımlar üreten küçük/orta ölçekli e-ticaret satıcıları; profesyonel görsel ve metin üretimi için zaman/bütçe kısıtı yaşayan bağımsız tasarımcı ve girişimciler.

## Product Backlog URL

(https://miro.com/app/board/uXjVH_MoPAE=/?share_link_id=108646424315)

Backlog detayları için: [PRODUCT_BACKLOG.md](./PRODUCT_BACKLOG.md)

---

# Sprint 1

## Sprint Notes

Sprint 1'de hedeflenen işler:
- Takım rollerinin netleştirilmesi (Product Owner, Scrum Master, Developer)
- GitHub reposunun ve README'nin oluşturulması
- Product Backlog'un çıkarılması ve puanlanması
- Sprint board'un (Miro) kurulması
- Daily Scrum rutininin başlatılması
- Tasarımcı Agent için prompt üretim mantığının ilk taslağının çıkarılması
- Metin Yazarı Agent için taslak akışın belirlenmesi

## Sprint içinde tamamlanması tahmin edilen puan

35 puan

## Puan Tamamlama Mantığı

Her task, zorluk derecesine göre Fibonacci puanlaması (1-2-3-5-8) ile puanlanmıştır. Story başına düşen toplam puan, sprint toplam puanının yarısını geçmeyecek şekilde sınırlandırılmıştır. Sprint 1 için takım süreç kurulumu (Story 5) ve Tasarımcı Agent'ın ilk adımları (Story 1, Story 2) öncelikli olarak seçilmiştir.

## Daily Scrum

Daily Scrum toplantıları Slack üzerinden yazılı olarak yürütülmüştür. Toplantı kayıtları ekran görüntüsü olarak aşağıda paylaşılmıştır:

*(Buraya Slack/WhatsApp daily scrum ekran görüntülerini ekleyin: `![Daily Scrum](görsel-linki)`)*

## Sprint Board Update

Sprint boyunca Miro üzerinde 4 sütunlu bir board kullanılmıştır: **Backlog / To Do / In Progress / Done**. Backlog kartları story'lere göre renklendirilmiştir (ör. Story 1 mavi, Story 2 mor, Story 3 turuncu, Story 4 yeşil, Story 5 sarı).

Sprint 1 başında, takım süreç kurulumuyla ilgili task'lar (GitHub reposu, README, backlog'un işlenmesi, board kurulumu, Daily Scrum rutini, rol netleştirme) doğrudan **In Progress**'e alınmıştır çünkü bu işler sprint başlar başlamaz devreye girmiştir.

![Sprint Board 1](/readme-img/sprint-board-0.png)
![Sprint Board 2](/readme-img/sprint-board-1.png)

## Ürün Durumu

| | |
|---|---|
| ![Ürün Durumu 1](/readme-img/ürün-durum-1.png) | ![Ürün Durumu 2](/readme-img/ürün-durum-2.png) |
| ![Ürün Durumu 3](/readme-img/ürün-durum-3.png) | ![Ürün Durumu 4](/readme-img/ürün-durum-4.png) |

## Sprint Review

Sprint 1 sırasında aşağıdaki hedefler başarıyla tamamlanmıştır:

**Tamamlanan Çalışmalar:**
- ✅ Takım rollerinin netleştirilmesi ve sorumlulukların tanımlanması
- ✅ GitHub reposunun oluşturulması ve README'nin ilk versiyonunun hazırlanması
- ✅ Product Backlog'un detaylı şekilde çıkarılması ve her task'ın puanlanması
- ✅ Miro üzerinde Sprint board'un kurulması ve 4 sütunlu workflow'un implementasyonu
- ✅ Daily Scrum rutininin Slack üzerinden başlatılması
- ✅ Tasarımcı Agent için prompt üretim mantığının ilk taslağının oluşturulması
- ✅ Metin Yazarı Agent için temel akış ve yapısının belirlenmesi

**Katılımcı Görüşleri:**
- Takım, sprint hedeflerine uygun şekilde işleri tamamladığına memnun
- Agile metodoloji ve scrum framework'ün etkin şekilde uygulanabildiği gözlemlenmiştir
- İletişim kanalları (Slack, Miro) takım iş birliğine uygun şekilde kurulmuştur

**Sprint Çıktısı:** 35 puan başarıyla tamamlanmıştır. Proje altyapısı ve takım süreci sağlam bir şekilde kurulmuş, ürün geliştirme için hazırlanmıştır.

## Sprint Retrospective

**İyi Giden Noktalar:**
- 🟢 Takımın hızlı şekilde organize olması ve roller konusunda anlaşmaya varması
- 🟢 Daily Scrum'ların disiplinli şekilde yürütülmesi
- 🟢 Miro board'un renkli kartlarla organize edilmesi - görsel olarak takip kolaylaştı
- 🟢 Product Owner'ın ürün vizyonunu çok açık şekilde iletmesi
- 🟢 Teknik setup (GitHub, README, backlog) hızlı tamamlanması

**Geliştirilmesi Gereken Noktalar:**
- 🟡 Tasarımcı Agent için prompt mühendisliği konusu daha derinlemesine çalışılması gerekiyor
- 🟡 Daily Scrum'lar daha yapılandırılmış bir format (What, How, Blockers) izlenebilir
- 🟡 Sprint board'da task completion rate'in daha açık şekilde takip edilmesi
- 🟡 Teknik dökümanların (Agent lojiği) daha detaylı hazırlanması

**Bir Sonraki Sprint İçin Alınan Aksiyonlar:**
1. Sprint 2'de Tasarımcı Agent'ın prototipinin oluşturulması
2. LLM entegrasyonu için teknik spec dökümanının detaylı hazırlanması
3. Daily Scrum format'ı standardize edilmesi (360 format)
4. Sprint velocity'nin daha doğru tahmin edilmesi için velocity tracking'in başlatılması
