from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

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


def get_sentiment(text: str) -> str:
    text = text.lower()

    positive_words = [
        "love","like","good","great","awesome","amazing","happy",
        "excellent","fantastic","nice","wonderful","enjoy",
        "pleased","delight","best"
    ]

    negative_words = [
        "sad","bad","terrible","awful","hate","worst",
        "horrible","angry","upset","disappointed",
        "poor","disgusting","annoying","painful"
    ]

    # Check negative first
    if any(word in text for word in negative_words):
        return "sad"

    if any(word in text for word in positive_words):
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


@app.post("/")
def sentiment_root(request: SentimentRequest):
    return analyze(request.sentences)


@app.get("/")
def health():
    return {"message": "Sentiment API running"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
