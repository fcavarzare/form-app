# IMAGEM VULNERÁVEL PARA TESTE DE TRIVY
FROM python:3.7-slim-buster

WORKDIR /app

# O Debian Buster antigo tem vulnerabilidades no glibc e openssl
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates ./templates

EXPOSE 8000

# Voltando para Root para o Trivy reclamar disso também
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

