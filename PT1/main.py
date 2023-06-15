from prettytable import PrettyTable
from typing import List, Optional

import PT1.connect
from models import Authors, Quotes
from decors import time_of, handle_empty_result, cache_decorator

table = PrettyTable()


@time_of
@cache_decorator
@handle_empty_result
def find_by_name(name: str) -> Optional[List[Quotes]]:
    """
    Пошук цитат за іменем автора.

    :param name: Ім'я автора.

    :return: Optional[List[Quotes]]: Список цитат, якщо знайдено. None, якщо нічого не знайдено.
    """
    author = Authors.objects(full_name__istartswith=name.strip()).first()
    if author:
        quotes = Quotes.objects(author=author)
        return quotes


@time_of
@cache_decorator
@handle_empty_result
def find_by_tag(tag: str) -> Optional[List[Quotes]]:
    """
    Пошук цитат за тегом, або частиною тегу.

    :param tag: Тег цитати.


    :return: Optional[List[Quotes]]: Список цитат, якщо знайдено. None, якщо нічого не знайдено.
    """
    quote = Quotes.objects(tags__istartswith=tag).all()
    if quote:
        return quote


@time_of
@cache_decorator
@handle_empty_result
def find_by_tags(tags: str) -> Optional[List[Quotes]]:
    """
    Пошук цитат за списком тегів. (Не виконує пошук за частиною тегів.)

    :param tags: Теги, розділені (тільки!) комою, без пробілів та інших знаків.

    :return: Optional[List[Quotes]]: Список цитат, якщо знайдено збіг. None, якщо нічого не знайдено.
    """
    tag_list = tags.strip().split(',')
    quotes = Quotes.objects(tags__in=tag_list).all()
    if quotes:
        return quotes


@time_of
@cache_decorator
@handle_empty_result
def find_by_quote(part_of_quote: str) -> Optional[List[Quotes]]:
    """
    Пошук цитат за частиною тексту цитати.

    :param part_of_quote: Частина тексту цитати.

    :return: Optional[List[Quotes]]: Список цитат, якщо знайдено. None, якщо нічого не знайдено.
    """
    quotes = Quotes.objects(quote__icontains=part_of_quote).all()
    if quotes:
        return quotes


@time_of
@cache_decorator
@handle_empty_result
def find_by_place(place: str) -> Optional[List[Quotes]]:
    """
    Пошук цитат за місцем народження автора.

    :param place: Місце народження автора.

    :return: Optional[List[Quotes]]: Список цитат, якщо знайдено збіг. None, якщо нічого не знайдено.
    """
    authors = Authors.objects(born_loc__contains=place).all()
    if authors:
        quotes = Quotes.objects(author__in=authors)
        return quotes


COMMANDS = {
    'name': find_by_name,
    'tag': find_by_tag,
    'tags': find_by_tags,
    'quote': find_by_quote,
    'born': find_by_place
}


def print_quotes(quotes: Optional[List[Quotes]]) -> None:
    """
    Виведення цитат на екран у вигляді таблиці зі стовбцями: ['Author', 'Quote', 'Tags']
    :param quotes: (Optional[List[Quotes]]): Список цитат.
    """
    table.clear_rows()
    table.field_names = ['Author', 'Quote', 'Tags']
    for quote in quotes:
        table.add_row([quote.author.full_name, quote.quote, ', '.join(quote.tags)])
    table.align = "c"
    table.valign = "m"
    table.max_width['Quote'] = 50
    table.max_width['Tags'] = 30
    print(table)


def main():
    while True:
        user_input = input("Provide the command:\n>>> ")
        parts = user_input.split(":")
        if len(parts) != 2:
            print("Wrong search format. Example: <name:Steve Martin>")
            continue
        command, value = parts
        if command in COMMANDS.keys():
            quotes = COMMANDS[command](value)
            print_quotes(quotes)
        elif command == 'exit':
            print("Exiting the script...")
            break
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
