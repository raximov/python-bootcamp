# Architecture Review

## 1. Project Structure (Loyiha Strukturasi)
Hozirgi holatda barcha kod (`app.py`) bitta fayl ichida yozilgan. Bu - eng keng tarqalgan "Monolithic file" xatosidir. Dastur hajmi kattalashgani sari uni o'qish, test qilish va kengaytirish qiyinlashadi. School21 talablariga mos keladigan to'g'ri struktura (masalan, `routes`, `models`, `services`, `config`) umuman yo'q.

## 2. Layer Separation (Qatlamlarga ajratish)
Dasturda Layered Architecture (Qatlamli arxitektura) qoidalari buzilgan:
- **Presentation Layer (Routes/Controllers):** To'g'ridan-to'g'ri bazaga (DB) murojaat qilmoqda (masalan, `User.query.filter_by(...)`).
- **Business Logic Layer (Services):** Mavjud emas. O'yin logikasi (`check_winner` va harakat qilish logikasi) to'g'ridan-to'g'ri `app.route` ichida (controllerda) yozilgan.
- **Data Access Layer (Repositories/DAOs):** Mavjud emas, ORM dan to'g'ridan-to'g'ri foydalanilgan.

## 3. Dependency Direction (Bog'liqlik yo'nalishi)
Bog'liqliklar aralashib ketgan. Controllers ma'lumotlar bazasi modellari bilan to'g'ridan-to'g'ri bog'langan. To'g'ri yo'nalish: `Controller -> Service -> Repository -> Database` bo'lishi kerak edi. SOLID prinsiplaridan D (Dependency Inversion) umuman ishlatilmagan.

## 4. Missing Files (Yetishmayotgan fayllar)
Quyidagi muhim qismlar yetishmayapti:
- `config.py` (Sozlamalar va muhit o'zgaruvchilarini saqlash uchun)
- `.env` (Maxfiy kalitlar va DB URL uchun)
- `models/` (Ma'lumotlar bazasi modellari uchun alohida modul)
- `services/` (Biznes logikasi, masalan, o'yin va avtorizatsiya ustida ishlash uchun)
- `routes/` (API endpointlarni guruhlash uchun)
- `schemas/` yoki `dto/` (Kirib kelayotgan ma'lumotlarni validatsiya qilish uchun, masalan, Marshmallow yoki Pydantic ishlatilmagan)
- `middlewares/` (Auth middleware alohida joylanishi kerak)
- `utils/` yoki `helpers/` (Yordamchi funksiyalar uchun)

## 5. Anti-Patterns (Yomon amaliyotlar)
- **Hardcoded Secrets:** Bazaga ulanish kodi (`SQLALCHEMY_DATABASE_URI`) to'g'ridan-to'g'ri `app.py` ichida ochiq yozilgan. Bu xavfsizlik (security) uchun juda yomon.
- **Fat Controllers:** Barcha mantiq marshrutlar ichida yozilgan. (`/games/<id>/move` ichida juda ko'p tekshiruv va biznes logikasi mavjud).
- **Silent Exception Swallowing:** `auth_required` dekoratori ichida `except Exception:` blokida barcha xatolar tutib olinib, foydalanuvchiga faqat bitta umumiy xato xabari yuborilmoqda. Asl xatoni debug qilish imkonsiz.
- **Global Object Mutations:** O'yin taxtasi (board) string ko'rinishida saqlanmoqda, bu ma'lumotlarni o'zgartirish va validatsiya qilishni qiyinlashtiradi.

## 6. Logic Qayerda Noto'g'ri?
- **Auth Strategy:** `/login` da Base64 formatida token yasab berish yoki kelayotgan ma'lumotlarni xavfsiz formatda qaytarish yaxshi implement qilinmagan.
- **Game Status Handling:** `WAITING`, `IN_PROGRESS`, `FINISHED`, `DRAW` kabi holatlar magic string'lar ko'rinishida yozilgan. Ularni `Enum` classiga aylantirish kerak.
- **Concurrency Issues:** `move` endpointida "Race condition" ehtimoli bor. Ikki foydalanuvchi bir vaqtda so'rov yuborsa, DB deadlock yuzaga kelishi yoki ma'lumot yozishda xatolik bo'lishi mumkin.
- **Error Handling:** Foydalanuvchi mavjud bo'lmagan o'yinga harakat qilsa yoki noto'g'ri UUID yuborsa bo'ladigan xatoliklar markaziy Error Handler orqali ushlanmagan.
