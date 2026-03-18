from fastapi import FastAPI,HTTPException,Path
from pydantic import BaseModel
import yfinance as yf
from typing import Optional
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
    try:
        symbol = symbol.upper()
        stock = yf.Ticker(symbol)
        data = stock.info

        if not data or "currentPrice" not in data:
            raise HTTPException(status_code=404, detail="Invalid stock symbol")

        return {
            "symbol": symbol,
            "company": data.get("longName"),
            "price": data.get("currentPrice"),
            "market_cap": data.get("marketCap")
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Error fetching stock data")

@app.get("/ai-stock-summary")
def ai_stock_summary(symbol: str):
    try:
        symbol = symbol.upper()
        stock = yf.Ticker(symbol)
        data = stock.info

        if not data or "currentPrice" not in data:
            raise HTTPException(status_code=404, detail="Invalid stock symbol")

        company = data.get("longName") or symbol
        price = data.get("currentPrice")
        market_cap = data.get("marketCap")

        summary = generate_summary(company, price, market_cap)

        return {
            "symbol": symbol,
            "company": company,
            "price": price,
            "market_cap": market_cap,
            "ai_summary": summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
def generate_summary(company, price, market_cap):
    prompt = f"""
Explain this company in simple terms:

Company: {company}
Price: {price}
Market Cap: {market_cap}

Include:
- what the company does
- recent outlook
- risks

Keep it under 100 words.
"""

    response = client.chat.completions.create(
        model="groq/compound",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content