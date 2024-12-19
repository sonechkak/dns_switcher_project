from fastapi import FastAPI
from src.cloudflare.routes.zones import router as zones_router
from src.cloudflare.routes.records import router as records_router

app = FastAPI()

app.include_router(zones_router, prefix="/zones", tags=["zones"])
app.include_router(records_router, prefix="/records", tags=["records"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.01.", port=8000)