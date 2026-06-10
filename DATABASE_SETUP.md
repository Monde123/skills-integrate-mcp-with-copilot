# Database Setup Guide

## Overview

The Mergington High School API now uses **SQLAlchemy ORM** with **SQLite** as the default database for persistent storage.

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create environment configuration:

```bash
cp .env.example .env
```

3. Run the application:

```bash
cd src
uvicorn app:app --reload
```

The database will automatically initialize on first run and seed with sample data.

## Database Configuration

### SQLite (Default - Best for Development)

Edit `.env`:

```
DATABASE_URL=sqlite:///./activities.db
```

### PostgreSQL (Production)

Edit `.env`:

```
DATABASE_URL=postgresql://user:password@localhost/mergington
```

Install PostgreSQL driver:

```bash
pip install psycopg2-binary
```

### MySQL

Edit `.env`:

```
DATABASE_URL=mysql+pymysql://user:password@localhost/mergington
```

Install MySQL driver:

```bash
pip install pymysql
```

## Database Schema

### Activities Table

- **id**: Integer (Primary Key)
- **name**: String (Unique)
- **description**: String
- **schedule**: String
- **max_participants**: Integer
- **created_at**: DateTime (Auto)
- **updated_at**: DateTime (Auto)

### Participants Table

- **id**: Integer (Primary Key)
- **activity_id**: Integer (Foreign Key)
- **email**: String
- **enrolled_at**: DateTime (Auto)

## Data Persistence

✅ All data now persists across server restarts
✅ Database file is created automatically (`activities.db`)
✅ Sample data is seeded on first run
✅ Ready for production deployment

## Next Steps

- Add user authentication (OAuth/OIDC)
- Implement role-based access control
- Add database migrations support
- Set up automated backups
