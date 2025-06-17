from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class Expense(BaseModel):
    amount: float = Field(..., gt=0, description="Expense amount must be positive")
    description: str = Field(..., min_length=1)
    paid_by: str = Field(..., min_length=1)
    timestamp: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
