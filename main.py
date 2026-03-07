from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. Define the input JSON shape
class SentimentRequest(BaseModel):
    sentences: list[str]

# 2. Simple rule-based sentiment function
def get_sentiment(text: str) -> str:
    text = text.lower()
    if any(word in text for word in ["love", "good", "great", "awesome", "amazing", "happy"]):
        return "happy"
    if any(word in text for word in ["sad", "bad", "terrible", "awful", "hate"]):
        return "sad"
    return "neutral"

# 3. The POST endpoint
@app.post("/sentiment")
def batch_sentiment(request: SentimentRequest):
    results = []
    for sentence in request.sentences:
        sentiment = get_sentiment(sentence)
        results.append({"sentence": sentence, "sentiment": sentiment})
    return {"results": results}
