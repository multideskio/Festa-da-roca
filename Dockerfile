# Use a imagem oficial do Python como base
FROM python:3.11-slim

# Defina variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código
COPY . .

# Crie o diretório para o banco de dados SQLite (se necessário)
RUN mkdir -p src/database

# Exponha a porta em que a aplicação vai rodar
EXPOSE 5001

# Comando para executar a aplicação
CMD ["python", "src/main.py"]
