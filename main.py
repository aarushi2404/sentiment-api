from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI()

# Enable CORS so external evaluators can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class SentimentRequest(BaseModel):
    sentences: list[str]

# Sentiment logic
def get_sentiment(text: str) -> str:
    text = text.lower()

    positive = ["love","good","great","awesome","amazing","happy","excellent","fantastic"]
    negative = ["sad","bad","terrible","awful","hate","worst","horrible"]

    if any(word in text for word in positive):
        return "happy"

    if any(word in text for word in negative):
        return "sad"

    return "neutral"


@app.post("/sentiment")
def batch_sentiment(request: SentimentRequest):

    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": get_sentiment(sentence)
            }
            for sentence in request.sentences
        ]
    }


# Required for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
