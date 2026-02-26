FROM python:3.11-alpine

# Instala dependências necessárias para o pymssql e runtime
RUN apk add --no-cache \
    freetds \
    libstdc++

# Dependências apenas para compilação (removidas após o uso para diminuir a imagem)
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    freetds-dev \
    g++

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Remove as dependências de build para manter a imagem limpa e segura
RUN apk del .build-deps

COPY app.py .
COPY templates ./templates

# Cria um usuário sem privilégios para rodar a aplicação (Melhor Prática de Segurança)
RUN adduser -D appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
