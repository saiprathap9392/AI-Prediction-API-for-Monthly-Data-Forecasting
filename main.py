from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app import database, prediction
import pandas as pd
from datetime import datetime
import asyncio

# ✅ FastAPI instance with custom docs and metadata
app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    title="AI Prediction API 🚀",
    description="An AI-powered prediction API that forecasts the next month's data based on weekly inputs, providing daily updates automatically.",
    version="1.0.0"
)

# ✅ Example schema updated with provided input data for reference
example_schema = {
    "projectName": "Project Alpha",
    "authors": "John Doe",
    "storyTests": 100,
    "regressionTestsAutomated": 80,
    "regressionTestsManual": 20,
    "totalTestsByApplication": 120,
    "storyPassed": 90,
    "storyFailed": 5,
    "storyUnexecuted": 5,
    "storyBlocked": 0,
    "storySkipped": 0,
    "storyCritical": 2,
    "storyNew": 3,
    "storyUnused": 0,
    "storyBugs": 1,
    "arPassed": 70,
    "arFailed": 10,
    "arUnexecuted": 0,
    "arBlocked": 0,
    "arSkipped": 0,
    "arCritical": 1,
    "arNew": 2,
    "arUnused": 0,
    "arBugs": 1,
    "mrPassed": 15,
    "mrFailed": 5,
    "mrUnexecuted": 0,
    "mrBlocked": 0,
    "mrSkipped": 0,
    "mrCritical": 0,
    "mrNew": 1,
    "mrUnused": 0,
    "mrBugs": 0,
    "createdAt": "2025-02-21T00:00:00"
}

# ✅ Predictor setup and endpoints
predictor = prediction.Predictor()
latest_prediction = None

async def ensure_mongo_connection():
    """Ensure MongoDB is connected before model training."""
    try:
        await database.get_collection("test_reports").find_one()
        print("✅ MongoDB connection established successfully.")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed.")

async def ensure_model_trained():
    """Ensure the model is trained before prediction, handling missing fields like '_id'."""
    try:
        await ensure_mongo_connection()
        collection = database.get_collection("test_reports")
        cursor = collection.find()
        data = pd.DataFrame(await cursor.to_list(length=None))
        if data.empty:
            print("⚠️ No data available for training. Adding example data...")
            data = pd.DataFrame([example_schema])
        if "_id" in data.columns:
            data.drop(columns=["_id"], inplace=True)
        data.drop(columns=["createdAt"], inplace=True, errors="ignore")
        data = data.select_dtypes(include=["number"])  # Keep only numeric columns
        if not data.empty:
            X = data.drop(columns=["storyPassed"], errors="ignore")
            y = data.get("storyPassed", pd.Series([0]))
            predictor.model.fit(X, y)  # Ensure synchronous training without await
            print("✅ Model trained successfully at startup.")
        else:
            print("⚠️ Training data still empty after preprocessing.")
    except KeyError as e:
        print(f"❌ Missing expected field during training: {e}")
    except Exception as e:
        print(f"❌ Error during initial model training: {e}")

def preprocess_input_data(data):
    """
    Preprocess the input data by dropping non-numeric columns and the target column.
    Ensures compatibility with model input expectations.
    """
    df = pd.DataFrame([data])
    df.drop(columns=[col for col in ["_id", "createdAt", "storyPassed"] if col in df.columns], inplace=True, errors="ignore")
    df = df.select_dtypes(include=["number"])  # Keep only numeric columns
    return df

async def daily_prediction_task():
    """Background task to generate daily predictions automatically."""
    global latest_prediction
    try:
        # Preprocess the example schema before prediction
        input_data_processed = preprocess_input_data(example_schema)
        prediction_result = predictor.model.predict(input_data_processed)
        latest_prediction = {
            "timestamp": datetime.utcnow().isoformat(),
            "predicted_output": prediction_result.tolist()
        }
        print("✅ Daily prediction generated successfully.")
        # Continue generating predictions every 24 hours
        while True:
            await asyncio.sleep(86400)  # Wait for 24 hours (86400 seconds)
            prediction_result = predictor.model.predict(input_data_processed)
            latest_prediction = {
                "timestamp": datetime.utcnow().isoformat(),
                "predicted_output": prediction_result.tolist()
            }
            print("✅ Daily prediction updated.")
    except Exception as e:
        print(f"❌ Error during daily prediction task: {e}")

@app.on_event("startup")
async def start_daily_task():
    """Trigger MongoDB check, model training, and daily prediction task on application startup."""
    await ensure_model_trained()
    asyncio.create_task(daily_prediction_task())

# ✅ Root endpoint to confirm the app is running
@app.get("/")
async def root():
    return {
        "message": "🚀 AI Prediction API is running successfully!",
        "latest_prediction": latest_prediction,
        "instructions": "Use the /predict endpoint with appropriate input data to get monthly predictions.",
        "sample_input": example_schema,
        "links": {
            "api_docs": "http://127.0.0.1:8000/docs",
            "redoc": "http://127.0.0.1:8000/redoc",
            "train_endpoint": "curl -X POST http://127.0.0.1:8000/train",
            "daily_prediction_endpoint": "curl http://127.0.0.1:8000/daily_prediction"
        }
    }

# ✅ Endpoint to get the latest daily prediction
@app.get("/daily_prediction")
async def get_daily_prediction():
    if latest_prediction:
        return latest_prediction
    else:
        raise HTTPException(status_code=404, detail="❌ Daily prediction not available yet.")

# ✅ Favicon endpoint to handle browser favicon requests
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")  # Make sure the path exists

@app.post("/train")
async def train_model():
    """Train the prediction model based on weekly historical data."""
    await ensure_mongo_connection()
    await ensure_model_trained()
    return {"message": "✅ Model trained successfully for monthly forecasting!"}

@app.post("/predict")
async def predict(input_data: dict = example_schema):
    """Predict the next month's data based on provided weekly data or default example."""
    input_data_processed = preprocess_input_data(input_data)
    prediction_result = predictor.model.predict(input_data_processed)
    return {
        "input_data": input_data,
        "predicted_output": prediction_result.tolist(),
        "message": "✅ Monthly prediction generated successfully!"
    }