# Використовуємо офіційний Python образ
FROM python:3.12-slim

# Встановлюємо залежності для PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо requirements.txt
COPY requirements.txt .

# Встановлюємо залежності Python
RUN pip install -r requirements.txt

# Копіюємо проект
COPY . .

# Відкриваємо порт
EXPOSE 8000

# Запускаємо команду для старту
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]