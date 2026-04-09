from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.routes import router
from database.db import engine, Base
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create all tables at startup for prototype simplicity
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bank Fraud Detection Prototype API")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled Exception on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please contact support."},
    )

app.include_router(router)

@app.get("/")
def read_root():
    return {"status": "Active", "module": "Bank Fraud AI Prototype"}
