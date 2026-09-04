# Mirzo Yusuf (Bodomzor) Jome Masjidi — Rasmiy Sayt

Toshkent shahri, Yunusobod tumani, Bodomzor ko'chasidagi Mirzo Yusuf jome masjidining rasmiy veb-sayti.

## 🕌 Masjid haqida
- **Manzil:** Toshkent shahri, Yunusobod tumani
- **Koordinatlar:** 41.3372993, 69.2911802

## 🛠 Texnologiyalar
- Vanilla HTML/CSS/JavaScript
- Tailwind CSS (CDN)
- Firebase Realtime Database
- Aladhan API (namoz vaqtlari)
- Telegram Bot (duo va obunalar)

## 📁 Fayl tuzilmasi
```
├── index.html        — Asosiy sahifa
├── admin.html        — Admin boshqaruv paneli
├── main.js           — Barcha JavaScript mantiq
├── firebase-config.js — Firebase konfiguratsiyasi (alohida)
└── assets/
    └── images/       — Rasmlar
```

## ⚙️ Sozlash

### Firebase
1. [Firebase Console](https://console.firebase.google.com) da yangi loyiha yarating
2. `firebase-config.js` faylidagi `YOUR_*` qiymatlarni almashtiring

### Telegram Bot
1. `@BotFather` orqali yangi bot yarating
2. Admin panelga kiring (`admin.html`)
3. **Bot sozlamalari** bo'limida token va admin IDlarni kiriting

## 🔐 Admin Panel
`admin.html` fayliga kiring — standart parol: `masjid2026`

> ⚠️ **Muhim:** Standart parolni zudlik bilan o'zgartiring!
