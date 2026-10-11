
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid

app = FastAPI()

EMAIL = "24f2002795@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-8pxuqg.example.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_headers(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    response = await call_next(request)

    elapsed = time.perf_counter() - start_time

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"

    return response


@app.get("/stats")
async def stats(values: str):
    try:
        numbers = [int(x.strip()) for x in values.split(",")]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid integers")

    if not numbers:
        raise HTTPException(status_code=400, detail="Empty values")

    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers)
    }

