from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import yfinance as yf

app = FastAPI()

class StockResponse(BaseModel):
    symbol: str
    company: str | None
    price: float | None
    market_cap: int | None

@app.get("/")
def home():
    return {"message": "AI Stock Research API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/stock", response_model=StockResponse)
def get_stock(symbol: str):
    if not data:
        raise HTTPException(status_code=404, detail="Stock not found")
    stock = yf.Ticker(symbol)
    data = stock.info

    return {
        "symbol": symbol,
        "company": data.get("longName"),
        "price": data.get("currentPrice"),
        "market_cap": data.get("marketCap")
    }