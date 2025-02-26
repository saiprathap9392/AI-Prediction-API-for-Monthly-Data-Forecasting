import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

def handle_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    return data.fillna(0)

def normalize_data(data: pd.DataFrame) -> pd.DataFrame:
    return (data - data.mean()) / data.std()

def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    mse = mean_squared_error(y_true, y_pred)
    return {
        "mean_squared_error": mse,
        "rmse": np.sqrt(mse),
    }

def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    data = handle_missing_values(data)
    data = normalize_data(data)
    return data