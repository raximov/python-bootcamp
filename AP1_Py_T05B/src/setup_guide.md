# Setup Guide

Loyihani lokal muhitda tekshirish va ishga tushirish uchun qo'llanma.

## 1. Talablar:
Loyiha komputeringizda ishlashi uchun shular o'rnatilgan bo'lishi kerak:
- **Python 3.9+**
- (Ixtiyoriy) Postman yoki Curl API larni tekshirib olish uchun.

## 2. Database ni sozlash:
Loyiha T04 talabi bo'yicha **PostgreSQL + SQLAlchemy** bilan ishlaydi.

`DATABASE_URL` ni o'rnating:
```bash
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/tictactoe"
```

Kerak bo'lsa quyidagicha DB yarating:
```bash
createdb tictactoe
```

## 3. Integratsiya paketlari to'plamini o'rnatish
1. Pipni yangilab modulning root katalogida turing (`src` ichida):
`pip install -r requirements.txt`
2. Yoki avtomatik tarzda:
```bash
pip install Flask Flask-SQLAlchemy psycopg2-binary bcrypt marshmallow
```

## 4. Serverni yoqish
```bash
python app.py
```
*Server ishga tushganda CLI konsolda: "Backend muvaffaqiyatli ishga tushdi..." e'lon qilinadi va barcha SQLAlchemy modellari asosida jadvallar `create_all` orqali yaratiladi.*

## 5. Test (Postman yoki cURL):
Server ishga tushgach, avvalo bitta user ro'yhatdan o'tkazing:
```bash
curl -X POST http://127.0.0.1:5000/auth/signup \
-H "Content-Type: application/json" \
-d '{"login": "player1", "password": "password123"}'
```
Token yasash:
Buning uchun `player1:password123` yozuvini base64 formatda kodlang bu sizga taxminan `cGxheWVyMTpwYXNzd29yZDEyMw==` berishi kerak.

Skeynari yurgizisangiz va test etsangiz hammasi soz ishlayotganini ko'rishingiz mumkin.
