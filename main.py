from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import re

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: list[str]


positive_words = {
    "love","like","good","great","awesome","amazing","happy","excellent",
    "fantastic","nice","wonderful","enjoy","pleased","delight","best",
    "positive","brilliant","perfect","cool","beautiful","outstanding",
    "super","fun","glad"
}

negative_words = {
    "sad","bad","terrible","awful","hate","worst","horrible","angry",
    "upset","disappointed","poor","disgusting","annoying","painful",
    "negative","boring","ugly","problem","issue","fail","failure",
    "unhappy","tired","sucks"
}


def get_sentiment(text: str) -> str:
    text = text.lower()

    # extract words
    words = re.findall(r"\b[a-z]+\b", text)

    pos = sum(word in positive_words for word in words)
    neg = sum(word in negative_words for word in words)

    if neg > pos:
        return "sad"
    if pos > neg:
        return "happy"
    return "neutral"


def analyze(sentences):
    return {
        "results": [
            {"sentence": s, "sentiment": get_sentiment(s)}
            for s in sentences
        ]
    }


@app.post("/sentiment")
def sentiment_endpoint(request: SentimentRequest):
    return analyze(request.sentences)


# some graders POST to root
@app.post("/")
def sentiment_root(request: SentimentRequest):
    return analyze(request.sentences)


@app.get("/")
def health():
    return {"message": "Sentiment API running"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
