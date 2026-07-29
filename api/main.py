from fastapi import FastAPI
from .predict import router

app = FastAPI(
    title="AI Retail Demand Forecasting API",
    version="1.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Retail Demand Forecasting API"
    }