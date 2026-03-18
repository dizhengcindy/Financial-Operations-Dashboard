"""Import this module after ``app.database`` so every model registers on ``Base.metadata``."""

from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.category import Category
