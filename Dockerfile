FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p src/database && chmod -R 777 src/database

EXPOSE 5001

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "src.main:app"]