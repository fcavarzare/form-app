import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pymssql

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DB_SERVER = os.getenv("DB_SERVER", "mssql")
DB_USER = os.getenv("DB_USER", "sa")
# Removido default sensível (não deixe senha hardcoded no código)
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "appdb")

def get_conn():
    return pymssql.connect(
        server=DB_SERVER,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        login_timeout=2,
        timeout=5,
    )

# Liveness: só garante que o processo está vivo
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# Readiness: garante que a app consegue falar com o SQL
@app.get("/readyz")
def readyz():
    try:
        conn = pymssql.connect(
            server=DB_SERVER,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            login_timeout=2,
            timeout=2,
        )
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        conn.close()
        return {"status": "ready"}
    except Exception:
        # 503 = NotReady no Kubernetes (sem reiniciar o pod)
        return {"status": "db-down"}, 503

@app.get("/", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
def submit(request: Request, nome: str = Form(...), email: str = Form(...), mensagem: str = Form(...)):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO FormData (Nome, Email, Mensagem) VALUES (%s, %s, %s)",
        (nome, email, mensagem)
    )
    conn.commit()
    conn.close()
    return templates.TemplateResponse("success.html", {
        "request": request,
        "nome": nome
    })

@app.get("/listar", response_class=HTMLResponse)
def listar(request: Request):
    conn = get_conn()
    cursor = conn.cursor(as_dict=True)
    cursor.execute("SELECT * FROM FormData ORDER BY Id DESC")
    dados = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("list.html", {
        "request": request,
        "dados": dados
    })