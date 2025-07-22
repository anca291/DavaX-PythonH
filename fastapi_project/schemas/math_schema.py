from pydantic import BaseModel, Field
from typing import Optional

class MathRequest(BaseModel):
    operation: str = Field(..., description="Operation: 'pow', 'fibonacci', or 'factorial'")
    number: int = Field(..., description="Base number or the number to calculate")
    exponent: Optional[int] = Field(None, description="Exponent for power operation (only used if operation is 'pow')")
