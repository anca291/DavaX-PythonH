from pydantic import BaseModel

class PowResponse(BaseModel):
    base: float
    exponent: float
    result: float
