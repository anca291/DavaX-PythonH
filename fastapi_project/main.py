from fastapi import FastAPI, HTTPException
from schemas.math_schema import MathRequest
from models.math_model import MathResponse
from controllers.math_controller import compute_math_operation
from fastapi.responses import JSONResponse
from db.mongo_handler import get_recent_requests
from datetime import datetime
from prometheus_fastapi_instrumentator import Instrumentator

import asyncio
from concurrent.futures import ThreadPoolExecutor

# Inițializare FastAPI + Prometheus
app = FastAPI()
Instrumentator().instrument(app).expose(app)

# Executor global pentru thread-uri
executor = ThreadPoolExecutor(max_workers=4)

@app.post("/math", response_model=MathResponse)
async def math_endpoint(payload: MathRequest):
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(
            executor,
            compute_math_operation,
            payload.operation,
            payload.number,
            payload.exponent
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint GET: istoricul operațiilor din MongoDB
@app.get("/math/history")
def get_math_history(limit: int = 10):
    records = get_recent_requests(limit)

    for rec in records:
        rec["_id"] = str(rec["_id"])
        if isinstance(rec["timestamp"], datetime):
            rec["timestamp"] = rec["timestamp"].isoformat()

    return JSONResponse(content=records)