from fastapi import FastAPI

from app.routers import auth as AuthRouter
from app.routers import company as CompanyRouter

app = FastAPI()

app.include_router(AuthRouter.router)
app.include_router(CompanyRouter.router)

@app.get("/", tags=["Health Check"])
async def health_Check():
    return "API service is healthy and running!"
