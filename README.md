# First steps FastAPI

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