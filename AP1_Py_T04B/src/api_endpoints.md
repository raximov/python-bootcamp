# API Endpoints Documentation

Loyiha bo'yicha RESTful Web API strukturlanib yozilgan bo'lib asosan Postman yoki bash `curl` yordamida har xil Request va Responselar hosil qilinadi.

---

### Muvaffaqiyatli Javoblar (2xx)
- 200 OK
- 201 Created

### Xatoliklar (4xx, 5xx)
- 400 Bad Request
- 401 Unauthorized
- 404 Not Found
- 409 Conflict (Login doim band bo'lganda)
- 500 Internal Server Error

---

## 1. Authentication Endpoints

### 1.`POST /auth/signup`
**Tavsif:** Yangi foydalanuvchini ro'yxatdan o'tkazish.
**Body (JSON):**
```json
{
    "login": "bob",
    "password": "strongpassword123"
}
```
**Response (201 Created):**
```json
{
    "success": true,
    "message": "Foydalanuvchi yaratildi",
    "id": "uuid-v4-..."
}
```

### 2.`POST /auth/login`
**Tavsif:** Foydalanuvchini tizimdan tekshirish (`Authorization: Basic base64(login:password)` orqali).
**Response (200 OK):**
```json
{
    "id": "uuid-v4-..."
}
```

---

## 2. Games Endpoints

**(Barcha Games marshrutlari Basic Base64 (login:passwd) ni `Authorization` Header orqali talab qiladi.)**

### 3. `POST /games` yoki `POST /games/create`
**Tavsif:** Tizimdagi ro'yxatdan o'tgan foydalanuvchi o'yin boshlash uchun "Waiting" formatdagi game objecti tuzadi. Backend uni `X` simvoli deb olib boradi.
**Body (JSON):**
```json
{
    "opponent": "user"
}
```
`opponent`: `user` yoki `computer` (`user` default).
**Response (201 Created):**
```json
{
    "message": "Yangi o'yin yaratildi",
    "game": {
        "id": "uuid-v4-...",
        "status": "WAITING_FOR_PLAYERS",
        "opponent": "user"
    }
}
```

### 4. `GET /games`
**Tavsif:** Tizimdagi kutish rejimida ('WAITING_FOR_PLAYERS') yotgan barcha o'yinlarni chiqarish (Authorization talab qilinadi).
**Response (200 OK):**
```json
{
    "games": [
        {
            "id": "uuid-v4-...",
            "player_x": "uuid-v4-..."
        }
    ]
}
```

### 5. `POST /games/{id}/join`
**Tavsif:** Biror aniq o'zingizniki bo'lmagan GameID orqali o'yinga ulanasiz va simvolingiz `O`. Va natijada DB 'IN_PROGRESS / PLAYER_TURN' ga tushadi.
**Response (200 OK):**
```json
{
    "message": "Qo'shildingiz!",
    "status": "PLAYER_TURN"
}
```

### 6. `POST /games/{id}/move`
**Tavsif:** Joriy o'yin navbati sizda bo'lsa katakka siljish harakati.
**Body (JSON):**
```json
{
    "position": 5
}
```
**Response (200 OK):**
```json
{
    "board": "----X----",
    "status": "PLAYER_TURN",
    "winner": null
}
```

### 7. `GET /games/{id}`
**Tavsif:** Ma'lumotlarni joriy paytda kim yutgani yoki o'yin qaysi stateligini tomosha qilish.
**Response (200 OK):**
```json
{
    "id": "uuid-v4-...",
    "board": "----X--O-",
    "status": "PLAYER_TURN",
    "player_x": "uuid-v4-...",
    "player_o": "uuid-v4-...",
    "winner": null,
    "current_turn": "uuid-v4-..."
}
```

---

## 3. User Endpoints

### 8. `GET /users/{uuid}`
**Tavsif:** Foydalanuvchi profil ma'lumotlarini qaytaradi (Authorization talab qilinadi).
**Response (200 OK):**
```json
{
    "id": "uuid-v4-...",
    "login": "bob"
}
```
