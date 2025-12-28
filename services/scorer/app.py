import logging
import os

import pandas as pd
from confluent_kafka import Consumer, Producer

from src.logger.logger import setup_logging
from src.scripts.inference import make_pred
from src.scripts.io_utils import decode_json, encode_json
from src.scripts.preprocessing import preprocess

setup_logging()
logger = logging.getLogger(__name__)

BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TICKETS_TOPIC = os.getenv("KAFKA_TICKETS_TOPIC", "tickets")
SCORES_TOPIC = os.getenv("KAFKA_SCORES_TOPIC", "tickets_scored")


class TicketScorerService:
    """Service that consumes tickets from Kafka, scores them, and publishes results."""

    def __init__(self):
        self.consumer = Consumer(
            {
                "bootstrap.servers": BROKER,
                "group.id": "ticket-scorer",
                "auto.offset.reset": "earliest",
            }
        )
        self.consumer.subscribe([TICKETS_TOPIC])
        self.producer = Producer({"bootstrap.servers": BROKER})

        logger.info(
            f"TicketScorerService initialized. "
            f"Subscribed to topic: {TICKETS_TOPIC}, "
            f"producing to: {SCORES_TOPIC}"
        )
        self.processed_total = 0

    def process_ticket(self, ticket: dict):
        try:
            ticket_id = ticket["ticket_id"]
            df_raw = pd.DataFrame([ticket["data"]])

            preprocessed = preprocess(df_raw)
            pred_df = make_pred(preprocessed)

            result = {
                "ticket_id": str(ticket_id),
                "predicted_priority": str(pred_df["predicted_priority"].iloc[0]),
                "customer_age": int(df_raw["Customer Age"].iloc[0]),
                "customer_gender": str(df_raw["Customer Gender"].iloc[0]),
                "product_purchased": str(df_raw["Product Purchased"].iloc[0]),
                "ticket_type": str(df_raw["Ticket Type"].iloc[0]),
                "ticket_channel": str(df_raw["Ticket Channel"].iloc[0]),
                "ticket_status": str(df_raw["Ticket Status"].iloc[0]),
                "ticket_subject": str(df_raw["Ticket Subject"].iloc[0]),
                "age_type": str(preprocessed["Age Type"].iloc[0]),
                "days_from_purchase": int(preprocessed["Days From Purchase"].iloc[0]),
            }

            self.producer.produce(SCORES_TOPIC, value=encode_json(result))
            self.producer.flush()
            self.processed_total += 1
        except Exception as e:
            logger.error(f"Error while processing ticket: {e}", exc_info=True)

    def run(self):
        logger.info("TicketScorerService started. Waiting for messages...")
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error(f"Kafka error: {msg.error()}")
                continue
            try:
                ticket = decode_json(msg.value())
                self.process_ticket(ticket)
            except Exception as e:
                logger.error(f"Invalid message format: {e}", exc_info=True)
            if self.processed_total % 1000 == 0:
                logger.info(f"Processed {self.processed_total} rows")


if __name__ == "__main__":
    service = TicketScorerService()
    try:
        service.run()
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
