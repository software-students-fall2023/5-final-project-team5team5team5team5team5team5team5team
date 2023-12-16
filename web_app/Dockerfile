FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/web_app/

RUN pip install --no-cache-dir -r /app/web_app/requirements.txt

COPY . /app/web_app

EXPOSE 5000

WORKDIR /app/web_app

CMD ["python", "app.py"]
