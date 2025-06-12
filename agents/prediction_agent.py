import os
from openai import OpenAI
import yfinance as yf

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_history_summary(stock: str):
    try:
        ticker = yf.Ticker(stock)
        hist = ticker.history(period="3mo")
        if hist.empty:
            return "No historical price data available."

        closing_prices = hist["Close"].dropna().tolist()
        avg_price = sum(closing_prices) / len(closing_prices)
        latest_price = closing_prices[-1]
        change = latest_price - closing_prices[0]
        pct_change = (change / closing_prices[0]) * 100

        summary = (
            f"Over the past 3 months, the stock has moved from ₹{closing_prices[0]:.2f} "
            f"to ₹{latest_price:.2f}, a change of ₹{change:.2f} ({pct_change:.2f}%). "
            f"The average price during this period was ₹{avg_price:.2f}."
        )
        return summary
    except Exception as e:
        return f"Error fetching historical data: {e}"

def predict_future(stock, news, trend):
    try:
        history_summary = get_history_summary(stock)

        prompt = (
            f"Stock: {stock}\n\n"
            f"🗞️ Recent News Summary:\n{news.get('summary', 'No news available')}\n\n"
            f"📊 Technical Trend Analysis:\n{trend.get('analysis', 'No trend analysis available')}\n\n"
            f"📈 Historical Performance (last 3 months):\n{history_summary}\n\n"
            f"Using this data, do the following:\n\n"
            f"1. Predict the stock price over:\n"
            f"   - Next 7 days\n"
            f"   - Next 15 days\n"
            f"   - Next 1 month\n"
            f"   - Next 3 months\n\n"
            f"2. Suggest buying and selling targets for:\n"
            f"   - Short-term buyers (1–15 days)\n"
            f"   - Long-term investors (1–3 months)\n\n"
            f"3. Estimate the overall **sentiment**: Bullish, Bearish, or Neutral — with emoji.\n"
            f"4. Provide a **confidence level**: High, Medium, or Low — with a short explanation why.\n\n"
            f"Format the response as HTML using clear <h2> headers, bullet points, and friendly language."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
        )

        content = response.choices[0].message.content

        html_result = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                h2 {{ color: #2E86C1; }}
                p {{ margin-bottom: 1em; }}
            </style>
        </head>
        <body>
            <h1>Stock Price Prediction for {stock}</h1>
            <h2>📈 Historical Summary</h2>
            <p>{history_summary}</p>
            <h2>🔮 Forecast</h2>
            {content}
        </body>
        </html>
        """
        return {"html_prediction": html_result}
    except Exception as e:
        return {"error": str(e)}