# Authentication Flow

Loyiha bo'yicha Basic Authentication mexanizmi amalga oshirildi. Tokenlar Base64 yordamida `login:password` ko'rinishida kodlanadi. Parollar esa ma'lumotlar bazasida saqlanishidan avval **bcrypt** yordamida hashlangan.

## Arxitektura ish jarayoni:

1. **Ro'yxatdan o'tish (Signup) - `/auth/signup`:**
   - Client -> Server: Ro'yxatdan o'tish uchun Login va password input qilish. Min length=3 (login), 6 (parol).
   - Marshmallow Schema orqali tekshirish amalga oshiriladi.
   - AuthService -> UserService -> Hash Password -> DB (Create User).
   - Server -> Client: 201 Created va foydalanuvchining ID raqami.

2. **Tizimga kirish (Login) - `/auth/login`:**
   - Marshmallow Schema logik tekshiruvi.
   - Tizimdan `User` larni login orqali axtarish. Hashlangan parol bilan bcrypt ning `checkpw` funksiyasi vositasida avtorizatsiya taqiqlab ochiladi.
   - Client foydalanishi uchun Base64 header encode algoritmini client side yasashi faraz qilinadi (shart emas ochiq token berish).

3. **Autentifikatsiya Middleware (auth_required):**
   - Hamma yopiq marshrutlar boshida turuvchi decorator (wrap).
   - `request.headers.get("Authorization")` ni qidiradi.
   - Kelayotgan Header Format albatta: `Basic bG9naW46cGFzc3dvcmQ=` (misol uchun) bo'lishi talab etiladi.
   - Topib base64dan decode olinib parollar tekshirilgandan so'ng, marshrutlarga `current_user` objecti uzatiladi. 
