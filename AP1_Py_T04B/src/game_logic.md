# Game Logic Flow

Loyiha "Tic-Tac-Toe" ni ikkita personaj qatnashadigan holatda tarmoq orqali amalga oshirdi. Markaziy jarayonlarda **State Machine** ishlatilgan.

## Game States: State Machine

Barcha marshrutlar navbat va stateni qat'iy tekshiradi:
- **`WAITING_FOR_PLAYERS`**: Birinchi foydalanuvchi `POST /games/create` orqali o'yin yaratganda o'yin shunday holat bilan saqlanadi. Ular harakat qilolmaydi, ungacha o'yinga ulanishlari kerak.
- **`PLAYER_TURN`**: Boshqa biror ishtirokchi qatnashishni ixtiyor etganda (`POST /games/{id}/join`), holat shunday o'zgaradi. Faqat shu holatdagina ikkala personaj (`current_turn_id` yordamida kimniki ekani tasdiqlangach) harakat qilishi mumkin.
- **`DRAW`**: Agar `board` parametrida 9 ta element orasida '-' belgi mavjud bo'lmasa qisqacha 'DRAW' tushiriladi va o'yin tugaydi.
- **`PLAYER_WIN`**: Navbat bajaruvchi harakatidan so'ng algoritmni tekshirib `(3x3 qatorlar, 3x3 ustunlar yoki diagonallar)` g'olib chiqsa g'irromlik qilinmasligi uchun `winner_id` aniqlanadi.

## Gameplay Logic:
- Server har doim taxtani String holatida List strukturasiga tarqatib saqlab kiritayotgan indeks band emasligini ta'minlaydi (`idx = input - 1` ya'ni Client uchun list 1..9 va server uchun taxta 0..8 array deb qabul qiindi).
- Qaysi o'yinchinining ramzi kimligini doimo user idlarni player x va player o lar bilan solishtirilgan holda aniqlaydi. 
