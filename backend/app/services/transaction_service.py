from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.transaction import Transaction


class TransactionService:
    """Transactions scoped to accounts the user owns."""

    @staticmethod
    def _account_for_user(
        db: Session, account_id: UUID, user_id: UUID
    ) -> Optional[Account]:
        return (
            db.query(Account)
            .filter(
                Account.id == account_id,
                Account.user_id == user_id,
                Account.deleted.is_(False),
            )
            .first()
        )

    @staticmethod
    def list_for_account(
        db: Session,
        account_id: UUID,
        user_id: UUID,
        page: int = 1,
        limit: int = 50,
    ) -> Tuple[Optional[Account], List[Transaction], int]:
        """
        Returns (account_or_none, items, total).
        If account_or_none is None, caller should respond 404.
        """
        account = TransactionService._account_for_user(db, account_id, user_id)
        if account is None:
            return None, [], 0

        base = db.query(Transaction).filter(
            Transaction.account_id == account_id,
            Transaction.deleted.is_(False),
        )
        total = base.count()
        offset = (page - 1) * limit
        items = (
            base.order_by(Transaction.transaction_date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return account, items, total
