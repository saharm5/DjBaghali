FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081

CMD ["sh", "-c", "python manage.py migrate --noinput && \
                  python manage.py collectstatic --noinput && \
                  python manage.py runserver 0.0.0.0:8081"]
