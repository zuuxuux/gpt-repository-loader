from app.api.chat import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
