from fastapi import FastAPI, Query, HTTPException
from graph.stock_graph import run_stock_graph

app = FastAPI()

@app.get("/predict")
def predict(stock: str):
    try:
        return run_stock_graph(stock)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))