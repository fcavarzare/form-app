# Estágio 1: Builder (Compilação)
FROM python:3.11-alpine AS builder

# Dependências de compilação necessárias para o pymssql
RUN apk add --no-cache \
    gcc \
    python3-dev \
    musl-dev \
    freetds-dev \
    g++

WORKDIR /install

COPY requirements.txt .

# Instala as dependências em um diretório específico para facilitar a cópia
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Estágio 2: Runtime (Final)
FROM python:3.11-alpine

# Instala apenas as bibliotecas de runtime necessárias
RUN apk add --no-cache \
    freetds \
    libstdc++

WORKDIR /app

# Copia as bibliotecas instaladas do estágio builder
COPY --from=builder /install /usr/local

# Copia o código da aplicação
COPY app.py .
COPY templates ./templates

# Cria um usuário sem privilégios e ajusta permissões
RUN adduser -D appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
