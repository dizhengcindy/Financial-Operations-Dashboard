from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.transaction import TransactionListResponse, TransactionResponse
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/accounts", tags=["transactions"])


@router.get(
    "/{account_id}/transactions",
    response_model=TransactionListResponse,
)
def list_account_transactions(
    account_id: UUID,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List transactions for an account owned by the current user."""
    account, items, total = TransactionService.list_for_account(
        db, account_id, current_user.id, page=page, limit=limit
    )
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )
    return TransactionListResponse(
        items=[TransactionResponse.model_validate(t) for t in items],
        total=total,
        page=page,
        limit=limit,
    )
