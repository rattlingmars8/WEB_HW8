import random
from faker import Faker

from source.models import User, WayToContact

fake = Faker('uk-UA')


def seed_users(num: int = 50):
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
