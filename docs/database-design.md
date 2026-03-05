# Financial Operations Dashboard

## Database Design

### Users Table
columns
- id (uuid, primary key)
- name (text, not null)
- email (text, not null, unique)
- password_hash (text, not null)
- created_at (timestamp)
- updated_at (timestamp)

### Accounts Table
columns
- id (uuid, primary key)
- user_id (uuid, foreign key -> users.id)
- type (enum, not null)
- name (text)
- balance (numeric, default 0)
- created_at (timestamp)
- updated_at (timestamp)

indexes
- index(user_id, created_at)

### transactions
- id (uuid, primary key)
- account_id (uuid, FK → accounts.id)
- category_id (uuid, FK → categories.id)
- amount (numeric)
- merchant (text)
- description (text)
- transaction_date (timestamp)
- created_at (timestamp)
- updated_at (timestamp)

indexes
- index(account_id, transaction_date)


### categories
- id (uuid, primary key)
- user_id (uuid, FK → users.id)
- name (text)
- description (text)
- created_at (timestamp)
- updated_at (timestamp)

indexes
- index(account_id, category_id)