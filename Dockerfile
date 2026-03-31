FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create volume for persistent storage
VOLUME ["/data"]

EXPOSE 5000

CMD ["python", "app.py"]