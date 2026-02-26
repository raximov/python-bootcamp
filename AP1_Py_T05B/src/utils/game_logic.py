def check_winner(board: str) -> str:
    """
    O'yin taxtasini qabul qilib, joriy holatda g'olib bor yoki yo'qligini tekshiradi.
    O'yin taxtasi '---------' (9 ta belgi) korinishida keladi.
    Qaytaradigan qiymatlari:
    - 'X': X yutdi
    - 'O': O yutdi
    - 'DRAW': Durang bo'ldi
    - None: Yin davom etmoqda
    """
    win_conf = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), # Qatorlar
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # Ustunlar
        (0, 4, 8), (2, 4, 6)             # Diagonallar
    ]
    
    for a, b, c in win_conf:
        if board[a] == board[b] == board[c] and board[a] != '-':
            return board[a]
            
    if '-' not in board:
        return 'DRAW'
        
    return None
