import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from app.database import get_collection
from app.utils import preprocess_data

class Predictor:
    def __init__(self):
        self.model = RandomForestRegressor()

    async def train_model(self):
        # Fetch data from MongoDB
        collection = get_collection('test_reports')
        cursor = collection.find()
        data = pd.DataFrame(await cursor.to_list(length=None))

        # Preprocess data
        data['id'] = data['_id'].astype(str)
        data.drop(columns=['_id', 'createdAt'], inplace=True, errors='ignore')
        data = preprocess_data(data)

        # Split data for training
        X = data.drop(columns=['storyPassed'])
        y = data['storyPassed']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

    async def predict(self, input_data: dict):
        # Prepare input data for prediction
        input_df = pd.DataFrame([input_data])
        input_data_processed = preprocess_data(input_df)
        return self.model.predict(input_data_processed)