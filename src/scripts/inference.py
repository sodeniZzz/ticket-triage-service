import numpy as np
import pandas as pd
from catboost import CatBoostClassifier, Pool

from src.scripts.io_utils import ROOT_PATH
from src.scripts.preprocessing import CAT_FEATURES, TEXT_FEATURES

MODEL_PATH = ROOT_PATH / "src" / "models" / "model.cbm"

model = CatBoostClassifier()
model.load_model(MODEL_PATH)


def make_pred(df: pd.DataFrame) -> pd.DataFrame:
    pool = Pool(df, cat_features=CAT_FEATURES, text_features=TEXT_FEATURES)
    probs = model.predict_proba(pool)
    idx = np.argmax(probs, axis=1)
    preds = model.classes_[idx]
    submission = pd.DataFrame({"index": df.index, "predicted_priority": preds})
    return submission
