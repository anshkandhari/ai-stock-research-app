from fastapi import FastAPI,HTTPException,Path
from pydantic import BaseModel
import yfinance as yf
from typing import Optional

app = FastAPI()

class StockResponse(BaseModel):
    symbol: str
    company: Optional[str]
    price: Optional[float]
    market_cap: Optional[int]

@app.get("/")
def home():
    return {"message": "AI Stock Research API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/stock", response_model=StockResponse)
def get_stock(symbol: str):
    stock = yf.Ticker(symbol)
    data = stock.info

    if not data:
        raise HTTPException(status_code=404, detail="Stock not found")

    return {
        "symbol": symbol,
        "company": data.get("longName"),
        "price": data.get("currentPrice"),
        "market_cap": data.get("marketCap")
    }
