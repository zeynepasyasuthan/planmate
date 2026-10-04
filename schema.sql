PRAGMA foreign_keys = ON;

-- USERS
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discord_id INTEGER UNIQUE NOT NULL,
    username TEXT NOT NULL,
    budget INTEGER NOT NULL
);

-- BOŞ GÜNLER
CREATE TABLE IF NOT EXISTS days (
    user_id INTEGER NOT NULL,
    day TEXT NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- İLGİ ALANLARI
CREATE TABLE IF NOT EXISTS interests (
    user_id INTEGER NOT NULL,
    interest TEXT NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- AKTİVİTELER
-- 0 = sadece birlikte
-- 1 = tek başına da yapılabilir

CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    price INTEGER NOT NULL,
    solo INTEGER NOT NULL
);

-- EĞLENCELİ
INSERT OR IGNORE INTO activities
(name, category, price, solo)
VALUES
('Park challenge', 'fun', 0, 0),
('Komik video çek', 'fun', 0, 1),
('Evde eğlence challenge', 'fun', 20, 1);

-- SAKİN
INSERT OR IGNORE INTO activities
(name, category, price, solo)
VALUES
('Birlikte yürüyüş', 'relax', 0, 0),
('Mini spa', 'relax', 30, 1),
('Müzik dinleme saati', 'relax', 0, 1);

-- HAREKETLİ
INSERT OR IGNORE INTO activities
(name, category, price, solo)
VALUES
('Basketbol', 'active', 0, 0),
('Bisiklet turu', 'active', 0, 0),
('Evde egzersiz', 'active', 0, 1);

-- OYUN
INSERT OR IGNORE INTO activities
(name, category, price, solo)
VALUES
('Kutu oyunu', 'games', 20, 0),
('Online oyun', 'games', 0, 0),
('Tek kişilik oyun gecesi', 'games', 0, 1);

-- YEMEK
INSERT OR IGNORE INTO activities
(name, category, price, solo)
VALUES
('Bir şeyler yemeye git', 'food', 40, 0),
('Evde yemek hazırla', 'food', 30, 1),
('Yeni tarif dene', 'food', 30, 1);

-- KAFE
INSERT OR IGNORE INTO activities
(name, category, price, solo)
VALUES
('Kafeye git', 'cafe', 50, 0),
('Kafede oyun oyna', 'cafe', 60, 0),
('Evde kahve molası', 'cafe', 15, 1);

-- DIŞ MEKAN
INSERT OR IGNORE INTO activities
(name, category, price, solo)
VALUES
('Parkta yürüyüş', 'outdoor', 0, 1),
('Fotoğraf yürüyüşü', 'outdoor', 0, 1),
('Mini piknik', 'outdoor', 40, 0);

-- YARATICI
INSERT OR IGNORE INTO activities
(name, category, price, solo)
VALUES
('Çizim challenge', 'creative', 10, 0),
('Fotoğraf challenge', 'creative', 0, 1),
('Mini tasarım yap', 'creative', 0, 1);

-- FİLM
INSERT OR IGNORE INTO activities
(name, category, price, solo)
VALUES
('Film gecesi', 'movie', 20, 0),
('Komedi filmi izle', 'movie', 0, 1),
('Dizi maratonu', 'movie', 20, 1);