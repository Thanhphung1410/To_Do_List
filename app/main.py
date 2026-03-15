from fastapi import FastAPI

app = FastAPI(title="To-Do API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Hello To-Do"}
