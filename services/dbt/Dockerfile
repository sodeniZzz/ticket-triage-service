FROM python:3.12-slim

WORKDIR /dbt

COPY services/dbt/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/dbt /dbt

CMD ["bash", "-c", "dbt deps && dbt build"]
