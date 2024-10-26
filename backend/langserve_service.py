import os
from langchain.prompts import PromptTemplate 
import uvicorn 
import os 
from pydantic import BaseModel
from langchain.llms import OpenAI
from fastapi import FastAPI, HTTPException
from data.api import fetch_historical_prices
from services.trade_signal import get_trade_signal, calculate_ema_50,calculate_ema_200, calculate_rsi
from dotenv import load_dotenv 
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Load API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Langserve
app = FastAPI(
    title="Langserve Service",
    version="1.0",
    description="A simple API Server"    
    )


# Add CORS middleware to allow requests from the frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from the frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Prompt template for generating explanations
prompt_template = """
The current trade signal is '{signal}'.
The RSI is {rsi:.2f}, the price is {current_price}, the 50 day EMA is {ema_50} and the 200 day EMA is {ema_200}.
Explain why this signal was generated. Also put emphasis on the crossing of the 50 and 200 day ema.
"""
template = PromptTemplate(
    input_variables=["signal", "rsi", "ema_50", "ema_200", "current_price"],
    template=prompt_template
)

# Initialize OpenAI LLM
llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0.7, max_tokens=250)


# Taking the input from the user 
class SymbolRequest(BaseModel):
    symbol: str


@app.get("/")  # Root route for testing
async def root():
    return {"message": "Langserve API is running"}

@app.post("/generate-explanation")
async def generate_explanation(request: SymbolRequest):
    symbol = request.symbol

    try:
        # Fetch forex data from Oanda
        # Fetch daily prices for EUR/USD (last 100 days)
        prices = fetch_historical_prices(symbol, granularity="D", count=110)

        # Debugging: Print the prices fetched from OANDA to ensure valid data
        print(f"Prices for {symbol}: {prices}")

        # Calculate the 14-day RSI (based on daily prices)
        rsi = calculate_rsi(prices, window=14)

        # Calculate the 50-day EMA (based on daily prices)
        ema_50 = calculate_ema_50(prices)

        # Calculate the 200-day EMA (based on daily prices)
        ema_200 = calculate_ema_200(prices)

        current_price = prices[-1]

        # Generate the trade signal
        signal = get_trade_signal(rsi, ema_50, ema_200, current_price)

        # Generate explanation using OpenAI's LLM
        prompt = template.format(signal=signal, rsi=rsi, ema_50=ema_50, ema_200=ema_200, current_price=current_price)
        explanation = llm(prompt)

        # Return the response
        return {
            "symbol": symbol,
            "signal": signal,
            "rsi": rsi,
            "ema_50": ema_50,
            "ema_200": ema_200,
            "current_price": current_price,
            "explanation": explanation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))