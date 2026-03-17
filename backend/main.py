from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Stock Research API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/stock")
def get_stock(symbol: str):
    stock = yf.Ticker(symbol)
    data = stock.info

    return {
        "symbol": symbol,
        "company": data.get("longName"),
        "price": data.get("currentPrice"),
        "market_cap": data.get("marketCap")
    }