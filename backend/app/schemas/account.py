from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.account import AccountType


class AccountBase(BaseModel):
    type: AccountType
    name: Optional[str] = None
    balance: Decimal = Decimal("0")


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    type: Optional[AccountType] = None
    name: Optional[str] = None
    balance: Optional[Decimal] = None


class AccountResponse(AccountBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
