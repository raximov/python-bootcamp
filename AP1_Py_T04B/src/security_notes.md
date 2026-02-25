# Security Notes & Improvements

Eski loyiha (`app.py` monolit) xavfsizlik va clean architecture bo'yicha sezilarli zaifliklarga ega edi. Pulinga yechimlar va "Security Improvements" faza orqali quyidagi yaxshilanishlar amalga oshirildi:

## 1. Parol Hashing (Bcrypt)
Foydalanuvchilarning parollarini ma'lumotlar bazasida clear-text shaklida yoxud umuman xavfsiz holda saqlash xavfi bartaraf etildi. Barcha Login va Signup jarayonlari avtomatik ravishda `bcrypt` bilan ishlashga o'tkazildi (salt generation yordamida rainbow table hujumiga qarshi).

## 2. SQL Injection himoyasi
Database bilan barcha qatlam ishi Python dagi ishonchli **SQLAlchemy ORM** dan API Endpoint Controlleriga uzatildi. Hech qanaqa 'Raw SQL' querylar bo'lmagani tufayli "SQL Injection" o'z-o'zidan limitasiyalanib himoyalandi.

## 3. Input Validation
Mijozdan uzatiluvchi barcha ma'lumotlar avvalo Flask Route orqali Business Logicga, ma'lumotlar bazasiga o'tkazilmasdan **Marshmallow** kutubxonasi yordamida qat'iy tipik checklar ustidan o'tishi ta'minlandi (`schemas/*.py`).
Bu degani ma'nosiz bo'lgan uzunliklar (Max length, Min length), Required fields bor yo'qligi va int/string tekshirishlari validatsiyasi tushuntirildi va tekshirilmoqda.

## 4. Error Handling & Exception Flow
Eski `app.py` da "Silent exception handling" orqali umumiy tracebackni bekitib hamma xatoni 1 ta tip bilan yozish xavfli jarayon edi, natijada mijoz nimaga xatoning asl nusxasini bilolmasligi ortidan debug logikasi buzilishi mumkin emas.
Hozirda marshrutlarda maxsus **`@app.errorhandler`** va **`GameException`** exception handling ishonchli Custom exceptions yaratiladi va mijozga kerakli status code blan faqat kerakli xabarlar JSON tipda server qulamay yuboriladi. Generic 500 error serverni saqlash niyatida.

## 5. Authorization Middleware
Eskisidagi magic yozuvlar `encode` va `decode` maxsus utils orqali yopildi. Foydalanuvchini idsi qaysi id ekanligi faqatgina valid token yuborilganda tasdiqlangan user qabul qilinadi.
