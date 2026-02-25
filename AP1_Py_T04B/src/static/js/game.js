// static/js/game.js

const API_BASE = window.location.origin;
let currentUser = null;
let currentGameId = null;
let gamePollingInterval = null;

// UI Elements
const authSection = document.getElementById('auth-section');
const lobbySection = document.getElementById('lobby-section');
const gameSection = document.getElementById('game-section');
const userInfo = document.getElementById('user-info');
const authMessage = document.getElementById('auth-message');
const gameMessage = document.getElementById('game-message');
const gamesList = document.getElementById('games-list');

// Initialize
function init() {
    const saved = localStorage.getItem('tictactoe_auth');
    if (saved) {
        currentUser = JSON.parse(saved);
        showLobby();
    } else {
        showAuth();
    }
}

// Navigation
function showAuth() {
    authSection.classList.remove('hidden');
    lobbySection.classList.add('hidden');
    gameSection.classList.add('hidden');
    userInfo.classList.add('hidden');
    stopPolling();
}

function showLobby() {
    authSection.classList.add('hidden');
    lobbySection.classList.remove('hidden');
    gameSection.classList.add('hidden');
    userInfo.classList.remove('hidden');
    document.getElementById('username-display').textContent = currentUser.login;
    fetchGames();
    stopPolling();
}

function showGame(gameId) {
    currentGameId = gameId;
    authSection.classList.add('hidden');
    lobbySection.classList.add('hidden');
    gameSection.classList.remove('hidden');
    userInfo.classList.remove('hidden');
    fetchGameDetails();
    startPolling();
}

// Auth API
function getAuthHeader() {
    if (!currentUser) return {};
    const creds = btoa(`${currentUser.login}:${currentUser.password}`);
    return { 'Authorization': `Basic ${creds}` };
}

async function login() {
    const loginVal = document.getElementById('login-user').value;
    const passVal = document.getElementById('login-pass').value;

    try {
        const creds = btoa(`${loginVal}:${passVal}`);
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Authorization': `Basic ${creds}` }
        });

        if (res.ok) {
            const data = await res.json();
            currentUser = { login: loginVal, password: passVal, uuid: data.uuid };
            localStorage.setItem('tictactoe_auth', JSON.stringify(currentUser));
            showLobby();
        } else {
            authMessage.textContent = "Login failed. Check credentials.";
        }
    } catch (err) {
        authMessage.textContent = "Error connecting to server.";
    }
}

async function signup() {
    const loginVal = document.getElementById('signup-user').value;
    const passVal = document.getElementById('signup-pass').value;

    try {
        const res = await fetch(`${API_BASE}/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ login: loginVal, password: passVal })
        });

        if (res.ok) {
            authMessage.textContent = "Registered! Now please Login.";
            document.querySelector('[data-tab="login-tab"]').click();
        } else {
            const data = await res.json();
            authMessage.textContent = data.message || "Registration failed.";
        }
    } catch (err) {
        authMessage.textContent = "Error connecting to server.";
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem('tictactoe_auth');
    showAuth();
}

// Lobby API
async function fetchGames() {
    try {
        const res = await fetch(`${API_BASE}/games`, { headers: getAuthHeader() });
        const data = await res.json();
        gamesList.innerHTML = '';
        if (data.games && data.games.length > 0) {
            data.games.forEach(g => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span>Game ${g.id.substring(0, 8)}...</span>
                    <button class="btn-small" onclick="joinGame('${g.id}')">Join</button>
                `;
                gamesList.appendChild(li);
            });
        } else {
            gamesList.innerHTML = '<li>No open games found.</li>';
        }
    } catch (err) {
        console.error("Failed to fetch games", err);
    }
}

async function createGame(opponentType) {
    try {
        const res = await fetch(`${API_BASE}/games`, {
            method: 'POST',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ opponent: opponentType })
        });
        const data = await res.json();
        if (res.ok) {
            showGame(data.game.id);
        }
    } catch (err) {
        console.error("Failed to create game", err);
    }
}

