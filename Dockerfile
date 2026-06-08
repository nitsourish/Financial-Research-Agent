# Dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

#Copy applications
COPY . .

#set environment
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
