# PlanMate

PlanMate, Discord kullanıcılarını ortak boş zamanları, bütçeleri ve aktivite tercihleri üzerinden eşleştirerek kişiselleştirilmiş sosyal etkinlik önerileri sunan bir Discord botudur.

Botun temel amacı yalnızca aktivite önermek değil, aynı zamanda aynı gün müsait olan ve benzer aktiviteler yapmak isteyen kullanıcıları bulup ortak bütçelerine uygun planlar oluşturmaktır.

---

## Projenin Amacı

Bir grup arkadaş içinde plan yapmak çoğu zaman şu sorulara dönüşür:

- Kim hangi gün boş?
- Kim ne yapmak istiyor?
- Herkesin bütçesi uygun mu?
- Ne yapılabilir?
- Kimlerle yapılabilir?

PlanMate bu süreci otomatikleştirir.

Kullanıcılar bir kez profil oluşturduktan sonra boş oldukları günleri, genel bütçelerini ve sevdikleri aktivite türlerini sisteme kaydeder.

Daha sonra herhangi bir kullanıcı aktivite aramak istediğinde bot o güne özel isteklerini alır, kayıtlı kullanıcıları karşılaştırır ve her zaman **3 farklı öneri** üretir.

---

# Temel Özellikler

- Discord kullanıcı hesabı üzerinden otomatik kullanıcı tanıma
- Kullanıcı kayıt sistemi
- Boş günlerin kaydedilmesi
- İlgi alanlarının kaydedilmesi
- Genel bütçe bilgisinin tutulması
- Belirli bir gün için aktivite arama
- O güne özel bütçe belirleme
- Aktivite türü seçme
- Kullanıcılar arasında uygunluk kontrolü
- Ortak bütçe hesaplama
- Kişiselleştirilmiş aktivite önerileri
- Her aramada 3 öneri sunma
- Uygun kişi bulunamazsa solo aktivite önerme
- Aynı kişiyi mümkün olduğunca tekrar önermeme
- Yeni öneriler oluşturma
- Kullanıcı profili görüntüleme ve düzenleme
- SQLite veri tabanı entegrasyonu
- Discord butonları, menüler ve modal formlar ile etkileşim

---

# Bot Nasıl Çalışır?

Bot sunucuya başlangıç mesajını gönderir:

```text
🎉 Bugün ne yapmak istersin?

Sana uygun aktiviteleri ve
beraber yapabileceğin kişileri bulabilirim.

[ ▶ BAŞLA ]
```

Kullanıcı `BAŞLA` butonuna bastığında Discord ID üzerinden sistemde kayıtlı olup olmadığı kontrol edilir.

Kullanıcı kayıtlı değilse kayıt süreci başlatılır.

Kayıtlıysa doğrudan ana menü açılır.

---

# Kullanıcı Kayıt Sistemi

Yeni kullanıcıdan üç temel bilgi alınır.

### Boş Günler

Kullanıcı haftanın hangi günlerinde genellikle boş olduğunu seçer.

Birden fazla gün seçilebilir.

```text
Pazartesi
Salı
Çarşamba
Perşembe
Cuma
Cumartesi
Pazar
```

### İlgi Alanları

Kullanıcı yapmak istediği veya sevdiği aktivite türlerini seçer.

Örneğin:

```text
Eğlenceli
Sakin
Hareketli
Oyun
Yemek
Kafe
Dış Mekan
Yaratıcı
Film / Dizi
```

Bir kullanıcı birden fazla ilgi alanına sahip olabilir.

### Genel Bütçe

Kullanıcı normal şartlarda bir aktivite için ayırabileceği maksimum bütçeyi girer.

Örneğin:

```text
100 TL
```

Bu değer kullanıcının genel profilinde saklanır.

---

# Ana Menü

Kayıtlı kullanıcı `BAŞLA` butonuna bastığında:

```text
👋 Hoş geldin!

Bugün ne yapmak istersin?

[ 🎯 Aktivite Bul ]

[ 👤 Profilim ]

[ ✏️ Profilimi Düzenle ]
```

ekranıyla karşılaşır.

---

# Aktivite Arama

Kullanıcı `Aktivite Bul` seçeneğine bastığında bot üç bilgi ister.

### Gün

Kullanıcı hangi gün için plan yapmak istediğini seçer.

Örneğin:

```text
Cumartesi
```

### O Günkü Bütçe

Kullanıcı yalnızca bu plan için harcamak istediği maksimum miktarı girer.

Örneğin kullanıcı profilinde:

```text
Genel bütçe: 100 TL
```

olmasına rağmen o gün:

```text
30 TL
```

harcamak isteyebilir.

