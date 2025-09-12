from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def hello():
    return "Hello Fast"

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)