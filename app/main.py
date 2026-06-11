from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return "Crypto Intelligence Platform"

@app.get("/health")
def health():
    return "OK"