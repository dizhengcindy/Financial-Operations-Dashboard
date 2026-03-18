import os
from functools import lru_cache

# When SECRET_KEY is unset, every worker must share the same fallback or JWTs
# break under multiple processes. This value is dev-only — set SECRET_KEY in prod.
_DEFAULT_DEV_SECRET_KEY = (
    "dev-insecure-fixed-key-set-SECRET_KEY-env-in-production-min-32-chars!!"
)


@lru_cache
def get_settings():
    return Settings()


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://localhost:5432/financial_operations",
    )
    # From env so all workers share one key; never generate per-process random here.
    SECRET_KEY: str = os.getenv("SECRET_KEY") or _DEFAULT_DEV_SECRET_KEY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))
