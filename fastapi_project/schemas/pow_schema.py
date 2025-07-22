from pydantic import BaseModel, Field

class PowRequest(BaseModel):
    base: float = Field(..., description="The base number")
    exponent: float = Field(..., description="The exponent")
