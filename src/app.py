import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pymssql

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DB_SERVER = os.getenv("DB_SERVER", "mssql")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "MinhaSenhaFort3@")
DB_NAME = os.getenv("DB_NAME", "appdb")

def get_conn():
    return pymssql.connect(
        server=DB_SERVER,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )

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

