import random

from faker import Faker
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_current_environment
from app.core.config import Environment
from app.db.database import SessionLocal
from app.enums.task_status import TaskStatus
from app.models.task import Task

fake = Faker()
Faker.seed(42)
random.seed(42)


def reset_database(db: Session) -> None:
    """Remove all development data."""
    db.execute(text("TRUNCATE TABLE tasks RESTART IDENTITY CASCADE"))


def seed_database(db: Session, count: int = 50) -> None:
    """Populate the database with development data."""

    tasks = [
        Task(
            title=fake.sentence(nb_words=4).rstrip("."),
            status=random.choice(list(TaskStatus)),
        )
        for _ in range(count)
    ]

    db.add_all(tasks)

def check_environment() -> None:
    if get_current_environment() == Environment.PROD:
        raise RuntimeError("Database seeding is not allowed in production.")

def main() -> None:
    check_environment()

    db = SessionLocal()

    try:
        reset_database(db)
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
