from fastapi import FastAPI

from app.routers import auth as AuthRouter
from app.routers import company as CompanyRouter
from app.routers import user as UserRouter
from app.routers import task as TaskRouter

app = FastAPI()

app.include_router(AuthRouter.router)
app.include_router(CompanyRouter.router)
app.include_router(UserRouter.router)
app.include_router(TaskRouter.router)


@app.get("/", tags=["Health Check"])
async def health_Check():
    return "API service is healthy and running!"
