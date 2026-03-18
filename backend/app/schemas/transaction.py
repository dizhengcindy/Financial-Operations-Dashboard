from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class TransactionResponse(BaseModel):
    id: UUID
    account_id: UUID
    category_id: Optional[UUID] = None
    amount: Optional[Decimal] = None
    merchant: Optional[str] = None
    description: Optional[str] = None
    transaction_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TransactionListResponse(BaseModel):
    items: List[TransactionResponse]
    total: int
    page: int
    limit: int
