import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_news(stock):
    try:
        prompt = f"Analyze recent news for the stock: {stock}. Provide a summary."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        # Properly access the message content
        content = response.choices[0].message.content
        return {"summary": content}
    except Exception as e:
        return {"error": str(e)}
