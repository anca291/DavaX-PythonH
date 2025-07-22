from functools import lru_cache

from fastapi import HTTPException


@lru_cache(maxsize=1024)
def fibonacci(n):
    a = 0
    b = 1
    #print(f"Calculating fibonacci({n})")
    # Check if n is less than 0
    if n < 0:
        raise HTTPException(status_code=400, detail="Incorrect input")

    # Check if n is equal to 0
    elif n == 0:
        return 0

    # Check if n is equal to 1
    elif n == 1:
        return b
    else:
        for i in range(1, n):
            c = a + b
            a = b
            b = c
        return b


@lru_cache(maxsize=1024)
def pow_function(base: int, exponent: int):
    try:
        return base ** exponent
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")


@lru_cache(maxsize=1024)
def factorial(n: int):
    if n < 0:
        raise HTTPException(status_code=400, detail="Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
