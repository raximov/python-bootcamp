# Database Design

Ma'lumotlar bazasi UUID asosida ishlaydi asosan ikki `users` va `games` jadvallarini o'z ichiga oladi.

## Users jadvali

| Field | Type | Properties | Description |
|---|---|---|---|
| id | UUID | PRIMARY KEY, Default: uuid4 | Foydalanuvchining unikal identifikatori |
| login | VARCHAR(80) | UNIQUE, NOT NULL | Tizimga kirish uchun login |
| password | VARCHAR(200) | NOT NULL | Bcrypt yordamida heshlangan parol |

## Games jadvali

| Field | Type | Properties | Description |
|---|---|---|---|
| id | UUID | PRIMARY KEY, Default: uuid4 | O'yinning unikal identifikatori |
| board | VARCHAR(9) | Default: '---------' | 9 ta katakdan iborat taxta. Har bir belgi '-', 'X', yoki 'O' bo'lishi mumkin. |
| status | ENUM | Default: WAITING_FOR_PLAYERS | O'yin joriy holati. (WAITING_FOR_PLAYERS, PLAYER_TURN, DRAW, PLAYER_WIN) |
| player_x_id | UUID | FOREIGN KEY (users.id) | 'X' simvolini tanlagan o'yinchi (yaratgan). |
| player_o_id | UUID | FOREIGN KEY (users.id) | 'O' simvolini tanlagan o'yinchi (qo'shilgan). |
| current_turn_id | UUID | FK (users.id) | Ayni vaqtda yurish navbati qaysi id egasiga tegishli. |
| winner_id | UUID | FK (users.id), NULLABLE | Agar o'yin kimningdir g'alabasi bilan tugasa shuni saqlaymiz |

## Relationships

- Bir `User` bir necha marta ko'plab `Games` larda ham `player_x_id` yoki `player_o_id` bo'lishi ehtimoli bor. O'yin bazaviy ma'lumotlar strukturasida ushbu bog'lanish `current_turn_id` va `winner_id` vositasida saqlanadi.
