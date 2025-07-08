FROM python:3.11-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do projeto
COPY . .

# Criar e liberar acesso à pasta do banco
RUN mkdir -p src/database && chmod -R 777 src/database

# Expor porta padrão
EXPOSE 5001

# Rodar o app com Gunicorn (produção)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "src.main:app"]
