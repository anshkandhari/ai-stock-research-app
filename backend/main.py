from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Stock Research API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/hello")
def say_hello():
    return {"message": "Hello from FastAPI backend"}
@app.get("/stock")
def get_stock(symbol: str):
    return {
        "symbol": symbol,
        "message": "Stock endpoint working"
    }