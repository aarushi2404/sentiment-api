from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: list[str]


def get_sentiment(text: str) -> str:
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.1:
        return "happy"
    elif polarity < -0.1:
        return "sad"
    else:
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


@app.post("/")
def sentiment_root(request: SentimentRequest):
    return analyze(request.sentences)


@app.get("/")
def health():
    return {"message": "Sentiment API running"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
