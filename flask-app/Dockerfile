FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["puyhon", "app.py"]