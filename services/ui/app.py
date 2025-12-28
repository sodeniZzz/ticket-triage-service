import streamlit as st

home = st.Page(
    "pages/home.py",
    title="Home",
    icon=":material/home:",
    default=True,
)

analytics = st.Page(
    "pages/analytics.py",
    title="Analytics",
    icon=":material/analytics:",
)

pg = st.navigation([home, analytics])
pg.run()
