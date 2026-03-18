from fastapi import FastAPI

# Ensure Base.metadata includes every mapper. Import `database` first so Base
# exists; then import `app.models` (do not import models from database.py — that
# circularizes when e.g. transaction.py loads database before Transaction exists).
import app.database  # noqa: F401
import app.models  # noqa: F401

from app.routes import account_routes, auth_routes, transaction_routes, user_routes

app = FastAPI(title="Financial Operations Dashboard API")

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(account_routes.router)
app.include_router(transaction_routes.router)


@app.get("/")
def root():
    return {"message": "Financial Operations Dashboard API running"}
