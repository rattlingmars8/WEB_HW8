import json

import connect
from mongoengine import disconnect
from models import Authors, Quotes


def read_authors(authors_json_file: str):
    with open(authors_json_file, 'r', encoding='utf-8') as fd:
        result = json.load(fd)
    return result


def read_quotes(quotes_json_file: str):
    with open(quotes_json_file, 'r', encoding='utf-8') as fd:
        result = json.load(fd)
    return result


def seed_authors():
    Authors.objects().delete()
    authors = read_authors('authors.json')
    for author in authors:
        Authors(
            full_name=author.get('fullname'),
            born_date=author.get('born_date'),
            born_loc=author.get('born_location'),
            desc=author.get('description')
        ).save()


def seed_quotes():
    Quotes.objects().delete()
    quotes = read_quotes('quotes.json')
    for quote in quotes:
        Quotes(
            tags=quote.get('tags'),
            author=Authors.objects.get(full_name=quote.get('author')),
            quote=quote.get('quote'),
        ).save()


if __name__ == "__main__":
    seed_authors()
    seed_quotes()
    disconnect()
