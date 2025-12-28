FROM python:3.12-slim

ENV AIRFLOW_HOME=/opt/airflow
WORKDIR /opt/airflow

COPY services/airflow/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/airflow/dags /opt/airflow/dags
COPY services/dbt /dbt
RUN dbt deps --project-dir /dbt
CMD ["bash", "-lc", "airflow db init && airflow scheduler"]
