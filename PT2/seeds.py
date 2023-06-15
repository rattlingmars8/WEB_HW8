import random
from faker import Faker
from typing import List

from source.models import User, WayToContact

fake = Faker('uk-UA')


def seed_users(num: int = 50) -> List[User]:
    """
    Заповнення списку користувачів випадковими даними.

    :param num: Кількість користувачів для створення (за замовчуванням 50).
    :return: Список об'єктів класу User з випадковими даними.
    """
    users = []
    for _ in range(num):
        way_to_contact = random.choice(list(WayToContact))  # Випадковий вибір способу зв'язку
        users.append(
            User(
                fullname=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                way_to_contact=way_to_contact
            )
        )
    return users
