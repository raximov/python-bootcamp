// static/js/game.js

// O'yin identifikatori (misol uchun, test-uuid)
let gameUUID = "test-uuid";

// O'yin rejimi: "2player" – ikki o'yinchi, "singleplayer" – kompyuterga qarshi o'yin.
let mode = "2player";

// 3x3 o'lchamdagi global o'yin maydoni (0 – bo'sh, 1 – X, 2 – O)
let board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
];

// O'yin tugaganligini bildiruvchi flag
let gameOver = false;

// DOMda o'yin maydonini yangilash
function updateBoard(board) {
    for (let i = 0; i < board.length; i++) {
        for (let j = 0; j < board[i].length; j++) {
            let cell = document.querySelector(`td[data-i="${i}"][data-j="${j}"]`);
            if (board[i][j] === 1) {
                cell.textContent = "X"; // Belgilar odatda o'zgarmaydi
            } else if (board[i][j] === 2) {
                cell.textContent = "O";
            } else {
                cell.textContent = "";
            }
        }
    }
}

// Foydalanuvchi qadamini serverga yuborish
function sendMove() {
    if (gameOver) return; // Agar o'yin tugagan bo'lsa, yangi qadam yubormaymiz

    let endpoint = (mode === "2player") ? `/game2/${gameUUID}` : `/game/${gameUUID}`;
    fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            uuid: gameUUID,
            board: board
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Server xatosi");
        }
        return response.json();
    })
    .then(data => {
        board = data.board;
        updateBoard(board);
        document.getElementById("message").textContent = data.message;
        // Agar server "O'yin tugadi" deb bildirsa, o'yin tugagan deb belgilaymiz
        if (data.message.includes("tugadi")) {
            gameOver = true;
        }
    })
    .catch(error => console.error("Xato:", error));
}

// O'yinni qayta boshlash uchun so'rov yuborish
function sendRestart() {
    fetch(`/restart/${gameUUID}`, { method: "POST" })
    .then(response => {
        if (!response.ok) {
            throw new Error("O'yinni qayta boshlashda server xatosi");
        }
        return response.json();
    })
    .then(data => {
        board = data.board;
        updateBoard(board);
        document.getElementById("message").textContent = "O'yin qayta boshlandi";
        gameOver = false;
    })
    .catch(error => console.error("Xato:", error));
}

// O'yin maydoni hujayralariga bosish hodisasi
document.querySelectorAll("#board td").forEach(cell => {
    cell.addEventListener("click", function() {
        if (gameOver) return; // Agar o'yin tugagan bo'lsa, yangi qadam qabul qilinmaydi

        let i = parseInt(this.getAttribute("data-i"));
        let j = parseInt(this.getAttribute("data-j"));
        if (board[i][j] !== 0) return; // Hujayra band bo'lsa, qadam qo'ymaymiz

        if (mode === "2player") {
            let countX = board.reduce((sum, row) => sum + row.filter(c => c === 1).length, 0);
            let countO = board.reduce((sum, row) => sum + row.filter(c => c === 2).length, 0);
            board[i][j] = (countX === countO) ? 1 : 2;
        } else {
            board[i][j] = 1;
        }
        updateBoard(board);
        sendMove();
    });
});

// "O'yinni qayta boshlash" tugmasi uchun hodisa
document.getElementById("restartButton").addEventListener("click", function() {
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ];
    updateBoard(board);
    gameOver = false;
    sendRestart();
});

// Sahifa yuklanganda o'yin maydonini ko'rsatish
updateBoard(board);
