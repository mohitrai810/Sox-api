FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y sox libsox-dev libsox-fmt-all && \
    apt-get clean

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