Bu durumda aktivite aramasında **30 TL esas alınır**.

Kullanıcının genel bütçesi değiştirilmez.

### Aktivite Türü

Kullanıcı yapmak istediği aktivite türünü seçer.

Örneğin:

```text
😂 Eğlenceli
😌 Sakin
🏃 Hareketli
🍔 Yemek
☕ Sosyal
🎮 Oyun
🌳 Dış Mekan
🎨 Yaratıcı
```

Bu bilgilerle sistem içerisinde bir aktivite isteği oluşturulur.

Örneğin:

```text
Kullanıcı: Eymen
Gün: Cumartesi
Bütçe: 50 TL
Tercih: Eğlenceli
```

---

# Kullanıcı Eşleştirme Sistemi

Bot aktivite arayan kullanıcının seçtiği gün üzerinden diğer kayıtlı kullanıcıları kontrol eder.

Örneğin:

```text
Eymen → Cumartesi
```

seçtiğinde bot cumartesi günü müsait olan kullanıcıları bulur.

Örnek:

```text
Ali
Lina
Zeynep
```

Daha sonra bu kullanıcıların:

- bütçeleri,
- ilgi alanları,
- boş günleri,
- aktivite tercihleri

kontrol edilir.

---

# Bütçe Sistemi

İki kullanıcının bütçelerinin aynı olması gerekmez.

Örneğin:

```text
Ayşe: 30 TL
Eymen: 60 TL
```

Bu iki kullanıcı yine eşleşebilir.

Ortak bir aktivite için kullanılabilecek maksimum bütçe:

```text
min(30, 60) = 30 TL
```

olur.

Dolayısıyla:

```text
7 TL     → uygun
15 TL    → uygun
25 TL    → uygun
30 TL    → uygun
45 TL    → uygun değil
```

Bot yalnızca iki kişinin de karşılayabildiği aktiviteleri önerebilir.

Bu nedenle eşleşme bütçelerin birbirine yakın olmasına göre değil, **önerilen aktivitenin iki kullanıcının bütçesine de uygun olup olmadığına göre** yapılır.

---

# 3 Öneri Kuralı

PlanMate'in temel kurallarından biri her aktivite aramasında kullanıcıya **3 öneri sunmasıdır**.

### Üç uygun kullanıcı bulunursa

```text
1 kişi + aktivite
1 kişi + aktivite
1 kişi + aktivite
```

### İki uygun kullanıcı bulunursa

```text
2 kişi ile aktivite
1 solo aktivite
```

### Bir uygun kullanıcı bulunursa

```text
1 kişi ile aktivite
2 solo aktivite
```

### Hiç uygun kullanıcı bulunmazsa

```text
3 solo aktivite
```

Bu sayede bot hiçbir zaman yalnızca:

```text
Uygun kullanıcı bulunamadı.
```

mesajıyla işlemi sonlandırmaz.

Her durumda kullanıcıya alternatif bir plan sunmaya çalışır.

---

# Örnek Sonuç

Eymen aşağıdaki isteği gönderir:

```text
Cumartesi
50 TL
Eğlenceli
```

Botun sonucu:

```text
🎉 Sana 3 öneri buldum!


1️⃣ Ali ile parkta oyun

💰 Ücretsiz
👥 2 kişi
😂 Eğlenceli


2️⃣ Lina ile kafeye git

💰 30 TL / kişi
👥 2 kişi
☕ Sosyal


3️⃣ Evde oyun gecesi

💰 10 TL
👤 Tek başına
🎮 Oyun
```

Kullanıcı daha sonra:

```text
[ 1️⃣ SEÇ ]

[ 2️⃣ SEÇ ]

[ 3️⃣ SEÇ ]

[ 🔄 3 YENİ ÖNERİ ]
```

butonlarından birini kullanabilir.

---

# Yeni Öneriler

Kullanıcı ilk üç öneriyi beğenmezse:

```text
🔄 3 YENİ ÖNERİ
```

butonuna basabilir.

Bot aynı aktivite isteğini kullanır fakat mümkün olduğunca daha önce gösterilmiş aktiviteleri tekrar etmemeye çalışır.

Örneğin ilk sonuç:

```text
Ali ile bowling
Lina ile kafeye git
Evde film izle
```

ise ikinci sonuç farklı seçeneklerden oluşturulabilir.

---

# Proje Mimarisi

Proje tek bir Python dosyası içerisinde geliştirilmeyecektir.

Temel dosya yapısı:

