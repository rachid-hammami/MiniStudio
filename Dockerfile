# ========= MiniStudio Dockerfile =========
FROM python:3.11-slim

WORKDIR /app

# 🔧 Installe curl pour le healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# 🧩 Installe les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 📦 Copie le code source
COPY . .

EXPOSE 8000

# 🌍 Variables d'environnement
ENV HOST=0.0.0.0
ENV PORT=8000
ENV APP_ENV=development
ENV PYTHONPATH=/app

# 🚀 Lance Uvicorn avec hot reload
CMD ["uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
