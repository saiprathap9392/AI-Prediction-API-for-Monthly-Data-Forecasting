# AI-Prediction-API-for-Monthly-Data-Forecasting
AI Prediction API for Monthly Data Forecasting Description


Features
Monthly data forecasting.

Daily automatic predictions.

MongoDB integration.

FastAPI with Swagger documentation.

Setup
Prerequisites
Python 3.8+

MongoDB

Steps
Set up a virtual environment:
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # macOS/Linux


pip install -r requirements.txtpip install -r requirements.txt
et up MongoDB:

Start MongoDB: mongod

Create a .env file:
MONGODB_URL=mongodb://localhost:27017
Run the API:
uvicorn app.main:app --reload
Access the API:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc


Endpoints
GET /: Check API status.

POST /train: Train the model.

POST /predict: Get monthly predictions.

GET /daily_prediction: Get daily predictions.

Project Structure

ai-prediction-api/
├── app/
│   ├── main.py           # FastAPI app
│   ├── database.py       # MongoDB connection
│   ├── prediction.py     # ML model
│   ├── models.py         # Data models
│   └── utils.py          # Utilities
├── .env                  # Environment variables
├── requirements.txt      # Dependencies
└── README.md             # Documentation
