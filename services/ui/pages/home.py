import os
import time
import uuid

import pandas as pd
import streamlit as st
from confluent_kafka import Producer

from src.scripts.io_utils import encode_json

BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TICKETS_TOPIC = os.getenv("KAFKA_TICKETS_TOPIC", "tickets")

st.set_page_config(layout="wide")

st.title("Ticket Triage Service")
st.divider()
st.markdown(
    """
    1. **Upload** a CSV file with support tickets.
    2. Click **Send** to stream tickets.
    3. Open **Analytics** to view predicted priorities and statistics.
    """
)


def send_to_kafka(df: pd.DataFrame):
    producer = Producer({"bootstrap.servers": BROKER})

    df = df.copy()
    df["ticket_id"] = [str(uuid.uuid4()) for _ in range(len(df))]

    progress_bar = st.progress(0)

    for i, row in df.iterrows():
        message = {
            "ticket_id": row["ticket_id"],
            "data": row.drop("ticket_id").to_dict(),
        }
        producer.produce(TICKETS_TOPIC, value=encode_json(message))
        progress_bar.progress((i + 1) / len(df))
        time.sleep(0.001)

    producer.flush()


uploaded_file = st.file_uploader("Upload", type=["csv"], label_visibility="collapsed")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head(5))

    if st.button("Send"):
        with st.spinner("Sending..."):
            send_to_kafka(df)
            st.success("✅ Tickets successfully sent!")
            st.info("Check the **Analytics** to see the results.")
