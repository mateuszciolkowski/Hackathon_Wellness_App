FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY init_db.py .


COPY ./app /app/app


COPY main.py .

CMD ["python", "main.py"]
