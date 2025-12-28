FROM python:3.12-slim

WORKDIR /app

COPY services/scorer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src
COPY services/scorer /app

CMD ["python", "app.py"]
