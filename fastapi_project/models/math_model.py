from pydantic import BaseModel
from typing import Optional

class MathResponse(BaseModel):
    operation: str
    number: int
    exponent: Optional[int] = None
    result: float
