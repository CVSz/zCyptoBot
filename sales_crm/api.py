from fastapi import FastAPI

from sales_crm.forecasting import forecast_revenue
from sales_crm.pipeline import pipeline_value

app = FastAPI()


@app.get("/pipeline")
def pipeline():
    return {"value": pipeline_value()}


@app.get("/forecast")
def forecast():
    return {"forecast": forecast_revenue()}
