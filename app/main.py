from fastapi import FastAPI

from app.routers import auth as AuthRouter

app = FastAPI()

app.include_router(AuthRouter.router)


@app.get("/", tags=["Health Check"])
async def health_Check():
    return "API service is healthy and running!"
