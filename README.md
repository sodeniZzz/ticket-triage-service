# Ticket Triage Service

<p align="center">
  <a href="#about">About</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#project-structure">Project Structure</a> •
  <a href="#docker-way-to-quick-start">Quick Start</a>
</p>

 > [!NOTE]
 >
 > This repository is a **student project** for the 2025 HSE/MTS MLOps course. It is based on the Kaggle dataset [customer-support-ticket-dataset](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset/data).

## About

This project is an end-to-end ticket triage service for customer support. Tickets are streamed via Kafka, scored in real time by an ML inference service (CatBoost priority prediction), stored in ClickHouse and visualized in a Streamlit analytics dashboard with dbt marts refreshed on a schedule by Airflow.

<img width="1188" height="590" alt="one-pager" src="https://github.com/user-attachments/assets/a33bd1e5-f716-41ac-9562-d18ccd85cb5b" />

## Architecture

**Components:**

- **ui (Streamlit UI)**
  - Accepts a CSV file with support tickets (one row = one ticket)
  - Publishes tickets to Kafka topic `tickets`
  - Provides two pages:
    - **Home**: upload + send
    - **Analytics**: charts and tables built from dbt marts

- **scorer (ML Service)**
  - Loads a pre-trained **CatBoost** model
  - Runs preprocessing
  - Consumes tickets from Kafka topic `tickets`
  - Publishes scored results to Kafka topic `tickets_scored`

- **clickhouse**
  - Kafka-engine table consumes messages from topic `tickets_scored`
  - Materialized view writes data into `db_tickets.tickets` MergeTree for analytics
  - Table schema is analytics-optimized (compression codecs, tuned partitioning/sorting)

- **dbt**
  - Builds `stg_tickets` staging model from `db_tickets.tickets`
  - Produces analytical models for the dashboard (distributions, top products, recent open tickets)
  - Runs schema validations and data-quality tests

- **airflow**
  - Schedules dbt runs (keeps marts up-to-date for analytics)

- **Kafka Infrastructure**
  - **Kafka** (KRaft mode)
  - **kafka-setup**: auto-creates topics `tickets` and `tickets_scored`

## Project Structure

```text
ticket-triage-service/
├── clickhouse/
│   └── init/
│       └── create_schema.sql
├── services/
│   ├── airflow/
│   │   ├── dags/
│   │   │   └── dbt_marts.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── dbt/
│   │   ├── models/
│   │   │   ├── marts/
│   │   │   │   ├── mart_age_type_priority.sql
│   │   │   │   ├── mart_gender_priority.sql
│   │   │   │   ├── mart_priority_distribution.sql
│   │   │   │   ├── mart_recent_open_tickets.sql
│   │   │   │   ├── mart_status_distribution.sql
│   │   │   │   ├── mart_ticket_channel_distribution.sql
│   │   │   │   ├── mart_ticket_type_distribution.sql
│   │   │   │   ├── mart_top_products_critical.sql
│   │   │   │   └── schema.yml
│   │   │   ├── sources/
│   │   │   │   └── source.yml
│   │   │   └── staging/
│   │   │       ├── stg_tickets.sql
│   │   │       └── stg_tickets.yml
│   │   ├── dbt_project.yml
│   │   ├── Dockerfile
│   │   ├── packages.yml
│   │   ├── profiles.yml
│   │   └── requirements.txt
│   ├── scorer/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── ui/
│       ├── .streamlit/
│       │   └── config.toml
│       ├── pages/
│       │   ├── analytics.py
│       │   └── home.py
│       ├── app.py
│       ├── Dockerfile
│       └── requirements.txt
├── src/
│   ├── logger/
│   │   ├── logger_config.json
│   │   └── logger.py
│   ├── models/
│   │   └── model.cbm
│   └── scripts/
│       ├── inference.py
│       ├── io_utils.py
│       └── preprocessing.py
├── .gitignore
├── .pre-commit-config.yaml
├── docker-compose.yml
└── README.md
```


<h2 id="docker-way-to-quick-start">🐳 Docker-way to Quick Start</h2>

### Prerequisites
- Docker ≥ 20.10
- Docker Compose ≥ v2
- Disk space ~ 4 GB

### Build & Run

```bash
docker compose up -d --build
```

### Open interfaces

- Streamlit UI → [http://localhost:8501](http://localhost:8501)


### Workflow

1. **Upload a CSV file** with support tickets through Streamlit UI.

2. **Click Send** to stream tickets.

3. **Go to Analytics** to explore triage results:
   - Total processed tickets
   - Priority / status / type / channel distributions
   - Top products by critical rate
   - Recent open tickets

### Logs

Each service writes logs. You can view them with:
```bash
docker compose logs <service_name> # Example: scorer, ui, dbt...
```

### UI screenshots

<img width="1840" height="1106" alt="1ui" src="https://github.com/user-attachments/assets/b45cdfb1-579b-4115-9fc8-82f836657af6" />

<img width="1840" height="1106" alt="2ui" src="https://github.com/user-attachments/assets/8e7597ac-e196-4180-9346-07214274dea5" />

<img width="1840" height="1106" alt="3ui" src="https://github.com/user-attachments/assets/8ab8124e-4734-4a94-8125-4c380c7572a9" />