async function joinGame(gameId) {
    try {
        const res = await fetch(`${API_BASE}/games/${gameId}/join`, {
            method: 'POST',
            headers: getAuthHeader()
        });
        if (res.ok) {
            showGame(gameId);
        }
    } catch (err) {
        console.error("Failed to join game", err);
    }
}

// Game API
async function fetchGameDetails() {
    if (!currentGameId) return;
    try {
        const res = await fetch(`${API_BASE}/games/${currentGameId}`, { headers: getAuthHeader() });
        if (res.ok) {
            const game = await res.json();
            renderGame(game);
        }
    } catch (err) {
        console.error("Failed to fetch game details", err);
    }
}

async function makeMove(pos) {
    if (!currentGameId) return;
    try {
        const res = await fetch(`${API_BASE}/games/${currentGameId}/move`, {
            method: 'POST',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ position: parseInt(pos) })
        });
        const data = await res.json();
        if (res.ok) {
            renderGame(data);
        } else {
            gameMessage.textContent = data.message || "Invalid move.";
        }
    } catch (err) {
        console.error("Failed to make move", err);
    }
}

// Rendering
function renderGame(game) {
    const boardStr = game.board; // e.g. "X-O---X--"
    const cells = document.querySelectorAll('.cell');

    for (let i = 0; i < 9; i++) {
        const val = boardStr[i] === '-' ? '' : boardStr[i];
        cells[i].textContent = val;
        cells[i].setAttribute('data-val', val);
    }

    document.getElementById('player-x-name').textContent = game.player_x_login || 'Unknown';
    document.getElementById('player-o-name').textContent = game.player_o_login || (game.opponent === 'computer' ? 'Computer' : 'Waiting...');

    document.getElementById('score-x').textContent = game.score_x || 0;
    document.getElementById('score-o').textContent = game.score_o || 0;

    const badge = document.getElementById('game-status-badge');
    badge.textContent = game.status.replace(/_/g, ' ');

    const playAgainBtn = document.getElementById('play-again');

    if (game.status === 'PLAYER_WIN') {
        gameMessage.textContent = game.winner_login ? `${game.winner_login} won!` : "Game Over! Someone won.";
        playAgainBtn.classList.remove('hidden');
        stopPolling();
    } else if (game.status === 'DRAW') {
        gameMessage.textContent = "Draw";
        playAgainBtn.classList.remove('hidden');
        stopPolling();
    } else if (game.status === 'PLAYER_TURN') {
        playAgainBtn.classList.add('hidden');
        if (game.current_turn === currentUser.uuid) {
            gameMessage.textContent = "Your turn!";
        } else {
            gameMessage.textContent = "Opponent's turn...";
        }
    } else {
        gameMessage.textContent = "";
    }
}

// Polling
function startPolling() {
    stopPolling();
    gamePollingInterval = setInterval(fetchGameDetails, 3000);
}

function stopPolling() {
    if (gamePollingInterval) {
        clearInterval(gamePollingInterval);
        gamePollingInterval = null;
    }
}

// Event Listeners
document.getElementById('login-btn').addEventListener('click', login);
document.getElementById('signup-btn').addEventListener('click', signup);
document.getElementById('logout-btn').addEventListener('click', logout);
document.getElementById('create-pve').addEventListener('click', () => createGame('computer'));
document.getElementById('create-pvp').addEventListener('click', () => createGame('user'));
document.getElementById('refresh-games').addEventListener('click', fetchGames);
document.getElementById('back-to-lobby').addEventListener('click', showLobby);
document.getElementById('play-again').addEventListener('click', async () => {
    // Determine opponent type from current state
    const playerOName = document.getElementById('player-o-name').textContent;
    const opponentType = (playerOName === 'Computer' || playerOName === 'computer_bot') ? 'computer' : 'user';
    createGame(opponentType);
});

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));
        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).classList.remove('hidden');
    });
});

document.getElementById('board').addEventListener('click', (e) => {
    if (e.target.classList.contains('cell')) {
        makeMove(e.target.dataset.pos);
    }
});

// Auto-init
init();
window.joinGame = joinGame; // Make accessible globally for onclick
