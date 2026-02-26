const app = {
    accessToken: localStorage.getItem('accessToken'),
    refreshToken: localStorage.getItem('refreshToken'),
    currentUser: null,
    currentGame: null,
    pollingInterval: null,

    init: async function() {
        if (this.accessToken) {
            await this.fetchUserInfo();
        }
        this.render();
    },

    // --- API Methods ---
    api: async function(url, method = 'GET', body = null, auth = true) {
        const headers = { 'Content-Type': 'application/json' };
        if (auth && this.accessToken) {
            headers['Authorization'] = `Bearer ${this.accessToken}`;
        }

        const options = { method, headers };
        if (body) options.body = JSON.stringify(body);

        let response = await fetch(url, options);

        // Handle Token Refresh
        if (response.status === 401 && auth && this.refreshToken) {
            const refreshSuccess = await this.handleTokenRefresh();
            if (refreshSuccess) {
                headers['Authorization'] = `Bearer ${this.accessToken}`;
                response = await fetch(url, options);
            } else {
                this.logout();
                return null;
            }
        }

        return response;
    },

    handleAuth: async function(isSignup = false) {
        const endpoint = isSignup ? '/auth/signup' : '/auth/login';
        const login = document.getElementById(isSignup ? 'signup-login' : 'login-input').value;
        const password = document.getElementById(isSignup ? 'signup-password' : 'password-input').value;
        const errorEl = document.getElementById('auth-error');

        errorEl.classList.add('hidden');

        try {
            const res = await this.api(endpoint, 'POST', { login, password }, false);
            const data = await res.json();

            if (res.ok) {
                if (isSignup) {
                    alert("Muvaffaqiyatli ro'yxatdan o'tdingiz! Endi kiring.");
                    this.toggleAuthMode();
                } else {
                    this.accessToken = data.accessToken;
                    this.refreshToken = data.refreshToken;
                    localStorage.setItem('accessToken', data.accessToken);
                    localStorage.setItem('refreshToken', data.refreshToken);
                    await this.fetchUserInfo();
                    this.render();
                }
            } else {
                errorEl.innerText = data.error || data.message || "Xatolik yuz berdi";
                errorEl.classList.remove('hidden');
            }
        } catch (e) {
            console.error(e);
        }
    },

    handleTokenRefresh: async function() {
        try {
            const res = await fetch('/auth/refresh', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refreshToken: this.refreshToken })
            });
            const data = await res.json();
            if (res.ok) {
                this.accessToken = data.accessToken;
                localStorage.setItem('accessToken', data.accessToken);
                return true;
            }
        } catch (e) {}
        return false;
    },

    fetchUserInfo: async function() {
        const res = await this.api('/auth/userinfo');
        if (res && res.ok) {
            this.currentUser = await res.json();
        } else {
            this.logout();
        }
    },

    logout: function() {
        this.accessToken = null;
        this.refreshToken = null;
        this.currentUser = null;
        localStorage.clear();
        this.stopPolling();
        this.render();
    },

    toggleAuthMode: function() {
        document.getElementById('login-form').classList.toggle('hidden');
        document.getElementById('signup-form').classList.toggle('hidden');
        document.getElementById('auth-title').innerText = 
            document.getElementById('login-form').classList.contains('hidden') ? "Ro'yxatdan o'tish" : "Xush kelibsiz!";
    },

    // --- Game Methods ---
    createGame: async function(opponent) {
        const res = await this.api('/games/create', 'POST', { opponent });
        const data = await res.json();
        if (res.ok) {
            this.openGame(data.game);
        }
    },

    fetchWaitingGames: async function() {
        const res = await this.api('/games');
        if (res && res.ok) {
            const data = await res.json();
            const list = document.getElementById('waiting-games-list');
            list.innerHTML = data.games.length === 0 ? '<p style="color: var(--text-muted);">Hozircha ochiq o\'yinlar yo\'q...</p>' : '';
            data.games.forEach(g => {
                const div = document.createElement('div');
                div.className = 'list-item animate-fade';
                div.innerHTML = `
                    <span>O'yin #${g.id.substring(0,8)}</span>
                    <button class="btn btn-primary" style="width: auto; padding: 4px 12px; font-size: 0.8rem;" onclick="app.joinGame('${g.id}')">Qo'shilish</button>
                `;
                list.appendChild(div);
            });
        }
    },

    joinGame: async function(gameId) {
        const res = await this.api(`/games/${gameId}/join`, 'POST');
        if (res.ok) {
            const gameData = await this.api(`/games/${gameId}`);
            this.openGame(await gameData.json());
        }
    },

    makeMove: async function(position) {
        if (!this.currentGame || this.currentGame.current_turn !== this.currentUser.id) return;
        
        const res = await this.api(`/games/${this.currentGame.id}/move`, 'POST', { position });
        if (res.ok) {
            this.currentGame = await res.json();
            this.updateBoard();
        }
    },

    openGame: function(game) {
        this.currentGame = game;
        document.getElementById('dashboard').classList.add('hidden');
        document.getElementById('game-view').classList.remove('hidden');
        this.updateBoard();
        this.startPolling();
    },

    showDashboard: function() {
        this.currentGame = null;
        this.stopPolling();
        document.getElementById('game-view').classList.add('hidden');
        document.getElementById('dashboard').classList.remove('hidden');
        this.render();
    },

    updateBoard: function() {
        if (!this.currentGame) return;
        
        const cells = document.querySelectorAll('.cell');
        const board = this.currentGame.board;
        
        cells.forEach((cell, i) => {
            cell.innerText = board[i] === '-' ? '' : board[i];
            cell.className = 'cell' + (board[i] === 'X' ? ' x' : board[i] === 'O' ? ' o' : '');
        });

        const isMyTurn = this.currentGame.current_turn === this.currentUser.id;
        document.getElementById('game-status-text').innerText = isMyTurn ? "Sizning navbatingiz!" : "Raqib kutilmoqda...";
        document.getElementById('game-info').innerText = `X: ${this.currentGame.player_x_login} vs O: ${this.currentGame.player_o_login}`;

        if (this.currentGame.status === 'PLAYER_WIN' || this.currentGame.status === 'DRAW') {
            this.stopPolling();
            document.getElementById('game-results').classList.remove('hidden');
            document.getElementById('game-board').classList.add('hidden');
            document.getElementById('game-status-text').innerText = "O'yin tugadi!";
            
            if (this.currentGame.status === 'DRAW') {
                document.getElementById('winner-announcement').innerText = "DURANG!";
            } else {
                const isIWin = this.currentGame.winner === this.currentUser.id;
                document.getElementById('winner-announcement').innerText = isIWin ? "SIZ G'ALABA QOZONDINGIZ! 🎉" : "Siz yutqazdingiz... 💀";
                document.getElementById('winner-announcement').style.color = isIWin ? 'var(--success)' : 'var(--error)';
            }
        } else {
            document.getElementById('game-results').classList.add('hidden');
            document.getElementById('game-board').classList.remove('hidden');
        }
    },

    // --- Stats Methods ---
    fetchStats: async function() {
        const historyRes = await this.api('/games/history');
        if (historyRes.ok) {
            const data = await historyRes.json();
            const list = document.getElementById('history-list');
            list.innerHTML = '';
            data.games.slice(0, 5).forEach(g => {
                const div = document.createElement('div');
                div.className = 'list-item';
                const result = g.status === 'DRAW' ? 'Durang' : (g.winner === this.currentUser.id ? 'G\'alaba' : 'Mag\'lubiyat');
                div.innerHTML = `<span>Vs ${g.player_o_login === this.currentUser.login ? g.player_x_login : g.player_o_login}</span> <b>${result}</b>`;
                list.appendChild(div);
            });
        }

        const lbRes = await this.api('/games/leaderboard?n=5');
        if (lbRes.ok) {
            const data = await lbRes.json();
            const list = document.getElementById('leaderboard-list');
            list.innerHTML = '';
            data.leaderboard.forEach((r, i) => {
                const div = document.createElement('div');
                div.className = 'list-item';
                div.innerHTML = `<span>#${i+1} ${r.login}</span> <span style="color: var(--primary)">${(r.win_ratio * 100).toFixed(0)}%</span>`;
                list.appendChild(div);
            });
        }
    },

    // --- UI Rendering ---
    render: function() {
        if (this.currentUser) {
            document.getElementById('auth-section').classList.add('hidden');
            document.getElementById('app-section').classList.remove('hidden');
            document.getElementById('username-display').innerText = this.currentUser.login;
            document.getElementById('user-avatar').innerText = this.currentUser.login[0].toUpperCase();
            this.fetchWaitingGames();
            this.fetchStats();
        } else {
            document.getElementById('auth-section').classList.remove('hidden');
            document.getElementById('app-section').classList.add('hidden');
        }
    },

    startPolling: function() {
        this.stopPolling();
        this.pollingInterval = setInterval(async () => {
            if (this.currentGame) {
                const res = await this.api(`/games/${this.currentGame.id}`);
                if (res.ok) {
                    this.currentGame = await res.json();
                    this.updateBoard();
                }
            } else {
                this.fetchWaitingGames();
            }
        }, 3000);
    },

    stopPolling: function() {
        if (this.pollingInterval) clearInterval(this.pollingInterval);
    }
};

// Start app
app.init();
