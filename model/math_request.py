from pydantic import BaseModel
from typing import Optional


class MathRequest(BaseModel):
    number: int
    exponent: Optional[int] = None
