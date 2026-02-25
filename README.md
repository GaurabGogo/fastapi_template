# Travel App ✈️

FastAPI Travel App built with Clean Architecture, async PostgreSQL, and modern Python tooling.

Built using:

- ⚡ FastAPI
- 🚀 uv (fast Python package manager)
- 🐘 PostgreSQL (async with asyncpg)
- 🧬 SQLAlchemy 2.0
- 🔄 Alembic (migrations)
- 🧹 Ruff (linting & formatting)

---

# 📦 Tech Stack

- **Framework:** FastAPI
- **Package Manager:** uv
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (async)
- **Migrations:** Alembic
- **Validation:** Pydantic v2
- **Rate Limiting:** slowapi

### Core Dependencies

```text
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.6.0
pydantic-settings>=2.1.0
sqlalchemy[asyncio]>=2.0.25
asyncpg>=0.29.0
alembic>=1.13.1
greenlet>=3.0.3
slowapi>=0.1.9
```

---

# 🚀 Getting Started

## 1️⃣ Install uv

If you don’t have uv installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or:

```bash
pip install uv
```

Verify installation:

```bash
uv --version
```

---

## 2️⃣ Setup Project

From the project root (where `pyproject.toml` exists):

### Create virtual environment

```bash
uv venv
```

### Activate virtual environment

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
uv sync
```

---

# 🏃 Running the Application

Start development server:

```bash
uv run dev
```

This is a shortcut for `uvicorn main:app --reload`.

### Dashboard URL

```
http://127.0.0.1:8000
```

### Environment Variables

The app uses a `.env` file for configuration. Standard variables include:

- `APP_HOST`: Default `0.0.0.0` (binds to all interfaces)
- `APP_PORT`: Default `8000`
- `DATABASE_URL`: Async SQLAlchemy connection string

Swagger Docs:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

# 🗄 Database Migrations (Alembic)

### Standard Migrations

```bash
uv run migrate-generate -m "Initial migration"
uv run migrate-upgrade
uv run migrate-downgrade
```

### Manual Commands

```bash
uv run alembic revision --autogenerate -m "description"
uv run alembic upgrade head
```

---

# 🧹 Linting & Formatting

Run Ruff:

```bash
uv run ruff check .
```

Auto-fix issues:

```bash
uv run ruff check . --fix
```

Format code:

```bash
uv run ruff format .
```

---

# 🏗 Project Structure

```
travel_app/
├── src/
│   ├── app.py           # Application entry point & registration
│   ├── core/            # Global utilities (responses, errors, logging)
│   ├── database/        # Async DB configuration
│   ├── sessions/        # Session Tracking Domain (Models, Schemas, Repos, Controllers)
│   └── users/           # User Domain (Model, Schema, Repo, Service, Controller)
├── alembic/             # Database migrations
├── pyproject.toml       # Modern uv & ruff configuration
└── README.md
```

# 🐳 Running with Docker

Start the entire stack (API + PostgreSQL) with a single command:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`. The containerized environment automatically preserves the virtual environment and uses health checks to ensure the database is ready before the app starts.

---

# 🏗 Production Tip (Docker)

Install only production dependencies in container builds:

---

# 🧠 Requirements

- Python 3.11+
- PostgreSQL
- uv

---

# 📌 Notes

- **Clean Domain-Centric Architecture**
- **Async Foundation**: SQLAlchemy 2.0 with `asyncpg`
- **Modern Tooling**: Managed by `uv` for speed and simplicity
- **Developer UX**: Custom `uv` scripts for common tasks
- **Production Ready**: Rate limiting, structured logging, and global error handling
- **Advanced Querying**: Standardized pagination, sorting, and name search
- **Session Tracking**: Built-in support for travel sessions with strict location geometry validation

---

# 📄 License

MIT