```text
planmate/
│
├── bot.py
├── config.py
│
├── database/
│   ├── database.py
│   └── schema.sql
│
├── models/
│   ├── user.py
│   ├── activity.py
│   ├── activity_request.py
│   └── recommendation.py
│
├── services/
│   ├── registration_service.py
│   ├── matching_service.py
│   └── recommendation_service.py
│
├── views/
│   ├── start_view.py
│   ├── register_view.py
│   ├── activity_view.py
│   └── recommendation_view.py
│
├── data/
│   └── planmate.db
│
├── requirements.txt
└── .env
```

Genel çalışma mantığı:

```text
Discord Kullanıcısı
        ↓
Discord UI
        ↓
Services
        ↓
Database
        ↓
SQLite
```

---

# Ana Class Yapısı

Projede temel olarak aşağıdaki modeller kullanılacaktır:

```python
User
Activity
ActivityRequest
Recommendation
```

Servis tarafında:

```python
RegistrationService
MatchingService
RecommendationService
```

Veri tabanı tarafında:

```python
Database
```

Discord arayüzünde:

```python
StartView
RegisterView
ActivityView
RecommendationView
```

kullanılacaktır.

---

# Veri Tabanı

PlanMate veri saklama işlemleri için SQLite kullanır.

Temel tablolar:

```text
users
user_available_days
user_interests
activities
activity_requests
```

---

## users

Kullanıcıların temel bilgilerini saklar.

```text
id
discord_id
username
default_budget
```

---

## user_available_days

Kullanıcıların hangi günlerde müsait olduğunu saklar.

Örnek:

```text
user_id | day
-------------------
1       | saturday
1       | sunday
2       | saturday
```

---

## user_interests

Kullanıcıların ilgi alanlarını saklar.

Örnek:

```text
user_id | interest
-------------------
1       | games
1       | cafe
1       | fun
```

---

## activities

Botun önerebileceği aktiviteleri saklar.

Bir aktivite için aşağıdaki bilgiler tutulabilir:

```text
id
name
category
price_per_person
min_people
max_people
solo_allowed
description
```

Örneğin:

```text
Kafeye gitmek
Kategori: Sosyal
Fiyat: 70 TL
Minimum kişi: 1
Maksimum kişi: 6
```

---

## activity_requests

Kullanıcıların yaptığı aktivite aramalarını saklamak için kullanılabilir.

Örneğin:

```text
user_id
requested_day
budget
category
created_at
```

Bu tablo ileride kullanıcı davranışlarını analiz etmek için de kullanılabilir.

---

# Kullanılan Teknolojiler

- Python
- discord.py
- SQLite
- SQL
- Object-Oriented Programming
- Discord Buttons
- Discord Select Menus
- Discord Modals
- Git
- GitHub

---

# Kurulum

Projeyi bilgisayara klonlayın:

```bash
git clone <repository-url>
```

Proje klasörüne girin:

```bash
cd planmate
```

Gerekli Python paketlerini yükleyin:

```bash
pip install -r requirements.txt
```

`.env` dosyasını oluşturun:

```text
DISCORD_TOKEN=your_discord_bot_token
```

Botu çalıştırın:

```bash
python bot.py
```

---

# Güvenlik

Discord bot token'ı hiçbir zaman doğrudan Python dosyasına yazılmamalıdır.

Token `.env` dosyasında tutulmalıdır.

`.env` dosyası GitHub'a yüklenmemelidir.

`.gitignore` içerisinde:

```text
.env
__pycache__/
*.db
```

gibi dosyaların bulunması önerilir.

---

# Demo Sürümünün Kapsamı

İlk sürümde aşağıdaki özelliklerin tamamlanması hedeflenmektedir:

- Kullanıcı kayıt sistemi
- Discord ID üzerinden kullanıcı tanıma
- Boş günlerin kaydedilmesi
- İlgi alanlarının kaydedilmesi
- Bütçe kaydı
- Kullanıcı profili
- Profil düzenleme
- Aktivite arama
- O güne özel bütçe
- Aktivite tercihi
- Kullanıcı eşleştirme
- Bütçe kontrolü
- SQLite aktivite veri tabanı
- Her zaman 3 öneri üretme
- Solo aktivite desteği
- Yeni öneri oluşturma

---

# Gelecekte Eklenebilecek Özellikler

Projenin sonraki sürümlerinde aşağıdaki özellikler eklenebilir:

- Kullanıcıların önerilere puan vermesi
- Daha gelişmiş eşleşme puanı
- Kullanıcıların daha önce yaptığı aktiviteleri kaydetme
- Favori aktiviteler
- Aynı aktivitenin sık tekrarlanmasını engelleme
- Grup oluşturma
- Üç veya daha fazla kullanıcıyı aynı aktivitede eşleştirme
- Aktivite daveti gönderme
- Diğer kullanıcının dav