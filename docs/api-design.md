Protected routes (except register/login): `Authorization: Bearer <token>`.

### Auth
POST   /auth/register
POST   /auth/login
GET    /auth/me

### Users
PATCH  /users/me
DELETE /users/me

### Accounts
GET    /accounts
POST   /accounts
GET    /accounts/{account_id}
PATCH  /accounts/{account_id}
DELETE /accounts/{account_id}

### Transactions
GET    /accounts/{account_id}/transactions
POST   /accounts/{account_id}/transactions
PATCH  /transactions/{transaction_id}
DELETE /transactions/{transaction_id}

### Categories
GET    /categories
POST   /categories
PATCH  /categories/{category_id}
DELETE /categories/{category_id}

### Analytics
GET /analytics/spending-by-category
GET /analytics/monthly-spending
GET /analytics/net-worth
