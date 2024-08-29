from fastapi import FastAPI


app = FastAPI()



@app.get("/", tags=["Health Check"])
async def health_Check():
    return "API service is healthy and running!"