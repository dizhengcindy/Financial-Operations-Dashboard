from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import hash_password, verify_password


class UserService:
    @staticmethod
    def email_in_use_by_other(
        db: Session, email: str, exclude_user_id: UUID
    ) -> bool:
        normalized = email.lower().strip()
        return (
            db.query(User)
            .filter(
                User.email == normalized,
                User.id != exclude_user_id,
                User.deleted.is_(False),
            )
            .first()
            is not None
        )

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return (
            db.query(User)
            .filter(User.email == email.lower().strip(), User.deleted.is_(False))
            .first()
        )

    @staticmethod
    def get_by_email_including_deleted(db: Session, email: str) -> Optional[User]:
        """Any row with this email (used for register vs soft-deleted reuse)."""
        return (
            db.query(User)
            .filter(User.email == email.lower().strip())
            .first()
        )

    @staticmethod
    def _release_email_from_soft_deleted_users(db: Session, email: str) -> None:
        """Free a unique email held only by soft-deleted rows (for PATCH email)."""
        normalized = email.lower().strip()
        for row in (
            db.query(User)
            .filter(User.email == normalized, User.deleted.is_(True))
            .all()
        ):
            row.email = f"{row.id}@released.deleted.local"

    @staticmethod
    def get_by_id(db: Session, user_id: UUID) -> Optional[User]:
        return (
            db.query(User)
            .filter(User.id == user_id, User.deleted.is_(False))
            .first()
        )

    @staticmethod
    def create_user(db: Session, schema: UserCreate) -> User:
        user = User(
            name=schema.name.strip(),
            email=schema.email.lower().strip(),
            password_hash=hash_password(schema.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def reactivate_deleted_user(db: Session, user: User, schema: UserCreate) -> User:
        """Reuse row for same email after soft delete; keeps unique(email) valid."""
        user.name = schema.name.strip()
        user.email = schema.email.lower().strip()
        user.password_hash = hash_password(schema.password)
        user.deleted = False
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[User]:
        user = UserService.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def update_user(db: Session, user: User, schema: UserUpdate) -> User:
        data = schema.model_dump(exclude_unset=True)
        if "email" in data:
            new_email = data["email"].lower().strip()
            if UserService.email_in_use_by_other(db, new_email, user.id):
                raise ValueError("Email already in use")
            UserService._release_email_from_soft_deleted_users(db, new_email)
            user.email = new_email
        if "name" in data:
            user.name = data["name"].strip()
        if "password" in data:
            user.password_hash = hash_password(data["password"])
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def soft_delete_user(db: Session, user: User) -> None:
        user.deleted = True
        db.commit()
