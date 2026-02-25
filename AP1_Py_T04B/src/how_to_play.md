# How To Play Tic-Tac-Toe API

This project is a backend API (no browser game board).  
You play by sending HTTP requests.

## 1. Start server

From `src/`:

```bash
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/tictactoe"
python app.py
```

If you get PostgreSQL auth errors and just want to play now, use SQLite:

```bash
export DATABASE_URL="sqlite:///tictactoe.db"
python app.py
```

## 2. Play in Postman (recommended)

## 2.1 Create Postman environment

Create an environment and add:

- `base_url` = `http://127.0.0.1:5000`
- `game_id` = (empty)

## 2.2 Register users

Request 1:

- Method: `POST`
- URL: `{{base_url}}/auth/signup`
- Headers: `Content-Type: application/json`
- Body (raw JSON):

```json
{
  "login": "player1",
  "password": "password123"
}
```

Request 2 (same endpoint, different login):

```json
{
  "login": "player2",
  "password": "password123"
}
```

## 2.3 Login check (optional)

- Method: `POST`
- URL: `{{base_url}}/auth/login`
- Authorization tab: `Basic Auth`
- Username: `player1`
- Password: `password123`

Postman will generate `Authorization: Basic ...` automatically.

## 2.4 Vs computer flow

1. Create game:
   - Method: `POST`
   - URL: `{{base_url}}/games`
   - Authorization: `Basic Auth` (`player1/password123`)
   - Body:

```json
{
  "opponent": "computer"
}
```

2. Copy `game.id` from response into environment variable `game_id`.

3. Make move:
   - Method: `POST`
   - URL: `{{base_url}}/games/{{game_id}}/move`
   - Authorization: `Basic Auth` (`player1/password123`)
   - Body:

```json
{
  "position": 1
}
```

4. Check state:
   - Method: `GET`
   - URL: `{{base_url}}/games/{{game_id}}`
   - Authorization: `Basic Auth` (`player1/password123`)

## 2.5 P2P (two players) flow

1. Player1 creates game:
   - Method: `POST`
   - URL: `{{base_url}}/games`
   - Authorization: `Basic Auth` (`player1/password123`)
   - Body:

```json
{
  "opponent": "user"
}
```

2. Copy returned `game.id` to `{{game_id}}`.

3. Player2 gets waiting games:
   - Method: `GET`
   - URL: `{{base_url}}/games`
   - Authorization: `Basic Auth` (`player2/password123`)

4. Player2 joins:
   - Method: `POST`
   - URL: `{{base_url}}/games/{{game_id}}/join`
   - Authorization: `Basic Auth` (`player2/password123`)

5. Turns:
   - Player1 move: `POST {{base_url}}/games/{{game_id}}/move` body `{"position":1}`
   - Player2 move: `POST {{base_url}}/games/{{game_id}}/move` body `{"position":5}`
   - Each request uses that player's own Basic Auth.

## 3. Useful endpoints

- `GET /games/GAME_ID`: current board/state
- `GET /users/<uuid>`: user info

All `/games/*` and `/users/*` endpoints require `Authorization: Basic ...`.

## 4. Troubleshooting PostgreSQL auth error

If you see:
`password authentication failed for user "postgres"`

It means your local PostgreSQL password is different from the one in `DATABASE_URL`.

Run these as a machine admin:

```bash
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'postgres';
CREATE DATABASE tictactoe;
\q
```

Then:

```bash
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/tictactoe"
python app.py
```

## 5. cURL alternative (if needed)

If you prefer terminal instead of Postman, use the same endpoints with `curl` commands from previous version.
