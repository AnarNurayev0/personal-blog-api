# Personal Blog API

Based on the [Personal Blog](https://roadmap.sh/projects/personal-blog) project
from roadmap.sh, implemented as a backend-only REST API with role-based admin
auth and PostgreSQL storage instead of the filesystem.

Backend-only personal blog built with **FastAPI**, **SQLModel** and **PostgreSQL**.
Guests can read published articles; users with the `admin` role can manage articles
and admin accounts. This is a backend-only REST API — there is no frontend. Explore
it through the interactive docs at `/docs`.

**Live demo:** https://personal-blog-api-94rd.onrender.com
**API docs:** https://personal-blog-api-94rd.onrender.com/docs

## Tech stack

- Python, FastAPI, Uvicorn
- SQLModel (on top of SQLAlchemy 2.0), PostgreSQL, Alembic for migrations
- HTTP Basic Auth with Argon2 password hashing (`argon2-cffi`)
- Pydantic Settings for configuration

## Authentication & authorization

- Auth is HTTP Basic (username + password sent on every request).
- Users are stored in a `users` table with a `role` column (`admin` / `user`).
  Passwords are never stored in plain text — only their Argon2 hash.
- `401 Unauthorized` — missing or invalid credentials.
- `403 Forbidden` — valid credentials, but the account's role is not `admin`.
- All `/admin/*` routes are protected at the router level
  (`dependencies=[Depends(require_admin)]`), so any route added under those
  routers is protected automatically.
- **Bootstrapping:** `POST /admin` (create a new admin) itself requires an
  existing admin to call it. There is no public registration endpoint, so the
  very first admin account must be inserted directly into the database with
  an Argon2-hashed password before the API can be used to create further
  admins.

## Endpoints

### Public

| Method | Path | Description |
|---|---|---|
| GET | `/articles` | List published articles |
| GET | `/articles/{id}` | Get one published article by id |

Only articles with `published = true` are returned here.

### Admin — articles (`admin` role required)

| Method | Path | Description |
|---|---|---|
| GET | `/admin/articles` | List all articles (published or not) |
| GET | `/admin/articles/{id}` | Get one article by id (any status) |
| POST | `/admin/articles` | Create an article (accepts a single object or a list) |
| PUT | `/admin/articles/{id}` | Replace an article's fields |
| PATCH | `/admin/articles/{id}` | Partially update an article |
| DELETE | `/admin/articles/{id}` | Delete an article |

### Admin — management (`admin` role required)

| Method | Path | Description |
|---|---|---|
| GET | `/admin/me` | Return the currently authenticated admin |
| POST | `/admin` | Create a new admin account (requires an existing admin) |
| GET | `/admin/users` | List all users |

### System

| Method | Path | Description |
|---|---|---|
| GET | `/` | Root, returns a simple status message |
| GET | `/health` | Health check |

## Data model

**users** — `id`, `username` (unique), `password` (Argon2 hash), `role` (defaults to `user`), `created_at`.

**articles** — `id`, `title`, `content`, `published` (boolean, defaults to `true`), `author_id` (FK → `users.id`), `created_at`, `updated_at` (auto-updated on change).

## Getting started

```bash
git clone https://github.com/AnarNurayev0/personal-blog-api.git
cd personal-blog-api
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
DATABASE_HOSTNAME=your-db-host
DATABASE_PORT=5432
DATABASE_USERNAME=your-db-username
DATABASE_PASSWORD=your-db-password
DATABASE_NAME=your-db-name
```

Run migrations and start the server:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`, docs at `http://localhost:8000/docs`.

### Creating the first admin

Since `POST /admin` requires an existing admin, the first admin has to be
created directly in the database.

1. Generate an Argon2 hash locally:

```bash
   python -c "from argon2 import PasswordHasher; import getpass; print(PasswordHasher().hash(getpass.getpass()))"
```

2. Insert the user with that hash:

```sql
   INSERT INTO users (username, password, role)
   VALUES ('your-username', '<hash>', 'admin');
```

From then on, that admin can create further admins through `POST /admin`.

## Deployment

Deployed on [Render](https://render.com), against a managed PostgreSQL
instance (Supabase). Migrations are run with `alembic upgrade head` before
the API is exposed.

> **Note:** the API runs on Render's free tier, which spins down after a
> period of inactivity. The first request after idling can take 30–50
> seconds to respond while the service wakes up — this is expected, not
> a sign the API is broken. Subsequent requests are fast.

## License

MIT