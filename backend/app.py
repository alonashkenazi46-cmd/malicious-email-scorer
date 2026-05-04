from fastapi import FastAPI
from pydantic import BaseModel
from scorer import analyze_email

app = FastAPI(title="Malicious Email Scorer")


class EmailRequest(BaseModel):
    subject: str
    sender: str
    reply_to: str = ""
    body: str


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "Malicious Email Scorer"
    }


@app.post("/analyze")
def analyze(request: EmailRequest):
    return analyze_email(
        subject=request.subject,
        sender=request.sender,
        reply_to=request.reply_to,
        body=request.body
    )