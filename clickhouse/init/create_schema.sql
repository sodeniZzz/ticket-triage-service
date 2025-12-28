CREATE DATABASE db_tickets;
USE db_tickets;

CREATE TABLE tickets_scored_queue
(
    ticket_id             String,
    predicted_priority    String,
    customer_age          Int32,
    customer_gender       String,
    product_purchased     String,
    ticket_type           String,
    ticket_channel        String,
    ticket_status         String,
    ticket_subject        String,
    age_type              String,
    days_from_purchase    Int32
)
ENGINE = Kafka
SETTINGS
    kafka_broker_list    = 'kafka:9092',
    kafka_topic_list     = 'tickets_scored',
    kafka_group_name     = 'ch_tickets_scored_consumer',
    kafka_format         = 'JSONEachRow',
    kafka_num_consumers = 3;


CREATE TABLE tickets
(
    ticket_id             String CODEC(ZSTD),
    predicted_priority    LowCardinality(String),
    customer_age          Int32 CODEC(T64),
    customer_gender       LowCardinality(String),
    product_purchased     LowCardinality(String),
    ticket_type           LowCardinality(String),
    ticket_channel        LowCardinality(String),
    ticket_status         LowCardinality(String),
    ticket_subject        String CODEC(ZSTD),
    age_type              LowCardinality(String),
    days_from_purchase    Int32 CODEC(T64)
)
ENGINE = MergeTree
PARTITION BY intDiv(days_from_purchase, 30)
ORDER BY (predicted_priority, ticket_type);

CREATE MATERIALIZED VIEW tickets_scored_mv TO tickets AS
SELECT * FROM tickets_scored_queue;
