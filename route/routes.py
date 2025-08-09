import asyncio

from fastapi import APIRouter
from starlette.responses import JSONResponse

from model.math_request import MathRequest
from service.service_audit import log_math_operation, get_recent_requests
from service.service_math import fibonacci, pow_function, factorial
from service.service_redis_publisher import publish_to_redis

router = APIRouter()


@router.post("/fibonacci", response_model=int)
async def calculate_fibonacci(math_request: MathRequest):
    nth_number = math_request.number
    math_request_dict = dict(math_request)
    asyncio.create_task(log_math_operation("fibonacci", math_request_dict))
    publish_to_redis("fibonacci", math_request_dict)
    return fibonacci(nth_number)


@router.post("/pow", response_model=int)
async def calculate_pow(math_request: MathRequest):
    if math_request.exponent is None:
        return JSONResponse(status_code=400, content={"error": "Exponent is required for pow"})
    math_request_dict = dict(math_request)
    asyncio.create_task(log_math_operation("pow", math_request_dict))
    publish_to_redis("pow", math_request_dict)
    return pow_function(math_request.number, math_request.exponent)


@router.post("/factorial", response_model=int)
async def calculate_factorial(math_request: MathRequest):
    math_request_dict = dict(math_request)
    asyncio.create_task(log_math_operation("factorial", math_request_dict))
    publish_to_redis("factorial", math_request_dict)
    return factorial(math_request.number)


@router.get("/math/history")
def get_math_history(limit: int = 10):
    records = get_recent_requests(limit)

    for rec in records:
        rec["_id"] = str(rec["_id"])
        # if isinstance(rec["timestamp"], datetime):
        rec["timestamp"] = rec["timestamp"].isoformat()

    return JSONResponse(content=records)
