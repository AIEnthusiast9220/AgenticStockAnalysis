import os
import yfinance as yf
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_trends(stock):
    try:
        ticker = yf.Ticker(stock)
        data = ticker.history(period="7d")

        if data.empty or len(data) < 2:
            return {"error": "Not enough trend data"}

        last_price = data["Close"].iloc[-1]
        prev_price = data["Close"].iloc[-2]
        trend = "upward" if last_price > prev_price else "downward"

        # Optional: get AI commentary on trend
        prompt = (
            f"Stock {stock} shows a {trend} trend. "
            f"Yesterday's close: {prev_price:.2f}, latest close: {last_price:.2f}. "
            f"Provide a brief analysis."
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        ai_comment = response.choices[0].message.content

        return {
            "current_price": float(last_price),
            "previous_price": float(prev_price),
            "trend": trend,
            "analysis": ai_comment,
        }
    except Exception as e:
        return {"error": str(e)}
