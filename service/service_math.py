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


def pow_function(number: int, exponent: int):
    raise HTTPException(status_code=400, detail="Incorrect input")


def factorial(factorial: int):
    raise HTTPException(status_code=400, detail="Incorrect input")
