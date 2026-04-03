from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Support Env Server Live"}

@app.get("/health")
def health():
    return {"status": "healthy"}

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)

if __name__ == '__main__':
    main()
