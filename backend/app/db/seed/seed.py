from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import Environment
from app.core.config import get_current_environment
from app.db.database import SessionLocal
from app.db.seed.todos import create_tasks, create_random_tasks
from app.db.seed.users import create_users


def truncate_tables(db: Session) -> None:
    """Remove all development data."""
    db.execute(text("TRUNCATE TABLE tasks, users RESTART IDENTITY CASCADE"))


def seed_database(db: Session, count: int = 50) -> None:
    """Populate the database with development data."""
    users = create_users(db)
    create_tasks(db, users)
    create_random_tasks(db, users, 100)

def check_environment() -> None:
    if get_current_environment() == Environment.PROD:
        raise RuntimeError("Database seeding is not allowed in production.")

def main() -> None:
    check_environment()

    db = SessionLocal()

    try:
        truncate_tables(db)
        seed_database(db)

        db.commit()
        print("Database seeded successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
