import os

import clickhouse_connect
import plotly.express as px
import streamlit as st


def get_ch_client():
    host = os.getenv("CLICKHOUSE_HOST", "clickhouse")
    port_http = int(os.getenv("CLICKHOUSE_PORT", "8123"))
    user = os.getenv("CLICKHOUSE_USER", "default")
    password = os.getenv("CLICKHOUSE_PASSWORD", "")
    database = os.getenv("CLICKHOUSE_DATABASE", "db_tickets")

    client = clickhouse_connect.get_client(
        host=host,
        port=port_http,
        username=user,
        password=password,
        database=database,
    )
    return client, database


def get_pie_chart(df, names, values, title):
    if df.empty:
        st.info("No data to display.")
        return
    fig = px.pie(df, names=names, values=values, title=title)
    fig.update_layout(
        title={
            "text": title,
            "x": 0.3,
            "font": {"size": 22},
        }
    )
    st.plotly_chart(fig, use_container_width=True)


def get_stacked_priority_bar(df, title):
    if df.empty:
        st.info("No data to display.")
        return

    fig = px.bar(
        df,
        x="group",
        y="count",
        color="predicted_priority",
        barmode="stack",
    )
    fig.update_layout(
        title={"text": title, "x": 0.5, "xanchor": "center", "font": {"size": 22}}
    )
    st.plotly_chart(fig, use_container_width=True)


CH_CLIENT, CH_DB = get_ch_client()


st.set_page_config(layout="wide")
st.title("Ticket Triage Analytics")


total_tickets = int(
    CH_CLIENT.query_df(f"SELECT count() AS cnt FROM {CH_DB}.tickets")["cnt"].iloc[0]
)
st.metric("Tickets processed", total_tickets, border=True)


col1, col2 = st.columns(2)
with col1:
    df_status = CH_CLIENT.query_df(f"SELECT * FROM {CH_DB}.mart_status_distribution")
    get_pie_chart(df_status, "ticket_status", "tickets_count", "Status distribution")
with col2:
    df_priority = CH_CLIENT.query_df(
        f"SELECT * FROM {CH_DB}.mart_priority_distribution"
    )
    get_pie_chart(
        df_priority, "predicted_priority", "tickets_count", "Priority distribution"
    )


col3, col4 = st.columns(2)
with col3:
    df_type = CH_CLIENT.query_df(f"SELECT * FROM {CH_DB}.mart_ticket_type_distribution")
    get_pie_chart(df_type, "ticket_type", "tickets_count", "Ticket type distribution")

with col4:
    df_channel = CH_CLIENT.query_df(
        f"SELECT * FROM {CH_DB}.mart_ticket_channel_distribution"
    )
    get_pie_chart(
        df_channel, "ticket_channel", "tickets_count", "Ticket channel distribution"
    )


df_products = CH_CLIENT.query_df(f"SELECT * FROM {CH_DB}.mart_top_products_critical")
if df_products.empty:
    st.info("No data to display.")
else:
    fig = px.bar(
        df_products.sort_values("critical_rate", ascending=True),
        x="critical_rate",
        y="product_purchased",
        orientation="h",
    )
    fig.update_layout(
        title={
            "text": "Top 10 products with high critical rate",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 22},
        }
    )
    st.plotly_chart(fig, use_container_width=True)


col5, col6 = st.columns(2)
with col5:
    df_age = CH_CLIENT.query_df(f"SELECT * FROM {CH_DB}.mart_age_type_priority")
    get_stacked_priority_bar(df_age, "Priority distribution by Age Type")

with col6:
    df_gender = CH_CLIENT.query_df(f"SELECT * FROM {CH_DB}.mart_gender_priority")
    get_stacked_priority_bar(df_gender, "Priority distribution by Gender")


st.subheader("Recent scored tickets with Open status")
df_recent_open = CH_CLIENT.query_df(f"SELECT * FROM {CH_DB}.mart_recent_open_tickets")
if df_recent_open.empty:
    st.info("No data to display.")
else:
    st.dataframe(df_recent_open, width="content")
