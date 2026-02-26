import os
import pymssql

from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from prometheus_fastapi_instrumentator import Instrumentator

# v1.0.1 - Ajuste de resiliência e segurança
app = FastAPI()
Instrumentator().instrument(app).expose(app)
templates = Jinja2Templates(directory="templates")

DB_SERVER = os.getenv("DB_SERVER", "mssql")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD")  # sem default sensível
DB_NAME = os.getenv("DB_NAME", "appdb")


def get_conn(timeout: int = 5) -> pymssql.Connection:
    """
    Conexão padrão para uso nas rotas.
    - login_timeout: tempo máximo para autenticar/abrir sessão
    - timeout: timeout de operações (query)
    """
    if not DB_PASSWORD:
        # Falha explícita: ajuda a diagnosticar secret/env faltando
        raise RuntimeError("DB_PASSWORD is not set")

    return pymssql.connect(
        server=DB_SERVER,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        login_timeout=2,
        timeout=timeout,
    )


# Liveness: só garante que o processo está vivo (NÃO depende do DB)
@app.get("/healthz")
def healthz():
    print("Healthcheck requested")
    return {"status": "ok"}


# Readiness: garante que a app consegue falar com o SQL
@app.get("/readyz")
def readyz():
    try:
        conn = get_conn(timeout=2)
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.fetchone()
        finally:
            conn.close()

        return {"status": "ready"}
    except Exception:
        # 503 => Pod fica NotReady (Service para de enviar tráfego) sem reiniciar
        raise HTTPException(status_code=503, detail="db-down")


@app.get("/", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
def submit(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    mensagem: str = Form(...),
):
    try:
        conn = get_conn(timeout=5)
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO FormData (Nome, Email, Mensagem) VALUES (%s, %s, %s)",
                (nome, email, mensagem),
            )
            conn.commit()
        finally:
            conn.close()

        return templates.TemplateResponse("success.html", {"request": request, "nome": nome})

    except Exception as e:
        # Retorno amigável em HTML (sem crash). Você pode criar um template error.html se quiser.
        return HTMLResponse(
            content=f"<h3>Erro ao gravar no banco</h3><pre>{str(e)}</pre>",
            status_code=500,
        )


@app.get("/listar", response_class=HTMLResponse)
def listar(request: Request):
    try:
        conn = get_conn(timeout=5)
        try:
            cursor = conn.cursor(as_dict=True)
            cursor.execute("SELECT * FROM FormData ORDER BY Id DESC")
            dados = cursor.fetchall()
        finally:
            conn.close()

        return templates.TemplateResponse("list.html", {"request": request, "dados": dados})

    except Exception as e:
        return HTMLResponse(
            content=f"<h3>Erro ao consultar o banco</h3><pre>{str(e)}</pre>",
            status_code=500,
        )