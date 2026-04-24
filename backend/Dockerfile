FROM python:3.11-slim
WORKDIR /app

# Production environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Layer cache dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy actual app contents
COPY . .

# Avoid running container as root
RUN useradd -m myuser
USER myuser

EXPOSE 8000

# Run production-grade uvicorn loop
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]