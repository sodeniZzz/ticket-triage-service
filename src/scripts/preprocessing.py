import pandas as pd

NUM_FEATURES = ["Customer Age", "Days From Purchase"]
CAT_FEATURES = [
    "Customer Gender",
    "Product Purchased",
    "Ticket Type",
    "Ticket Channel",
    "Age Type",
]
TEXT_FEATURES = ["Ticket Description", "Ticket Subject"]
DROP_COLUMNS = [
    "Ticket ID",
    "Customer Name",
    "Customer Email",
    "Resolution",
    "Time to Resolution",
    "Customer Satisfaction Rating",
    "Ticket Status",
    "Date of Purchase",
    "First Response Time",
    "Ticket Priority",
]


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    purchase_dt = pd.to_datetime(df["Date of Purchase"], format="%Y-%m-%d")
    response_dt = pd.to_datetime(df["First Response Time"], format="%Y-%m-%d %H:%M:%S")
    df["Days From Purchase"] = (response_dt - purchase_dt).dt.days
    df["Days From Purchase"] = df["Days From Purchase"].fillna(0)

    df["Age Type"] = pd.cut(
        df["Customer Age"],
        bins=[0, 30, 55, 150],
        labels=["Young", "Middle", "Old"],
        right=True,
        include_lowest=True,
    ).astype(str)

    df = df.drop(DROP_COLUMNS, axis=1)

    return df
