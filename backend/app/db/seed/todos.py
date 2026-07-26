import random

from faker import Faker
from sqlalchemy.orm import Session

from app.enums.task_status import TaskStatus
from app.models.task import Task
from app.models.user import User

fake = Faker()

# Les données générées seront toujours identiques
Faker.seed(42)
random.seed(42)


def create_tasks(db: Session, users: dict[str, User]) -> None:

    db.add_all([
        Task(
            title="Vérifier les sauvegardes",
            owner=users["admin"],
            status=TaskStatus.TODO,
        ),
        Task(
            title="Déployer la nouvelle version",
            owner=users["admin"],
            status=TaskStatus.IN_PROGRESS,
        ),

        Task(
            title="Acheter du lait",
            owner=users["alice"],
            status=TaskStatus.TODO,
        ),
        Task(
            title="Aller courir",
            owner=users["alice"],
            status=TaskStatus.DONE,
        ),

        Task(
            title="Lire un livre",
            owner=users["bob"],
            status=TaskStatus.TODO,
        ),
        Task(
            title="Faire les courses",
            owner=users["bob"],
            status=TaskStatus.IN_PROGRESS,
        ),
    ])


def create_random_tasks(
    db: Session,
    users: dict[str, User],
    count: int = 20,
) -> None:
    """Create reproducible random tasks."""

    owners = [
        users["admin"],
        users["alice"],
        users["bob"],
    ]

    tasks = []

    for _ in range(count):
        tasks.append(
            Task(
                title=fake.sentence(nb_words=4).rstrip("."),
                owner=random.choice(owners),
                status=random.choice(list(TaskStatus)),
            )
        )

    db.add_all(tasks)
