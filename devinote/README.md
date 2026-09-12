# Devinote

### Install
`pip install "fastapi[standard]"`

### Run 🚀
`fastapi dev main.py --port 9090`

### Run with uvicorn 🚀
`uvicorn main:app --reload --port 9090`

### create with CURL
`curl.exe -X POST "http://127.0.0.1:9090/posts" -H "Content-Type: application/json" -d '{ "title": "Fourth Post", "content": "This is the fourth post." }'`

### Install venv
```
python3 -m venv venv

py -V:3.14 -m venv venv
```

### Init Alembic
`alembic init alembic`

#### Migrate
`alembic revision --autogenerate -m "init schema"`

### Run migration
`alembic upgrade head`

### Run migration downgrade previous version (Comando para ejecutar migracion version anterior, revertir el ultimo cambio)
`alembic downgrade -1`

## Stack
1. Python
2. FastAPI
3. SQLModel -> ORM
4. SQLite -> DataBase