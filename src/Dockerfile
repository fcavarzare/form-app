# IMAGEM PARA SIMULAR FALHA DE SEGURANÇA NO TRIVY
# A versão full (não slim) tem muito mais pacotes e, consequentemente, mais vulnerabilidades.
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates ./templates

# Rodando como root para o Trivy também apontar esse risco
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

