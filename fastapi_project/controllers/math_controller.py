from models.math_model import MathResponse
from db.mongo_handler import log_math_operation
from cache import cache
import logging
logging.basicConfig(level=logging.INFO)

def compute_math_operation(operation: str, number: int, exponent: int = None) -> MathResponse:
    logging.info(f"Computing {operation}({number}, {exponent})")
    if operation == "pow":
        if exponent is None:
            raise ValueError("Exponent must be provided for 'pow'")
        key = f"{number}^{exponent}"
        if key in cache:
            print(f"[CACHE HIT] Using cached result for key: {key}")
            result = cache[key]
        else:
            print(f"[CACHE MISS] Calculating result for key: {key}")
            result = pow(number, exponent)
            cache[key] = result
        log_math_operation(operation, {"base": number, "exponent": exponent}, result)
        return MathResponse(operation=operation, number=number, exponent=exponent, result=result)

    elif operation == "fibonacci":
        key = f"fib({number})"
        if key in cache:
            print(f"[CACHE HIT] Using cached result for key: {key}")
            result = cache[key]
        else:
            print(f"[CACHE MISS] Calculating result for key: {key}")
            result = fibonacci(number)
            cache[key] = result
        log_math_operation(operation, {"number": number}, result)
        return MathResponse(operation=operation, number=number, result=result)

    elif operation == "factorial":
        key = f"fact({number})"
        if key in cache:
            print(f"[CACHE HIT] Using cached result for key: {key}")
            result = cache[key]
        else:
            print(f"[CACHE MISS] Calculating result for key: {key}")
            result = factorial(number)
            cache[key] = result
        log_math_operation(operation, {"number": number}, result)
        return MathResponse(operation=operation, number=number, result=result)

    else:
        raise ValueError("Unsupported operation")


# Utility functions
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
