from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.models.task import Task


def clear_database(session: Session) -> None:
    session.execute(delete(Task))
    session.commit()
