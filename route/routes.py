import asyncio

from fastapi import APIRouter
from starlette.responses import JSONResponse

from model.math_request import MathRequest
from service.service_audit import log_math_operation, get_recent_requests
from service.service_math import fibonacci, pow_function, factorial
from service.service_streaming import stream_log

router = APIRouter()


@router.post("/fibonacci", response_model=int)
async def calculate_fibonacci(math_request: MathRequest):
    nth_number = math_request.number
    asyncio.create_task(log_math_operation("fibonacci", dict(math_request)))
    stream_log("fibonacci", {"number": math_request.number})
    return fibonacci(nth_number)


@router.post("/pow", response_model=int)
async def calculate_pow(math_request: MathRequest):
    if math_request.exponent is None:
        return JSONResponse(status_code=400, content={"error": "Exponent is required for pow"})
    asyncio.create_task(log_math_operation("pow", dict(math_request)))
    stream_log("pow", {"number": math_request.number, "exponent": math_request.exponent})
    return pow_function(math_request.number, math_request.exponent)


@router.post("/factorial", response_model=int)
async def calculate_factorial(math_request: MathRequest):
    asyncio.create_task(log_math_operation("factorial", dict(math_request)))
    stream_log("factorial", {"number": math_request.number})
    return factorial(math_request.number)


@router.get("/math/history")
def get_math_history(limit: int = 10):
    try:
        records = get_recent_requests(limit)

        if not records:
            return JSONResponse(content={"message": "No history found"}, status_code=200)

        output = []
        for rec in records:
            rec["_id"] = str(rec["_id"])
            timestamp = rec.get("timestamp")
            rec["timestamp"] = timestamp.isoformat() if hasattr(timestamp, "isoformat") else None
            output.append(rec)

        return JSONResponse(content=output)

    except Exception as e:
        import traceback
        print("❌ ERROR in /math/history:", traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": str(e)})
