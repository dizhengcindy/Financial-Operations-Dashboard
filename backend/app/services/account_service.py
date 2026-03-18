from uuid import UUID

from sqlalchemy.orm import Session

from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate


class AccountService:
    @staticmethod
    def list_accounts(db: Session, user_id: UUID):
        return (
            db.query(Account)
            .filter(Account.deleted.is_(False), Account.user_id == user_id)
            .all()
        )

    @staticmethod
    def get_account(db: Session, account_id: str, user_id: UUID):
        account = (
            db.query(Account)
            .filter(
                Account.id == UUID(account_id),
                Account.deleted.is_(False),
                Account.user_id == user_id,
            )
            .first()
        )
        return account

    @staticmethod
    def create_account(db: Session, schema: AccountCreate, user_id: UUID):
        account = Account(**schema.model_dump(), user_id=user_id)
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def update_account(
        db: Session, account_id: str, schema: AccountUpdate, user_id: UUID
    ):
        account = (
            db.query(Account)
            .filter(
                Account.id == UUID(account_id),
                Account.deleted.is_(False),
                Account.user_id == user_id,
            )
            .first()
        )
        if not account:
            return None
        update_data = schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(account, key, value)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def delete_account(db: Session, account_id: str, user_id: UUID) -> bool:
        result = (
            db.query(Account)
            .filter(
                Account.id == UUID(account_id),
                Account.deleted.is_(False),
                Account.user_id == user_id,
            )
            .update({"deleted": True})
        )
        db.commit()
        return result > 0